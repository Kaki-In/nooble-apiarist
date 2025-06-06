import quart.wrappers as _quart_wrappers
import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

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
        args = await self.get_request_args(request)

        if account is None:
            return False

        if not await account.get_role() in [_nooble_database_roles.Role.ADMIN, _nooble_database_roles.Role.ADMIN_TEACHER]:
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

        await configuration.get_mail_service().send_edited_address_mail(await account.get_object(), mail, await self_account.get_object())

        await account.update({
            "$set": {
                "mail": mail
            }
        })

        await configuration.get_mail_service().send_edited_address_mail(await account.get_object(), mail, await self_account.get_object())

        return await self.make_response(None, configuration)




