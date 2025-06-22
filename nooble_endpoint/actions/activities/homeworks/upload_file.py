import quart.wrappers as _quart_wrappers
import nooble_database.objects as _nooble_database_objects
import io as _io
import asyncio as _asyncio
import datetime as _datetime
import json as _json

from ....configuration import NoobleEndpointConfiguration
from ....templates.nooble_activity_action import NoobleEndpointActivityAction

class UploadHomeworkFileActivityAction(NoobleEndpointActivityAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        file_result = await self.get_activity_file(configuration, request)

        if file_result is None:
            return False
        
        args = await self.get_request_args(request)

        if not "name" in args:
            return False
        
        if type(args["name"]) is not str:
            return False
        
        files = await self.get_files(request)

        if not "file-content" in files:
            return False
        
        if not files["file-content"].filename :
            return False
        
        account = await self.get_account(request, configuration)

        if account is None:
            return True # non-allowed request
        
        file_data = _json.loads(file_result[1])

        for homework in file_data:
            if homework['sender_id'] == account.get_id(): # homework already laid
                return False

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        if not await account.get_role() == _nooble_database_objects.Role.STUDENT:
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        activity_files = await self.get_activity_file(configuration, request)\
        
        if activity_files is None:
            return await self.make_response(None, configuration, 500)

        activity_data = _json.loads(activity_files[1])

        args = await self.get_request_args(request)
        
        name: str = args["name"]

        file_content = (await self.get_files(request))["file-content"]
        if not file_content.filename:
            return await self.make_response(None, configuration, 500)
        
        filename: str = file_content.filename

        file_bytes = await _asyncio.get_event_loop().run_in_executor(None, file_content.stream.read)

        file = configuration.get_resources().create_file(file_bytes)

        new_file = await configuration.get_database().get_files().create_new_file(
            name,
            filename,
            _datetime.datetime.now(),
            account.get_id(),
            file.get_path(),
            _nooble_database_objects.FileType.SECTION_FILE,
            len(file.get_content())
        )

        activity_data.append(
            {
                "sender_id": account.get_id(),
                "file_id": new_file.get_id()
            }
        )

        await self.overwrite_savefile(_json.dumps(activity_data).encode(), configuration, request)

        return await self.make_response(new_file.get_id(), configuration)


