from database.database import Database
from .accounts import NoobleAccountsList
from .activity_save_files import NoobleActivitySaveFilesList
from .class_sections import NoobleClassSectionsList
from .class_subscriptions import NoobleClassSubscriptionsList

import database_layering.facades as _database_layering_facades

class NoobleDatabase(_database_layering_facades.DatabaseFacade):
    def get_accounts_list(self) -> NoobleAccountsList:
        return NoobleAccountsList(
            self.get_database().get_table('accounts')
        )
    
    def get_activity_save_files_list(self) -> NoobleActivitySaveFilesList:
        return NoobleActivitySaveFilesList(
            self.get_database().get_table('activity_savefiles')
        )
    
    def get_classes_list(self) -> NoobleClassSectionsList:
        return NoobleClassSectionsList(
            self.get_database().get_table('classes')
        )
    
    def get_class_sections(self) -> NoobleClassSectionsList:
        return NoobleClassSectionsList(
            self.get_database().get_table('class_sections')
        )
    
    def get_class_subscriptions_list(self) -> NoobleClassSubscriptionsList:
        return NoobleClassSubscriptionsList(
            self.get_database().get_associative_table('class_subscriptions', 'account', 'class')
        )

