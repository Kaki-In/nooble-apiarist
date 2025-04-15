from .element import CachedDatabaseElement

from .._utils.show_query import _show_query
from .._utils.cached_element import _CachedElement

import database as _database

import typing as _T

class CachedAutoIncrementDatabaseTable(_database.DatabaseTable[int], _CachedElement):
    def __init__(self, configuration: _database.TableConfiguration, columns: list[str]) -> None:
        super().__init__(configuration)

        self._columns = columns

        self._children: list[CachedDatabaseElement[int]] = []
        self._deleted_children: list[CachedDatabaseElement[int]] = []
        self._added_children: list[CachedDatabaseElement[int]] = []

        # the auto increment could not fit with distant database ; however, it will be refreshed just before adding waiting elements
        # it is there only to prevent from bad id with new elements (to reduce the lucks that an id changes at the bad moment)
        self._auto_increment = self.request_auto_increment()
    
    def request_auto_increment(self) -> int:
        return int(
            self.get_configuration().get_database().send_sql_query_for_result(  
                _show_query(self.get_configuration().get_name())
            )[0]['Auto_Increment'][0]
        )
    
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
        auto_increment = self.request_auto_increment()

        self._auto_increment = auto_increment + len(self._added_children)

        for i in range(len(self._added_children)):
            added_child = self._added_children[i]

            added_child.get_configuration().set_id(auto_increment + i)

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
    
    def get_element(self, id: int) -> CachedDatabaseElement[int]:
        found_child: CachedDatabaseElement[int] | None = None

        for child in self._added_children + self._children:
            if child.get_configuration().get_id() == id:
                found_child = child
        
        if found_child is None:
            found_child = CachedDatabaseElement(_database.ElementConfiguration(self._conf, id), self._columns)

            if not found_child.exists():
                raise ValueError("this child does not exist")
        
        return found_child
    
    def add_element(self, **properties: _database.SQLVariable) -> None:
        element = CachedDatabaseElement(_database.ElementConfiguration(self._conf, self._auto_increment), self._columns)
        self._auto_increment += 1
        
        self._added_children.append(element)
    
    def find_elements_with_clause(self, table_cols: _database.SQLTable | _database.SQLColumn = _database.SQLTable("*"), *clauses: _database.SQLClause) -> list[CachedDatabaseElement[int]]: # type:ignore
        elements = super().find_elements_with_clause(table_cols, *clauses)

        results = []

        for element in elements: 
            results.append(self.get_element(element.get_configuration().get_id()))
        
        return results
    
    def delete_element(self, element: CachedDatabaseElement) -> None: # type:ignore
        if element in self._children:
            self._children.remove(element)
        
        self._deleted_children.append(element)






