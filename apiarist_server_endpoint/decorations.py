import typing as _T
import asyncio as _asyncio
import json as _json

_description_type = _T.TypeVar("_description_type")
_object = _T.TypeVar("_object")

class NoobleEndpointDecorations():
    @staticmethod
    def description(description:str):
        def descriptor(func: _T.Any):
            return _nooble_endpoint_description(description, func)
            
        return descriptor
    
    @staticmethod
    def validity(*criteria: str):
        def validator(func: _T.Any):
            return _nooble_endpoint_validity(list(criteria), func)
            
        return validator
    
    @staticmethod
    def allow_only_when(*criteria: str):
        def allower(func: _T.Any):
            return _nooble_endpoint_allows(list(criteria), func)
            
        return allower
    
    @staticmethod
    def arguments(**args: str):
        def arguments(func: _T.Any):
            return _nooble_endpoint_arguments(args, func)
            
        return arguments
    
    @staticmethod
    def returns(**data: str):
        def returns(func: _T.Any):
            return _nooble_endpoint_returns(data, func)
            
        return returns
    
    @staticmethod
    def example(example_in: _T.Any, example_out:_T.Any):
        def examples(func: _T.Any):
            return _nooble_endpoint_example((_json.dumps(example_in, indent=4), _json.dumps(example_out, indent=4)), func)
            
        return examples

class _NoobleEndpointDescriptedObject(_T.Generic[_description_type, _object]):
    def __init__(self, name:str, content: _description_type, obj: _T.Any) -> None:
        self._name = name
        self._content = content
        self._obj = obj

    def get_name(self) -> str:
        return self._name

    def get_content(self, name:str) -> _description_type | None:
        if name == self._name:
            return self._content
        
        elif isinstance(self._obj, _NoobleEndpointDescriptedObject):
            return self._obj.get_content(name)
        
        else:
            return None
    
    def __call__(self, *args, **kwargs) -> _object | '_NoobleEndpointDescriptedObject':
        data = self._obj(*args, **kwargs)

        if type(data) is self._obj or isinstance(self._obj, _NoobleEndpointDescriptedObject):
            return _NoobleEndpointDescriptedObject(self._name, self._content, data)

        return data
    
    def __getattribute__(self, name: str) -> _T.Any:
        if name in ("_content", "_name", "_obj", "get_name", "get_content", "__call__"):
            return object.__getattribute__(self, name)

        return self._obj.__getattribute__(name)
    
    def __setattr__(self, name: str, value: _T.Any) -> None:
        if name in ("_content", "_name", "_obj"):
            return object.__setattr__(self, name, value)

        self._obj.__setattr__(name, value)

    def __repr__(self) -> str:
        return "<_NEDO[" + self.get_name() + "] object at " + hex(id(self))[-4:] + ">"

class _nooble_endpoint_description(_NoobleEndpointDescriptedObject[str, _T.Any]):
    def __init__(self, content: str, obj: _T.Any) -> None:
        super().__init__("description", content, obj)

class _nooble_endpoint_validity(_NoobleEndpointDescriptedObject[list[str], _T.Any]):
    def __init__(self, content: list[str], obj: _T.Any) -> None:
        super().__init__("validity", content, obj)
    
class _nooble_endpoint_allows(_NoobleEndpointDescriptedObject[list[str], _T.Any]):
    def __init__(self, content: list[str], obj: _T.Any) -> None:
        super().__init__("allows", content, obj)
    
class _nooble_endpoint_arguments(_NoobleEndpointDescriptedObject[dict[str, str], _T.Any]):
    def __init__(self, content: dict[str, str], obj: _T.Any) -> None:
        super().__init__("arguments", content, obj)

class _nooble_endpoint_returns(_NoobleEndpointDescriptedObject[dict[str, str], _T.Any]):
    def __init__(self, content: dict[str, str], obj: _T.Any) -> None:
        super().__init__("returns", content, obj)
    
class _nooble_endpoint_example(_NoobleEndpointDescriptedObject[tuple[str, str], _T.Any]):
    def __init__(self, content: tuple[str, str], obj: _T.Any) -> None:
        super().__init__("example", content, obj)

    


