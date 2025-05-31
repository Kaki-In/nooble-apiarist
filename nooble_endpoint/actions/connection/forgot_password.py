import quart.wrappers as _quart_wrappers
import typing as _T

import asyncio as _asyncio
import random as _random

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class ForgotPassword(NoobleEndpointAction):
    async def is_valid(self, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)
        
        if not "username" in args:
            return False
        
        if type(args["username"]) is not str:
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return self.get_account(request, configuration) is None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        mail_address: str = args["username"]

        account = await configuration.get_database().get_accounts().get_account_by_mail(mail_address)

        if account is None:
            return await self.make_response(
                {
                    "reason": 3
                },
                configuration,
                code=401
            )
        
        new_password = self.create_new_password()
        await account.update({
            "$set": {
                "password": new_password
            }
        })
        
        _asyncio.create_task(configuration.get_mail_service().send_new_password_mail(await account.ensure_object(), new_password))

        return await self.make_response({
            "first_name": (await account.ensure_object())["profile"]["first_name"],
            "last_name": (await account.ensure_object())["profile"]["last_name"],
        }, configuration)
    
    def create_new_password(self) -> str:
        a = ""

        for i in range(8):
            a += _random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123465789")

        return a



