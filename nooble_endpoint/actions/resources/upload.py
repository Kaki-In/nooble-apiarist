import quart.wrappers as _quart_wrappers
import io as _io
import asyncio as _asyncio
import datetime as _datetime

import nooble_database.objects.file_types as _nooble_database_file_types
import local_utils.images as _local_utils_images

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description(
    "Charger un fichier dans le serveur. " \
    "Un fichier doit accompagner cette requête"
)
@_apiarist.NoobleEndpointDecorations.arguments(
    name = "le nom personnalisé du fichier",
    type = "le type de fichier à appliquer au filtre (optionel)",
    file = "en tant que fichier, le fichier à inclure (comprenant un nom de fichier)"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le type de fichier spécifié correspond bien à un type de fichier valide",
    "le type de fichier renseigné n'est pas un fichier de section",
    "le fichier est fourni",
    "le fichier fourni possède un nom",
    "si le fichier est une image de profile, alors elle doit être carrée",
    "si le fichier est une décoration, alors elle doit mesurer 900x300px"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté"
)
@_apiarist.NoobleEndpointDecorations.returns(
    new_file = "l'identifiant du fichier",
    date = "la date de chargement du fichier",
    size = "la taille du fichier",
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "name": "bootstraaaaap",
        "type": "profile image"
    },
    {
        "id": "bcd9238de",
        "sent_date": 294837948123,
        "size": 2449,
    }
)
class UploadFileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "name" in args
        and "type" in args
        ):
            return False
        
        if not (
            type(args["name"]) is str
        ):
            return False
        
        try:
            file_type = _nooble_database_file_types.FileType.from_raw_filetype(args["type"])

            if file_type == _nooble_database_file_types.FileType.SECTION_FILE:
                return False
            
        except ValueError:
            return False

        
        files = await self.get_files(request)

        if not "file-content" in files:
            return False
        
        if not files["file-content"].filename :
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)
        
        name: str = args["name"]
        file_type = _nooble_database_file_types.FileType.from_raw_filetype(args["type"])

        file_content = (await self.get_files(request))["file-content"]
        if not file_content.filename:
            return await self.make_response(None, configuration, 500)
        
        filename: str = file_content.filename

        file_bytes = _io.BytesIO()
        await _asyncio.get_event_loop().run_in_executor(None, file_content.save, file_bytes)

        if not await self.ensure_veracity(file_type, file_bytes.getvalue()):
            return await self.make_response("invalid file given", configuration, 400)

        file = configuration.get_resources().create_file(file_bytes.getvalue())

        created_file = await configuration.get_database().get_files().create_new_file(
            name,
            filename,
            _datetime.datetime.now(),
            account.get_id(),
            file.get_path(),
            file_type,
            len(file.get_content())
        )

        data = await created_file.ensure_object()

        return await self.make_response(
            {
                "new_file": data["_id"],
                "size": data["size"],
                "date": data["sent_date"]
            },
            configuration
        )

    async def ensure_veracity(self, filetype:_nooble_database_file_types.FileType, content:bytes) -> bool:
        if filetype == _nooble_database_file_types.FileType.DECORATION_BANNER:
            try:
                image = await _local_utils_images.from_bytes(content)

                return image.get_size() == (900, 300)
            except:
                return False
        elif filetype == _nooble_database_file_types.FileType.PROFILE_ICON:
            try:
                image = await _local_utils_images.from_bytes(content)

                return image.get_width() == image.get_height()
            except:
                return False
        elif filetype == _nooble_database_file_types.FileType.SECTION_FILE:
            # Section files must be created directly using an API
            return False
        
        return False

