from ..base_objects.directory import NoobleSettingsDirectory
from ..base_objects.sub_file import NoobleSettingsSubFile

from ..objects.mail_identity import MailIdentityConfigurationObject

from .nooble_mail_templates import NoobleMailTemplatesConfiguration

import typing as _T

class NoobleTemplatesConfiguration(NoobleSettingsDirectory):
    def __init__(self, pathname: str, identity: NoobleSettingsSubFile[_T.Any, MailIdentityConfigurationObject]) -> None:
        super().__init__(pathname)

        self._mail_templates = NoobleMailTemplatesConfiguration(self._create_sub_element_path("mail"), identity)

    def get_mail_templates(self) -> NoobleMailTemplatesConfiguration:
        return self._mail_templates


