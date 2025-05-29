import typing as _T

class ActivityObject(_T.TypedDict):
    _id: int

    icon: str
    title: str
    content: str
    creator: int
    date: int

