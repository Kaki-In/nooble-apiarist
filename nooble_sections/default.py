from .map import NoobleSectionsMap

from .section_exporters.container import NoobleContainerSectionExporter
from .section_exporters.activity import NoobleActivitySectionExporter
from .section_exporters.image import NoobleImageSectionExporter
from .section_exporters.audio import NoobleAudioSectionExporter
from .section_exporters.file import NoobleFileSectionExporter
from .section_exporters.integration import NoobleIntegrationSectionExporter
from .section_exporters.raw_text import NoobleRawTextSectionExporter
from .section_exporters.rich_text import NoobleRichTextSectionExporter
from .section_exporters.video import NoobleVideoSectionExporter

import nooble_activities.manager as _nooble_activities_manager
import nooble_resources_manager as _nooble_resources_manager
import nooble_conf.files as _nooble_conf_files

def get_default_sections_map(activities_manager: _nooble_activities_manager.NoobleActivitiesManager, resources_manager: _nooble_resources_manager.NoobleResourcesManager, configuration: _nooble_conf_files.NoobleBindingSettings) -> NoobleSectionsMap:
    map = NoobleSectionsMap()

    map.add_exporter(NoobleContainerSectionExporter())
    map.add_exporter(NoobleActivitySectionExporter(activities_manager, resources_manager, configuration))
    map.add_exporter(NoobleImageSectionExporter())
    map.add_exporter(NoobleAudioSectionExporter())
    map.add_exporter(NoobleFileSectionExporter())
    map.add_exporter(NoobleIntegrationSectionExporter())
    map.add_exporter(NoobleRawTextSectionExporter())
    map.add_exporter(NoobleRichTextSectionExporter())
    map.add_exporter(NoobleVideoSectionExporter())

    return map


