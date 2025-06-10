import quart.wrappers as _quart_wrappers

import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir les informations d'un cours")
@_apiarist.NoobleEndpointDecorations.arguments(
    class_id = "l'identifiant du cours"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant désigne bien un cours existant"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur ou",
    "l'utilisateur a accès à ce cours"
)
@_apiarist.NoobleEndpointDecorations.returns(
    content = "le contenu du cours",
    description = "la description du cours",
    last_modification = "l'heure de dernière modification",
    last_modifier = "l'identifiant du dernier compte ayant modifié le cours",
    name = "le nom du cours"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "class_id": "fdcb23b428"
    },
    {
        "content": {
            "type": "section",
            "data": "..."
        },
        "description": "Angular",
        "last_modification": 2948759329234,
        "last_modifier": "dbfc327493",
        "name": "WE4B"
    }
)
class GetClassDataAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "class_id" in args:
            return False
        
        if not type(args["class_id"]) is str:
            return False
        
        nooble_class = configuration.get_database().get_classes().get_class(args["class_id"])

        if not await nooble_class.exists():
            return False

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False

        args = await self.get_request_args(request)

        if not (
            (await account.get_role()).is_admin()
            or account.get_id() in await configuration.get_database().get_classes().get_class(args["class_id"]).get_accounts_ids()
        ):
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return False

        args = await self.get_request_args(request)
        class_id: str = args["class_id"]

        nooble_class = configuration.get_database().get_classes().get_class(class_id)

        class_data = await nooble_class.ensure_object()
        
        content = class_data["content"]

        client_content = await configuration.get_sections().export(content).export_to_client_json(configuration.get_database(), account)

        return await self.make_response(
            {
                "content": client_content,
                "description": class_data["description"],
                "last_modification": class_data["last_modification"],
                "last_modifier": class_data["last_modifier"],
                "name": class_data["name"]
            },
            configuration
        )

