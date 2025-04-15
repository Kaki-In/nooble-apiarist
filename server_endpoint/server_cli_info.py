import typing as _T

class ServerEndpointClientInformation():
    def __init__(self, data: 'dict[str, _T.Any]'):
        self._data = data

    def get(self, name: str):
        return self._data[name]
    
