import typing as _T

_data_type = _T.TypeVar("_data_type")

class SectionObject(_T.TypedDict, _T.Generic[_data_type]):
    type:str
    data: _data_type

# Raw Text

class RawTextSectionObject(SectionObject[str]):
    pass

# Rich Text

class RichTextSectionObject(SectionObject[str]):
    pass

# Container

class ContainerSectionDataObject(_T.TypedDict):
    is_horizontal: bool
    is_wrapping: bool
    children: list[SectionObject]

class ContainerSectionObject(SectionObject[ContainerSectionDataObject]):
    pass

# Audio

class AudioSectionObject(SectionObject[str]):
    pass

# Video

class VideoSectionObject(SectionObject[str]):
    pass

# Image

class ImageSectionObject(SectionObject[str]):
    pass

# Integration

class IntegrationSectionDataObject(_T.TypedDict):
    width: str | int
    height: str | int
    src: str
    permissions: list[str]

class IntegrationSectionObject(SectionObject[IntegrationSectionDataObject]):
    pass

# Activity

class ActivitySectionDataObject(_T.TypedDict):
    file_id: str

class ActivitySectionObject(SectionObject[ActivitySectionDataObject]):
    pass

# Files

class FileSectionDataObject(_T.TypedDict):
    filename: str
    description: str
    src: str

class FileSectionObject(SectionObject[FileSectionDataObject]):
    pass

