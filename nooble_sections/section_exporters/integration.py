from nooble_database.objects.section_objects import FileSectionDataObject
from ..templates import NoobleSectionExporter
from ..sections.integration import NoobleIntegrationSection, NoobleIntegrationSectionData

import nooble_database.objects as _nooble_database_objects

class NoobleIntegrationSectionExporter(NoobleSectionExporter[_nooble_database_objects.section_objects.IntegrationSectionDataObject, NoobleIntegrationSectionData, NoobleIntegrationSection]):
    def __init__(self):
        super().__init__("integration")

    def export(self, exporter, data: _nooble_database_objects.section_objects.IntegrationSectionDataObject) -> NoobleIntegrationSection:
        return NoobleIntegrationSection(
            data["width"],
            data['height'],
            data["src"],
            data["permissions"]
        )

