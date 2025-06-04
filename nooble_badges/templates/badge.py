import local_utils.images as _local_utils_images
import nooble_database.database as _nooble_database

import nooble_conf.default_assets as _nooble_assets

class NoobleBadge():
    def __init__(self, name: str, max_level: int) -> None:
        self._name = name
        self._max_level = max_level

    def get_name(self) -> str:
        return self._name
    
    def get_max_level(self) -> int:
        return self._max_level
    
    async def get_image(self, level: int) -> _local_utils_images.Image:
        return await _local_utils_images.from_bytes(
            _nooble_assets.get_default_asset_content(
                f"badges/{self._name}/{level}.png"
            )
        )
    
    async def get_price_to_level(self, level: int, account: _nooble_database.NoobleAccount) -> int:
        raise NotImplementedError("not implemented for " + repr(self))
    
    async def is_elligible_to_level(self, level: int, account: _nooble_database.NoobleAccount) -> bool:
        raise NotImplementedError("not implemented for " + repr(self))
    
    def get_title(self, level: int) -> str:
        raise NotImplementedError("not implemented for " + repr(self))
    
    def get_description(self, level: int) -> str:
        raise NotImplementedError("not implemented for " + repr(self))
    

