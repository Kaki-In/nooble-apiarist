import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Chercher un compte")
@_apiarist.NoobleEndpointDecorations.arguments(
    pattern = "le motif à chercher dans le compte",
    count = "le nombre de comptes à retourner",
    offset = "le nombre de comptes à ignorer"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le compte est supérieur à 0",
    "le nombre de comptes à ignorer est supérieur ou égal à 0"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "count": 20,
        "offset": 20,
        "pattern": 'ohn'
    },
    [
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
    ]
)
class SearchAccountAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "offset" in args
        and "count" in args
        ):
            return False
        
        if not (
            type(args["pattern"]) is str
        and type(args["offset"]) is int
        and type(args["count"]) is int
        ):
            return False
        
        if not (
            args["pattern"]
        and args["count"] > 0
        and args["offset"] >= 0
        ):
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

        pattern: str = args["pattern"]
        count: int = args["count"]
        offset: int = args["offset"]

        accounts = await configuration.get_database().get_accounts().find(
            {
                "$or": [
                    {
                        "mail": {
                            "$regex": pattern,
                            "$options": 'i' # case insensitive
                        }
                    },
                    {
                        "profile.first_name": {
                            "$regex": pattern,
                            "$options": 'i' # case insensitive
                        }
                    },
                    {
                        "profile.last_name": {
                            "$regex": pattern,
                            "$options": 'i' # case insensitive
                        }
                    },
                    {
                        "profile.description": {
                            "$regex": pattern,
                            "$options": 'i' # case insensitive
                        }
                    },
                ]
            },
            skip = offset,
            limit = count
        )

        returned_objects = []

        for account in accounts:
            returned_objects.append(
                {
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
            )
            
            if account["role"] != "admin":
                returned_objects[-1]["profile"]["classes"] = [(await nooble_class.ensure_object())["_id"] for nooble_class in await configuration.get_database().get_classes().get_account_classes(account["_id"])]

        return await self.make_response(returned_objects, configuration, 200)



