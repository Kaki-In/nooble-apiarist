import database as _database

import typing as _T

_IdType = _T.TypeVar("_IdType")

class DatabaseElementFacade(_T.Generic[_IdType]):
    def __init__(self, element: _database.DatabaseElement[_IdType]) -> None:
        self._element = element

    def get_element(self) -> _database.DatabaseElement[_IdType]:
        return self._element


