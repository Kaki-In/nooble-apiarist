from ..templates.nooble_object import NoobleObject
from ..objects.roles import Role
from ..objects.account_object import AccountObject

from .nooble_profile import NoobleProfile
from .nooble_safe import NoobleSafe

from .nooble_activity_notification import NoobleActivityNotification

class NoobleAccount(NoobleObject[AccountObject]):
    def get_profile(self) -> NoobleProfile:
        last_object = self.get_last_known_object()

        if last_object:
            return NoobleProfile(self, last_object['profile'])
        
        else:
            return NoobleProfile(self)
    
    def get_safe(self) -> NoobleSafe:
        last_object = self.get_last_known_object()

        if last_object:
            return NoobleSafe(self, last_object['safe'])
        
        else:
            return NoobleSafe(self)
    
    async def get_mail(self) -> str:
        data = await self.get_object()
        return data['mail']
    
    async def get_role(self) -> Role:
        data = await self.get_object()
        return Role.from_raw_role(data['role'])
    
    async def get_activities(self) -> list[NoobleActivityNotification]:
        data = await self.get_object()
        return [
            NoobleActivityNotification(self, activity['activity'], activity) for activity in data['activities']
        ]
    
    async def mark_activities_as_read(self) -> None:
        await self.update(
            {
                "$set": {
                    'activities.$[].read': True
                }
            }
        )
    
