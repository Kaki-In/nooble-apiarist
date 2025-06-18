from .base_struct.badges_list import NoobleBadgesList

from .badges.here_for_long import HereForLongBadge
from .badges.here_for_short import HereForShortBadge

DEFAULT_BADGES_LIST = NoobleBadgesList()
DEFAULT_BADGES_LIST.add_badge(HereForLongBadge())
DEFAULT_BADGES_LIST.add_badge(HereForShortBadge())


