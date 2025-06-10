import quart.wrappers as _quart_wrappers
import nooble_database.objects as _nooble_database_objects

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Créer une nouvelle décoration")
@_apiarist.NoobleEndpointDecorations.arguments(
    name = "le nom de la décoration",
    price = "le prix de la décoration",
    image_id = "l'identifiant de l'image de la décoration"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'image de décoration existe",
    "l'image est bien une image de décoration"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur",
    "l'utilisateur est le propriétaire de l'image"
)
@_apiarist.NoobleEndpointDecorations.returns(
    new_decoration = "l'identifiant de la nouvelle décoration"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "name": "Clair de lune",
        "price": 200,
        "image_id": "2834fa0b28"
    },
    {
        "new_decoration": "8bcd3a40182"
    }
)
class CreateDecorationAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "name" in args
        and "price" in args
        and "image_id" in args
        ):
            return False
        
        if not (
            type(args["name"]) is str
        and type(args["price"]) is int
        and type(args["image_id"]) is str
        ):
            return False
        
        file = configuration.get_database().get_files().get_file(args["image_id"])

        if not await file.exists():
            return False
        
        if await file.get_filetype() != _nooble_database_objects.FileType.DECORATION_BANNER:
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        if not (await account.get_role()).is_admin():
            return False
        
        args = await self.get_request_args(request)

        file = configuration.get_database().get_files().get_file(args["image_id"])

        if not await file.get_sender_id() != account.get_id():
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)

        decoration = await configuration.get_database().get_decorations().create_decoration(
            args["name"],
            args["image_id"],
            args["price"]
        )

        await account.update({
            "$push": {
                "safe.decorations": decoration.get_id()
            }
        })

        return await self.make_response({
            "new_decoration": decoration.get_id()
        }, configuration)
        

