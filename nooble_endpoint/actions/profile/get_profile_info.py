import quart.wrappers as _quart_wrappers
import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir les informations sur le profil d'un utilisateur")
@_apiarist.NoobleEndpointDecorations.arguments(
    user_id = "l'identifiant de l'utilisateur (optionnel); si non renseigné, désignera l'utilisateur effectuant la requête"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    first_name = "le prénom de l'utilisateur",
    last_name = "le nom de famille de l'utilisateur",
    profile_image = "l'identifiant de l'image de profil de l'utilisateur",
    active_decoration = "la décoration présente sur le profil de l'utilisateur",
    active_badges = "les badges présents sur le profil de l'utilisateur",
    description = "la description de l'utilisateur",
    classes = "si l'utilisateur n'est pas un administrateur, la liste des cours auxquels l'utilisateur participe"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "user_id": "429d7c938"
    },
    {
        "first_name": "John",
        "last_name": "doe",
        "profile_image": "bd349283c",
        "active_decoration": "8bcd3a40182",
        "active_badges": [
            ["here_for_long", 3],
            ["...", 1],
            "...",
        ],
        "description": "Foobar",
        "classes": [
            "bc3849dec2"
        ]
    }
)
class GetProfileInfoAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if "user_id" in args:
            return type(args["user_id"]) is str

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        if "user_id" in args:
            user_id: str = args["user_id"]

            account = configuration.get_database().get_accounts().get_account(user_id)
        else:
            account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500) 
        
        profile_info: dict = await account.get_profile().get_object() # type: ignore

        if await account.get_role() != _nooble_database_roles.Role.ADMIN:
            profile_info["classes"] = [(await nooble_class.ensure_object())["_id"] for nooble_class in await configuration.get_database().get_classes().get_account_classes(account.get_id())]
        
        owned_badges = await account.get_safe().get_owned_badges()

        profile_info["badges"] = [badge for badge in owned_badges if badge[0] in profile_info["badges"]]
        
        return await self.make_response(profile_info, configuration, 200)
