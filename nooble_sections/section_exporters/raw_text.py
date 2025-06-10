from ..templates import NoobleSectionExporter
from ..sections.raw_text import NoobleRawTextSection

class NoobleRawTextSectionExporter(NoobleSectionExporter[str, str, NoobleRawTextSection]):
    def __init__(self):
        super().__init__("raw-text")

    def export(self, exporter, data: str) -> NoobleRawTextSection:
        return NoobleRawTextSection(data)
    

