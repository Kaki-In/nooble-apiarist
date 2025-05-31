from ..templates.nooble_object import NoobleObject
from ..objects.class_object import ClassObject
from ..objects.section_object import SectionObject

import datetime as _datetime

class NoobleClass(NoobleObject[ClassObject]):
    async def get_name(self) -> str:
        return (await self.get_object())["name"]
    
    async def get_description(self) -> str:
        return (await self.get_object())["description"]
    
    async def get_last_modification_date(self) -> _datetime.datetime:
        return _datetime.datetime.fromtimestamp((await self.get_object())["last_modification"])
    
    async def get_last_modification_author_id(self) -> int:
        return (await self.get_object())["last_modifier"]
    
    async def get_content(self) -> SectionObject:
        return (await self.get_object())["content"]
    
    async def get_accounts_ids(self) -> list[int]:
        return (await self.get_object())["accounts"]


