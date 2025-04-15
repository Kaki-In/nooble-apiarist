import database as _database

class _show_query(_database.SQLQueryRule):
    def __init__(self, name: str):
        super().__init__("SHOW", "TABLE STATUS LIKE " + _database.SQLTable(name).toSql())

