import datetime as _datetime
import typing as _T

_value_type = _T.TypeVar('_value_type')

class SQLVariable(_T.Generic[_value_type]):
    def __init__(self, value: _value_type):
        self._value = value

    def get_value(self) -> _value_type:
        return self._value

    def __str__(self) -> str:
        if self._value is None:
            return "NULL"
        return self.toSql()
    
    def toSql(self) -> str:
        return "NULL"
    
    def __repr__(self) -> str:
        return repr(str(self))
    
    def __len__(self) -> int:
        return 0

class SQLNull(SQLVariable[None]):
    def __init__(self):
        super().__init__(None)

class SQLString(SQLVariable[str]):
    def __init__(self, value: str):
        super().__init__(value)
    
    def from_sql(sql_data: str) -> 'SQLString': # type: ignore
        return SQLString(sql_data)
    
    def toSql(self) -> str:
        return repr(self._value)

class SQLBlob(SQLVariable[bytes]):
    def __init__(self, value: bytes):
        super().__init__(value)

    def from_sql(self, sql_data: str) -> 'SQLBlob': # type: ignore
        if sql_data[:2] != "0x":
            raise SyntaxError("invalid blob syntax")
        
        return SQLBlob(bytes.fromhex(sql_data[2:]))
    
    def toSql(self) -> str:
        return "0x" + self.get_value().hex()

class SQLInteger(SQLVariable[int]):
    def __init__(self, value: int):
        super().__init__(value)
    
    def from_sql(sql_data: str) -> 'SQLInteger': # type: ignore
        if sql_data[0] == sql_data[-1] and sql_data[0] in ('"', "'"):
            value = int(sql_data[1:-1])
        else:
            value = int(sql_data)
        return SQLInteger(value)

    def toSql(self) -> str:
        return str(self._value)

class SQLFloat(SQLVariable[float]):
    def __init__(self, value: float):
        super().__init__(value)
    
    def from_sql(sql_data: str) -> 'SQLFloat': # type: ignore
        if sql_data[0] == sql_data[-1] and sql_data[0] in ('"', "'"):
            value = float(sql_data[1:-1])
        else:
            value = float(sql_data)
        
        return SQLFloat(value)
    
    def toSql(self) -> str:
        return str(self._value)

class SQLBool(SQLVariable[bool]):
    def __init__(self, value: bool):
        super().__init__(value)
    
    def from_sql(sql_data: str) -> 'SQLBool': # type: ignore
        if sql_data[0] == sql_data[-1] and sql_data[0] in ('"', "'"):
            value = bool(float(sql_data[1:-1]))
        else:
            value = bool(float(sql_data))
        
        return SQLBool(value)
    
    def toSql(self) -> str:
        return "1" if self._value else "0"

class SQLDate(SQLVariable[_datetime.datetime | _datetime.date]):
    def __init__(self, value: _datetime.datetime | _datetime.date):
        super().__init__(value)
    
    def from_sql(sql_data: str) -> 'SQLDate': # type: ignore
        return SQLDate(_datetime.datetime.strptime(sql_data, '%Y-%m-%d %H:%M:%S'))
    
    def toSql(self) -> str:
        return "'" + self.get_value().strftime('%Y-%m-%d %H:%M:%S') + "'"

class SQLColumn(SQLVariable[str | tuple[str, SQLVariable]]):
    def __init__(self, name: str | tuple[str, SQLVariable]):
        truename = name if type(name) is str else name[0]
        
        for char in truename:
            if not char.lower() in "abcdefghijklmnopqrstuvwxyz_.-":
                raise ValueError("unhautorized column character :" + char)
        
        super().__init__(name)
    
    def from_sql(sql_data: str) -> 'SQLColumn': # type: ignore
        if not (sql_data[0] == sql_data[-1] == '`'):
            raise ValueError("bad column name format")
        
        return SQLColumn(sql_data[1:-1])
    
    def toSql(self) -> str:
        value = self.get_value()

        if type(value) is str:
            return '`' + value + '`'
        else:
            return str(value[1]) + " AS " + '`' + value[0] + '`'

class SQLRenamedColumn(SQLColumn):
    def __init__(self, name: str, content: SQLVariable[str]):
        super().__init__((name, content))
    
class SQLFunction(SQLVariable[tuple[str, tuple[SQLVariable, ...]]]):
    def __init__(self, name: str, *vars: SQLVariable):
        super().__init__((name, vars))
    
    def toSql(self) -> str:
        name, vars = self.get_value()
        args = ""
        for arg in vars:
            if args:
                args += ", "
            
            args += str(arg)
        
        return name  + "(" + args + ")"
    
