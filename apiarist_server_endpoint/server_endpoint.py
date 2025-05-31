from .server_action import ServerEndpointAction
from .server_configuration import ServerEndpointConfiguration

import quart as _quart
import typing as _T

import typing as _T

_configuration_type = _T.TypeVar("_configuration_type", bound = ServerEndpointConfiguration)

class ServerEndpoint(_T.Generic[_configuration_type]):
    def __init__(self, configuration: _configuration_type):
        self._configuration = configuration
        self._id = 0

    def get_configuration(self) -> _configuration_type:
        return self._configuration

    def add_action(self, name: str, action: ServerEndpointAction[_configuration_type], *methods: str) -> None:
        async def action_launcher():
            return await action(self._configuration, _quart.request)
        
        action_launcher.__name__ = str(self._id)
        self._id += 1

        self._configuration._quart.route(name, methods=list(methods)) (action_launcher)
    
    async def run(self, certfile: str, keyfile: str) -> None:
        await self._configuration.get_quart().run_task(host = self._configuration.get_host(), port = self._configuration.get_port(), certfile = certfile, keyfile = keyfile)
    
    async def run_locally(self) -> None:
        await self._configuration.get_quart().run_task(self._configuration.get_host(), self._configuration.get_port())
