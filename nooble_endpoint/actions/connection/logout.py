import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class LogoutAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        token = self.get_client_token(request)

        if token is None: # would not be the case for an allowed request
            return await self.make_response(None, configuration, 500)
        
        configuration.get_registrations().remove_registration(token)

        return await self.make_response("", configuration)


