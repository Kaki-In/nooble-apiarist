import quart.wrappers as _quart_wrappers
import nooble_database.objects.file_types as _nooble_database_file_types

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class DeleteFileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "id" in args:
            return False
        
        if not type(args["id"]) is str:
            return False
        
        file = configuration.get_database().get_files().get_file(args['id'])

        if not await file.exists():
            return False
                
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        args = await self.get_request_args(request)

        file = configuration.get_database().get_files().get_file(args['id'])

        if await file.get_sender_id() != account.get_id():
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)

        file = configuration.get_database().get_files().get_file(args['id'])

        file_type = await file.get_filetype()

        if file_type == _nooble_database_file_types.FileType.DECORATION_BANNER:
            decoration = await configuration.get_database().get_decorations().get_decoration_from_image(file.get_id())

            if decoration is not None:
                return await self.make_response({
                    "reason": "there is already a decoration attached with this image"
                }, configuration, 400)
            
        elif file_type == _nooble_database_file_types.FileType.PROFILE_ICON:
            await account.update(
                {
                    "$set": {
                        "profile_image": None
                    }
                }
            )

        elif file_type == _nooble_database_file_types.FileType.SECTION_FILE:
            return await self.make_response({
                "reason": "this file is linked with a section"
            }, configuration, 400)
        
        await file.destroy()

        return await self.make_response(None, configuration)
            


