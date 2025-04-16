import pymysql as _pymysql
import datetime as _datetime
import typing as _T

from .rules import *

class DatabaseConfiguration():
    def __init__(self, host: str, user: str, password: str, name: str):
        self._host = host
        self._user = user
        self._password = password
        self._name = name
    
    def get_host(self) -> str:
        return self._host
    
    def get_user(self) -> str:
        return self._user
    
    def get_password(self) -> str:
        return self._password
    
    def get_name(self) -> str:
        return self._name
    
    def set_host(self, host:str) -> None:
        self._host = host
    
    def set_user(self, user:str) -> None:
        self._host = user
    
    def set_password(self, password:str) -> None:
        self._host = password
    
    def set_name(self, name:str) -> None:
        self._host = name
    
    def send_sql_queries(self, *queries: SQLQueryRule) -> None:
        connection = _pymysql.connect(
            host = self.get_host(),
            user = self.get_user(),
            password = self.get_password(),
            database = self.get_name(),
            cursorclass = _pymysql.cursors.DictCursor) # type: ignore
        
        try:
            with connection.cursor() as cursor:
                for query in queries:
                    cursor.execute(str(query))
            
            connection.commit()
        except Exception as exc:
            print("Error while handling query", *queries)
            raise
    
    def send_sql_queries_for_result(self, *queries: SQLQueryRule) -> tuple[dict[str, _T.Any]]:
        connection = _pymysql.connect(
            host = self.get_host(),
            user = self.get_user(),
            password = self.get_password(),
            database = self.get_name(),
            cursorclass = _pymysql.cursors.DictCursor) # type: ignore
        
        try:
            with connection.cursor() as cursor:
                for query in queries:
                    cursor.execute(str(query))
                result = cursor.fetchall()
        
            return result # type: ignore
        except Exception as exc:
            print("Error while handling query", *queries)
            raise
