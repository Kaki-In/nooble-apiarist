from .nooble_object import NoobleObject

import typing as _T

_object_type = _T.TypeVar("_object_type", bound=_T.Mapping[str, _T.Any])
_data_type = _T.TypeVar("_data_type", bound=_T.Mapping[str, _T.Any])

class NoobleSubObject(_T.Generic[_object_type, _data_type]):
    def __init__(self, object: NoobleObject[_object_type], last_object: _T.Optional[_data_type] = None):
        self._object = object
        self._last_object = last_object

    async def ensure_object(self) -> _data_type:
        return self._last_object or await self.get_object()

    def get_last_object(self) -> _data_type | None:
        return self._last_object
    
    def get_parent_object(self) -> NoobleObject[_object_type]:
        return self._object
    
    async def get_object(self) -> _data_type:
        result = await self._get_sub_object_from(await self._object.get_object())

        self._last_object = result

        return result
    
    async def _get_sub_object_from(self, object: _object_type) -> _data_type:
        raise NotImplementedError("get_sub_object_from not implemented for " + repr(self))
    


