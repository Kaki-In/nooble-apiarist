import database as _database

class DatabaseFacade():
    def __init__(self, database: _database.Database) -> None:
        self._database = database
    
    def get_database(self) -> _database.Database:
        return self._database




