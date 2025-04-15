import database as _database
import database_layering.facades as _database_layering_facades

import local_utils.images as _local_utils_images

class NoobleClass(_database_layering_facades.DatabaseElementFacade[int]):
    def get_id(self) -> int:
        return self.get_element().get_configuration().get_id()
    
    def get_name(self) -> str:
        return self.get_element().get("name")[0]
    
    async def get_thumbnail(self) -> _local_utils_images.Image:
        return await _local_utils_images.from_bytes(self.get_element().get("thumbnail")[0])
    
    def get_section_id(self) -> int:
        return self.get_element().get("section")[0]
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_thumbnail(self, thumbnail: _local_utils_images.Image) -> None:
        self.get_element().set(
            thumbnail = _database.SQLBlob(bytes(thumbnail))
        )

