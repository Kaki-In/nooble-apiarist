import os as _os

class NoobleSettingsDirectory():
    def __init__(self, pathname:str) -> None:
        if not _os.path.exists(pathname):
            _os.makedirs(pathname)
        
        self._pathname = pathname
    
    def get_pathname(self) -> str:
        return self._pathname
    
    def _create_sub_element_path(self, name:str) -> str:
        return self._pathname + _os.path.sep + name
    
