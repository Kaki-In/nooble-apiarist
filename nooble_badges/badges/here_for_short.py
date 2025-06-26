from nooble_database.database.nooble_account import NoobleAccount
from ..templates.badge import NoobleBadge

import local_utils.images as _local_utils_images
import datetime as _datetime

HERE_FOR_SHORT_BADGE_PRICES = [1, 2, 3, 5, 10, 20, 40]

class HereForShortBadge(NoobleBadge):
    """

    Levels : 
     - 0: now
     - 1: 1 minute
     - 2: 1 hour
     - 3: 1 day
     - 4: 1 week
     - 5: 1 month
     - 6: 1 year

    """

    def __init__(self) -> None:
        super().__init__("here_for_short", 6)

    async def get_price_to_level(self, level: int, account: NoobleAccount) -> int:
        return (HERE_FOR_SHORT_BADGE_PRICES[level])
    
    async def is_elligible_to_level(self, level: int, account: NoobleAccount) -> bool:
        if level == 0:
            return True

        if level == 1:
            return (_datetime.datetime.now() - await account.get_creation_date()) > _datetime.timedelta(minutes=1)

        if level == 2:
            return (_datetime.datetime.now() - await account.get_creation_date()) > _datetime.timedelta(hours=1)

        if level == 3:
            return (_datetime.datetime.now() - await account.get_creation_date()) > _datetime.timedelta(days=1)

        if level == 4:
            return (_datetime.datetime.now() - await account.get_creation_date()) > _datetime.timedelta(days=7)

        if level == 5:
            return (_datetime.datetime.now() - await account.get_creation_date()) > _datetime.timedelta(days=30)

        if level == 6:
            return (_datetime.datetime.now() - await account.get_creation_date()) > _datetime.timedelta(days=365)
        
        return False

    def get_title(self, level: int) -> str:
        return [
            "Fresh newborn",
            "Just Landed",
            "Settling In",
            "Class Visitor",
            "Weekly Regular",
            "Committed Learner",
            "Platform Veteran"
        ][level]
    
    def get_description(self, level: int) -> str:
        return [
            "Celebrating his own birth",
            "Newcomer who just arrived",
            "Have been here for an hour.",
            "A full day with us",
            "A week already? Time flies!",
            "Here a month — thanks for sticking around!",
            "Glad they are still with us"
        ][level]
    
    
