import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class MarkActivitiesAsReadAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "activites" in args:
            return False
        
        if not type(args["activities"]) is list:
            return False
        
        account = await self.get_account(request, configuration)

        for activity_id in args["activities"]:
            if not type(activity_id) is str:
                return False
            
            if account is None: # don't verifying because it is simply a non-allowed request
                continue

            activity = await account.get_activity(activity_id)
            if not await activity.exists():
                return False

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)
        
        activities: list[str] = args["activities"]

        await account.mark_activities_as_read(*activities)

        return await self.make_response(None, configuration)

    
