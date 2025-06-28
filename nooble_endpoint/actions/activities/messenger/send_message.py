import quart.wrappers as _quart_wrappers
import nooble_database.objects as _nooble_database_objects
import json as _json
import datetime as _datetime

from ....configuration import NoobleEndpointConfiguration
from ....templates.nooble_activity_action import NoobleEndpointActivityAction

class SendMessageActivityAction(NoobleEndpointActivityAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        file_result = await self.get_activity_file(configuration, request)

        if file_result is None:
            return False

        account = await self.get_account(request, configuration)

        if account is None:
            return True # non-allowed request
        
        args = await self.get_request_args(request)
        
        if not "message" in args:
            return False
        
        if type(args["message"]) != str:
            return False
        
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

        message: str = (await self.get_request_args(request))["message"]

        file_data["messages"].append({
            "user_id": account.get_id(),
            "timestamp": _datetime.datetime.now().timestamp(),
            "content": message
        })

        await self.overwrite_savefile(_json.dumps(file_data).encode(), configuration, request)

        return await self.make_response(None, configuration)
            


