from ..configuration import NoobleEndpointConfiguration

from .nooble_action import NoobleEndpointAction

import nooble_database.objects as _nooble_database_objects
import nooble_database.database as _nooble_database
import quart.wrappers as _quart_wrappers

class NoobleEndpointActivityAction(NoobleEndpointAction):
    def __init__(self, name:str) -> None:
        super().__init__()

        self._name = name

    async def get_activity_file(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> None | tuple[_nooble_database.NoobleFile, bytes]:
        args = await self.get_request_args(request)

        if not "activity_id" in args:
            return None
        
        if type(args["activity_id"]) is not str:
            return None
        
        file = configuration.get_database().get_files().get_file(args["activity_id"])

        if not await file.exists():
            return None
        
        file_data = await file.ensure_object()

        if file_data["filetype"] != "section file":
            return None
        
        activity_name = file_data["name"]

        if not activity_name == self._name:
            return None
        
        activity_file = configuration.get_resources().get_file(file_data["filepath"])
        
        return file, activity_file.get_content()
    
    async def overwrite_savefile(self, data: bytes, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> None:
        args = await self.get_request_args(request)

        file = configuration.get_database().get_files().get_file(args["activity_id"])
    
        configuration.get_resources().get_file(await file.get_filepath()).overwrite(data)

        


