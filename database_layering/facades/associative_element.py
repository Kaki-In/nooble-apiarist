import database as _database

import typing as _T

_Id1Type = _T.TypeVar("_Id1Type")
_Id2Type = _T.TypeVar("_Id2Type")

class AssociativeDatabaseElementFacade(_T.Generic[_Id1Type, _Id2Type]):
    def __init__(self, element: _database.DatabaseAssociativeElement[_Id1Type, _Id2Type]) -> None:
        self._element = element
    
    def get_element(self) -> _database.DatabaseAssociativeElement[_Id1Type, _Id2Type]:
        return self._element


