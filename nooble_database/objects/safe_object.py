import typing as _T

class SafeObject(_T.TypedDict):
    quota:int
    badges: list[int]
    decorations: list[int]


