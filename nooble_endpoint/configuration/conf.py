import apiarist_server_endpoint as _server_endpoint

import nooble_server_registrations as _registrations
import nooble_database.database as _nooble_database
import nooble_conf.directories as _nooble_conf_directories
import nooble_conf.files as _nooble_conf_files
import nooble_mail_service as _nooble_mail_service
import nooble_badges.default as _nooble_badges
import nooble_resources_manager as _nooble_resources
import nooble_activities.default as _nooble_activities
import nooble_sections.default as _nooble_sections
import nooble_notifications as _nooble_notifications

class NoobleEndpointConfiguration(_server_endpoint.ServerEndpointConfiguration):
    def __init__(self, configuration: _nooble_conf_directories.NoobleConfiguration):
        endpoint_configuration = configuration.get_endpoint_settings()
        binding_settings = endpoint_configuration.get_binding_settings()

        super().__init__(binding_settings.get_host(), binding_settings.get_port())

        self._database = _nooble_database.NoobleDatabase(configuration.get_database_settings())
        self._mails = _nooble_mail_service.NoobleMailSender(configuration.get_mail_settings(), configuration.get_templates().get_mail_templates())
        self._registrations = _registrations.NoobleRegistrationsList(endpoint_configuration.get_registration_settings())
        self._resources = _nooble_resources.NoobleResourcesManager(configuration.get_resources_manager_settings())

        self._activities_manager = _nooble_activities.get_default_activity_manager(self._resources)
        self._sections_map = _nooble_sections.get_default_sections_map(self._activities_manager, self._resources)

        self._notifications = _nooble_notifications.NoobleAccountsNotifier(self._database)

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
    
    def get_activities(self) -> _nooble_activities.NoobleActivitiesManager:
        return self._activities_manager
    
    def get_sections(self) -> _nooble_sections.NoobleSectionsMap:
        return self._sections_map
    
    def get_notifier(self) -> _nooble_notifications.NoobleAccountsNotifier:
        return self._notifications
    

