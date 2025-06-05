from .manager import NoobleActivitiesManager

from .activities.homework import HomeworkActivity

import nooble_resources_manager as _nooble_resrouces_manager

def get_default_activity_manager(manager: _nooble_resrouces_manager.NoobleResourcesManager) -> NoobleActivitiesManager:
    activities_manager = NoobleActivitiesManager(manager)

    activities_manager.add_activity(HomeworkActivity())

    return activities_manager

