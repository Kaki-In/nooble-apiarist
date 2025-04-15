from .operator import *

class SQLClause():
    def __init__(self, name: str, *args: SQLVariable):
        self._name = name
        self._args = args
    
    def __str__(self):
        data = ""
        for arg in self._args:
            if data:
                data += ", "
            data += str(arg)
        
        return self._name + " " + data



class SQLClauseWhere(SQLClause):
    def __init__(self, condition: SQLVariable):
        super().__init__("WHERE", condition)

class SQLClauseFrom(SQLClause):
    def __init__(self, table: SQLVariable):
        super().__init__("FROM", table)

class SQLClauseConstraint(SQLClause):
    def __init__(self, table: SQLVariable):
        super().__init__("CONSTRAINT", table)

class SQLClauseGroupBy(SQLClause):
    def __init__(self, column: SQLVariable):
        super().__init__("GROUP BY", column)

class SQLClauseHaving(SQLClause):
    def __init__(self, condition: SQLVariable):
        super().__init__("HAVING", condition)

class SQLClauseOrderBy(SQLClause):
    def __init__(self, column: SQLVariable):
        super().__init__("ORDER BY", column)

class SQLClauseUsing(SQLClause):
    def __init__(self, column: SQLVariable):
        super().__init__("USING", column)

class SQLClauseWhereCurrent(SQLClause):
    def __init__(self, condition: SQLVariable):
        super().__init__("WHERE CURRENT", condition)

class SQLClauseTop(SQLClause):
    def __init__(self, column: SQLVariable):
        super().__init__("TOP", column)

class SQLClauseDistinct(SQLClause):
    def __init__(self):
        super().__init__("DISTINCT")

class SQLClauseOffset(SQLClause):
    def __init__(self, number: SQLInteger):
        super().__init__("OFFSET", number)

class SQLClauseLimit(SQLClause):
    def __init__(self, number: SQLInteger):
        super().__init__("LIMIT", number)

class SQLClauseDesc(SQLClause):
    def __init__(self):
        super().__init__("DESC")

class SQLClauseSet(SQLClause):
    def __init__(self, *equalities: SQLOpEquality):
        super().__init__("SET", *equalities) 

class SQLClauseValues(SQLClause):
    def __init__(self, *values: SQLVariable):
        super().__init__("VALUES", SQLFunction('', *values))

