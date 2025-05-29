from .templates.directory import NoobleSettingsDirectory
from .nooble_database_configuration import NoobleDatabaseConfiguration

import os as _os

if _os.name == "posix":     # linux systems
    DEFAULT_CONF_DIR = _os.environ["HOME"] + _os.path.sep + ".nooble"
elif _os.name == "nt":      # windows systems
    DEFAULT_CONF_DIR = _os.environ["HOME_PATH"] + _os.path.sep + ".nooble"

class NoobleConfiguration(NoobleSettingsDirectory):
    def __init__(self) -> None:
        super().__init__( DEFAULT_CONF_DIR )

        self._db_configuration = NoobleDatabaseConfiguration(self._create_sub_element_path("database"))

    def get_database_configuration(self) -> NoobleDatabaseConfiguration:
        return self._db_configuration


