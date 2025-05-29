import settings as _settings

class RoundTablesMailPropertiesSettings(_settings.SettingsPropertiesList):
    def __init__(self, file: _settings.PropertySettingsFile):
        super().__init__(file, host = [str], user = [str, str], name = [str], hostname = [str])

    def get_mail_host(self) -> str:
        return self.to_str(self.get_file()['host'][0])
    
    def get_user_and_password(self) -> tuple[str, str]:
        data = self.get_file()['user']

        return self.to_str(data[0]), self.to_str(data[1])
    
    def get_name(self) -> str:
        return self.to_str(self.get_file()['name'] [0])
    
    def get_hostname(self) -> str:
        return self.to_str(self.get_file()['hostname'] [0])
    


