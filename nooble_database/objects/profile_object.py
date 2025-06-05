import typing as _T

class ProfileObject(_T.TypedDict):
    first_name: str
    last_name: str
    profile_image: _T.Optional[str]
    active_decoration: _T.Optional[str]
    active_badges: list[str]
    description: str

