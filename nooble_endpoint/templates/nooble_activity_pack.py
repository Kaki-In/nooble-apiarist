from .nooble_activity_action import NoobleEndpointActivityAction

class NoobleActivityActionsPack():
    def __init__(self, name:str) -> None:
        self._name = name
        self._actions = {}
        self._methods = {}

    def get_name(self) -> str:
        return self._name

    def add_action(self, name:str, action: NoobleEndpointActivityAction, *methods:str) -> None:
        self._actions[name] = action
        self._methods[name] = methods

    def get_actions(self) -> list[str]:
        return list(self._actions)
    
    def get_action(self, name:str) -> NoobleEndpointActivityAction:
        return self._actions[name] 
    
    def get_methods(self, name:str) -> list[str]:
        return list(self._methods[name])
    
