import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class BuyBadgeAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "name" in args:
            return False
        
        if type(args["name"]) is not str:
            return False
        
        badges = configuration.get_badges()

        if not args["name"] in badges.get_badges_names():
            return False
        
        account = await self.get_account(request, configuration)

        if account is None:
            return True # not allowed raise then
        
        actual_badge_level = -1
        for badge in await account.get_safe().get_owned_badges():
            if badge[0] == args["name"]:
                actual_badge_level = badge[1]
        
        if actual_badge_level == badges.get_badge(args["name"]).get_max_level():
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)

        args = await self.get_request_args(request)

        badge_name:str = args["name"]

        badge = configuration.get_badges().get_badge(badge_name)

        actual_badge_level = -1
        for owned_badge in await account.get_safe().get_owned_badges():
            if owned_badge[0] == args["name"]:
                actual_badge_level = owned_badge[1]

        price = await badge.get_price_to_level(actual_badge_level + 1, account)
        
        if price > await account.get_safe().get_quota():
            return await self.make_response({
                "you don't own enough nooblards to perform this action"
            }, configuration, 402)
        
        await account.get_safe().decrease(price)

        if actual_badge_level == -1 : #not owned previously
            await account.update({
                "$push": {
                    "nooble.safe.badges": [badge_name, actual_badge_level+1]
                }
            })
        else:
            await account.update(
                {
                    "$set": {
                        'nooble.safe.badges.$[element].1': actual_badge_level + 1
                    }
                },
                array_filters=[
                    {
                        'element.0': badge_name
                    }
                ]
            )
        
        return await self.make_response(
            {
                "new_quota": await account.get_safe().get_quota()
            }, configuration
        )
        


