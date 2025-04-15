import server_endpoint as _server_endpoint
import quart as _quart
import json as _json

from ..configuration import *

class StopAction(_server_endpoint.ServerEndpointAction):
    def __init__(self):
        super().__init__()
    
    async def execute(self, configuration: NoobleConfiguration, request: _quart.Request, **data):
        exit()
