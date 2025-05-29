import pymongo.asynchronous.collection as _pymongo_collection

import typing as _T

_object_type = _T.TypeVar("_object_type", bound=_T.Mapping[str, _T.Any])

class NoobleObject(_T.Generic[_object_type]):
    def __init__(self, collection: _pymongo_collection.AsyncCollection[_object_type], id: int, last_object: _T.Optional[_object_type] = None) -> None:
        self._coll = collection
        self._id = id
        self._last_object: _object_type | None = last_object

    def get_last_known_object(self) -> _object_type | None:
        return self._last_object

    async def get_object(self) -> _object_type :
        result = await self._coll.find_one(self._id) 

        self._last_object = result

        if result is None:
            raise ReferenceError('no such object')
        
        return result
    
    async def exists(self) -> bool:
        result = await self._coll.find_one(self._id) 
        return result is not None
    
    def get_collection(self) -> _pymongo_collection.AsyncCollection[_object_type]:
        return self._coll
    
    def get_id(self) -> int:
        return self._id
    
    async def update(self, fields: _T.Mapping[str, _T.Any], array_filters: _T.Optional[_T.Sequence[_T.Mapping[str, _T.Any]]] = None) -> bool:
        result = await self._coll.update_one(
            {
                '_id': self._id
            },
            fields,
            array_filters=array_filters
        )

        return result.matched_count == 1

    async def destroy(self) -> bool:
        result = await self._coll.delete_one({
            "_id": self._id
        })

        return result.deleted_count == 1
    



