from .connection import ForgotPasswordAction, LoginAction, GetLogInfoAction, LogoutAction
from .profile import GetProfileInfoAction, ModifyProfileAction, UpdateProfileAction
from .classes import AddClassAccountAction, CreateClassAction, DeleteClassAction, GetClassAccountsAction, GetClassDataAction, RemoveClassAccountAction, EditClassAction, SearchClassAction, GetClassContentAction
from .accounts import AddAccountAction, DeleteAccountAction, ModifyAccountMailAction, ModifyAccountRoleAction, UpdatePasswordAction, SearchAccountAction, GetAccountInformationAction
from .resources import GetSelfFilesAction, UploadFileAction, DownloadFileAction, DeleteFileAction
from .thread import GetThreadAction, MarkActivitiesAsReadAction
from .badges import BuyBadgeAction, GetBadgeInfoAction, ListBadgesAction, GetBadgeThumbnailAction
from .decorations import BuyDecorationAction, CreateDecorationAction, DeleteDecorationAction, GetDecorationInfoAction, ListDecorationsAction, ModifyDecorationAction
from .safe import GetSafeAction, GetBadgesAction, GetDecorationsAction, GetQuotaAction
from .activities import InitializeActivityAction, NoobleHomeworkActivityPack, GetActivitiesListAction, NoobleMessengerActivityPack
from .details import ApiDetailsAction

