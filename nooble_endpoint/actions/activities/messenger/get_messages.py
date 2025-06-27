import quart.wrappers as _quart_wrappers
import nooble_database.objects as _nooble_database_objects
import json as _json

from ....configuration import NoobleEndpointConfiguration
from ....templates.nooble_activity_action import NoobleEndpointActivityAction

class GetMessagesActivityAction(NoobleEndpointActivityAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        file_result = await self.get_activity_file(configuration, request)

        if file_result is None:
            return False

        account = await self.get_account(request, configuration)

        if account is None:
            return True # non-allowed request
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        activity_files = await self.get_activity_file(configuration, request)

        if activity_files is None:
            return await self.make_response(None, configuration, 500)

        file_data = _json.loads(activity_files[1])

        return await self.make_response(file_data, configuration)
            


