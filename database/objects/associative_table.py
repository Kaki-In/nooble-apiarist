from .database import *

import typing as _T

_Id1Type = _T.TypeVar("_Id1Type")
_Id2Type = _T.TypeVar("_Id2Type")

class AssociativeTableConfiguration(_T.Generic[_Id1Type, _Id2Type]):
    def __init__(self, database: DatabaseConfiguration, name: str, id1_column: str = 'id', id2_column: str = 'id'):
        self._database = database
        self._name = name
        self._id1_column = id1_column
        self._id2_column = id2_column
    
    def get_database(self) -> DatabaseConfiguration:
        return self._database
    
    def get_name(self) -> str:
        return self._name
    
    def get_first_id_column(self) -> str:
        return self._id1_column
    
    def get_second_id_column(self) -> str:
        return self._id2_column

    def set_database(self, database: DatabaseConfiguration) -> None:
        self._database = database
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_first_id_column(self, id: str) -> None:
        self._id1_column = id

    def set_second_id_column(self, id: str) -> None:
        self._id1_column = id
    
