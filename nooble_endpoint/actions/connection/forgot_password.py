import quart.wrappers as _quart_wrappers
import typing as _T

import asyncio as _asyncio
import random as _random

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description(
    "Restaurer son mot de passe et envoyer le nouveau mot de passe par mail. " \
    "Cette URL permet de définir un nouveau mot de passe pour le compte et de l'envoyer par mail à l'utilisateur. " \
    "Cette option est une faille de sécurité car elle ne vérifie pas l'identité de l'utilisateur avant de modifier son mot de passe. " \
    "L'idéal aurait été d'envoyer un lien de modification par mail au preálable, " \
    "mais le temps a été cours et cette option n'est pas nécessaire à petite échelle.")
@_apiarist.NoobleEndpointDecorations.arguments(
    username = "l'adresse mail du compte"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "il existe bien un compte possédant cette adresse mail"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur n'est pas connecté",
)
@_apiarist.NoobleEndpointDecorations.returns(
    first_name = "le prénom du compte",
    last_name = "le nom de famille du compte"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "username": "john.doe@utbm.fr"
    },
    {
        "first_name": "John",
        "last_name": "Doe",
    }
)
class ForgotPasswordAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)
        
        if not "username" in args:
            return False
        
        if type(args["username"]) is not str:
            return False
        
        account = await configuration.get_database().get_accounts().get_account_by_mail(args["username"])

        if account is None:
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        mail_address: str = args["username"]

        account = await configuration.get_database().get_accounts().get_existing_account_by_mail(mail_address)

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



