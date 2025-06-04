import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class DeleteDecorationAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "decoration_id" in args:
            return False
        
        if type(args["decoration_id"]) is not str:
            return False
        
        decoration = configuration.get_database().get_decorations().get_decoration(args["decoration_id"])

        if not await decoration.exists():
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        if not (await account.get_role()).is_admin():
            return False
        
        args = await self.get_request_args(request)

        decoration = configuration.get_database().get_decorations().get_decoration(args["decoration_id"])

        file = configuration.get_database().get_files().get_file(await decoration.get_image_id())

        if not await file.get_sender_id() != account.get_id():
            return False
        
        return True
    
    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        decoration = configuration.get_database().get_decorations().get_decoration(args["decoration_id"])

        file = configuration.get_database().get_files().get_file(await decoration.get_image_id())

        await file.destroy()
        await decoration.destroy()

        return await self.make_response(None, configuration)


