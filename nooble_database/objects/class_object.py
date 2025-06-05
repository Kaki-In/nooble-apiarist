import typing as _T

from .section_objects import SectionObject

class ClassObject(_T.TypedDict):
    _id: str
    
    name: str
    description: str
    last_modification: int
    last_modifier: str
    content: SectionObject
    accounts: list[int]
    


