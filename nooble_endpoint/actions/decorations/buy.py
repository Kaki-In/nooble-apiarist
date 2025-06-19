import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Acheter une décoration")
@_apiarist.NoobleEndpointDecorations.arguments(
    decoration = "l'identifiant de la décoration"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant de la décoration est bien valide",
    "la décoration n'est pas encore présente dans le coffre-fort"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
)
@_apiarist.NoobleEndpointDecorations.returns(
    new_quota = "le nouveau solde de nooblards"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "decoration": "b279d810d9f"
    },
    None
)
class BuyDecorationAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "decoration" in args:
            return False
        
        if type(args["decoration"]) is not str:
            return False
        
        account = await self.get_account(request, configuration)

        if account is None:
            return True # not allowed raised then
        
        decoration = configuration.get_database().get_decorations().get_decoration(args["decoration"])
        
        if not await decoration.exists():
            return False
        
        if decoration in await account.get_safe().get_owned_decorations():
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)

        args = await self.get_request_args(request)

        decoration_id:str = args["decoration"]

        decoration = configuration.get_database().get_decorations().get_decoration(decoration_id)

        quota = await account.get_safe().get_quota()
        price = await decoration.get_price()

        if price > quota:
            return await self.make_response({
                "reason": "you don't own enough nooblards to perform this action",
                "price": price,
                "quota": quota
            }, configuration, 402)
        
        quota -= price

        await account.update({
            "$push": {
                "safe.decorations": decoration_id
            },
            "$inc":{
                "safe.quota": -price
            } 
        })

        return await self.make_response(
            {
                "new_quota": quota
            }, configuration
        )
        



