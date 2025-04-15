import server_endpoint as _server_endpoint

from .actions import *
from .configuration import *

class NoobleEndpoint(_server_endpoint.ServerEndpoint[NoobleConfiguration]):
    def __init__(self, configuration: NoobleConfiguration):
        super().__init__(configuration)

        self.add_action("/setcolor", ChangeKeyboardColorAction(), "GET")
        self.add_action("/playsound", PlaySoundAction(), "GET")

        self.add_action("/play", StartMusicAction(), "GET")
        self.add_action("/pause", PauseMusicAction(), "GET")

        self.add_action("/stop", StopAction(), "GET")

    
