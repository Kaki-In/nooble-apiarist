from .database_rules import DatabaseRulesConfigurationObject
from .database_tables import DatabaseTablesConfigurationObject

import typing as _T

class DatabaseConfigurationObject(_T.TypedDict):
    host: str
    port: int
    dbname: str

    rules: DatabaseRulesConfigurationObject
    tables: DatabaseTablesConfigurationObject

