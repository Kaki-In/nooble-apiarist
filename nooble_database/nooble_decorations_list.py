from .templates.nooble_collection import NoobleCollection

from .nooble_decoration import NoobleDecoration

import local_utils.images as _local_utils_images

class NoobleDecorationsList(NoobleCollection):
    def get_decoration(self, id: int) -> NoobleDecoration:
        return NoobleDecoration(self.get_collection(), id)
    
    async def create_decoration(self, name:str, image:_local_utils_images.Image, price:int) -> NoobleDecoration:
        result = await self.get_collection().insert_one({
            "name":name,
            "image":str(image),
            "price":price
        })

        return self.get_decoration(result.inserted_id)

