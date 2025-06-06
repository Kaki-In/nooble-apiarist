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
        
        if not await file.get_filetype() == _nooble_database_objects.FileType.SECTION_FILE:
            return None
        
        activity, local_file = configuration.get_activities().get_activity_from_file(await file.get_filepath())

        if not activity.get_name() == self._name:
            return None
        
        return file, local_file
    
    async def overwrite_savefile(self, data: bytes, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> None:
        args = await self.get_request_args(request)

        file = configuration.get_database().get_files().get_file(args["activity_id"])
    
        configuration.get_resources().get_file(await file.get_filepath()).overwrite(self._name.encode() + b'\n' + data)

        


