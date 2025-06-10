from ..templates.nooble_collection import NoobleCollection

from .nooble_decoration import NoobleDecoration
from ..objects.decoration_object import DecorationObject

class NoobleDecorationsList(NoobleCollection[DecorationObject]):
    def get_decoration(self, id: str) -> NoobleDecoration:
        return NoobleDecoration(self.get_collection(), id)
    
    async def create_decoration(self, name:str, image_id:str, price:int) -> NoobleDecoration:
        object: DecorationObject = {
            "name":name,
            "image":image_id,
            "price":price
        } #type:ignore

        id = await self.insert_one(object)
        object["_id"] = id

        return NoobleDecoration(self.get_collection(), id, object)
    
    async def get_all_decorations(self) -> list[NoobleDecoration]:
        decorations = await self.find({})

        return [
            NoobleDecoration(self.get_collection(), decoration["_id"], decoration)
            for decoration in decorations
        ]
    
    async def get_decoration_from_image(self, image_id: str) -> NoobleDecoration | None:
        result = await self.find_one({
            "image_id": image_id
        })

        if result is None:
            return None
        
        else:
            return NoobleDecoration(self.get_collection(), result["_id"], result)

