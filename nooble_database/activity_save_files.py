from .activity_save_file import *

import database as _database
import database_layering as _database_layering

class ActivitySaveFilesListDatabaseTable(_database_layering.DatabaseTableFacade[int]):
    def get_save_file(self, id: int) -> ActivitySaveFileDatabaseElement:
        return ActivitySaveFileDatabaseElement(self.get_table().get_element(id))
    
    def delete_save_file(self, id: int) -> None:
        self.get_table().delete_element(self.get_save_file(id).get_element())




