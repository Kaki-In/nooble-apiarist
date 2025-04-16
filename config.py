import nooble_database as _nooble_database
import nooble_server_registrations as _nooble_server_registrations
import database as _database
import datetime as _datetime

import json as _json
import os as _os

import typing as _T

class DatabaseConfiguration():
    def __init__(self, json_data: _T.Any) -> None:
        self._host: str = json_data["host"]
        self._port: int = json_data["port"]
        self._password: str = json_data["password"]
        self._user: str = json_data["user"]
        self._database_name: str = json_data["database_name"]
    
    def get_host(self) -> str:
        return self._host
    
    def get_port(self) -> int:
        return self._port
    
    def get_password(self) -> str:
        return self._password
    
    def get_user(self) -> str:
        return self._user
    
    def get_database_name(self) -> str:
        return self._database_name
    
    def create_database(self) -> _nooble_database.NoobleDatabase:
        return _nooble_database.CachedNoobleDatabase(_database.DatabaseConfiguration(self._host, self._user, self._password, self._database_name))

class RegistrationsConfiguration():
    def __init__(self, json_data: _T.Any) -> None:
        self._tokens_size: int = json_data["tokens_size"]
        self._duration: int = json_data["duration"]
    
    def get_tokens_size(self) -> int:
        return self._tokens_size
    
    def get_duration(self) -> int:
        return self._duration
    
    def create_registrations_list(self) -> _nooble_server_registrations.NoobleRegistrationsList:
        return _nooble_server_registrations.NoobleRegistrationsList(_datetime.timedelta(self._duration), self._tokens_size)

class Configuration():
    def __init__(self, json_data: _T.Any) -> None:
        self._db_config = DatabaseConfiguration(json_data['database'])
        self._rg_config = RegistrationsConfiguration(json_data['registrations'])
    
    def get_db_config(self) -> DatabaseConfiguration:
        return self._db_config
    
    def get_rg_config(self) -> RegistrationsConfiguration:
        return self._rg_config

def _get_configuration() -> Configuration:
    dirname = _os.path.abspath(_os.path.dirname(__file__))
    a = open(dirname + "/config.json", "r")
    data = _json.loads(a.read())
    a.close()

    return Configuration(data)


MAIN_CONFIGURATION = _get_configuration()
