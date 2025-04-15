from .class_section import *

import database as _database
import database_layering.facades as _database_layering_facades

class NoobleClassSectionsList(_database_layering_facades.DatabaseTableFacade[int]):
    def get_section(self, id: int) -> NoobleClassSection:
        return NoobleClassSection(self.get_table().get_element(id))
    
    def delete_section(self, id: int) -> None:
        self.get_table().delete_element(self.get_section(id).get_element())




