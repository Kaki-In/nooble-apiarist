from typing import Any

from .objects import *

import typing as _T

_Id1Type = _T.TypeVar("_Id1Type")
_Id2Type = _T.TypeVar("_Id2Type")

class DatabaseAssociativeElement(_T.Generic[_Id1Type, _Id2Type]):
    def __init__(self, configuration: AssociativeElementConfiguration[_Id1Type, _Id2Type]):
        self._conf = configuration
    
    def get(self, *names: str):
        if len(names) == 0:
            raise ValueError("missing columns to get")
        
        table = self._conf.get_table()
        database = table.get_database()

        from_clause = SQLClauseFrom(SQLTable(table.get_name()))
        where_clause = SQLClauseWhere(SQLOpAnd(
            SQLOpEquality(SQLColumn(self._conf.get_table().get_first_id_column()), SQLString(str(self._conf.get_first_id()))),
            SQLOpEquality(SQLColumn(self._conf.get_table().get_second_id_column()), SQLString(str(self._conf.get_second_id()))),
        ))

        select_query = SQLSelectQuery(
            SQLTable(*[
                SQLColumn(name)
                for name in names
            ]),
            from_clause, where_clause
        )

        result = database.send_sql_query_for_result(select_query)[0]

        return [result[name] for name in names]
    
    def set(self, **name_and_values: SQLVariable) -> None:
        table = self._conf.get_table()
        database = table.get_database()
        
        where_clause = SQLClauseWhere(SQLOpAnd(
            SQLOpEquality(SQLColumn(self._conf.get_table().get_first_id_column()), SQLString(str(self._conf.get_first_id()))),
            SQLOpEquality(SQLColumn(self._conf.get_table().get_second_id_column()), SQLString(str(self._conf.get_second_id()))),
        ))

        operator = SQLClauseSet(
            *[
                SQLOpEquality(SQLColumn(name), name_and_values[name])
                for name in name_and_values
            ]
        )

        database.send_sql_query(SQLUpdateQuery(SQLTable(table.get_name()), operator, where_clause))
    
    def get_configuration(self) -> AssociativeElementConfiguration[_Id1Type, _Id2Type]:
        return self._conf
    
    def set_configuration(self, configuration: AssociativeElementConfiguration[_Id1Type, _Id2Type]) -> None:
        self._conf = configuration
    
    def exists(self) -> bool:
        table = self._conf.get_table()
        database = table.get_database()

        from_clause = SQLClauseFrom(SQLTable(table.get_name()))

        where_clause = SQLClauseWhere(SQLOpAnd(
            SQLOpEquality(SQLColumn(self._conf.get_table().get_first_id_column()), SQLString(str(self._conf.get_first_id()))),
            SQLOpEquality(SQLColumn(self._conf.get_table().get_second_id_column()), SQLString(str(self._conf.get_second_id()))),
        ))

        return bool(database.send_sql_query_for_result(SQLSelectQuery(SQLTable("*"), from_clause, where_clause)))
    
