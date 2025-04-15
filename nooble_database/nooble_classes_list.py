from .nooble_class import ClassDatabaseElement

import database_layering as _database_layering

class NoobleClassListDatabaseTable(_database_layering.DatabaseTableFacade[int]):
    def get_class(self, id: int) -> ClassDatabaseElement:
        return ClassDatabaseElement(self.get_table().get_element(id))
    
    def delete_class(self, id: int) -> None:
        self.get_table().delete_element(self.get_class(id).get_element())

