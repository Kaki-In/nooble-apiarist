from .server_action import ServerEndpointAction
from .server_configuration import ServerEndpointConfiguration
from .decorations import _NoobleEndpointDescriptedObject

import quart as _quart
import typing as _T

import typing as _T

_configuration_type = _T.TypeVar("_configuration_type", bound = ServerEndpointConfiguration)

class ServerEndpoint(_T.Generic[_configuration_type]):
    def __init__(self, configuration: _configuration_type, base_origin: str):
        self._configuration = configuration
        self._id = 0
        self._base_origin = base_origin
        
        self._actions:dict[str, tuple[ServerEndpointAction | _NoobleEndpointDescriptedObject, list[str]]] = {}

    def get_configuration(self) -> _configuration_type:
        return self._configuration

    def add_action(self, name: str, action: ServerEndpointAction[_configuration_type] | _NoobleEndpointDescriptedObject, *methods: str) -> None:
        async def action_launcher():
            request = _quart.request

            if request.method == "OPTIONS":
                response = await _quart.make_response("", 204)
            else:
                response = await action(self._configuration, request)

            if not isinstance(response, _quart.Response):
                response = await _quart.make_response(response)

            origin = request.headers.get("Origin") or self._base_origin

            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"

            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

            return response
        
        action_launcher.__name__ = str(self._id)
        self._id += 1

        self._actions[name] = (action, list(methods))

        self._configuration._quart.route(name, methods=list(methods)+["OPTIONS"]) (action_launcher)

    def get_actions(self) -> list[str]:
        return list(self._actions)
    
    def get_action(self, name:str) -> tuple[ServerEndpointAction | _NoobleEndpointDescriptedObject, list[str]]:
        return self._actions[name]
            
    async def run(self, certfile: str, keyfile: str) -> None:
        await self._configuration.get_quart().run_task(host = self._configuration.get_host(), port = self._configuration.get_port(), certfile = certfile, keyfile = keyfile)
    
    async def run_locally(self) -> None:
        await self._configuration.get_quart().run_task(self._configuration.get_host(), self._configuration.get_port())
