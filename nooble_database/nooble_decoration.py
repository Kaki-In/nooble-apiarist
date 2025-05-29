from .templates.nooble_object import NoobleObject
from .objects.decoration_object import DecorationObject

class NoobleDecoration(NoobleObject[DecorationObject]):
    async def get_image_id(self) -> int:
        object = await self.get_object()
        return object['image']
    
    async def get_name(self) -> str:
        object = await self.get_object()
        return object['name']
    
    async def get_price(self) -> int:
        object = await self.get_object()
        return object['price']


