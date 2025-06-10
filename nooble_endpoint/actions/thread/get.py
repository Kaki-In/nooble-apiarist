import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir son flux d'activités")
@_apiarist.NoobleEndpointDecorations.arguments(
    notreadonly = "vrai s'il faut uniquement retourner les activités non lues",
    count = "le nombre d'activités à retourner",
    offset = "le nombre d'activités à sauter"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le compte est supérieur à 0",
    "l'offset n'est pas négatif"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    activity_id = "l'identifiant de l'activité",
    read = "vrai lorsque l'activité a été lue",
    activity_data = "les données de l'activité"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "notreadonly": 4,
        "count": 20,
        "offset": 40
    },
    [
        {
            "activity_id": "8cdc823bd",
            "read": False,
            "activity_data": {
                "title": "Nouvelle notification",
                "content": "Il s'est passé quelque chose à ce moment là",
                "creator": "dcb823dcb85",
                "date": 6540479450,
                "icon": "account"
            }
        }
    ]
)
class GetThreadAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "notreadonly" in args
        and "offset" in args
        and "count" in args
        ):
            return False
        
        if not (
            type(args["notreadonly"]) is bool
        and type(args["count"]) is int
        and type(args["offset"]) is int
        ):
            return False
        
        if not (
            args["count"] > 0
        and args["offset"] >= 0
        ):
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)

        notreadonly: bool = args["notreadonly"]
        count: int = args["count"]
        offset: int = args["offset"]

        activities = [
            await activity.ensure_object()
            for activity in await account.get_activities()
            if not ((await activity.ensure_object())["read"] and notreadonly)
        ][offset:offset+count]

        activities_objects = []

        for notification in activities:
            activity = configuration.get_database().get_activities().get_activity(notification["activity"])
            activity_object = await activity.get_object()

            activities_objects.append({
                "activity_id": notification["activity"],
                "read": notification["read"],

                "activity_data": {
                    "title": activity_object["title"],
                    "content": activity_object["content"],
                    "creator": activity_object["creator"],
                    "date": activity_object["date"],
                    "icon": activity_object["icon"]
                }
            })

        return await self.make_response(activities_objects, configuration)



