from .objects import *
from .associative_element import *

import typing as _T

_Id1Type = _T.TypeVar("_Id1Type")
_Id2Type = _T.TypeVar("_Id2Type")

class DatabaseAssociativeTable(_T.Generic[_Id1Type, _Id2Type]):
    def __init__(self, configuration: AssociativeTableConfiguration) :
        self._conf = configuration
    
    def get_element(self, id1: _Id1Type, id2: _Id2Type) -> DatabaseAssociativeElement[_Id1Type, _Id2Type]:
        return DatabaseAssociativeElement(AssociativeElementConfiguration(self._conf, id1, id2))
    
    def add_element(self, **properties: SQLVariable) -> DatabaseAssociativeElement[_Id1Type, _Id2Type]:
        if not self._conf.get_first_id_column() in properties \
         and not self._conf.get_second_id_column() in properties:
            raise ValueError("missing ids arguments")

        columns = []
        values = []
        
        for property in properties:
            columns.append(SQLColumn(property))
            values.append(properties[property])
            
        self._conf.get_database().send_sql_queries(SQLInsertIntoQuery(SQLTable(self._conf.get_name()), columns, SQLTable(*values)))

        return self.get_element(properties[self._conf.get_first_id_column()].get_value(), properties[self._conf.get_second_id_column()].get_value())
    
    def find_elements_with_clause(self, table_cols: SQLTable | SQLColumn = SQLTable("*"), *clauses: SQLClause) -> list[DatabaseAssociativeElement[_Id1Type, _Id2Type]]:
        from_clause = SQLClauseFrom(SQLTable(self._conf.get_name()))

        result = self._conf.get_database().send_sql_queries_for_result(SQLSelectQuery(table_cols, from_clause, *clauses))
        
        r_list = []
        for element in result:
            r_list.append(self.get_element(element[self.get_configuration().get_first_id_column()], element[self.get_configuration().get_second_id_column()]))

        return r_list

    def delete_element(self, element: DatabaseAssociativeElement[_Id1Type, _Id2Type]) -> None:
        from_clause = SQLClauseFrom(SQLTable(self._conf.get_name()))

        where_clause = SQLClauseWhere(SQLOpAnd(
            SQLOpEquality(SQLColumn(self._conf.get_first_id_column()), SQLString(str(element.get_configuration().get_first_id()))),
            SQLOpEquality(SQLColumn(self._conf.get_second_id_column()), SQLString(str(element.get_configuration().get_second_id()))),
        ))
        
        self._conf.get_database().send_sql_queries(SQLDeleteFromQuery(from_clause, where_clause))
    
    def get_name(self) -> str:
        return self._conf.get_name()
    
    def get_configuration(self) -> AssociativeTableConfiguration:
        return self._conf
    
    def set_configuration(self, configuration: AssociativeTableConfiguration) -> None:
        self._conf = configuration
    
    def __len__(self) -> int:
        return len(self.find_elements_with_clause(SQLTable("*")))

