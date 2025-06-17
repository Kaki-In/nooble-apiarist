from .file import NoobleFileResource

import nooble_conf.files as _nooble_conf_files
import random as _random
import os as _os
import datetime as _datetime

class NoobleResourcesManager():
    def __init__(self, configuration: _nooble_conf_files.NoobleResourcesManagerSettings):
        self._configuration = configuration

        if not _os.path.exists(self._configuration.get_base_directory()):
            _os.makedirs(self._configuration.get_base_directory())

    def get_configuration(self) -> _nooble_conf_files.NoobleResourcesManagerSettings:
        return self._configuration
    
    def create_file(self, content: bytes) -> NoobleFileResource:
        filename = self.create_random_filepath()

        basedir_filename = self._configuration.get_base_directory() + _os.path.sep + filename

        dirname = _os.path.dirname(basedir_filename)

        if not _os.path.exists(dirname):
            _os.makedirs(dirname)

        a = open(basedir_filename, 'wb')
        a.write(content)
        a.close()

        return NoobleFileResource(self._configuration.get_base_directory(), filename)

    def create_random_filepath(self) -> str:
        a = ""

        dirpath = self.get_actual_dirpath()

        based_dirpath = self._configuration.get_base_directory() + _os.path.sep + dirpath
        
        while not a or (_os.path.exists(based_dirpath) and a in _os.listdir(based_dirpath)):
            a = ""

            for _ in range(self._configuration.get_random_filenames_length()):
                a += _random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

        return dirpath + _os.path.sep + a

    def get_actual_dirpath(self) -> str:
        actual_date = _datetime.datetime.now()

        return f"{actual_date.year}{actual_date.month}{actual_date.day}"
    
    def get_file(self, path:str) -> NoobleFileResource:
        return NoobleFileResource(self._configuration.get_base_directory(), path)

