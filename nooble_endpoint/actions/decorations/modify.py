import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Modifier une décoration")
@_apiarist.NoobleEndpointDecorations.arguments(
    decoration_id = "l'identifiant de la décoration",
    name = "le nom de la décoration (optionnel)",
    price = "le prix de la décoration (optionel)",
    image = "l'identifiant de l'image de la décoration (optionel)"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant de décoration désigne bien une décoration existante",
    "au moins le nouveau nom, prix ou la nouvelle image a été renseigné",
    "l'identifiant de l'image désigne bien une image de décoration existante, si présente"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "decoration_id": "8bcd3a40182",
        "name": "Clair de soleil"
    },
    None
)
class ModifyDecorationAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "decoration_id" in args:
            return False

        argument_provided = False

        if "name" in args:
            if type(args["name"]) is not str:
                return False
            
            argument_provided = True
            
        if "price" in args:
            if type(args["price"]) is not int:
                return False

            argument_provided = True

        if "image" in args:
            if type(args["image"]) is not str:
                return False

            argument_provided = True

        if not argument_provided:
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
        args = await self.get_request_args(request)

        decoration = configuration.get_database().get_decorations().get_decoration(args["decoration_id"])

        updated_attributes = {}

        if "name" in args:
            updated_attributes["name"] = args["name"]

        if "price" in args:
            updated_attributes["price"] = args["price"]
        
        if "image" in args:
            updated_attributes["image"] = args["image"]

        await decoration.update(
            {
                "$set": updated_attributes
            }
        )
        
        return await self.make_response(None, configuration)


        

