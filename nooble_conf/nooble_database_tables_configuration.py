from .objects.database_tables import DatabaseTablesConfigurationObject
from .objects.database import DatabaseConfigurationObject
from .templates.sub_file import NoobleSettingsSubFile

class NoobleDatabaseTablesSettings(NoobleSettingsSubFile[DatabaseConfigurationObject, DatabaseTablesConfigurationObject]):
    def _get_data_from_file(self, file_data: DatabaseConfigurationObject) -> DatabaseTablesConfigurationObject:
        return file_data["tables"]
    
    def get_accounts_name(self) -> str:
        return self.get_data()["accounts"]
    
    def get_activities_name(self) -> str:
        return self.get_data()["activities"]
    
    def get_classes_name(self) -> str:
        return self.get_data()["classes"]
    
    def get_decorations_name(self) -> str:
        return self.get_data()["decorations"]
    
    def get_files_name(self) -> str:
        return self.get_data()["files"]


