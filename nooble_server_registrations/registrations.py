from .registration import NoobleRegistration

import datetime as _datetime
import nooble_database.database as _nooble_database
import random as _random
import nooble_conf.files as _nooble_conf_files

class NoobleRegistrationsList():
    def __init__(self, configuration: _nooble_conf_files.NoobleRegistrationsSettings) -> None:
        self._configuration = configuration

        self._registrations: dict[str, NoobleRegistration] = {}

    def get_configuration(self) -> _nooble_conf_files.NoobleRegistrationsSettings:
        return self._configuration
    
    def get_registration(self, token: str) -> NoobleRegistration:
        return self._registrations[token]
    
    def has_registration(self, token: str) -> bool:
        return token in self._registrations
    
    def add_registration(self, account: _nooble_database.NoobleAccount) -> str:
        token = self.create_new_token()
        self._registrations[token] = NoobleRegistration(account, _datetime.datetime.now() + self._configuration.get_tokens_duration())
        return token
    
    def remove_registration(self, token: str) -> None:
        del self._registrations[token]
    
    def delete_unused_registrations(self) -> None:
        now = _datetime.datetime.now()

        for token in list(self._registrations):
            registration = self._registrations[token]
            if registration.get_date_end() < now:
                del self._registrations[token]
    
    def create_new_token(self) -> str:
        while True:
            a = ""

            for _ in range(self._configuration.get_tokens_size()):
                a += _random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
            
            if not a in self._registrations:
                return a




