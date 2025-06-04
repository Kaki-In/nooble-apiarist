import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class ModifyDecorationAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "decoration_id" in args:
            return False

        argument_provided = False

        if "name" in args:
            if type(args["name"]) is not str:
                return False
            
            argument_provided = True
            
        if "price" in args:
            if type(args["price"]) is not int:
                return False

            argument_provided = True

        if not argument_provided:
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

        if "name" in args:
            await decoration.update({
                "$set": {
                    "name": args["name"]
                }
            })

        if "price" in args:
            await decoration.update({
                "$set": {
                    "price": args["price"]
                }
            })
        
        return await self.make_response(None, configuration)


        

