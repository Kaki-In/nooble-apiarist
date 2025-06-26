import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Acheter un badge")
@_apiarist.NoobleEndpointDecorations.arguments(
    name = "nom du badge"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le nom de badge désigne un badge existant",
    "il est possible d'obtenir un nouveau niveau de ce badge",
    "l'utilisateur est elligible à ce badge"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    new_quota = "le nombre de nooblards présents dans le porte monnaie après achat",
    new_level = "le nouveau niveau correspondant au badge acheté (0 pour le premier niveau)"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "name": "here_for_long"
    },
    {
        "new_quota": 32,
        "new_level": 2
    }
)
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
        
        if not await badges.get_badge(args['name']).is_elligible_to_level(actual_badge_level + 1, account):
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
        quota = await account.get_safe().get_quota()
        
        if price > quota:
            return await self.make_response({
                "reason": "you don't own enough nooblards to perform this action",
                "price": price,
                "quota": quota
            }, configuration, 402)
        
        await account.get_safe().decrease(price)
        quota -= price

        if actual_badge_level == -1 : #not owned previously
            await account.update({
                "$push": {
                    "safe.badges": [badge_name, actual_badge_level+1]
                }
            })
        else:
            await account.update(
                {
                    "$set": {
                        'safe.badges.$[element].1': actual_badge_level + 1
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
                "new_quota": quota,
                "new_level": actual_badge_level+1
            }, configuration
        )
        


