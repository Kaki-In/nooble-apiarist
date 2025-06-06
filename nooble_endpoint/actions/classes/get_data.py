import quart.wrappers as _quart_wrappers

import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetClassDataAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "class_id" in args:
            return False
        
        if not type(args["class_id"]) is str:
            return False
        
        nooble_class = configuration.get_database().get_classes().get_class(args["class_id"])

        if not await nooble_class.exists():
            return False

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False

        args = await self.get_request_args(request)

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
        account = await self.get_account(request, configuration)

        if account is None:
            return False

        args = await self.get_request_args(request)
        class_id: str = args["class_id"]

        nooble_class = configuration.get_database().get_classes().get_class(class_id)

        class_data = await nooble_class.ensure_object()
        
        content = class_data["content"]

        client_content = await configuration.get_sections().export(content).export_to_client_json(configuration.get_database(), account)

        return await self.make_response(
            {
                "content": client_content,
                "description": class_data["description"],
                "last_modification": class_data["last_modification"],
                "last_modifier": class_data["last_modifier"],
                "name": class_data["name"]
            },
            configuration
        )

