import database as _database
import database_layering as _database_layering

class ClassSubscriptionDatabaseElement(_database_layering.AssociativeDatabaseElementFacade[int, int]):
    def get_account_id(self) -> int:
        return self.get_element().get_configuration().get_first_id()
    
    def get_class_id(self) -> int:
        return self.get_element().get_configuration().get_second_id()
    
    def is_teacher(self) -> bool:
        return self.get_element().get('as_teacher')[0]
    
    
