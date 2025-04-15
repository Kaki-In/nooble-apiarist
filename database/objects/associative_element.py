from .associative_table import *

import typing as _T

_Id1Type = _T.TypeVar("_Id1Type")
_Id2Type = _T.TypeVar("_Id2Type")

class AssociativeElementConfiguration(_T.Generic[_Id1Type, _Id2Type]):
    def __init__(self, table: AssociativeTableConfiguration, id1: _Id1Type, id2: _Id2Type):
        self._table = table

        self._id1 = id1
        self._id2 = id2

        if not type(id1) in (int, str) or type(id2) in (int, str):
            raise TypeError()
    
    def get_table(self) -> AssociativeTableConfiguration:
        return self._table
    
    def set_table(self, table: AssociativeTableConfiguration) -> None:
        self._table = table
    
    def get_first_id(self) -> _Id1Type:
        return self._id1
    
    def get_second_id(self) -> _Id2Type:
        return self._id2
    
    def set_first_id(self, id: _Id1Type) -> None:
        self._id1 = id

    def set_second_id(self, id: _Id2Type) -> None:
        self._id2 = id


