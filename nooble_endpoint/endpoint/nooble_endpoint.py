import apiarist_server_endpoint as _server_endpoint
from nooble_endpoint.configuration.conf import NoobleEndpointConfiguration

from ..actions import *
from ..configuration import *

class NoobleEndpoint(_server_endpoint.ServerEndpoint[NoobleEndpointConfiguration]):
    def __init__(self, configuration: NoobleEndpointConfiguration):
        super().__init__(configuration)

        self.add_action("/connection/forgot-password", ForgotPasswordAction(), "POST")
        self.add_action("/connection/login", LoginAction(), "POST")
        self.add_action("/connection/log-info", GetLogInfoAction(), "POST", "GET")
        self.add_action("/connection/logout", LogoutAction(), "POST")

        self.add_action("/profile/get-info", GetProfileInfoAction(), "POST", "GET")
        self.add_action("/profile/modify", ModifyProfileAction(), "POST")
        self.add_action("/profile/update", UpdateProfileAction(), "POST")
    
        self.add_action("/classes/add-account", AddClassAccountAction(), "POST")
        self.add_action("/classes/create", CreateClassAction(), "POST")
        self.add_action("/classes/delete", DeleteClassAction(), "POST")
        self.add_action("/classes/get-accounts", GetClassAccountsAction(), "POST")
        self.add_action("/classes/data", GetClassDataAction(), "POST", "GET")
        self.add_action("/classes/remove-account", RemoveClassAccountAction(), "POST")
    


