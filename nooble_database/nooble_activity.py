from .templates.nooble_object import *
from .objects.activity_object import ActivityObject

import local_utils.images as _local_utils_images
import datetime as _datetime

class NoobleActivity(NoobleObject[ActivityObject]):
    async def get_icon(self) -> _local_utils_images.Image:
        object = await self.get_object()
        return await _local_utils_images.from_string(object['icon'])
    
    async def get_title(self) -> str:
        object = await self.get_object()
        return object['title']
    
    async def get_content(self) -> str:
        object = await self.get_object()
        return object['content']
    
    async def get_creator_id(self) -> int:
        object = await self.get_object()
        return object['creator']
    
    async def get_date(self) -> _datetime.datetime:
        object = await self.get_object()
        return _datetime.datetime.fromtimestamp(object['date'])
 

