from ..objects.database_rules import DatabaseRulesConfigurationObject
from ..objects.database import DatabaseConfigurationObject
from ..base_objects.sub_file import NoobleSettingsSubFile

class NoobleDatabaseRulesSettings(NoobleSettingsSubFile[DatabaseConfigurationObject, DatabaseRulesConfigurationObject]):
    def _get_data_from_file(self, file_data: DatabaseConfigurationObject) -> DatabaseRulesConfigurationObject:
        return file_data['rules']
    
    def get_new_users_nooblards_count(self) -> int:
        return self.get_data()['default_users_nooblards']


