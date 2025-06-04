from ..base_objects.file import NoobleSettingsFile
from ..objects.resources_manager import ResourcesManagerConfigurationObject

import os as _os

class NoobleResourcesManagerSettings(NoobleSettingsFile[ResourcesManagerConfigurationObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            "base_directory": _os.environ["HOME" if _os.name == "posix" else "HOMEPATH" if _os.name == "nt" else exit("Could not find user home")]+"/.nooble/uploaded",
            "random_filenames_length": 5
        })
    
    def get_base_directory(self) -> str:
        return self.get_content()['base_directory']
    
    def get_random_filenames_length(self) -> int:
        return self.get_content()['random_filenames_length']



