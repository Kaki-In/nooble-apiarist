from .connection import ForgotPasswordAction, LoginAction, GetLogInfoAction, LogoutAction
from .profile import GetProfileInfoAction, ModifyProfileAction, UpdateProfileAction
from .classes import AddClassAccountAction, CreateClassAction, DeleteClassAction, GetClassAccountsAction, GetClassDataAction, RemoveClassAccountAction, EditClassAction
from .accounts import AddAccountAction, DeleteAccountAction, ModifyAccountMailAction, ModifyAccountRoleAction
from .resources import GetSelfFilesAction, UploadFileAction, DownloadFileAction, DeleteFileAction
from .thread import GetThreadAction, MarkActivitiesAsReadAction
from .badges import BuyBadgeAction, GetBadgeInfosAction, ListBadgesAction, GetBadgeThumbnailAction
from .decorations import BuyDecorationAction, CreateDecorationAction, DeleteDecorationAction, GetDecorationInfosAction, ListDecorationsAction, ModifyDecorationAction
from .safe import GetSafeAction, GetBadgesAction, GetDecorationsAction, GetQuotaAction
from .activities import GetActivitiesListAction, NoobleHomeworkActivityPack
from .details import ApiDetailsAction

