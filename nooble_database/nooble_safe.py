from .objects.safe_object import SafeObject
from .objects.account_object import AccountObject
from .templates.nooble_sub_object import NoobleSubObject

class NoobleSafe(NoobleSubObject[AccountObject, SafeObject]):
    async def _get_sub_object_from(self, object: AccountObject) -> SafeObject:
        return object['safe']

    async def get_quota(self) -> int:
        return (await self.get_object())['quota'] 
        
    async def increase(self, count: int) -> None:
        await self.get_parent_object().update(
            {
                "$inc": {
                    'safe.quota': count
                }
            }
        )

    async def decrease(self, count: int) -> None:
        await self.get_parent_object().update(
            {
                "$dec": {
                    'safe.quota': count
                }
            }
        )
    
    async def set_quota(self, quota: int) -> None:
        await self.get_parent_object().update(
            {
                "$set": {
                    "safe.quota": quota
                }
            }
        )
    
