from ..templates import NoobleSection

import nooble_database.database as _nooble_database
import nooble_database.objects as _nooble_database_objects
import nooble_activities.manager as _nooble_activities_manager
import nooble_resources_manager as _nooble_resources_manager

import typing as _T

class ClientActivitySectionDataObject(_T.TypedDict):
    id:str

    javascript:str
    editable_javascript:str

    css:str

class NoobleActivitySection(NoobleSection[str, ClientActivitySectionDataObject, _nooble_database_objects.section_objects.ActivitySectionDataObject]):
    def __init__(self, activity_file: str, activities_manager: _nooble_activities_manager.NoobleActivitiesManager, resources_manager: _nooble_resources_manager.NoobleResourcesManager) -> None:
        super().__init__("activity", activity_file)

        self._manager = activities_manager
        self._resources = resources_manager

    async def get_used_files(self, database: _nooble_database.NoobleDatabase) -> list[str]:
        file = database.get_files().get_file(self.get_data())

        activity = self._manager.get_activity(await file.get_name())
        activity_data = self._resources.get_file(await file.get_filepath()).get_content()

        return await activity.get_used_files(activity_data, database)
    
    async def export_to_client_json_data(self, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> ClientActivitySectionDataObject:
        file = database.get_files().get_file(self.get_data())

        activity = self._manager.get_activity(await file.get_name())
        activity_data = self._resources.get_file(await file.get_filepath()).get_content()

        return {
            "id": self.get_data(),
            "css": activity.get_css(),
            "javascript": await activity.get_javascript(activity_data, database, account),
            "editable_javascript": await activity.get_javascript(activity_data, database, account)
        }
    
    async def export_to_database_json_data(self, database: _nooble_database.NoobleDatabase) -> _nooble_database_objects.section_objects.ActivitySectionDataObject:
        return {
            "file_id": self.get_data()
        }
    
    async def is_valid(self, database: _nooble_database.NoobleDatabase) -> bool:
        file = database.get_files().get_file(self.get_data())

        if not await file.exists():
            return False
        
        file_data = await file.ensure_object()

        if file_data["filetype"] != "section file":
            return False
        
        return True
    
    
        


