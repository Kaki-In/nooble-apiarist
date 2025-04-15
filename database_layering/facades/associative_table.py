import database as _database

import typing as _T

_Id1Type = _T.TypeVar('_Id1Type')
_Id2Type = _T.TypeVar('_Id2Type')

class DatabaseAssociativeTableFacade(_T.Generic[_Id1Type, _Id2Type]):
    def __init__(self, table: _database.DatabaseAssociativeTable[_Id1Type, _Id2Type]) -> None:
        self._table = table

    def get_table(self) -> _database.DatabaseAssociativeTable[_Id1Type, _Id2Type]:
        return self._table




