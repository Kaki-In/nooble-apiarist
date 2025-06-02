import typing as _T

from .file_types import RAW_FILE_TYPE

class FileObject(_T.TypedDict):
    _id: str

    name: str
    filename: str
    sent_date: int
    sender: str
    size: int
    filepath: str
    filetype: RAW_FILE_TYPE

