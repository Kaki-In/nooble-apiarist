from ..templates import NoobleSectionExporter
from ..sections.rich_text import NoobleRichTextSection

class NoobleRichTextSectionExporter(NoobleSectionExporter[str, str, NoobleRichTextSection]):
    def __init__(self):
        super().__init__("rich-text")

    def export(self, exporter, data: str) -> NoobleRichTextSection:
        return NoobleRichTextSection(data)
    

