import json as _json

import typing as _T
import os as _os

_data_type = _T.TypeVar("_data_type")

class NoobleSettingsFile(_T.Generic[_data_type]):
    def __init__(self, path:str, default_content: _data_type) -> None:
        self._path = path

        if not _os.path.exists(path + ".conf"):
            self.overwrite(default_content)

    def get_content(self) -> _data_type:
        a = open(self._path + ".conf", "r")
        data = a.read()
        a.close()

        return _json.loads(data)
    
    def overwrite(self, json_content: _data_type) -> None:
        a = open(self._path + ".conf", "w")
        a.write(_json.dumps(json_content, indent=4))
        a.close()


