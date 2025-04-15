from .account import *

import database as _database
import database_layering as _database_layering

class AccountsListDatabaseTable(_database_layering.DatabaseTableFacade[int]):
    def get_account(self, id: int) -> AccountDatabaseElement:
        return AccountDatabaseElement(self.get_table().get_element(id))
    
    def delete_account(self, id: int) -> None:
        self.get_table().delete_element(self.get_account(id).get_element())




