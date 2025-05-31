import typing as _T

_data_type = _T.TypeVar("_data_type")

class SectionObject(_T.TypedDict):
    type:str
    data: _T.Any
    uses_files: list[int]

class ContainerSectionDataObject(_T.TypedDict):
    is_horizontal: bool
    is_wrapping: bool
    children: list[SectionObject]

class IntegrationSectionDataObject(_T.TypedDict):
    width: str | int
    height: str | int
    src: str
    permissions: list[str]

class ActivitySectionDataObject(_T.TypedDict):
    id: int

class FileSectionDataObject(_T.TypedDict):
    filename: str
    description: str
    src: str


