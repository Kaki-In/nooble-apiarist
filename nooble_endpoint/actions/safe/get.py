import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir son coffre-fort")
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    quota = "solde de nooblards",
    badges = "badges possédés",
    decorations = "décorations achetées"
)
@_apiarist.NoobleEndpointDecorations.example(
    None,
    {
        "quota": 249,
        "badges": 
            [
                ["here_for_long", 2]
            ],
        "decorations":
            [
                "abcd6484fdbc",
                "9ab238dc638d"
            ]
    }
)
class GetSafeAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        return await self.make_response(await account.get_safe().get_object(), configuration)

