import quart.wrappers as _quart_wrappers
import nooble_database.objects as _nooble_database_objects

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir des informations de connection")
@_apiarist.NoobleEndpointDecorations.returns(
    connected = "vrai lorsque l'utilisateur est connecté",
    account = "si connecté, les informations de compte"
)
@_apiarist.NoobleEndpointDecorations.example(
    None,
    {
        "connected": True,
        "account": {
            "id": "8482f9209deb",
            "profile": 
            {
                "first_name": "John",
                "last_name": "Doe",
                "active_decoration": '3bd8527cf',
                "active_badges": [
                    ["here_for_long", 3]
                ],
                "classes": [
                    "abc2934",
                    "cb293cdb23f",
                    "..."
                ],
                "profile_image": "abc837b23",
                "description": "Ssalut toi"
            },
            "safe": 
            {
                "quota": 30,
                "decorations": [
                    '3bd8527cf', 
                    '8cab2940c3d'
                ],
                "badges": [
                    ["here_for_long", 30],
                    ["...", 394],
                    "..."
                ]
            },
            "role": "admin_teacher",
            "mail": "john.doe@utbm.fr"
        }
    }
)
class GetLogInfoAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(
                {
                    "connected": False,
                },
                configuration
            )
        
        profile_info: dict = await account.get_profile().get_object() # type: ignore

        if await account.get_role() != _nooble_database_objects.Role.ADMIN:
            profile_info["classes"] = [(await nooble_class.ensure_object())["_id"] for nooble_class in await configuration.get_database().get_classes().get_account_classes(account.get_id())]
        
        owned_badges = await account.get_safe().get_owned_badges()

        profile_info["badges"] = [badge for badge in owned_badges if badge[0] in profile_info["active_badges"]]
        
        account_object = await account.get_object()

        return await self.make_response(
            {
                "connected": True,
                "account": {
                    "id": account_object["_id"],
                    "profile": profile_info,
                    "safe": account_object["safe"],
                    "role": account_object["role"],
                    "mail": account_object["mail"]
                }
            }, 
            configuration
        )


