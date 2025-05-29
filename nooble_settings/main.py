from .endpoint import *
from .database import *
from .mail import *

import settings as _settings
import os as _os

class RoundTablesSettings(_settings.SettingsObject):
    def __init__(self, directory_path: str):
        directory = _settings.SettingsDirectory(_os.path.abspath(directory_path))
        super().__init__(directory, ['endpoint', 'database', 'mail'], [])

        self._endpoint_settings = RoundTablesEndpointSettings(directory.get_directory('endpoint'))
        self._database_settings = RoundTablesDatabaseSettings(directory.get_directory('database'))
        self._mail_settings = RoundTablesMailSettings(directory.get_directory('mail'))
    
    def get_endpoint_settings(self) -> RoundTablesEndpointSettings:
        return self._endpoint_settings

    def get_database_settings(self) -> RoundTablesDatabaseSettings:
        return self._database_settings
    
    def get_mail_settings(self) -> RoundTablesMailSettings:
        return self._mail_settings




