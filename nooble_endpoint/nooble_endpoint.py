import server_endpoint as _server_endpoint

from .actions import *
from .configuration import *

class NoobleEndpoint(_server_endpoint.ServerEndpoint[NoobleConfiguration]):
    def __init__(self, configuration: NoobleConfiguration):
        super().__init__(configuration)


    
