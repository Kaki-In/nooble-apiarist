from .element import CachedDatabaseElement

from .._utils.cached_element import _CachedElement

import database as _database

import typing as _T

_IdType = _T.TypeVar('_IdType')

class CachedNonAutoIncrementDatabaseTable(_database.DatabaseTable[_IdType], _CachedElement):
    def __init__(self, configuration: _database.TableConfiguration, columns: list[str]) -> None:
        super().__init__(configuration)

        self._columns = columns

        self._children: list[CachedDatabaseElement[_IdType]] = []
        self._deleted_children: list[CachedDatabaseElement[_IdType]] = []
        self._added_children: list[CachedDatabaseElement[_IdType]] = []
    
    def download_updates(self) -> None:
        for child in self._children.copy():
            if child.exists() and not child.is_auto_refreshing():
                child.download_updates()
            else:
                self._children.remove(child)
    
    def upload_updates(self) -> None:
        for child in self._children:
            if not child.is_auto_refreshing():
                child.upload_updates()
        
        self.delete_waiting_children()
        self.add_waiting_children()

    def add_waiting_children(self) -> None:
        for i in range(len(self._added_children)):
            added_child = self._added_children[i]

            super().add_element(
                **added_child._modified_values
            )

            self._added_children.remove(added_child)
            self._children.append(added_child)
        
    
    def delete_waiting_children(self) -> None:
        for child in self._deleted_children:
            if child.exists():
                super().delete_element(child)
        
        self._deleted_children = []
    
    def get_element(self, id: _IdType) -> CachedDatabaseElement[_IdType]:
        found_child: CachedDatabaseElement[_IdType] | None = None

        for child in self._added_children + self._children:
            if child.get_configuration().get_id() == id:
                found_child = child
        
        if found_child is None:
            found_child = CachedDatabaseElement(_database.ElementConfiguration(self._conf, id), self._columns)

            if not found_child.exists():
                raise ValueError("this child does not exist")
        
        return found_child
    
    def add_element(self, **properties: _database.SQLVariable) -> None:
        id_column = self.get_configuration().get_id_column()

        if not id_column in properties:
            raise ValueError("missing id")
        
        element = CachedDatabaseElement(_database.ElementConfiguration(self._conf, properties[id_column]), self._columns)

        self._added_children.append(element)
    
    def find_elements_with_clause(self, table_cols: _database.SQLTable | _database.SQLColumn = _database.SQLTable("*"), *clauses: _database.SQLClause) -> list[CachedDatabaseElement[_IdType]]: # type:ignore
        elements = super().find_elements_with_clause(table_cols, *clauses)

        results = []

        for element in elements: 
            results.append(self.get_element(element.get_configuration().get_id()))
        
        return results
    
    def delete_element(self, element: CachedDatabaseElement) -> None: # type:ignore
        if element in self._children:
            self._children.remove(element)
        
        self._deleted_children.append(element)






