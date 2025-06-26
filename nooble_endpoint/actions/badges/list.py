import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Lister les badges disponibles")
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    reached = "la liste des badges atteints",
    unreached = "la liste des badges qui ne peuvent pas encore être achetés"
)
@_apiarist.NoobleEndpointDecorations.example(
    None,
    {
        "reached": [
            {
                "name": "here_for_long",
                "level": 3,
                "price": 30,
                "title": "Resident",
                "description": "You have been here for 3 years"
            }
        ],
        "unreached": []
    }
)
class ListBadgesAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        owned_badges = await account.get_safe().get_owned_badges()
        
        badges = configuration.get_badges()

        badges_names = badges.get_badges_names()

        reached_badges = []
        unreached_badges = []

        for badge_name in badges_names:
            badge = badges.get_badge(badge_name)

            badge_level = -1

            for owned_badge in owned_badges:
                if owned_badge[0] == badge_name:
                    badge_level = owned_badge[1]
            
            print(badge_level, badge.get_max_level())
            
            if badge_level >= badge.get_max_level():
                continue

            if await badge.is_elligible_to_level(badge_level + 1, account):
                reached_badges.append({
                    "name": badge.get_name(),
                    "level": badge_level+1,
                    "price": await badge.get_price_to_level(badge_level + 1, account),
                    "title": badge.get_title(badge_level + 1),
                    "description": badge.get_description(badge_level + 1)
                })
            else:
                unreached_badges.append({
                    "name": badge.get_name(),
                    "level": badge_level+1,
                    "price": await badge.get_price_to_level(badge_level + 1, account),
                    "title": badge.get_title(badge_level + 1),
                    "description": badge.get_description(badge_level + 1)
                })

        return await self.make_response({
            "reached": reached_badges,
            "unreached": unreached_badges
        }, configuration)
        






 