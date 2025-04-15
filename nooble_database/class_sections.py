from .class_section import *

import database as _database
import database_layering as _database_layering

class ClassSectionsListDatabaseTable(_database_layering.DatabaseTableFacade[int]):
    def get_section(self, id: int) -> ClassSectionDatabaseElement:
        return ClassSectionDatabaseElement(self.get_table().get_element(id))
    
    def delete_section(self, id: int) -> None:
        self.get_table().delete_element(self.get_section(id).get_element())




