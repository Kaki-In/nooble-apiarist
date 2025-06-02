import nooble_database.database as _nooble_database
import datetime as _datetime

class NoobleRegistration():
    def __init__(self, account: _nooble_database.NoobleAccount, date_end: _datetime.datetime) -> None:
        self._account = account
        self._date_end = date_end
    
    def get_account(self) -> _nooble_database.NoobleAccount:
        return self._account
    
    def get_date_end(self) -> _datetime.datetime:
        return self._date_end

