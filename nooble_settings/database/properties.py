import settings as _settings

class RoundTablesDatabaseSettingsProperties(_settings.SettingsPropertiesList):
    def __init__(self, file: _settings.PropertySettingsFile):
        super().__init__(
            file,
            host = [str, int],
            user = [str, str],
            database = [str]
        )

    def get_host(self) -> tuple[str, int]:
        data = self.get_file()[ 'host' ]
        return self.to_str(data[0]), self.to_int(data[1])
    
    def get_user_and_password(self) -> tuple[str, str]:
        data = self.get_file()[ 'user' ]
        return self.to_str(data[0]), self.to_str(data[1])
    
    def get_database_name(self) -> str:
        return self.to_str(self.get_file()[ 'database' ][0])
    
    def set_host(self, host: str, port: int) -> None:
        self.get_file()['hostname'] = [ self.from_str(host), self.from_int(port) ]
    
    def set_user_and_password(self, user: str, password: str) -> None:
        self.get_file()['user'] = [ self.from_str(user), self.from_str(password) ]
    
    def set_database_name(self, dbname: str) -> None:
        self.get_file()['database'] = [ self.from_str(dbname) ]

