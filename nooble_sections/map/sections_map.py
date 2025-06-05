from ..templates import NoobleSection, NoobleSectionExporter

import typing as _T

import nooble_database.objects as _nooble_database_objects

class NoobleSectionsMap():
    def __init__(self) -> None:
        self._exporters = {}

    def add_exporter(self, exporter: NoobleSectionExporter) -> None:
        self._exporters[exporter.get_type()] = exporter

    def get_exporter(self, name:str) -> NoobleSectionExporter:
        return self._exporters[name]
    
    def export(self, object: _nooble_database_objects.SectionObject) -> NoobleSection:
        return self.get_exporter(object["type"]).export(self, object["data"])
    
