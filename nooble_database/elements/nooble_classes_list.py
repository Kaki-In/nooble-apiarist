from .nooble_class import NoobleClass

import database_layering.facades as _database_layering_facades

class NoobleClassList(_database_layering_facades.DatabaseTableFacade[int]):
    def get_class(self, id: int) -> NoobleClass:
        return NoobleClass(self.get_table().get_element(id))
    
    def delete_class(self, id: int) -> None:
        self.get_table().delete_element(self.get_class(id).get_element())

