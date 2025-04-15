import database as _database

from .._utils.cached_element import _CachedElement

import typing as _T

_Id1Type = _T.TypeVar("_Id1Type")
_Id2Type = _T.TypeVar("_Id2Type")

class CachedDatabaseAssociativeElement(_T.Generic[_Id1Type, _Id2Type], _database.DatabaseAssociativeElement[_Id1Type, _Id2Type], _CachedElement):
    def __init__(self, configuration: _database.AssociativeElementConfiguration, columns: list[str]) -> None:
        super().__init__(configuration)

        self._values: dict[str, _T.Any] = {}

        if self.exists():
            values = super().get(*columns)
        else:
            values = [None] * len(columns)

        for name in range(len(columns)):
            self._values[columns[name]] = values[name]
    
        self._modified_values: dict[str, _database.SQLVariable] = {}
    
    def download_updates(self) -> None:
        if not self.exists():
            return
        
        columns = list(self._values)

        values = super().get(*columns)

        for name in range(len(columns)):
            self._values[columns[name]] = values[name]
    
    def upload_updates(self) -> None:
        if not self.exists():
            return
        
        super().set(
            **self._modified_values
        )

        self._modified_values = {}
    
    def get(self, *columns: str) -> _T.Any:
        result = []

        for column in columns:
            if column in self._modified_values:
                value = self._modified_values[column].get_value()
            
            elif column in self._values:
                value = self._values[column]
            
            else:
                raise ValueError('unknown column ' + repr(column))
            
            result.append(value)
     
        return result
    
    def set(self, **data: _database.SQLVariable) -> None:
        self._modified_values.update(data)
    

