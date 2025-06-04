from nooble_database.database.nooble_account import NoobleAccount
from ..templates.badge import NoobleBadge

import local_utils.images as _local_utils_images
import datetime as _datetime

HERE_FOR_LONG_BADGE_YEARS = [1, 2, 3, 5, 10, 20]

class HereForLongBadge(NoobleBadge):
    """

    Levels : 
     - 0: 1 year
     - 1: 2 years
     - 2: 3 years
     - 3: 5 years
     - 4: 10 years
     - 5: 20 years

    """

    def __init__(self) -> None:
        super().__init__("here_for_long", 6)

    async def get_price_to_level(self, level: int, account: NoobleAccount) -> int:
        return (HERE_FOR_LONG_BADGE_YEARS[level]) * 100
    
    async def is_elligible_to_level(self, level: int, account: NoobleAccount) -> bool:
        return (_datetime.datetime.now() - await account.get_creation_date()) > _datetime.timedelta(days = HERE_FOR_LONG_BADGE_YEARS[level] * 365)
    
    def get_title(self, level: int) -> str:
        return [
            "Accustomed",
            "Integrated",
            "Grounded",
            "Resident",
            "Citizen",
            "Dean"
        ][level]
    
    def get_description(self, level: int) -> str:
        return f"You have been here for {HERE_FOR_LONG_BADGE_YEARS[level]} years"
    
    
