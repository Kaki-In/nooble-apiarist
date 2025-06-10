import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir des informations de connection")
@_apiarist.NoobleEndpointDecorations.arguments(
    username = "l'adresse mail du compte",
    password = "le mot de passe"
)
@_apiarist.NoobleEndpointDecorations.returns(
    connected = "vrai lorsque l'utilisateur est connecté",
    account = "si connecté, les informations de compte"
)
@_apiarist.NoobleEndpointDecorations.example(
    None,
    {
        "connected": True,
        "account": {
            "id": "8482f9209deb",
            "profile": 
            {
                "first_name": "John",
                "last_name": "Doe",
                "active_decoration": '3bd8527cf',
                "active_badges": [
                    ["here_for_long", 3]
                ]
            },
            "safe": 
            {
                "quota": 30,
                "decorations": [
                    '3bd8527cf', 
                    '8cab2940c3d'
                ]
            },
            "role": "admin_teacher",
            "mail": "john.doe@utbm.fr"
        }
    }
)
class GetLogInfoAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(
                {
                    "connected": False,
                },
                configuration
            )
        
        else :
            account_object = await account.get_object()

            return await self.make_response(
                {
                    "connected": True,
                    "account": {
                        "id": account_object["_id"],
                        "profile": account_object["profile"],
                        "safe": account_object["safe"],
                        "role": account_object["role"],
                        "mail": account_object["mail"]
                    }
                }, 
                configuration
            )


