import pymongo.asynchronous.collection as _pymongo_collection

import typing as _T

_data_type = _T.TypeVar("_data_type", bound=_T.Mapping[str, _T.Any])

class NoobleCollection(_T.Generic[_data_type]):
    def __init__(self, collection: _pymongo_collection.AsyncCollection[_data_type]) -> None:
        self._coll = collection

    def get_collection(self) -> _pymongo_collection.AsyncCollection[_data_type]:
        return self._coll
        
    async def update(self, identifiers: _T.Mapping[str, _T.Any], fields: _T.Mapping[str, _T.Any]) -> int:
        result = await self._coll.update_many(
            identifiers,
            fields
        )
        
        return result.matched_count

    async def find(self, fields: _T.Mapping) -> list[_data_type]:
        objects = self._coll.find(fields)

        results: list[_data_type] = []

        async for i in objects:
            results.append(i)

        return results
    
    async def find_one(self, fields: _T.Mapping) -> _data_type | None:
        return await self._coll.find_one(fields)
    
    async def insert_one(self, object: _data_type) -> str:
        result = await self._coll.insert_one(object)
        return result.inserted_id
    
    async def insert_many(self, *objects: _data_type) -> list[str]:
        result = await self._coll.insert_many(objects)
        return result.inserted_ids
    
    async def delete_one(self, fields: _T.Mapping[str, _T.Any]) -> bool:
        result = await self._coll.delete_one(fields)
        return result.deleted_count == 1
    
    async def delete_many(self, fields: _T.Mapping[str, _T.Any]) -> int:
        result = await self._coll.delete_many(fields)
        return result.deleted_count

 

