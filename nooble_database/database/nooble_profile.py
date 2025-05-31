from ..templates.nooble_sub_object import NoobleSubObject

from ..objects.profile_object import ProfileObject
from ..objects.account_object import AccountObject
from ..objects.section_object import SectionObject

class NoobleProfile(NoobleSubObject[AccountObject, ProfileObject]):
    async def _get_sub_object_from(self, object: AccountObject) -> ProfileObject:
        return object['profile']
    
    async def get_first_name(self) -> str:
        return (await self.get_object())['first_name'] 
    
    async def get_last_name(self) -> str:
        return (await self.get_object())['last_name'] 

    async def get_profile_image_id(self) -> int:
        return (await self.get_object())['profile_image']
    
    async def get_active_decoration_id(self) -> int | None:
        return (await self.get_object())['active_decoration']
    
    async def get_active_badges_ids(self) -> list[int]:
        return (await self.get_object())['active_badges']
    
    async def get_description(self) -> SectionObject:
        return (await self.get_object())['description']
    
