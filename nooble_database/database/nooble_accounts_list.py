import pymongo.asynchronous.collection as _pymongo_collection
from ..templates.nooble_collection import NoobleCollection
from .nooble_account import NoobleAccount
from ..objects.account_object import AccountObject

import re as _regex
import nooble_conf.files as _nooble_conf_files
import datetime as _datetime

class NoobleAccountsList(NoobleCollection[AccountObject]):
    def __init__(self, collection: _pymongo_collection.AsyncCollection[AccountObject], rules: _nooble_conf_files.NoobleDatabaseRulesSettings) -> None:
        super().__init__(collection)

        self._rules = rules

    def get_account(self, account_id: str) -> NoobleAccount:
        return NoobleAccount(self.get_collection(), account_id)
    
    async def get_existing_account_by_mail(self, mail:str) -> NoobleAccount:
        account = await self.get_account_by_mail(mail)

        if account is None:
            raise ReferenceError("no account using this mail adress")
        
        return account
    
    async def get_account_by_mail(self, mail: str) -> NoobleAccount | None:
        account = await self.find_one({"mail": mail})

        if account is None or account["_id"] is None:
            return None

        return NoobleAccount(self.get_collection(), account["_id"], account)
    
    async def get_decoration_owners(self, decoration_id: str) -> list[NoobleAccount]:
        return [
            NoobleAccount(
                self.get_collection(),
                account_data["_id"],
                account_data
            )

            for account_data in await self.find(
                {
                    "safe.decorations": decoration_id
                }
            )
        ]
    
    async def get_accounts_containing_username(self, username:str) -> list[NoobleAccount]:
        return [
            NoobleAccount(
                self.get_collection(),
                account_data["_id"],
                account_data
            )

            for account_data in await self.find(
                {
                    "mail": {
                        '$regex': _regex.escape(username),
                        '$options': 'i' # case insensitive
                    }
                }
            )
        ]
    
    async def create_new_account(self, mail: str, password: str, first_name: str, last_name: str) -> NoobleAccount:
        object: AccountObject = {
            "activities": [],
            "mail": mail,
            "password": password,
            "profile": {
                "active_badges": [],
                "active_decoration": None,
                "description": "Neither more nor less than {first_name} {last_name}",
                "first_name": first_name,
                "last_name": last_name,
                "profile_image": None
          },
            "role": "student",
            "safe": {
                "badges": [],
                "decorations": [],
                "quota": self._rules.get_new_users_nooblards_count()
            },
            "creation_date": int(_datetime.datetime.now().timestamp())
        } #type:ignore

        id = await self.insert_one(object)
        object["_id"] = id

        return NoobleAccount(self.get_collection(), id, object)
    

