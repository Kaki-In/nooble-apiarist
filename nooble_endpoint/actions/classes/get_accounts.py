import quart.wrappers as _quart_wrappers

import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetClassAccountsAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "class_id" in args:
            return False
        
        if not type(args["class_id"]) is int:
            return False
        
        nooble_class = configuration.get_database().get_classes().get_class(args["class_id"])

        if not await nooble_class.exists():
            return False

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        account = await self.get_account(request, configuration)

        if account is None:
            return False

        if not (
            await account.get_role() in [
                _nooble_database_roles.Role.ADMIN,
                _nooble_database_roles.Role.ADMIN_TEACHER
            ]
            or account.get_id() in await configuration.get_database().get_classes().get_class(args["class_id"]).get_accounts_ids()
        ):
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)
        class_id: int = args["class_id"]

        nooble_class = configuration.get_database().get_classes().get_class(class_id)
 
        return await self.make_response(
            await nooble_class.get_accounts_ids(),
            configuration
        )

