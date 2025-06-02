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
    
        self.add_action("/accounts/add", AddAccountAction(), "POST")
        self.add_action("/accounts/delete", DeleteAccountAction(), "POST")
        self.add_action("/accounts/modify-mail", ModifyAccountMailAction(), "POST")
        self.add_action("/accounts/modify-role", ModifyAccountRoleAction(), "POST")

    async def main(self) -> None:
        configuration = self.get_configuration().get_configuration()

        if configuration.get_uses_ssl():
            certfile = configuration.get_certificate_file()
            keyfile = configuration.get_key_file()

            if certfile is None:
                raise ValueError('certificate file not specified')

            if keyfile is None:
                raise ValueError('key file not specified')

            return await self.run(certfile, keyfile)
        
        else:
            return await self.run_locally()

