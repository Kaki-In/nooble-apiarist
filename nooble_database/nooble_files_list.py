import pymongo.asynchronous.collection as _pymongo_collection
import datetime as _datetime

from templates.nooble_collection import NoobleCollection

from .nooble_file import NoobleFile, FileObject

class NoobleFilesList(NoobleCollection):
    def __init__(self, collection: _pymongo_collection.AsyncCollection) -> None:
        super().__init__(collection)

    def get_file(self, id: int) -> NoobleFile:
        return NoobleFile(self.get_collection(), id)
    
    async def get_sender_files(self, sender_id: int) -> list[NoobleFile]:
        files = self.get_collection().find(sender = sender_id)

        file_results: list[NoobleFile] = []

        async for file in files:
            file_results.append(NoobleFile(self.get_collection(), file['_id']))

        return file_results
    
    async def create_new_file(self, name:str, filename:str, sent_date:_datetime.datetime, sender_id: int) -> NoobleFile:
        result = await self.get_collection().insert_one({
            "name" : name,
            "filename" : filename,
            "sent_date" : sent_date.timestamp(),
            "sender" : sender_id
        })

        return self.get_file(result.inserted_id)
    

