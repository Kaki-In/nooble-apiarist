from .variable import *

class SQLOperator(SQLVariable):
    def __init__(self, *variables: SQLVariable | str):
        super().__init__(variables)
        self._variables = variables
    
    def __str__(self) -> str:
        return "0"
    
    def __repr__(self) -> str:
        return repr(str(self))
    
    def __len__(self) -> int:
        return 1 + max([len(i if type(i) is SQLVariable else "") for i in self._variables])


class SQLJoinOn(SQLOperator):
    def __init__(self, condition: SQLVariable, *tables: SQLVariable):
        super().__init__(*tables)
        self._condition = condition

    def __str__(self):
        vars = ""

        for variable in self._variables:
            if vars:
                vars += ", "
            
            vars += str(variable)
                
        return 'JOIN ' + vars + " ON " + str(self._condition)

class SQLTable(SQLOperator):
    def __init__(self, *columns: SQLColumn | str):
        super().__init__(*columns)
    
    def toSql(self) -> str:
        return str(self)
    
    def __str__(self):
        if len(self._variables) == 1 and self._variables[0] != "*":
            return "`" + str(self._variables[0]) + "`"
        
        vars = ""

        for variable in self._variables:
            if vars:
                vars += ", "
            
            vars += str(variable)
                
        return vars 
    
    def __int__(self) -> int:
        return 0


class SQLUnaryOperator(SQLOperator):
    def __init__(self, name: str, value: SQLVariable):
        super().__init__(value)
        self._name = name
    
    def __str__(self) -> str:
        return self._name + " " + str(self._variables[0])

class SQLBinaryOperator(SQLOperator):
    def __init__(self, name: str, first: SQLVariable, second: SQLVariable):
        super().__init__(first, second)
        self._name = name
    
    def __str__(self) -> str:
        variables0: SQLVariable|str = self._variables[0]
        if len(variables0) > 1:
            variables0 = f"({variables0})"

        variables1 = self._variables[1]
        if len(variables1) > 1:
            variables1 = f"({variables1})"

        return str(variables0) + " " + self._name + " " + str(variables1)



class SQLOpNot(SQLUnaryOperator):
    def __init__(self, first: SQLVariable):
        super().__init__("NOT", first)




class SQLOpEquality(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("=", first, second)

class SQLOpLower(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("<", first, second)

class SQLOpGreater(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__(">", first, second)

class SQLOpLowerEqual(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("<=", first, second)

class SQLOpGreaterEqual(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__(">=", first, second)

class SQLOpGreaterUnequal(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("<>", first, second)




class SQLOpLike(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("LIKE", first, second)

class SQLOpAnd(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("AND", first, second)

class SQLOpOr(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("OR", first, second)




class SQLOpAdd(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("+", first, second)

class SQLOpSubstrac(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("-", first, second)

class SQLOpMultiply(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("*", first, second)

class SQLOpDivide(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("/", first, second)

class SQLOpModulo(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("%", first, second)

class SQLOpAndBitwise(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("&", first, second)

class SQLOpOrBitwise(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("|", first, second)

class SQLOpXorBitwise(SQLBinaryOperator):
    def __init__(self, first: SQLVariable, second: SQLVariable):
        super().__init__("^", first, second)


