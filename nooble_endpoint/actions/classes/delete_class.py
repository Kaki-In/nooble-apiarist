import quart.wrappers as _quart_wrappers

import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Supprimer un ancien cours")
@_apiarist.NoobleEndpointDecorations.arguments(
    class_id = "l'identifiant du cours"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant désigne bien un cours existant"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est un administrateur"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "class_id": "fdcb23b428"
    },
    None
)
class DeleteClassAction(NoobleEndpointAction):
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

        if not await account.get_role() in [_nooble_database_roles.Role.ADMIN, _nooble_database_roles.Role.ADMIN_TEACHER]:
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)
        class_id: str = args["class_id"]

        nooble_class = configuration.get_database().get_classes().get_class(class_id)

        section_content = configuration.get_sections().export(await nooble_class.get_content())

        for file_id in await section_content.get_recursive_used_files(configuration.get_database()):
            file = configuration.get_database().get_files().get_file(file_id)

            configuration.get_resources().get_file(await file.get_filepath()).destroy()
            await file.destroy()

        await nooble_class.destroy()
 
        return await self.make_response(None, configuration)

