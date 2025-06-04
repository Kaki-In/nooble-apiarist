import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

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
            
            if badge_level >= badge.get_max_level():
                continue

            if await badge.is_elligible_to_level(badge_level + 1, account):
                reached_badges.append({
                    "name": badge.get_name(),
                    "level": badge_level+1,
                    "price": await badge.get_price_to_level(badge_level + 1, account),
                    "title": badge.get_title(badge_level),
                    "description": badge.get_description(badge_level)
                })
            else:
                unreached_badges.append({
                    "name": badge.get_name(),
                    "level": badge_level+1,
                    "price": await badge.get_price_to_level(badge_level + 1, account),
                    "title": badge.get_title(badge_level),
                    "description": badge.get_description(badge_level)
                })

        return await self.make_response({
            "reached": reached_badges,
            "unreached": unreached_badges
        }, configuration)
        






 