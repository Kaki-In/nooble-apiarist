from .templates.file import NoobleSettingsFile
from .objects.database import DatabaseConfigurationObject
from .nooble_database_rules import NoobleDatabaseRulesSettings
from .nooble_database_tables_configuration import NoobleDatabaseTablesSettings

class NoobleDatabaseConfiguration(NoobleSettingsFile[DatabaseConfigurationObject]):
    def __init__(self, path: str) -> None:
        super().__init__(path, {
            "host": "localhost",
            "port": 27017,
            "dbname": "nooble-we4b-si40-sy43",

            "rules": {
                "default_users_nooblards": 20
            },

            "tables": {
                "accounts": "accounts",
                "activities": "activities",
                "classes": "classes",
                "decorations": "decorations",
                "files": "files"
            }
        })

    def get_host(self) -> str:
        return self.get_content()["host"]
    
    def get_port(self) -> int:
        return self.get_content()["port"]
    
    def get_dbname(self) -> str:
        return self.get_content()["dbname"]
    
    def get_rules(self) -> NoobleDatabaseRulesSettings:
        return NoobleDatabaseRulesSettings(self)
    
    def get_tables(self) -> NoobleDatabaseTablesSettings:
        return NoobleDatabaseTablesSettings(self)


