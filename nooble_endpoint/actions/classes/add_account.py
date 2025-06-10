import quart.wrappers as _quart_wrappers

import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Lier un compte à une classe")
@_apiarist.NoobleEndpointDecorations.arguments(
    user_id = "identifiant du compte",
    class_id = "identifiant de la classe"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant du compte désigne bien un compte existant",
    "l'identifiant de la classe désigne bien une classe existante"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    new_quota = "le nombre de nooblards présents dans le porte monnaie après achat",
    new_level = "le nouveau niveau correspondant au badge acheté (0 pour le premier niveau)"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "name": "here_for_long"
    },
    {
        "new_quota": 32,
        "new_level": 2
    }
)
class AddClassAccountAction(NoobleEndpointAction):
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
        
        if args["user_id"] in await nooble_class.get_accounts_ids():
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False

        if not await account.get_role() in [_nooble_database_roles.Role.ADMIN, _nooble_database_roles.Role.ADMIN_TEACHER]:
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        user_id: str = args["user_id"]
        class_id: str = args["class_id"]

        await configuration.get_database().get_classes().get_class(class_id).update({
            "$push": {
                "accounts": user_id
            }
        })

        return await self.make_response(None, configuration)

