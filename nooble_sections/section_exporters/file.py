from ..templates import NoobleSectionExporter
from ..sections.file import NoobleFileSection, NoobleFileSectionData

import nooble_database.objects as _nooble_database_objects

class NoobleFileSectionExporter(NoobleSectionExporter[_nooble_database_objects.section_objects.FileSectionDataObject, NoobleFileSectionData, NoobleFileSection]):
    def __init__(self):
        super().__init__("file")

    def export(self, exporter, data: _nooble_database_objects.section_objects.FileSectionDataObject) -> NoobleFileSection:
        return NoobleFileSection(
            data["filename"],
            data["description"],
            data["src"]
        )

