from ..templates import NoobleSectionExporter
from ..sections.video import NoobleVideoSection

class NoobleVideoSectionExporter(NoobleSectionExporter[str, str, NoobleVideoSection]):
    def __init__(self):
        super().__init__("video")

    def export(self, exporter, data: str) -> NoobleVideoSection:
        return NoobleVideoSection(data)
    

