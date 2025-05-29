import typing as _T

from .file_types import RAW_FILE_TYPE

class FileObject(_T.TypedDict):
    _id: int

    name: str
    filename: str
    sent_date: int
    sender: int
    size: int
    filepath: str
    filetype: RAW_FILE_TYPE

