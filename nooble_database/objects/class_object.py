import typing as _T

from .section_object import SectionObject

class ClassObject(_T.TypedDict):
    _id: int
    
    name: str
    description: str
    last_modification: int
    last_modifier: int
    content: SectionObject
    accounts: list[int]
    


