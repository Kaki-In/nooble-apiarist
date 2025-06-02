import typing as _T

class SafeObject(_T.TypedDict):
    quota:int
    badges: list[tuple[str, int]]
    decorations: list[int]


