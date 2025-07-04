from nooble_database.objects.section_objects import ActivitySectionDataObject

from ..templates import NoobleSectionExporter
from ..sections.activity import NoobleActivitySection

import nooble_database.objects as _nooble_database_objects
import nooble_activities.manager as _nooble_activities_manager
import nooble_resources_manager as _nooble_resources_manager
import nooble_conf.files as _nooble_conf_files

class NoobleActivitySectionExporter(NoobleSectionExporter[_nooble_database_objects.section_objects.ActivitySectionDataObject, ActivitySectionDataObject, NoobleActivitySection]):
    def __init__(self, activities_manager: _nooble_activities_manager.NoobleActivitiesManager, resources_manager: _nooble_resources_manager.NoobleResourcesManager, configuration: _nooble_conf_files.NoobleBindingSettings):
        super().__init__("activity")

        self._manager = activities_manager
        self._resources = resources_manager
        self._configuration = configuration

    def export(self, exporter, data: ActivitySectionDataObject) -> NoobleActivitySection:
        return NoobleActivitySection(data["file_id"], self._manager, self._resources, self._configuration)


