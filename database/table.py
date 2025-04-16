from .objects import *
from .element import *

import typing as _T

_IdType = _T.TypeVar("_IdType")

class DatabaseTable(_T.Generic[_IdType]):
    def __init__(self, configuration: TableConfiguration) :
        self._conf = configuration
    
    def get_element(self, id: _IdType) -> DatabaseElement[_IdType]:
        return DatabaseElement(ElementConfiguration(self._conf, id))
    
    def add_element(self, **properties: SQLVariable) -> DatabaseElement[_IdType]:
        columns = []
        values = []
        
        for property in properties:
            columns.append(SQLColumn(property))
            values.append(properties[property])
            
        id = self._conf.get_database().send_sql_queries_for_result(
            SQLInsertIntoQuery(SQLTable(self._conf.get_name()), columns, SQLTable(*values)),
            SQLSelectQuery(SQLTable(SQLColumn(("id", SQLFunction("LAST_UPDATE_ID")))))
        )[0]['id']

        return self.get_element(id)
    
    def find_elements_with_clause(self, table_cols: SQLTable | SQLColumn = SQLTable("*"), *clauses: SQLClause) -> list[DatabaseElement[_IdType]]:
        from_clause = SQLClauseFrom(SQLTable(self._conf.get_name()))

        result = self._conf.get_database().send_sql_queries_for_result(SQLSelectQuery(table_cols, from_clause, *clauses))
        
        r_list = []
        for element in result:
            r_list.append(self.get_element(element[self.get_configuration().get_id_column()]))

        return r_list

    def delete_element(self, element: DatabaseElement[_IdType]) -> None:
        from_clause = SQLClauseFrom(SQLTable(self._conf.get_name()))
        where_clause = SQLClauseWhere(SQLOpEquality(SQLColumn(self.get_configuration().get_id_column()), SQLString(str(element.get_configuration().get_id()))))
        
        self._conf.get_database().send_sql_queries(SQLDeleteFromQuery(from_clause, where_clause))
    
    def get_name(self) -> str:
        return self._conf.get_name()
    
    def get_configuration(self) -> TableConfiguration:
        return self._conf
    
    def set_configuration(self, configuration: TableConfiguration) -> None:
        self._conf = configuration
    
    def __len__(self) -> int:
        return len(self.find_elements_with_clause(SQLTable("*")))

