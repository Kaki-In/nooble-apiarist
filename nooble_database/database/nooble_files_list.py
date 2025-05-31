import pymongo.asynchronous.collection as _pymongo_collection
import datetime as _datetime

from ..templates.nooble_collection import NoobleCollection

from .nooble_file import NoobleFile, FileObject
from ..objects.file_types import FileType

class NoobleFilesList(NoobleCollection[FileObject]):
    def get_file(self, id: int) -> NoobleFile:
        return NoobleFile(self.get_collection(), id)
    
    async def get_sender_files(self, sender_id: int) -> list[NoobleFile]:
        files = self.get_collection().find(sender = sender_id)

        file_results: list[NoobleFile] = []

        async for file in files:
            file_results.append(NoobleFile(self.get_collection(), file['_id']))

        return file_results
    
    async def create_new_file(self, name:str, filename:str, sent_date:_datetime.datetime, sender_id: int, path: str, type: FileType, file_size: int) -> NoobleFile:
        object: FileObject = {
            "_id": -1,
            "name" : name,
            "filename" : filename,
            "sent_date" : int(sent_date.timestamp()),
            "sender" : sender_id,
            "filepath": path,
            "filetype": type.to_string(),
            "size": file_size
        }

        id = await self.insert_one(object)
        object["_id"] = id

        return NoobleFile(self.get_collection(), id, object)
    

