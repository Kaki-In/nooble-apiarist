from .profile_object import ProfileObject
from .safe_object import SafeObject
from .roles import RAW_ROLE
from .activity_notification_object import ActivityNotificationObject

import typing as _T

class AccountObject(_T.TypedDict):
    _id: int

    mail: str
    password: str
    profile: ProfileObject
    safe: SafeObject
    role: RAW_ROLE
    activities: list[ActivityNotificationObject]
    creation_date: int
    

