from .nooble_mail_identity import NoobleMailIdentitySettings
from .nooble_smtp_server import NoobleSmtpServerSettings

from ..base_objects.file import NoobleSettingsFile
from ..objects.mail_sender import MailSenderConfigurationObject

class NoobleMailSenderSettings(NoobleSettingsFile[MailSenderConfigurationObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            "identity": {
                "address": "no-reply@nooble.flopcreation.fr",
                "name": "Angular Nooble",
                "website": "https://api.nooble-angular.flopcreation.fr"
            },
            "smtp": {
                "smtp_host": "gmail.com",
                "smtp_password": "any",
                "smtp_port": 587,
                "smtp_username": "your.email@gmail.com",
                "uses_ssl": True,
                "uses_starttls": False
            }
        })

    def get_identity_configuration(self) -> NoobleMailIdentitySettings:
        return NoobleMailIdentitySettings(self)
    
    def get_smtp_server_configuration(self) -> NoobleSmtpServerSettings:
        return NoobleSmtpServerSettings(self)


