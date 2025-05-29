import enum as _enum
import typing as _T

RAW_FILE_TYPE = _T.Literal["profile icon", "section file", "decoration banner"]

class FileType(_enum.Enum):
    PROFILE_ICON = "profile icon"
    SECTION_FILE = "section file"
    DECORATION_BANNER = "decoration banner"

    @staticmethod
    def from_raw_filetype(file_type: RAW_FILE_TYPE) -> 'FileType':
        if file_type == "profile icon":
            return FileType.PROFILE_ICON
        
        if file_type == "section file":
            return FileType.SECTION_FILE
        
        if file_type == "decoration banner":
            return FileType.DECORATION_BANNER
        
        raise ValueError("invalid file type given")
    
    def __str__(self) -> RAW_FILE_TYPE:
        return self.value


