from .database import *

import typing as _T

_IdType = _T.TypeVar("_IdType")

class TableConfiguration(_T.Generic[_IdType]):
    def __init__(self, database: DatabaseConfiguration, name: str, id_column: str = 'id'):
        self._database = database
        self._name = name
        self._id_column = id_column
    
    def get_database(self) -> DatabaseConfiguration:
        return self._database
    
    def get_name(self) -> str:
        return self._name
    
    def get_id_column(self) -> str:
        return self._id_column

    def set_database(self, database: DatabaseConfiguration) -> None:
        self._database = database
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_id_column(self, id: str) -> None:
        self._id_column = id
    
