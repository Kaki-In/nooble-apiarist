import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Accéder aux informations de compte d'un utilisateur. ")
@_apiarist.NoobleEndpointDecorations.arguments(
    user_id = "l'utilisateur à considérer"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant renseigné désigne bien un utilisateur existant"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "user_id": '8482f9209deb'
    },
    {
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
        "role": "admin_teacher",
        "mail": "john.doe@utbm.fr"
    }
)
class GetAccountInformationAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "user_id" in args:
            return False
        
        if not type(args["user_id"]) is str:
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
        args = await self.get_request_args(request)

        user_id: str = args["user_id"]

        account = await configuration.get_database().get_accounts().get_account(user_id).get_object()

        returned_object = {
            "id": account["_id"],
            "profile": 
            {
                "active_badges": [[badge_name, badge_level] for badge_name, badge_level in account["safe"]["badges"] if badge_name in account["profile"]["active_badges"]],
                "first_name": account["profile"]["first_name"],
                "last_name": account["profile"]["last_name"],
                "active_decoration": account["profile"]["active_decoration"],
                "profile_image": account["profile"]["profile_image"],
                "description": account["profile"]["description"]
            },
            "mail": account["mail"],
            "role": account['role']
        }
    
    
        if account["role"] != "admin":
            returned_object["profile"]["classes"] = [(await nooble_class.ensure_object())["_id"] for nooble_class in await configuration.get_database().get_classes().get_account_classes(account["_id"])]

        return await self.make_response(returned_object, configuration, 200)



