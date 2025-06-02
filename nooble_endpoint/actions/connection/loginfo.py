import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetLogInfoAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(
                {
                    "connected": False,
                },
                configuration
            )
        
        else :
            account_object = await account.get_object()

            return await self.make_response(
                {
                    "connected": True,
                    "account": {
                        "id": account_object["_id"],
                        "profile": account_object["profile"],
                        "safe": account_object["safe"],
                        "role": account_object["role"],
                        "mail": account_object["mail"]
                    }
                }, 
                configuration
            )


