import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Chercher un cours")
@_apiarist.NoobleEndpointDecorations.arguments(
    pattern = "le motif à chercher dans le cours",
    count = "le nombre de cours à retourner",
    offset = "le nombre de cours à ignorer"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le compte est supérieur à 0",
    "le nombre de cours à ignorer est supérieur ou égal à 0"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "count": 20,
        "offset": 20,
        "pattern": 'gula'
    },
    [
        {
            "id": "bcdf284879c8d2",
            "content": {
                "type": "section",
                "data": "..."
            },
            "description": "Angular",
            "last_modification": 2948759329234,
            "last_modifier": "dbfc327493",
            "name": "WE4B"
        }

    ]
)
class SearchClassAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "pattern" in args
        and "offset" in args
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
            args["count"] > 0
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

        classes = await configuration.get_database().get_classes().find(
            {
                "$or": [
                    {
                        "name": {
                            "$regex": pattern,
                            "$options": 'i' # case insensitive
                        },
                    },
                    {
                        "description": {
                            "$regex": pattern,
                            "$options": 'i' # case insensitive
                        },
                    },
                ]
            },
            skip = offset,
            limit = count
        )

        returned_objects = []

        for nooble_class in classes:
            returned_objects.append(
                {
                    "id": nooble_class["_id"],
                    "content": nooble_class["content"],
                    "name": nooble_class["name"],
                    "description": nooble_class['description'],
                    "last_modification": nooble_class["last_modification"],
                    "last_modifier": nooble_class["last_modifier"]
                }
            )

        return await self.make_response(returned_objects, configuration, 200)



