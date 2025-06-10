import quart.wrappers as _quart_wrappers

import nooble_database.objects.file_types as _nooble_database_file_types

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Obtenir ses propres fichiers. Seuls les fichiers non gérés par des sections sont référencés ici.")
@_apiarist.NoobleEndpointDecorations.arguments(
    type = "le type de fichier à appliquer au filtre (optionel)"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le type de fichier indiqué est un type de fichier valide (profile icon, section file, decoration banner)"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    id = "l'identifiant du fichier",
    name = "le nom personnalisé du fichier",
    filename = "le nom (avec extension) du fichier",
    sent_date = "la date d'envoi du fichier",
    sender = "l'identifiant de l'exportateur du fichier",
    size = "la taille du fichier",
    filetype = "le type de fichier"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "type": "profile image"
    },
    [
        {
            "id": "bcd9238de",
            "name": "clair_de_lune",
            "filename": "clair_de_lune.png",
            "sent_date": 294837948123,
            "sender": "cbd298d784",
            "size": 2449,
            "filetype": "decoration banner"
        }
    ]
)
class GetSelfFilesAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if "type" in args:
            try:
                _nooble_database_file_types.FileType.from_raw_filetype(args["type"])
            except ValueError:
                return False

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        if "type" in args:
            files_type = args["type"]
        else:
            files_type = None

        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        files = await configuration.get_database().get_files().get_sender_files(account.get_id(), files_type)

        files_result = []

        for file in files:
            file_object = await file.ensure_object()

            if file_object["filetype"] == "section file":
                continue
            
            files_result.append(
                {
                    "id": file.get_id(),
                    "name": file_object["name"],
                    "filename": file_object["filename"],
                    "sent_date": file_object["sent_date"],
                    "sender": file_object["sender"],
                    "size": file_object["size"],
                    "filetype": file_object["filetype"]
                }
            )
        
        return await self.make_response(
            files_result,
            configuration
        )


