import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Supprimer une décoration")
@_apiarist.NoobleEndpointDecorations.arguments(
    decoration_id = "l'identifiant de la décoration"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant de décoration désigne bien une décoration existante"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "decoration_id": "8bcd3a40182"
    },
    None
)
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
        
        return True
    
    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        decoration = configuration.get_database().get_decorations().get_decoration(args["decoration_id"])

        await configuration.get_database().get_accounts().update(
            {
                "safe.decorations": decoration.get_id()
            },
            {
                "$pull": {
                    "safe.decorations": decoration.get_id()
                },
                "$inc": {
                    "safe.quota": await decoration.get_price()
                },
                "$set": {
                    "profile.active_decoration": None
                }
            }
        )

        await decoration.destroy()

        return await self.make_response(None, configuration)


