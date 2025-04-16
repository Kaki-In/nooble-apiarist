from .account import *

import database as _database
import database_layering.facades as _database_layering_facades

class NoobleAccountsList(_database_layering_facades.DatabaseTableFacade[int]):
    def get_account(self, id: int) -> NoobleAccount:
        return NoobleAccount(self.get_table().get_element(id))
    
    def delete_account(self, id: int) -> None:
        self.get_table().delete_element(self.get_account(id).get_element())
    
    def create_account(self, mail: str, name:str, surname:str, password:str, is_admin: bool) -> NoobleAccount:
        element = self.get_table().add_element(
            mail = _database.SQLString(mail),
            name = _database.SQLString(name),
            surname = _database.SQLString(surname),
            password = _database.SQLString(password),
            is_admin = _database.SQLBool(is_admin)
        )

        return NoobleAccount(element)




