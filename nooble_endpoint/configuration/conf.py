import server_endpoint as _server_endpoint

import nooble_database as _nooble_database

class NoobleConfiguration(_server_endpoint.ServerEndpointConfiguration):
    def __init__(self, host: str, port: int, hostname: str, database: _nooble_database.NoobleDatabase):
        super().__init__(host, port, hostname)

        self._database = database
    
    def get_database(self) -> _nooble_database.NoobleDatabase:
        return self._database
    

