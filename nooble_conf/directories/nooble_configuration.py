from .nooble_templates import NoobleTemplatesConfiguration

from ..base_objects.directory import NoobleSettingsDirectory

from ..files.nooble_database_configuration import NoobleDatabaseSettings
from ..files.nooble_mail_sender import NoobleMailSenderSettings
from ..files.nooble_endpoint_configuration import NoobleEndpointSettings
from ..files.nooble_resources_manager import NoobleResourcesManagerSettings

import os as _os
import typing as _T

if _os.name == "posix":     # linux systems
    DEFAULT_CONF_DIR = _os.environ["HOME"] + _os.path.sep + ".nooble"
elif _os.name == "nt":      # windows systems
    DEFAULT_CONF_DIR = _os.environ["HOMEPATH"] + _os.path.sep + ".nooble"

class NoobleConfiguration(NoobleSettingsDirectory):
    def __init__(self, dirname:_T.Optional[str] = None) -> None:
        super().__init__( dirname or DEFAULT_CONF_DIR )

        self._db_configuration = NoobleDatabaseSettings(self._create_sub_element_path("database"))
        self._mail_configuration = NoobleMailSenderSettings(self._create_sub_element_path("mail"))
        self._templates = NoobleTemplatesConfiguration(self._create_sub_element_path("templates"), self._mail_configuration.get_identity_configuration())
        self._endpoint_configuration = NoobleEndpointSettings(self._create_sub_element_path("endpoint"))
        self._resources_manager_configuration = NoobleResourcesManagerSettings(self._create_sub_element_path("resources_manager"))

    def get_database_settings(self) -> NoobleDatabaseSettings:
        return self._db_configuration
    
    def get_mail_settings(self) -> NoobleMailSenderSettings:
        return self._mail_configuration
    
    def get_templates(self) -> NoobleTemplatesConfiguration:
        return self._templates
    
    def get_endpoint_settings(self) -> NoobleEndpointSettings:
        return self._endpoint_configuration
    
    def get_resources_manager_settings(self) -> NoobleResourcesManagerSettings:
        return self._resources_manager_configuration


