import database as _database

import typing as _T

_IdType = _T.TypeVar('_IdType')

class DatabaseTableFacade(_T.Generic[_IdType]):
    def __init__(self, table: _database.DatabaseTable[_IdType]) -> None:
        self._table = table

    def get_table(self) -> _database.DatabaseTable[_IdType]:
        return self._table




