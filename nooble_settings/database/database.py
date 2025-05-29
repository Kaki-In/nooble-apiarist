import settings as _settings

from .properties import *

class RoundTablesDatabaseSettings(_settings.SettingsObject):
    def __init__(self, directory: _settings.SettingsDirectory):
        super().__init__(directory, [], ['database.properties'])

        self._properties = RoundTablesDatabaseSettingsProperties(directory.get_properties('database.properties'))

    def get_properties(self) -> RoundTablesDatabaseSettingsProperties:
        return self._properties
    
