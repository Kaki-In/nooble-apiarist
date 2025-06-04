import quart.wrappers as _quart_wrappers
import io as _io
import asyncio as _asyncio
import datetime as _datetime

import nooble_database.objects.file_types as _nooble_database_file_types
import local_utils.images as _local_utils_images

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class UploadFileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "name" in args
        and "type" in args
        ):
            return False
        
        if not (
            type(args["name"]) is str
        ):
            return False
        
        try:
            _nooble_database_file_types.FileType.from_raw_filetype(args["type"])
        except ValueError:
            return False

        
        files = await self.get_files(request)

        if not "file-content" in files:
            return False
        
        if not files["file-content"].filename :
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)
        
        name: str = args["name"]
        file_type = _nooble_database_file_types.FileType.from_raw_filetype(args["type"])

        file_content = (await self.get_files(request))["file-content"]
        if not file_content.filename:
            return await self.make_response(None, configuration, 500)
        
        filename: str = file_content.filename

        file_bytes = _io.BytesIO()
        await _asyncio.get_event_loop().run_in_executor(None, file_content.save, file_bytes)

        if not await self.ensure_veracity(file_type, file_bytes.getvalue()):
            return await self.make_response("invalid file given", configuration, 400)

        file = configuration.get_resources().create_file(file_bytes.getvalue())

        await configuration.get_database().get_files().create_new_file(
            name,
            filename,
            _datetime.datetime.now(),
            account.get_id(),
            file.get_path(),
            file_type,
            len(file.get_content())
        )

    async def ensure_veracity(self, filetype:_nooble_database_file_types.FileType, content:bytes) -> bool:
        if filetype == _nooble_database_file_types.FileType.DECORATION_BANNER:
            try:
                image = await _local_utils_images.from_bytes(content)

                return image.get_size() == (900, 300)
            except:
                return False
        elif filetype == _nooble_database_file_types.FileType.PROFILE_ICON:
            try:
                image = await _local_utils_images.from_bytes(content)

                return image.get_width() == image.get_height()
            except:
                return False
        else:
            return True
