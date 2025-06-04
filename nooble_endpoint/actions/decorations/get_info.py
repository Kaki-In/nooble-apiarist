import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetDecorationInfosAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "decoration" in args:
            return False
        
        if type(args["decoration"]) is not str:
            return False
        
        decoration = configuration.get_database().get_decorations().get_decoration(args["decoration"])
        
        if not await decoration.exists():
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        decoration = configuration.get_database().get_decorations().get_decoration(args["decoration"])
        decoration_object = await decoration.get_object()

        return await self.make_response({
            "name": decoration_object["name"],
            "price": decoration_object["price"],
            "image": decoration_object["image"]
        }, configuration)
        

