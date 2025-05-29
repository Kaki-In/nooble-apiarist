from .templates.nooble_collection import NoobleCollection

from .nooble_decoration import NoobleDecoration
from .objects.decoration_object import DecorationObject

class NoobleDecorationsList(NoobleCollection[DecorationObject]):
    def get_decoration(self, id: int) -> NoobleDecoration:
        return NoobleDecoration(self.get_collection(), id)
    
    async def create_decoration(self, name:str, image_id:int, price:int) -> NoobleDecoration:
        object: DecorationObject = {
            "_id": -1,
            "name":name,
            "image":image_id,
            "price":price
        }

        id = await self.insert_one(object)
        object["_id"] = id

        return NoobleDecoration(self.get_collection(), id, object)

