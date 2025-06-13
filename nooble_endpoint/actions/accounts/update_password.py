import quart.wrappers as _quart_wrappers
import hashlib as _hashlib

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Mettre à jour son mot de passe")
@_apiarist.NoobleEndpointDecorations.arguments(
    last_password = "l'ancien mot de passe",
    new_password = "le nouveau mot de passe"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le nouveau mot de passe n'est pas vide"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'ancien mot de passe est correct"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "last_password": "de62c209a",
        "new_password": "J'aimeLeRizAh!EtBootstrapAussi"
    },
    None
)
class UpdatePasswordAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "last_password" in args
        and "new_password" in args):
            return False
        
        if not (
            type(args["last_password"]) is str
        and type(args["new_password"]) is str
        ):
            return False
        
        if args["new_password"] == "":
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        args = await self.get_request_args(request)
        last_password: str = args["last_password"]

        if await account.get_password() != _hashlib.sha256(last_password.encode()).hexdigest():
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)
        new_password: str = args["new_password"]

        await account.update({
            "$set": {
                "password": _hashlib.sha256(new_password.encode()).hexdigest()
            }
        })

        await configuration.get_mail_service().send_new_password_mail(await account.get_object(), new_password)

        return self.make_response(None, configuration, 500)
        

