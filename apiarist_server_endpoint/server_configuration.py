import quart as _quart
import quart_cors as _quart_cors
import typing as _T

class ServerEndpointConfiguration():
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._quart = _quart_cors.cors(_quart.Quart(__name__), allow_origin="*.flopcreation.fr")

    def get_host(self) -> str:
        return self._host
    
    def get_port(self) -> int:
        return self._port
    
    def get_quart(self) -> _quart.Quart:
        return self._quart



