from .map import NoobleSectionsMap

from .section_exporters.container import NoobleContainerSectionExporter
from .section_exporters.activity import NoobleActivitySectionExporter

import nooble_activities.manager as _nooble_activities_manager

def get_default_sections_map(activities_manager: _nooble_activities_manager.NoobleActivitiesManager) -> NoobleSectionsMap:
    map = NoobleSectionsMap()

    map.add_exporter(NoobleContainerSectionExporter())
    map.add_exporter(NoobleActivitySectionExporter(activities_manager))

    return map


