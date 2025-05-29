import settings as _settings

class RoundTablesEndpointPropertiesSettings(_settings.SettingsPropertiesList):
    def __init__(self, file: _settings.PropertySettingsFile):
        super().__init__(
            file,
            address = [str, int],
            hostname = [str],
            client_timeout = [int],
            keys = [str, str]
        )
    
    def get_address(self) -> tuple[str, int]:
        data = self.get_file()[ 'address' ]
        return self.to_str(data[0]), self.to_int(data[1])
    
    def get_hostname(self) -> str:
        return self.to_str(self.get_file()[ 'hostname' ][0])
    
    def get_client_timeout(self) -> int:
        return self.to_int(self.get_file()[ 'client_timeout' ][0])
    
    def get_ssl_keys(self) -> tuple[str, str]:
        data = self.get_file()[ 'keys' ]
        return self.to_str(data[0]), self.to_str(data[1])

    def set_address(self, host: str, port: int) -> None:
        self.get_file()['address'] = [self.from_str(host), self.from_int(port)]

    def set_hostname(self, hostname: str) -> None:
        self.get_file()['hostname'] = [self.from_str(hostname)]
    
    def set_client_timeout(self, timeout: int) -> None:
        self.get_file()['client_timeout'] = [self.from_int(timeout)]
    
    def set_ssl_keys(self, public_key: str, private_key: str) -> None:
        self.get_file()['keys'] = [self.from_str(public_key), self.from_str(private_key)]


