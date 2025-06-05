from ..templates.activity import NoobleActivity

import nooble_resources_manager as _nooble_resources_manager
import nooble_database.database as _nooble_database

class NoobleActivitiesManager():
    def __init__(self, manager: _nooble_resources_manager.NoobleResourcesManager) -> None:
        self._activities: dict[str, NoobleActivity] = {}
        self._resources_manager = manager

    def get_activity(self, name:str) -> NoobleActivity:
        return self._activities[name]
    
    def add_activity(self, activity: NoobleActivity) -> None:
        self._activities[activity.get_name()] = activity

    def get_activities_names(self) -> list[str]:
        return list(self._activities)
    
    def get_activity_from_file(self, file_path: str) -> tuple[NoobleActivity, bytes]:
        resource = self._resources_manager.get_file(file_path)

        content = resource.get_content()
        first_line = content.split(b'\n')[0].decode()

        if not first_line in self._activities:
            raise KeyError(first_line)
        
        return self._activities[first_line], content[len(first_line)+1:]

