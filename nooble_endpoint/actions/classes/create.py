import quart.wrappers as _quart_wrappers

import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Créer un nouveau cours")
@_apiarist.NoobleEndpointDecorations.arguments(
    name = "le nom du nouveau cours",
    description = "une description brève du contenu du cours"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur"
)
@_apiarist.NoobleEndpointDecorations.returns(
    new_class = "l'identifiant du nouveau cours"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "name": "WE4B",
        "description": "Angular Tah les fous"
    },
    {
        "new_class": "cb264b9c2ef"
    }
)
class CreateClassAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not ( 
            "name" in args
        and "description" in args
        ):
            return False
        
        if not (
            type(args["name"]) is str
        and type(args["description"]) is str
        ):
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False

        if not (await account.get_role()).is_admin():
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)

        args = await self.get_request_args(request)

        name: str = args["name"]
        description: str = args["description"]

        new_class = await configuration.get_database().get_classes().create_class(name, description, account.get_id())

        return await self.make_response({
            "new_class": new_class.get_id()
        }, configuration)
    

