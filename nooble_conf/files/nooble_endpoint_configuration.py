from .nooble_binding_configuration import NoobleBindingSettings

from ..base_objects.file import NoobleSettingsFile

from ..objects.endoint import EndpointConfigurationObject

class NoobleEndpointSettings(NoobleSettingsFile[EndpointConfigurationObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            "binding": {
                "host": "0.0.0.0",
                 "port": 8622,
                 "public_key_file": None,
                 "private_key_file": None,
                 "use_ssl":  False
            },
            "registrations": {
                "token_duration_minutes": 1440,
                "tokens_size": 256
            }
        })

    def get_binding_settings(self) -> NoobleBindingSettings:
        return NoobleBindingSettings(self)


