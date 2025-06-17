import pymongo.asynchronous.collection as _pymongo_collection
import datetime as _datetime

from ..templates.nooble_collection import NoobleCollection

from .nooble_file import NoobleFile, FileObject
from ..objects.file_types import FileType

class NoobleFilesList(NoobleCollection[FileObject]):
    def get_file(self, id: str) -> NoobleFile:
        return NoobleFile(self.get_collection(), id)
    
    async def get_sender_files(self, sender_id: str, files_type: FileType | None = None) -> list[NoobleFile]:
        if files_type is None:
            files = await self.find(
                {
                    "sender": sender_id
                }
            )
        else:
            files = await self.find(
                {
                    "sender": sender_id,
                    "filetype": str(files_type)
                }
            )
        
        file_results: list[NoobleFile] = []

        for file in files:
            file_results.append(NoobleFile(self.get_collection(), file['_id']))

        return file_results
    
    async def create_new_file(self, name:str, filename:str, sent_date:_datetime.datetime, sender_id: str, path: str, type: FileType, file_size: int) -> NoobleFile:
        object: FileObject = {
            "name" : name,
            "filename" : filename,
            "sent_date" : int(sent_date.timestamp()),
            "sender" : sender_id,
            "filepath": path,
            "filetype": type.to_string(),
            "size": file_size
        } #type:ignore

        id = await self.insert_one(object)
        object["_id"] = id

        return NoobleFile(self.get_collection(), id, object)
    

