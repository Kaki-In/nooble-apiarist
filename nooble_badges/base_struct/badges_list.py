from ..templates.badge import NoobleBadge

class NoobleBadgesList():
    def __init__(self) -> None:
        self._badges: dict[str, NoobleBadge] = {}

    def add_badge(self, badge: NoobleBadge) -> None:
        self._badges[badge.get_name()] = badge

    def get_badge(self, name:str) -> NoobleBadge:
        return self._badges[name]
    
    def get_badges_names(self) -> list[str]:
        return list(self._badges)

