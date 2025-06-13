import quart.wrappers as _quart_wrappers
import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Modifier le rôle d'un compte")
@_apiarist.NoobleEndpointDecorations.arguments(
    user_id = "identifiant du compte utilisateur",
    role = "role à appliquer au compte"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le rôle est bien un rôle connu (admin, teacher, teacher_admin ou student)",
    "un compte utilisateur est bien décrit par l'identifiant"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur",
    "l'administrateur ne tente pas de modifier son propre rôle"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "user_id": "de62c209a",
        "role": "teacher_admin"
    },
    None
)
class ModifyAccountRoleAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "user_id" in args
        and "role" in args
        ):
            return False
        
        if not (
            type(args["user_id"]) is str
        and args["role"] in ["admin", 'teacher', "teacher_admin", "student"]
        ):
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
        self_account = await self.get_account(request, configuration)

        if self_account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)

        user_id: str = args["user_id"]
        role = _nooble_database_roles.Role.from_raw_role(args["role"])
        
        account = configuration.get_database().get_accounts().get_account(user_id)

        await account.update({
            "$set": {
                "role": args["role"]
            }
        })

        if role == _nooble_database_roles.Role.ADMIN:
            await configuration.get_database().get_classes().update(
                {},
                {
                    "$pull": {
                        "accounts": user_id
                    }
                }
            )

        await configuration.get_mail_service().send_edited_role_mail(await account.get_object(), await self_account.get_object())

        await configuration.get_notifier().notify_role_changed(role, account, self_account)

        return await self.make_response(None, configuration)




