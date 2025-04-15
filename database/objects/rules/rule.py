from .clause import *

class SQLQueryRule():
    def __init__(self, name: str, preclause: SQLTable | str | None, *clauses: SQLClause):
        self._name = name
        self._preclause = preclause
        self._clauses = clauses
    
    def __str__(self):
        data = self._name
        if self._preclause is not None:
            data += " " + str(self._preclause)
        
        for clause in self._clauses:
            data += " " + str(clause)
        
        return data + ";;"



class SQLSelectQuery(SQLQueryRule):
    def __init__(self, table: SQLTable | SQLColumn, *clauses: SQLClause):
        super().__init__("SELECT", str(table), *clauses)

class SQLInsertIntoQuery(SQLQueryRule):
    def __init__(self, table: SQLTable, columns: list[SQLColumn], values: SQLTable):
        values_names = ""

        for column in columns:
            if values_names:
                values_names += ", "
            values_names += str(column)

        super().__init__("INSERT INTO", str(table) + " (" + values_names + ")", SQLClauseValues(*[i for i in values.get_value()]))

class SQLDeleteFromQuery(SQLQueryRule):
    def __init__(self, *clauses: SQLClause):
        super().__init__("DELETE", None, *clauses)

class SQLUpdateQuery(SQLQueryRule):
    def __init__(self, table: SQLTable, *clauses: SQLClause):
        super().__init__("UPDATE", str(table), *clauses)

