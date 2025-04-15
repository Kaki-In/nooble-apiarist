from .server_configuration import *
from .server_cli_info import *

import quart as _quart #type:ignore
import typing as _T

class ServerEndpointAction():
    def __init__(self):
        pass
    
    async def __call__(self, configuration: ServerEndpointConfiguration, request: _quart.Request) -> _quart.Response:
        return await self.execute(configuration, request)
    
    async def execute(self, configuration: ServerEndpointConfiguration, request: _quart.Request, **data) -> _quart.Response:
        json_result = await self.main(configuration, request, ServerEndpointClientInformation(data))

        response: _quart.Response = await configuration.get_quart().make_response(json_result) # type:ignore
        
        return response
    
    async def main(self, configuration: ServerEndpointConfiguration, request: _quart.Request, client_data: ServerEndpointClientInformation) -> 'dict[str, _T.Any]':
        raise TypeError("this action is virtual")
