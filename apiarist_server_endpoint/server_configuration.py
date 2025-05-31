import quart as _quart
import typing as _T

class ServerEndpointConfiguration():
    def __init__(self, host: str, port: int, hostname: str):
        self._host = host
        self._port = port
        self._hostname = hostname
        self._quart = _quart.Quart(__name__)

    def get_host(self) -> str:
        return self._host
    
    def get_port(self) -> int:
        return self._port
    
    def get_hostname(self) -> str:
        return self._hostname
    
    def get_quart(self) -> _quart.Quart:
        return self._quart



