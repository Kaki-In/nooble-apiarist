import quart.wrappers as _quart_wrappers
import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetProfileInfoAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if "user_id" in args:
            return type(args["user_id"]) is str

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        if "user_id" in args:
            user_id: str = args["user_id"]

            account = configuration.get_database().get_accounts().get_account(user_id)
        else:
            account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response({
                
            }, configuration, 500) 
        
        profile_info: dict = await account.get_profile().get_object() # type: ignore

        if await account.get_role() != _nooble_database_roles.Role.ADMIN:
            profile_info["classes"] = await configuration.get_database().get_classes().get_account_classes(account.get_id())
        
        return await self.make_response(profile_info, configuration, 200)
