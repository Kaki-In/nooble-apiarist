import quart.wrappers as _quart_wrappers

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir la liste des décorations")
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    id = "l'identifiant de la décoration",
    name = "le nom de la décoration",
    price = "le prix de la décoration",
    image = "l'identifiant de l'image de la décoration"
)
@_apiarist.NoobleEndpointDecorations.example(
    None,
    [
        {
            "id": "8bcd3a40182",
            "price": 200,
            "name": "Clair de lune",
            "image": "2834fa0b28",
        }
    ]
)
class ListDecorationsAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        owned_decorations = await account.get_safe().get_owned_decorations()

        all_decorations = await configuration.get_database().get_decorations().get_all_decorations()

        new_decorations = []

        for decoration in all_decorations:
            decoration_name = await decoration.get_name()

            decoration_object = await decoration.get_object()

            if not decoration_name in owned_decorations:
                new_decorations.append(
                    {
                        "id": decoration.get_id(),
                        "price": decoration_object["price"],
                        "name": decoration_object["name"],
                        "image": decoration_object["image"],
                    }
                )
        
        return await self.make_response(new_decorations, configuration)



