from .users import *
from .properties import *

import settings as _settings

class RoundTablesEndpointSettings(_settings.SettingsObject):
    def __init__(self, directory: _settings.SettingsDirectory):
        super().__init__(directory, ['users', 'sessions'], ['endpoint.properties'])

        self._user_settings = RoundTablesEndpointUserSettings(directory.get_directory('users'))

        self._properties = RoundTablesEndpointPropertiesSettings(directory.get_properties('endpoint.properties'))
    
    def get_user_settings(self) -> RoundTablesEndpointUserSettings:
        return self._user_settings
    
    def get_properties(self) -> RoundTablesEndpointPropertiesSettings:
        return self._properties
    
