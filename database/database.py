import pymysql as _pymysql

from .objects import *
from .table import *
from .associative_table import *

class Database():
    def __init__(self, configuration: DatabaseConfiguration):
        self._conf = configuration
    
    def get_table(self, name: str, column_id:str = 'id') -> DatabaseTable:
        return DatabaseTable(TableConfiguration(self._conf, name, column_id))
    
    def get_associative_table(self, name: str, id1: str, id2: str) -> DatabaseAssociativeTable:
        return DatabaseAssociativeTable(AssociativeTableConfiguration(self._conf, name, id1, id2))
    
    def get_configuration(self) -> DatabaseConfiguration:
        return self._conf
    
    def set_configuration(self, configuration: DatabaseConfiguration) -> None:
        self._conf = configuration
    
