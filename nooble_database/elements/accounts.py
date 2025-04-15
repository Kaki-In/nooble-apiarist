from .account import *

import database as _database
import database_layering.facades as _database_layering_facades

class NoobleAccountsList(_database_layering_facades.DatabaseTableFacade[int]):
    def get_account(self, id: int) -> NoobleAccount:
        return NoobleAccount(self.get_table().get_element(id))
    
    def delete_account(self, id: int) -> None:
        self.get_table().delete_element(self.get_account(id).get_element())




