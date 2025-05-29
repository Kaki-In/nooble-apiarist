import settings as _settings

class RoundTablesEndpointDefaultUserImageSettings(_settings.SettingsImage):
    def __init__(self, file: _settings.ImageSettingsFile):
        super().__init__(file, required_dimensions=(
            256, 256
        ))
