from nooble_database.objects.section_objects import ContainerSectionDataObject

from ..templates import NoobleSectionExporter
from ..sections.container import NoobleContainerSection, NoobleContainerSectionData

import nooble_database.objects as _nooble_database_objects

class NoobleContainerSectionExporter(NoobleSectionExporter[_nooble_database_objects.section_objects.ContainerSectionDataObject, NoobleContainerSectionData, NoobleContainerSection]):
    def __init__(self):
        super().__init__("container")

    def export(self, exporter, data: ContainerSectionDataObject) -> NoobleContainerSection:
        return NoobleContainerSection(data["is_horizontal"], data["is_wrapping"], [
            exporter.export(child)
            for child in data["children"]
        ])


