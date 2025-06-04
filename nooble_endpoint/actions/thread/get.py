import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetThreadAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "readonly" in args
        and "offset" in args
        and "count" in args
        ):
            return False
        
        if not (
            type(args["readonly"]) is bool
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

        readonly: bool = args["readonly"]
        count: int = args["count"]
        offset: int = args["offset"]

        activities = [
            await activity.ensure_object()
            for activity in await account.get_activities()
            if (await activity.ensure_object())["read"] or not readonly
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



