import quart.wrappers as _quart_wrappers
import hashlib as _hashlib
import nooble_database.objects.roles as _nooble_database_roles
import asyncio as _asyncio
import random as _random

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class AddAccountAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "mail" in args
        and "first_name" in args
        and "last_name" in args
        ):
            return False
        
        if not (
            type(args["mail"]) is str
        and type(args["first_name"]) is str
        and type(args["last_name"]) is str
        ):
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

        mail: str = args["mail"]
        first_name: str = args["first_name"]
        last_name: str = args["last_name"]

        new_password = self.create_new_password()
        new_account = await configuration.get_database().get_accounts().create_new_account(mail, first_name, last_name, _hashlib.sha256(new_password.encode()).hexdigest())
        
        _asyncio.create_task(configuration.get_mail_service().send_new_password_mail(await new_account.ensure_object(), new_password))

        return await self.make_response({
            "new_account": new_account.get_id()
        }, configuration)
    
    def create_new_password(self) -> str:
        a = ""

        for i in range(8):
            a += _random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123465789")

        return a


