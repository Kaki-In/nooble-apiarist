from .associative_table import CachedAssociativeDatabaseTable
from .ai_table import CachedAutoIncrementDatabaseTable
from .non_ai_table import CachedNonAutoIncrementDatabaseTable

from ..enums.cached_table_type import CachedTableType
from .._utils.cached_element import _CachedElement

import database as _database
import typing as _T

class CachedDatabase(_database.Database, _CachedElement):
    """
    This database is a cached database, which first loads and caches the tables contents.
    """

    def __init__(self, configuration: _database.DatabaseConfiguration, **tables: (tuple[_T.Literal[CachedTableType.ASSOCIATIVE_TABLE], tuple[str, str], list[str]] | tuple[_T.Literal[CachedTableType.NON_AUTO_INCREMENT_TABLE, CachedTableType.AUTO_INCREMENT_TABLE], str, list[str]])):
        super().__init__(configuration)

        self._tables: dict[str, CachedAssociativeDatabaseTable | CachedAutoIncrementDatabaseTable | CachedNonAutoIncrementDatabaseTable] = {}
        
        for table_name in tables:
            table_info = tables[table_name]

            if table_info[0] == CachedTableType.ASSOCIATIVE_TABLE:
                col1, col2 = table_info[1]

                table = CachedAssociativeDatabaseTable(_database.AssociativeTableConfiguration(configuration, table_name, col1, col2), table_info[2])
            
            elif table_info[0] in (CachedTableType.AUTO_INCREMENT_TABLE, CachedTableType.NON_AUTO_INCREMENT_TABLE):

                table = CachedAutoIncrementDatabaseTable(_database.TableConfiguration(configuration, table_name, table_info[1]), table_info[2])
            
            else:
                raise ValueError("invalid table type")
            
            self._tables[table_name] = table
    
    def download_updates(self) -> None:
        for table_name in self._tables:
            table = self._tables[table_name]

            if not table.is_auto_refreshing():
                table.download_updates()
    
    def upload_updates(self) -> None:
        for table_name in self._tables:
            table = self._tables[table_name]

            if not table.is_auto_refreshing():
                table.upload_updates()
    
    def get_table(self, name: str, column_id: str = 'id') -> CachedAutoIncrementDatabaseTable | CachedNonAutoIncrementDatabaseTable:
        return self._tables[name] # type:ignore
    
    def get_associative_table(self, name: str, column_id: str = 'id') -> CachedAssociativeDatabaseTable: # type:ignore
        return self._tables[name] # type:ignore
    


