import typing as _T

from .objects import *

_IdType = _T.TypeVar("_IdType")

class DatabaseElement(_T.Generic[_IdType]):
    def __init__(self, configuration: ElementConfiguration[_IdType]):
        self._conf = configuration
    
    def get(self, *names: str) -> list:
        if len(names) == 0:
            raise ValueError("missing something to get")
        
        table = self._conf.get_table()
        database = table.get_database()

        from_clause = SQLClauseFrom(SQLTable(table.get_name()))
        where_clause = SQLClauseWhere(SQLOpEquality(SQLColumn(self._conf.get_table().get_id_column()), SQLString(str(self._conf.get_id()))))

        result = database.send_sql_query_for_result(SQLSelectQuery(SQLTable(*[SQLColumn(name) for name in names]), from_clause, where_clause))[0]

        return [result[name] for name in names]
    
    def set(self, **names_and_values: SQLVariable) -> None:
        table = self._conf.get_table()
        database = table.get_database()
        
        where_clause = SQLClauseWhere(SQLOpEquality(SQLColumn(self._conf.get_table().get_id_column()), SQLString(str(self._conf.get_id()))))

        operator = SQLClauseSet(
            *[
                SQLOpEquality(SQLColumn(name), names_and_values[name])
                for name in names_and_values
            ]
        )

        database.send_sql_query(SQLUpdateQuery(SQLTable(table.get_name()), operator, where_clause))
    
    def get_configuration(self) -> ElementConfiguration[_IdType]:
        return self._conf
    
    def set_configuration(self, configuration: ElementConfiguration[_IdType]) -> None:
        self._conf = configuration
    
    def exists(self) -> bool:
        table = self._conf.get_table()
        database = table.get_database()

        from_clause = SQLClauseFrom(SQLTable(table.get_name()))
        where_clause = SQLClauseWhere(SQLOpEquality(SQLColumn(self._conf.get_table().get_id_column()), SQLString(str(self._conf.get_id()))))

        return bool(database.send_sql_query_for_result(SQLSelectQuery(SQLTable("*"), from_clause, where_clause)))
    
