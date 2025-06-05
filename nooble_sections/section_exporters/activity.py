from nooble_database.objects.section_objects import ActivitySectionDataObject

from ..templates import NoobleSectionExporter
from ..sections.activity import NoobleActivitySection

import nooble_database.objects as _nooble_database_objects

import nooble_activities.manager as _nooble_activities_manager

class NoobleActivitySectionExporter(NoobleSectionExporter[_nooble_database_objects.section_objects.ActivitySectionDataObject, ActivitySectionDataObject, NoobleActivitySection]):
    def __init__(self, activities_manager: _nooble_activities_manager.NoobleActivitiesManager):
        super().__init__("activity")

        self._manager = activities_manager

    def export(self, exporter, data: ActivitySectionDataObject) -> NoobleActivitySection:
        return NoobleActivitySection(data["file_id"], self._manager)


