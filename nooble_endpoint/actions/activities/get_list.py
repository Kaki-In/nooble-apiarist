import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetActivitiesListAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        activities = configuration.get_activities().get_activities_names()

        return await self.make_response(activities, configuration)

