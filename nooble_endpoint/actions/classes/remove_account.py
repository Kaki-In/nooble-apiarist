import quart.wrappers as _quart_wrappers

import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Dissocier un compte d'un cours")
@_apiarist.NoobleEndpointDecorations.arguments(
    class_id = "l'identifiant du cours",
    user_id = "l'identifiant de l'utilisateur"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant désigne bien un cours existant"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur ou",
    "l'utilisateur a accès à ce cours"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "user_id": "cc2b3492",
        "class_id": "c273df84f"
    },
    None
)
class RemoveClassAccountAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "user_id" in args
        and "class_id" in args
        ):
            return False
        
        if not (
            type(args["user_id"]) is str
        and type(args["class_id"]) is str
        ):
            return False
        
        user = configuration.get_database().get_accounts().get_account(args['user_id'])

        if not await user.exists():
            return False
        
        nooble_class = configuration.get_database().get_classes().get_class(args['class_id'])

        if not await nooble_class.exists():
            return False
        
        if not args["user_id"] in await nooble_class.get_accounts_ids():
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

        user_id: str = args["user_id"]
        class_id: str = args["class_id"]

        await configuration.get_database().get_classes().get_class(class_id).update({
            "$pull": {
                "accounts": user_id
            }
        })

        return await self.make_response(None, configuration)

