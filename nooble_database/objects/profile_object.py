import typing as _T

from .section_object import SectionObject

class ProfileObject(_T.TypedDict):
    first_name: str
    last_name: str
    profile_image: _T.Optional[int]
    active_decoration: _T.Optional[int]
    active_badges: list[int]
    description: SectionObject

