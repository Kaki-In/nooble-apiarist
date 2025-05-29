from .default_image import *
from .properties import *

import settings as _settings

class RoundTablesEndpointUserSettings(_settings.SettingsObject):
    def __init__(self, directory: _settings.SettingsDirectory):
        super().__init__(directory, [], ['default_icon.png', 'users.properties'])

        self._default_image = RoundTablesEndpointDefaultUserImageSettings(directory.get_image('default_icon.png'))
    
    def get_default_image(self) -> RoundTablesEndpointDefaultUserImageSettings:
        return self._default_image
    

