from ..templates.badge import NoobleBadge

class NoobleBadgesList():
    def __init__(self) -> None:
        self._badges = {}

    def add_badge(self, badge: NoobleBadge) -> None:
        self._badges[badge.get_name()] = badge

    def get_badge(self, name:str) -> int:
        return self._badges[name]

