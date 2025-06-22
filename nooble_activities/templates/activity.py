import nooble_database.database as _nooble_database
import nooble_database.objects as _nooble_database_objects
import nooble_conf.files as _nooble_conf_files

import typing as _T

class NoobleActivity():
    def __init__(self, name:str) -> None:
        self._name = name
    
    def get_name(self) -> str:
        return self._name
    
    def create_empty_file(self) -> bytes:
        raise NotImplementedError("not implemented for " + repr(self))
    
    def get_resource_url(self, name:str, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        return configuration.get_host_url() + "/activities/resource/" + self._name + "/" + name
    
    def get_download_url(self, file_id: str, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        return configuration.get_host_url() + f"/resources/download?id={file_id}&type=section%20file"
    
    async def get_javascript(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        raise NotImplementedError("not implemented for " + repr(self))
        return """

class Activity // the Activity name is mandatory
{
    constructor(id, args) // id is the id of the activity, and args the json args given to the activity
    {
        // construction of the actvitiy
    }

    onRender(div)
    {
        // what to do when rendering the div
    }
}

"""

    async def get_editable_javascript(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        raise NotImplementedError("not implemented for " + repr(self))
        return """

class Activity // the Activity name is mandatory
{
    constructor(id, args) // id is the id of the activity, and args the json args given to the activity
    {
        // construction of the actvitiy
    }

    onRender(div)
    {
        // what to do when rendering the div
    }
}

"""

    def get_css(self, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def get_arguments(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> _T.Any:
        return None
    
    async def get_used_files(self, file: bytes, database: _nooble_database.NoobleDatabase) -> list[str]:
        return []
    

