from .activity_save_file import *

import database as _database
import database_layering.facades as _database_layering_facades

class NoobleActivitySaveFilesList(_database_layering_facades.DatabaseTableFacade[int]):
    def get_save_file(self, id: int) -> NoobleActivitySaveFile:
        return NoobleActivitySaveFile(self.get_table().get_element(id))
    
    def delete_save_file(self, id: int) -> None:
        self.get_table().delete_element(self.get_save_file(id).get_element())




