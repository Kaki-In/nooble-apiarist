from .registration import NoobleRegistration

import datetime as _datetime
import nooble_database as _nooble_database
import random as _random

class NoobleRegistrationsList():
    def __init__(self, registrations_duration: _datetime.timedelta, tokens_size: int) -> None:
        self._registrations_duration = registrations_duration
        self._tokens_size = tokens_size

        self._registrations: dict[str, NoobleRegistration] = {}
    
    def get_registrations_duration(self) -> _datetime.timedelta:
        return self._registrations_duration
    
    def get_tokens_size(self) -> int:
        return self._tokens_size
    
    def get_registration(self, token: str) -> NoobleRegistration:
        return self._registrations[token]
    
    def has_registration(self, token: str) -> bool:
        return token in self._registrations
    
    def add_registration(self, account: _nooble_database.NoobleAccount) -> str:
        token = self.create_new_token()
        self._registrations[token] = NoobleRegistration(account, _datetime.datetime.now() + self._registrations_duration)
        return token
    
    def delete_unused_registrations(self) -> None:
        now = _datetime.datetime.now()

        for token in list(self._registrations):
            registration = self._registrations[token]
            if registration.get_date_end() < now:
                del self._registrations[token]
    
    def create_new_token(self) -> str:
        while True:
            a = ""

            for _ in range(self._tokens_size):
                a += _random.choice(''.join([chr(i) for i in range(32, 126)]))
            
            if not a in self._registrations:
                return a




