import apiarist_server_endpoint as _server_endpoint
from nooble_endpoint.configuration.conf import NoobleEndpointConfiguration

from ..actions import *
from ..configuration import *
from ..templates.nooble_activity_pack import NoobleActivityActionsPack

class NoobleEndpoint(_server_endpoint.ServerEndpoint[NoobleEndpointConfiguration]):
    def __init__(self, configuration: NoobleEndpointConfiguration):
        super().__init__(configuration, configuration.get_configuration().get_host_url())

        self.add_action("/", ApiDetailsAction(self), "GET")

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
        self.add_action("/classes/get-accounts", GetClassAccountsAction(), "GET")
        self.add_action("/classes/get-content", GetClassContentAction(), "GET")
        self.add_action("/classes/data", GetClassDataAction(), "POST", "GET")
        self.add_action("/classes/remove-account", RemoveClassAccountAction(), "POST")
        self.add_action("/classes/edit", EditClassAction(), "POST")
        self.add_action("/classes/search", SearchClassAction(), "GET")
    
        self.add_action("/accounts/add", AddAccountAction(), "POST")
        self.add_action("/accounts/delete", DeleteAccountAction(), "POST")
        self.add_action("/accounts/modify-mail", ModifyAccountMailAction(), "POST")
        self.add_action("/accounts/modify-role", ModifyAccountRoleAction(), "POST")
        self.add_action("/accounts/update-password", UpdatePasswordAction(), "POST")
        self.add_action("/accounts/search", SearchAccountAction(), "GET")
        self.add_action("/accounts/get-info", GetAccountInformationAction(), "GET")

        self.add_action("/resources/get-self-files", GetSelfFilesAction(), "GET")
        self.add_action("/resources/upload", UploadFileAction(), "POST")
        self.add_action("/resources/delete", DeleteFileAction(), "POST")
        self.add_action("/resources/download", DownloadFileAction(), "GET")

        self.add_action("/thread/get", GetThreadAction(), "GET")
        self.add_action("/thread/mark-as-read", MarkActivitiesAsReadAction(), "POST")

        self.add_action("/badges/list", ListBadgesAction(), "GET")
        self.add_action("/badges/get-info", GetBadgeInfoAction(), "GET")
        self.add_action("/badges/get-thumbnail", GetBadgeThumbnailAction(), "GET")
        self.add_action("/badges/buy", BuyBadgeAction(), "POST")

        self.add_action("/decorations/buy", BuyDecorationAction(), "POST")
        self.add_action("/decorations/create", CreateDecorationAction(), "POST")
        self.add_action("/decorations/delete", DeleteDecorationAction(), "POST")
        self.add_action("/decorations/get-info", GetDecorationInfoAction(), "GET")
        self.add_action("/decorations/list", ListDecorationsAction(), "GET")
        self.add_action("/decorations/modify", ModifyDecorationAction(), "POST")

        self.add_action("/safe", GetSafeAction(), "GET")
        self.add_action("/safe/badges", GetBadgesAction(), "GET")
        self.add_action("/safe/decorations", GetDecorationsAction(), "GET")
        self.add_action("/safe/quota", GetQuotaAction(), "GET")

        self.add_action("/activities/list", GetActivitiesListAction(), "GET")
        self.add_action("/activities/init", InitializeActivityAction(), "POST")

        self.add_activity_resources(NoobleHomeworkActivityPack())
    
    def add_activity_resources(self, resource: NoobleActivityActionsPack) -> None:
        for action_name in resource.get_actions():
            self.add_action("/activities/resources/" + resource.get_name() + "/" + action_name, resource.get_action(action_name), *resource.get_methods(action_name))

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

