import quart.wrappers as _quart_wrappers
import nooble_database.objects.roles as _nooble_database_roles
import apiarist_server_endpoint as _apiarist

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

@_apiarist.NoobleEndpointDecorations.description("Modifier l'adresse courriel d'un compte utilisateur")
@_apiarist.NoobleEndpointDecorations.arguments(
    user_id = "identifiant du compte utilisateur",
    mail = "nouvelle adresse mail à appliquer au compte"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "un compte utilisateur est bien décrit par l'identifiant"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur",
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "user_id": "de62c209a",
        "mail": "foo.bar@utbm.fr"
    },
    None
)
class ModifyAccountMailAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "user_id" in args
        and "mail" in args
        ):
            return False
        
        if not (
            type(args["user_id"]) is str
        and type(args["mail"]) is str
        ):
            return False
        
        account = configuration.get_database().get_accounts().get_account(args["user_id"])

        if not await account.exists():
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
        self_account = await self.get_account(request, configuration)

        if self_account is None:
            return await self.make_response(None, configuration, 500)

        args = await self.get_request_args(request)

        user_id: str = args["user_id"]
        mail: str = args["mail"]
        
        account = configuration.get_database().get_accounts().get_account(user_id)

        await configuration.get_notifier().notify_mail_address_changed(await account.get_mail(), mail, account, self_account)

        await configuration.get_mail_service().send_edited_address_mail(await account.get_object(), mail, await self_account.get_object())

        await account.update({
            "$set": {
                "mail": mail
            }
        })

        await configuration.get_mail_service().send_edited_address_mail(await account.get_object(), mail, await self_account.get_object())

        return await self.make_response(None, configuration)




