from .properties import *

import settings as _settings

class RoundTablesMailSettings(_settings.SettingsObject):
    def __init__(self, directory: _settings.SettingsDirectory):
        super().__init__(directory, [], ['mail.properties'])

        self._properties = RoundTablesMailPropertiesSettings(directory.get_properties('mail.properties'))
    
    def get_properties(self) -> RoundTablesMailPropertiesSettings:
        return self._properties
    
