import quart.wrappers as _quart_wrappers
import apiarist_server_endpoint as _apiarist

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

@_apiarist.NoobleEndpointDecorations.description("Supprimer un compte")
@_apiarist.NoobleEndpointDecorations.arguments(
    user_id = "identifiant du compte utilisateur"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "un compte utilisateur est bien décrit par l'identifiant"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur",
    "l'administrateur ne tente pas de se supprimer lui-même"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "user_id": "de62c209a"
    },
    None
)
class DeleteAccountAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "user_id" in args:
            return False
        
        if not type(args["user_id"]) is str:
            return False
        
        account = configuration.get_database().get_accounts().get_account(args["user_id"])

        if not await account.exists():
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)
        args = await self.get_request_args(request)

        if account is None:
            return False

        if not (await account.get_role()).is_admin():
            return False
        
        if account.get_id() == args["user_id"]:
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        user_id: str = args["user_id"]

        account = configuration.get_database().get_accounts().get_account(user_id)

        files = await configuration.get_database().get_files().get_sender_files(user_id)

        await configuration.get_database().get_classes().update(
            {},
            {
                "$pull": {
                    "accounts": user_id
                }
            }
        )

        for file in files:
            file_object = await file.ensure_object()

            if file_object["filetype"] == "profile icon":
                await file.destroy()

        await account.destroy()

        return await self.make_response(None, configuration)
