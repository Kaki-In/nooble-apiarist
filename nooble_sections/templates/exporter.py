from .section import NoobleSection

from nooble_database.objects import SectionObject

import typing as _T

_section_type = _T.TypeVar("_section_type", bound=NoobleSection)
_data_type = _T.TypeVar("_data_type")
_input_data_type = _T.TypeVar("_input_data_type")

class NoobleSectionExporter(_T.Generic[_input_data_type, _data_type, _section_type]):
    def __init__(self, type:str):
        self._type = type
    
    def get_type(self) -> str:
        return self._type

    def export(self, exporter, data: _input_data_type) -> _section_type:
        raise NotImplementedError("not implemented for " + repr(self))

