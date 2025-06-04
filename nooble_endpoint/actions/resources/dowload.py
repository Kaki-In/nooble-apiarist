import quart.wrappers as _quart_wrappers
import quart as _quart

import nooble_database.objects.file_types as _nooble_database_file_types

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class DownloadFileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "id" in args
        and "type" in args
        ):
            return False
        
        if not type(args["id"]) is str:
            return False
        
        try:
            _nooble_database_file_types.FileType.from_raw_filetype(args["type"])
        except:
            return False
        
        file = configuration.get_database().get_files().get_file(args['id'])

        if not await file.exists():
            return False
        
        if not args["type"] == (await file.ensure_object())["filetype"]:
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        file_id: str = args["id"]

        file = configuration.get_database().get_files().get_file(file_id)

        resource = configuration.get_resources().get_file(await file.get_filepath())

        return await _quart.send_file(resource.get_content(), as_attachment=True, attachment_filename=await file.get_filename(), last_modified=await file.get_sent_date())




