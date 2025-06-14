import quart.wrappers as _quart_wrappers
import nooble_database.objects.file_types as _nooble_database_types

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Mettre à jour son propre profil")
@_apiarist.NoobleEndpointDecorations.arguments(
    first_name = "le prénom de l'utilisateur",
    last_name = "le nom de famille de l'utilisateur",
    profile_image = "l'identifiant de l'image de profil de l'utilisateur",
    active_decoration = "la décoration présente sur le profil de l'utilisateur",
    active_badges = "les badges présents sur le profil de l'utilisateur",
    description = "la description de l'utilisateur"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant d'image de profil désigne bel et un bien une image de profil existante",
    "l'identifiant de décoration désigne bel et bien une décoration déjà existante"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "les badges sont bel et bien possédés par cet utiilsateur",
    "la décoration est bel et bien possédée par cet utiilsateur",
    "l'utilisateur est propriétaire de l'image de profil"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "first_name": "John",
        "last_name": "Doe",
        "profile_image": "bd349283c",
        "active_decoration": "8bcd3a40182",
        "active_badges": ["here_for_long"],
        "description": "Foobar"
    },
    None
)
class UpdateProfileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "first_name" in args 
        and "last_name" in args
        and "active_badges" in args
        and "active_decoration" in args
        and "description" in args
        and "profile_image" in args
        ):
            return False
        
        if not (
            type(args["first_name"]) is str
        and type(args["last_name"]) is str
        and (type(args["active_decoration"]) is str or args["active_decoration"] == None)
        and (type(args["profile_image"]) is str or args["profile_image"] == None)
        and type(args["active_badges"]) is list
        and type(args["description"]) is str
        ):
            return False
        
        account = await self.get_account(request, configuration)

        if account is None:
            return True # non-allowed request
        
        for badge in args['active_badges']:
            if type(badge) is not int:
                return False
            
        if args["profile_image"] is not None:
            file_image = configuration.get_database().get_files().get_file(args["profile_image"])
            
            if not await file_image.exists():
                return False
                
            if not await file_image.get_filetype() != _nooble_database_types.FileType.PROFILE_ICON:
                return False
        
        if args["active_decoration"] is not None:
            decoration  = configuration.get_database().get_decorations().get_decoration(args["active_decoration"])
            if not await decoration.exists():
                return False

        return True
    
    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        args = await self.get_request_args(request)
        
        safe = await account.get_safe().get_object()

        badges: list[str] = args["active_badges"]

        for badge in badges:
            if not badge in [i[0] for i in safe["badges"]]:
                return False
            
        decoration: str|None = args["active_decoration"]

        if decoration is not None and not decoration in safe["decorations"]:
            return False
        
        if args["profile_image"] is not None:
            profile_image = configuration.get_database().get_files().get_file(args["profile_image"])

            if account.get_id() != await profile_image.get_sender_id():
                return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        first_name: str = args["first_name"]
        last_name: str = args["last_name"]
        active_decoration:str|None = args["active_decoration"]
        active_badges: list[str] = args["active_badges"]
        description: str = args["description"]
        profile_image: str|None = args["profile_image"]

        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500) # should not be the case
        
        await account.update({
            "$set": {
                "profile": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "active_decoration": active_decoration,
                    "active_badges": active_badges,
                    "description": description,
                    "profile_image": profile_image
                }
            }
        })

        return await self.make_response(None, configuration)
