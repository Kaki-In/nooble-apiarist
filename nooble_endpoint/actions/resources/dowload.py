import quart.wrappers as _quart_wrappers
import quart as _quart

import nooble_database.objects.file_types as _nooble_database_file_types
import datetime as _datetime

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Télécharger un fichier")
@_apiarist.NoobleEndpointDecorations.arguments(
    id = "l'identifiant du fichier",
    type = "le type de fichier à télécharger"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "l'identifiant de fichier désigne bien un fichier existant",
    "le type de fichier correspond parfaitement à celui indiqué en argument"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "id": "cb294387dc",
        "type": "profile image"
    },
    None
)
class DownloadFileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "id" in args
        and "type" in args
        ):
            return False
        
        if not type(args["id"]) is str:
            return False
        
        try:
            _nooble_database_file_types.FileType.from_raw_filetype(args["type"])
        except:
            return False
        
        file = configuration.get_database().get_files().get_file(args['id'])

        if not await file.exists():
            return False
        
        if not args["type"] == (await file.ensure_object())["filetype"]:
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        file_id: str = args["id"]

        file = configuration.get_database().get_files().get_file(file_id)

        file_object = await file.get_object()

        resource = configuration.get_resources().get_file(file_object["filepath"])

        filename = file_object["filename"]

        return await _quart.send_file(resource.get_content(), "document/"+filename.split(".")[-1],
                                      as_attachment=True,
                                      attachment_filename=filename,
                                      last_modified=_datetime.datetime.fromtimestamp(file_object["sent_date"]))




