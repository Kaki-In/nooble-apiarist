from .server_configuration import ServerEndpointConfiguration

import quart as _quart
import typing as _T
import json as _json

_configuration_type = _T.TypeVar("_configuration_type", bound = ServerEndpointConfiguration)

class ServerEndpointAction(_T.Generic[_configuration_type]):
    async def __call__(self, configuration: _configuration_type, request: _quart.Request) -> _T.Any:
        return await self.execute(configuration, request)
    
    async def execute(self, configuration: _configuration_type, request: _quart.Request) -> _T.Any:
        if not await self.is_valid(configuration, request):
            return "Bad Request", 400

        if not await self.is_allowed(configuration, request):
            return "Forbidden", 401

        response = await self.main(configuration, request)
        return response
    
    async def is_valid(self, configuration: _configuration_type, request: _quart.Request) -> bool:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def is_allowed(self, configuration: _configuration_type, request: _quart.Request) -> bool:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def main(self, configuration: _configuration_type, request: _quart.Request) -> _T.Any:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def get_request_args(self, request: _quart.Request) -> dict[str, _T.Any]:
        try:
            args: dict = await request.get_json(True)

            if type(args) is not dict:
                raise ValueError
        except:
            args = {}


        request_args = request.args.copy()

        for arg in request_args:
            try:
                request_args[arg] = _json.loads(request_args[arg])
            except:
                pass


        args.update(request_args)

        return args
    
