from .nooble_templates import NoobleTemplatesConfiguration
from ..files.nooble_database_configuration import NoobleDatabaseConfiguration

from ..base_objects.directory import NoobleSettingsDirectory

from ..files.nooble_mail_sender import NoobleMailSenderConfiguration

import os as _os
import typing as _T

if _os.name == "posix":     # linux systems
    DEFAULT_CONF_DIR = _os.environ["HOME"] + _os.path.sep + ".nooble"
elif _os.name == "nt":      # windows systems
    DEFAULT_CONF_DIR = _os.environ["HOME_PATH"] + _os.path.sep + ".nooble"

class NoobleConfiguration(NoobleSettingsDirectory):
    def __init__(self, dirname:_T.Optional[str] = None) -> None:
        super().__init__( dirname or DEFAULT_CONF_DIR )

        self._db_configuration = NoobleDatabaseConfiguration(self._create_sub_element_path("database"))
        self._mail_configuration = NoobleMailSenderConfiguration(self._create_sub_element_path("mail"))
        self._templates = NoobleTemplatesConfiguration(self._create_sub_element_path("templates"), self._mail_configuration.get_identity_configuration())

    def get_database_configuration(self) -> NoobleDatabaseConfiguration:
        return self._db_configuration
    
    def get_mail_configuration(self) -> NoobleMailSenderConfiguration:
        return self._mail_configuration
    
    def get_templates(self) -> NoobleTemplatesConfiguration:
        return self._templates


