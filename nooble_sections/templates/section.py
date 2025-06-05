import typing as _T

import nooble_database.database as _nooble_database
import nooble_database.objects as _nooble_database_objects

_data_type = _T.TypeVar("_data_type")
_client_export_data_type = _T.TypeVar("_client_export_data_type")
_database_export_data_type = _T.TypeVar("_database_export_data_type")

class NoobleSection(_T.Generic[_data_type, _client_export_data_type, _database_export_data_type]):
    def __init__(self, type:str, data: _data_type) -> None:
        self._type = type
        self._data = data

    def get_type(self) -> str:
        return self._type

    def get_data(self) -> _data_type:
        return self._data
    
    async def get_used_files(self, database: _nooble_database.NoobleDatabase) -> list[str]:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def get_recursive_used_files(self, database: _nooble_database.NoobleDatabase) -> list[str]:
        return await self.get_used_files(database)
    
    async def export_to_client_json_data(self, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> _client_export_data_type:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def export_to_database_json_data(self, database: _nooble_database.NoobleDatabase) -> _database_export_data_type:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def export_to_client_json(self, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> _nooble_database_objects.section_objects.SectionObject[_client_export_data_type]:
        return {
            "type": self._type,
            "data": await self.export_to_client_json_data(database, account)
        }
    
    async def export_to_database_json(self, database: _nooble_database.NoobleDatabase) -> _nooble_database_objects.section_objects.SectionObject[_database_export_data_type]:
        return {
            "type": self._type,
            "data": await self.export_to_database_json_data(database)
        }
    
    async def is_valid(self, database: _nooble_database.NoobleDatabase) -> bool:
        return True
    


