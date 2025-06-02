import quart.wrappers as _quart_wrappers
import hashlib as _hashlib
import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class AddAccountAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "mail" in args
        and "first_name" in args
        and "last_name" in args
        and "password" in args
        ):
            return False
        
        if not (
            type(args["mail"]) is str
        and type(args["first_name"]) is str
        and type(args["last_name"]) is str
        and type(args["password"]) is str
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
        password: str = args["password"]

        new_account = await configuration.get_database().get_accounts().create_new_account(mail, first_name, last_name, _hashlib.sha256(password.encode()).hexdigest())

        return await self.make_response({
            "new_account": new_account.get_id()
        }, configuration)
