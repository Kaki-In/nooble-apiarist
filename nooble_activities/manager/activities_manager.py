from ..templates.activity import NoobleActivity

import nooble_resources_manager as _nooble_resources_manager
import nooble_database.database as _nooble_database

class NoobleActivitiesManager():
    def __init__(self, manager: _nooble_resources_manager.NoobleResourcesManager) -> None:
        self._activities: dict[str, NoobleActivity] = {}

    def get_activity(self, name:str) -> NoobleActivity:
        return self._activities[name]
    
    def add_activity(self, activity: NoobleActivity) -> None:
        self._activities[activity.get_name()] = activity

    def get_activities_names(self) -> list[str]:
        return list(self._activities)
    