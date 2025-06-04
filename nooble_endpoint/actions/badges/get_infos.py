import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetBadgeInfosAction(NoobleEndpointAction):
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
        
        if not args["level"] in range(badges.get_badge(args["name"]).get_max_level()):
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        badge_name: str = args["name"]
        badge_level: int = args["level"]

        badge = configuration.get_badges().get_badge(badge_name)
        badge_image = await badge.get_image(badge_level)

        return await self.make_response({
            "title": badge.get_title(badge_level),
            "description": badge.get_description(badge_level),
            "image": str(badge_image)
        }, configuration)




