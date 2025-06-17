import nooble_database.database as _nooble_database
import nooble_database.objects as _nooble_database_objects

import typing as _T

class NoobleActivity():
    def __init__(self, name:str) -> None:
        self._name = name
    
    def get_name(self) -> str:
        return self._name
    
    def create_empty_file(self) -> bytes:
        raise NotImplementedError("not implemented for " + repr(self))
    
    def get_resource_url(self, name:str) -> str:
        return "/activities/resource/" + self._name + "/" + name
    
    def get_file_url(self, file_id: str) -> str:
        return f"/resources/download?id={file_id}&type=section file"
    
    async def get_javascript(self, file:bytes, database: _nooble_database.NoobleDatabase, account:_nooble_database.NoobleAccount) -> str:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def get_editable_javascript(self, file:bytes, database: _nooble_database.NoobleDatabase, account:_nooble_database.NoobleAccount) -> str:
        raise NotImplementedError("not implemented for " + repr(self))
    
    def get_css(self) -> str:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def get_arguments(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> _T.Any:
        return None
    
    async def get_used_files(self, file: bytes, database: _nooble_database.NoobleDatabase) -> list[str]:
        return []
    

