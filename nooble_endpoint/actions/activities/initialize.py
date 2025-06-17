import quart.wrappers as _quart_wrappers

import nooble_database.objects as _nooble_database_objects
import datetime as _datetime

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

import apiarist_server_endpoint as _apiarist
@_apiarist.NoobleEndpointDecorations.description("Initializer une nouvelle activité")
@_apiarist.NoobleEndpointDecorations.arguments(
    activity_name = "le nom de l'activité à initialiser"
)
@_apiarist.NoobleEndpointDecorations.validity(
    "le nom d'acitivté désigne bien un activité existante"
)
@_apiarist.NoobleEndpointDecorations.allow_only_when(
    "l'utilisateur est connecté",
    "l'utiliser est un administrateur ou un professeur"
)
@_apiarist.NoobleEndpointDecorations.returns(
    new_file = "l'identifiant du nouveau fichier d'activité"
)
@_apiarist.NoobleEndpointDecorations.example(
    {
        "activity_name": "homework"
    },
    {
        "new_file": "3bd2a7c8bd3"
    }
)
class InitializeActivityAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not "activity_name" in args:
            return False
        
        if not type(args["activity_name"]) is str:
            return False
        
        if not args["activity_name"] in configuration.get_activities().get_activities_names():
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration) 

        if account is None:
            return False
        
        if await account.get_role() == _nooble_database_objects.Role.STUDENT:
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration) 

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        args = await self.get_request_args(request)
        activity_name: str = args["activity_name"]

        activity = configuration.get_activities().get_activity(activity_name)

        file_bytes = activity.create_empty_file()

        file = configuration.get_resources().create_file(file_bytes)

        created_file = await configuration.get_database().get_files().create_new_file(
            activity_name,
            "activity.data",
            _datetime.datetime.now(),
            account.get_id(),
            file.get_path(),
            _nooble_database_objects.FileType.SECTION_FILE,
            len(file.get_content())
        )

        data = await created_file.ensure_object()

        return await self.make_response({
            "new_file": str(data["_id"])
        }, configuration)

