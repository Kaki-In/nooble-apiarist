from ..templates import NoobleSectionExporter
from ..sections.audio import NoobleAudioSection

class NoobleAudioSectionExporter(NoobleSectionExporter[str, str, NoobleAudioSection]):
    def __init__(self):
        super().__init__("audio")

    def export(self, exporter, data: str) -> NoobleAudioSection:
        return NoobleAudioSection(data)
    

