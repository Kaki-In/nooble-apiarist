import apiarist_server_endpoint as _server_endpoint

import nooble_server_registrations as _registrations
import nooble_database.database as _nooble_database
import nooble_conf.directories as _nooble_conf_directories
import nooble_conf.files as _nooble_conf_files
import nooble_mail_service as _nooble_mail_service
import nooble_badges.default as _nooble_badges
import nooble_resources_manager as _nooble_resources

class NoobleEndpointConfiguration(_server_endpoint.ServerEndpointConfiguration):
    def __init__(self, configuration: _nooble_conf_directories.NoobleConfiguration):
        endpoint_configuration = configuration.get_endpoint_settings()
        binding_settings = endpoint_configuration.get_binding_settings()

        super().__init__(binding_settings.get_host(), binding_settings.get_port())

        self._database = _nooble_database.NoobleDatabase(configuration.get_database_settings())
        self._mails = _nooble_mail_service.NoobleMailSender(configuration.get_mail_settings(), configuration.get_templates().get_mail_templates())
        self._registrations = _registrations.NoobleRegistrationsList(endpoint_configuration.get_registration_settings())
        self._resources = _nooble_resources.NoobleResourcesManager(configuration.get_resources_manager_settings())

        self._configuration = binding_settings
    
    def get_database(self) -> _nooble_database.NoobleDatabase:
        return self._database
    
    def get_mail_service(self) -> _nooble_mail_service.NoobleMailSender:
        return self._mails
    
    def get_registrations(self) -> _registrations.NoobleRegistrationsList:
        return self._registrations
    
    def get_badges(self) -> _nooble_badges.NoobleBadgesList:
        return _nooble_badges.DEFAULT_BADGES_LIST
    
    def get_configuration(self) -> _nooble_conf_files.NoobleBindingSettings:
        return self._configuration
    
    def get_resources(self) -> _nooble_resources.NoobleResourcesManager:
        return self._resources

