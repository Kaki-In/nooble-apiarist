from .table import *

import typing as _T

_IdType = _T.TypeVar("_IdType")

class ElementConfiguration(_T.Generic[_IdType]):
    def __init__(self, table: TableConfiguration, id: _IdType):
        self._table = table
        self._id = id

        if not type(id) in (int, str):
            raise TypeError()
    
    def get_table(self) -> TableConfiguration:
        return self._table
    
    def set_table(self, table: TableConfiguration) -> None:
        self._table = table
    
    def get_id(self) -> _IdType:
        return self._id
    
    def set_id(self, id: _IdType) -> None:
        self._id = id

