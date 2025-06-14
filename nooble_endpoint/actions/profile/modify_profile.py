import quart.wrappers as _quart_wrappers
import nooble_database.objects.file_types as _nooble_database_types
import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Modifier le profil d'un utilisateur")
@_apiarist.NoobleEndpointDecorations.arguments(
    user_id = "l'identifiant de l'utilisateur",
    first_name = "le prénom de l'utilisateur",
    last_name = "le nom de famille de l'utilisateur",
    profile_image = "l'identifiant de l'image de profil de l'utilisateur",
    active_decoration = "la décoration présente sur le profil de l'utilisateur",
    active_badges = "les badges présents sur le profil de l'utilisateur",
    description = "la description de l'utilisateur"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant du compte désigne bien un compte existant",
    "les badges sont bel et bien possédés par cet utiilsateur",
    "l'identifiant d'image de profil désigne bel et un bien une image de profil existante",
    "l'identifiant de décoration désigne bel et bien une décoration déjà existante"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur",
    "l'utilisateur ne modifie pas son propre profil (voir /profile/update)"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "user_id": "429d7c938",
        "first_name": "John",
        "last_name": "Doe",
        "profile_image": "bd349283c",
        "active_decoration": "8bcd3a40182",
        "active_badges": ["here_for_long"],
        "description": "Foobar"
    },
    None
)
class ModifyProfileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "user_id" in args
        and "first_name" in args 
        and "last_name" in args
        and "active_badges" in args
        and "active_decoration" in args
        and "description" in args
        and "profile_image" in args
        ):
            return False
        
        if not (
            type(args["user_id"]) is str
        and type(args["first_name"]) is str
        and type(args["last_name"]) is str
        and (type(args["active_decoration"]) is str or args["active_decoration"] is None)
        and (type(args["profile_image"]) is str or args["profile_image"] is None)
        and type(args["active_badges"]) is list
        and type(args["description"]) is str
        ):
            return False
        
        account = configuration.get_database().get_accounts().get_account(args["user_id"])

        if not await account.exists():
            return False
        
        owned_badges = await account.get_safe().get_owned_badges()

        for badge in args['active_badges']:
            if type(badge) is not str:
                return False
            
            if not badge in [badge[0] for badge in owned_badges]:
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
        
        if not (await account.get_role()).is_admin():
            return False
        
        args = await self.get_request_args(request)

        if account.get_id() == args["user_id"]:
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        self_account = await self.get_account(request, configuration)

        if self_account is None:
            return await self.make_response(None, configuration, 500)

        args = await self.get_request_args(request)

        user_id: str = args["user_id"]
        first_name: str = args["first_name"]
        last_name: str = args["last_name"]
        active_decoration: str|None = args["active_decoration"]
        active_badges: list[str] = args["active_badges"]
        description: str = args["description"]
        profile_image: str|None = args["profile_image"]

        account = configuration.get_database().get_accounts().get_account(user_id)

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

        await configuration.get_mail_service().send_edited_profile_mail(await account.ensure_object(), await self_account.ensure_object())

        await configuration.get_notifier().notify_profile_edit(account, self_account)

        return await self.make_response(None, configuration)
