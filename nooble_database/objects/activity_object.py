import typing as _T

class ActivityObject(_T.TypedDict):
    _id: str

    icon: str
    title: str
    content: str
    creator: str
    date: int

