import quart.wrappers as _quart_wrappers
import hashlib as _hashlib

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Se connecter")
@_apiarist.NoobleEndpointDecorations.arguments(
    username = "l'adresse mail du compte",
    password = "le mot de passe"
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
class LoginAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)
        
        if not "username" in args or not "password" in args:
            return False
        
        if not (type(args["username"]) is str and type(args["password"]) is str):
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        mail_address: str = args["username"]
        password: str = args["password"]

        account = await configuration.get_database().get_accounts().get_account_by_mail(mail_address)

        if account is None:
            return await self.make_response(
                {
                    "reason": "invalid token"
                },
                configuration,
                code=401
            )
        
        if _hashlib.sha256(password.encode()).hexdigest() != await account.get_password():
            return await self.make_response(
                {
                    "reason": "invalid token"
                },
                configuration,
                code=401
            )
        
        response = await self.make_response({
            "first_name": (await account.ensure_object())["profile"]["first_name"],
            "last_name": (await account.ensure_object())["profile"]["last_name"],
        }, configuration)

        self.set_client_token(response, configuration.get_registrations().add_registration(account), configuration)
        
        return response
