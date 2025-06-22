from .nooble_binding_configuration import NoobleBindingSettings
from .nooble_registrations_configuration import NoobleRegistrationsSettings

from ..base_objects.file import NoobleSettingsFile

from ..objects.endoint import EndpointConfigurationObject

class NoobleEndpointSettings(NoobleSettingsFile[EndpointConfigurationObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            "binding": {
                "host": "0.0.0.0",
                "host_url": "http://localhost:8622",
                "port": 8622,
                "cert_file": None,
                "key_file": None,
                "use_ssl":  False
            },
            "registrations": {
                "token_duration_minutes": 1440,
                "tokens_size": 256
            }
        })

    def get_binding_settings(self) -> NoobleBindingSettings:
        return NoobleBindingSettings(self)
    
    def get_registration_settings(self) -> NoobleRegistrationsSettings:
        return NoobleRegistrationsSettings(self)


