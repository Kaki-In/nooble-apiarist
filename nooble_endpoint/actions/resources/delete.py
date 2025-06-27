import quart.wrappers as _quart_wrappers
import nooble_database.objects.file_types as _nooble_database_file_types

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Supprimer un fichier")
@_apiarist.NoobleEndpointDecorations.arguments(
    id = "l'identifiant du fichier"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant de fichier désigne bien un fichier existant",
    "s'il s'agit d'une image de décoration, aucune décoration n'est liée à cette image",
    "il ne s'agit pas d'un fichier géré par une section"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utilisateur est propriétaire du fichier"
)
@_apiarist.NoobleEndpointDecorations.returns()
@_apiarist.NoobleEndpointDecorations.example(
    {
        "id": "cb294387dc"
    },
    None
)
class DeleteFileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "id" in args:
            return False
        
        if not type(args["id"]) is str:
            return False
        
        file = configuration.get_database().get_files().get_file(args['id'])

        if not await file.exists():
            return False

        file_type = await file.get_filetype()

        if file_type == _nooble_database_file_types.FileType.DECORATION_BANNER:
            decoration = await configuration.get_database().get_decorations().get_decoration_from_image(file.get_id())

            print(decoration)

            if decoration is not None:
                return False
            
        elif file_type == _nooble_database_file_types.FileType.SECTION_FILE:
            return False
                
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        args = await self.get_request_args(request)

        file = configuration.get_database().get_files().get_file(args['id'])

        if await file.get_sender_id() != account.get_id():
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)

        file = configuration.get_database().get_files().get_file(args['id'])
        
        if file.get_id() == await account.get_profile().get_profile_image_id():
            await account.update(
                {
                    "$set": {
                        "profile.profile_image": None
                    }
                }
            )

        configuration.get_resources().get_file(await file.get_filepath()).destroy()
        await file.destroy()

        return await self.make_response(None, configuration)
            


