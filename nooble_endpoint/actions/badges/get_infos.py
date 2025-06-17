import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir des informations sur un badge")
@_apiarist.NoobleEndpointDecorations.arguments(
    name = "nom du badge",
    level = "niveau du badge"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le nom de badge désigne un badge existant",
    "le badge est capable de s'étendre à ce niveau"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    max_level = "le niveau maximum du badge",
    title = "le titre de ce badge",
    description = "la description de ce badge"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "name": "here_for_long",
        "level": 4
    },
    {
        "max_level": 5,
        "title": "Citizen",
        "description": 'You have been here for 10 years'
    }
)
class GetBadgeInfoAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "level" in args
        and "name" in args
        ):
            return False
        
        if not (
            type(args["level"]) is int
        and type(args["name"]) is str
        ):
            return False
        
        badges = configuration.get_badges()

        if not args["name"] in badges.get_badges_names():
            return False
        
        if not args["level"] in range(badges.get_badge(args["name"]).get_max_level() + 1):
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)

        args = await self.get_request_args(request)

        badge_name: str = args["name"]
        badge_level: int = args["level"]

        badge = configuration.get_badges().get_badge(badge_name)

        return await self.make_response({
            "max_level": badge.get_max_level(),
            "title": badge.get_title(badge_level),
            "description": badge.get_description(badge_level),
        }, configuration)




