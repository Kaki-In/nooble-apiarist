from .file import NoobleSettingsFile

import typing as _T

_file_data_type = _T.TypeVar("_file_data_type")
_object_data_type = _T.TypeVar("_object_data_type")

class NoobleSettingsSubFile(_T.Generic[_file_data_type, _object_data_type]):
    def __init__(self, file: NoobleSettingsFile[_file_data_type]) -> None:
        self._file = file

    def get_data(self) -> _object_data_type:
        return self._get_data_from_file(self._file.get_content())

    def _get_data_from_file(self, file_data: _file_data_type) -> _object_data_type:
        raise NotImplementedError("not implemented for " + repr(self))
    
