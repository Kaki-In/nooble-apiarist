from .associative_element import CachedDatabaseAssociativeElement

from .._utils.cached_element import _CachedElement

import database as _database

import typing as _T

_Id1Type = _T.TypeVar('_Id1Type')
_Id2Type = _T.TypeVar('_Id2Type')

class CachedAssociativeDatabaseTable(_database.DatabaseAssociativeTable[_Id1Type, _Id2Type], _CachedElement):
    def __init__(self, configuration: _database.AssociativeTableConfiguration, columns: list[str]) -> None:
        super().__init__(configuration)

        self._columns = columns

        self._children: list[CachedDatabaseAssociativeElement[_Id1Type, _Id2Type]] = []
        self._deleted_children: list[CachedDatabaseAssociativeElement[_Id1Type, _Id2Type]] = []
        self._added_children: list[CachedDatabaseAssociativeElement[_Id1Type, _Id2Type]] = []
    
    def refresh(self) -> None:
        self.upload_updates()
        self.download_updates()
    
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
    
    def get_element(self, id1: _Id1Type, id2: _Id2Type) -> CachedDatabaseAssociativeElement[_Id1Type, _Id2Type]:
        found_child: CachedDatabaseAssociativeElement[_Id1Type, _Id2Type] | None = None

        for child in self._added_children + self._children:
            if child.get_configuration().get_first_id() == id1 and child.get_configuration().get_second_id() == id2:
                found_child = child
        
        if found_child is None:
            found_child = CachedDatabaseAssociativeElement(_database.AssociativeElementConfiguration(self._conf, id1, id2), self._columns)

            if not found_child.exists():
                raise ValueError("this child does not exist")
        
        return found_child
    
    def add_element(self, **properties: _database.SQLVariable) -> CachedDatabaseAssociativeElement:
        id_column_1 = self.get_configuration().get_first_id_column()
        id_column_2 = self.get_configuration().get_second_id_column()

        if not id_column_1 in properties:
            raise ValueError("missing id " + id_column_1)
        
        if not id_column_2 in properties:
            raise ValueError("missing id " + id_column_2)
        
        element = CachedDatabaseAssociativeElement(_database.AssociativeElementConfiguration(self._conf, properties[id_column_1], properties[id_column_2]), self._columns)

        self._added_children.append(element)

        return element
    
    def find_elements_with_clause(self, table_cols: _database.SQLTable | _database.SQLColumn = _database.SQLTable("*"), *clauses: _database.SQLClause) -> list[CachedDatabaseAssociativeElement[_Id1Type, _Id2Type]]: # type:ignore
        elements = super().find_elements_with_clause(table_cols, *clauses)

        results = []

        for element in elements: 
            results.append(self.get_element(element.get_configuration().get_first_id(), element.get_configuration().get_second_id()))
        
        return results
    
    def delete_element(self, element: CachedDatabaseAssociativeElement) -> None: # type:ignore
        if element in self._children:
            self._children.remove(element)
        
        self._deleted_children.append(element)






