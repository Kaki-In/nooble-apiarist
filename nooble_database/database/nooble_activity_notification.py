from ..objects.activity_notification_object import ActivityNotificationObject
from ..objects.account_object import AccountObject

from ..templates.nooble_sub_object import NoobleSubObject
from ..templates.nooble_object import NoobleObject

class NoobleActivityNotification(NoobleSubObject[AccountObject, ActivityNotificationObject]):
    def __init__(self, account: NoobleObject[AccountObject], activity_id: str, last_object: ActivityNotificationObject | None = None) -> None:
        super().__init__(account, last_object)

        self._activity_id = activity_id

    async def _get_sub_object_from(self, object: AccountObject) -> ActivityNotificationObject:
        for notification in object['activities']:
            if notification['activity'] == self._activity_id:
                return notification
            
        raise ReferenceError("no such activity")
    
    async def exists(self) -> bool:
        for notification in (await self.get_parent_object().ensure_object())['activities']:
            if notification['activity'] == self._activity_id:
                return True
            
        return False
    

    async def mark_as_read(self, read=True) -> bool:
        return await self.get_parent_object().update(
            {
                "$set": {
                    'activities.$[element].read': read
                }
            },
            array_filters=[
                {
                    'element.activity': self._activity_id
                }
            ]
        )



