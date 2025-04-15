from .accounts import AccountsListDatabaseTable
from .activity_save_files import ActivitySaveFilesListDatabaseTable
from .class_sections import ClassSectionsListDatabaseTable
from .class_subscriptions import ClassSubscriptionsListDatabaseTable

import database_layering as _database_layering

class NoobleDatabase(_database_layering.DatabaseFacade):
    def get_accounts_list(self) -> AccountsListDatabaseTable:
        return AccountsListDatabaseTable(
            self.get_database().get_table('accounts')
        )
    
    def get_activity_save_files_list(self) -> ActivitySaveFilesListDatabaseTable:
        return ActivitySaveFilesListDatabaseTable(
            self.get_database().get_table('activity_savefiles')
        )
    
    def get_classes_list(self) -> ClassSectionsListDatabaseTable:
        return ClassSectionsListDatabaseTable(
            self.get_database().get_table('classes')
        )
    
    def get_class_sections(self) -> ClassSectionsListDatabaseTable:
        return ClassSectionsListDatabaseTable(
            self.get_database().get_table('class_sections')
        )
    
    def get_class_subscriptions_list(self) -> ClassSubscriptionsListDatabaseTable:
        return ClassSubscriptionsListDatabaseTable(
            self.get_database().get_associative_table('class_subscriptions', 'account', 'class')
        )

