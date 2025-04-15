import server_endpoint as _server_endpoint

import nooble_database as _nooble_database
import nooble_server_registrations as _registrations

class NoobleConfiguration(_server_endpoint.ServerEndpointConfiguration):
    def __init__(self, host: str, port: int, hostname: str, database: _nooble_database.NoobleDatabase, registrations: _registrations.NoobleRegistrationsList):
        super().__init__(host, port, hostname)

        self._database = database
        self._registrations = registrations
    
    def get_database(self) -> _nooble_database.NoobleDatabase:
        return self._database
    
    def get_registrations(self) -> _registrations.NoobleRegistrationsList:
        return self._registrations
    

