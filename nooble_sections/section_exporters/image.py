from ..templates import NoobleSectionExporter
from ..sections.image import NoobleImageSection

class NoobleImageSectionExporter(NoobleSectionExporter[str, str, NoobleImageSection]):
    def __init__(self):
        super().__init__("image")

    def export(self, exporter, data: str) -> NoobleImageSection:
        return NoobleImageSection(data)
    

