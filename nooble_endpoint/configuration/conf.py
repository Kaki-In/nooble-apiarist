import apiarist_server_endpoint as _server_endpoint

import nooble_server_registrations as _registrations
import nooble_database.database as _nooble_database
import nooble_conf.directories.nooble_configuration as _nooble_configuration
import nooble_mail_service as _nooble_mail_service

class NoobleEndpointConfiguration(_server_endpoint.ServerEndpointConfiguration):
    def __init__(self, host: str, port: int, hostname: str, configuration: _nooble_configuration.NoobleConfiguration, registrations: _registrations.NoobleRegistrationsList):
        super().__init__(host, port, hostname)

        self._database = _nooble_database.NoobleDatabase(configuration.get_database_configuration())
        self._mails = _nooble_mail_service.NoobleMailSender(configuration.get_mail_configuration(), configuration.get_templates().get_mail_templates())
        self._registrations = registrations
    
    def get_database(self) -> _nooble_database.NoobleDatabase:
        return self._database
    
    def get_mail_service(self) -> _nooble_mail_service.NoobleMailSender:
        return self._mails
    
    def get_registrations(self) -> _registrations.NoobleRegistrationsList:
        return self._registrations
    

