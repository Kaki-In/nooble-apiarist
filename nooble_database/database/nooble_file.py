from ..templates.nooble_object import NoobleObject
from ..objects.file_object import FileObject
from ..objects.file_types import FileType

import datetime as _datetime

class NoobleFile(NoobleObject[FileObject]):
    async def get_name(self) -> str:
        object = await self.get_object()

        return object['name']
    
    async def get_filename(self) -> str:
        object = await self.get_object()
        return object['filename']
    
    async def get_sent_date(self) -> _datetime.datetime:
        object = await self.get_object()
        return _datetime.datetime.fromtimestamp(
            object['sent_date']
        )
    
    async def get_sender_id(self) -> int:
        object = await self.get_object()
        return object['sender']
    
    async def get_size(self) -> int:
        object = await self.get_object()
        return object["size"]
    
    async def get_filepath(self) -> str:
        object = await self.get_object()
        return object["filepath"]
    
    async def get_filetype(self) -> FileType:
        object = await self.get_object()
        return FileType.from_raw_filetype(object["filetype"])
    

