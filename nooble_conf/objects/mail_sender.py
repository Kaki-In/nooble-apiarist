from .smtp_server import SmtpServerConfigurationObject
from .mail_identity import MailIdentityConfigurationObject

import typing as _T

class MailSenderConfigurationObject(_T.TypedDict):
    smtp: SmtpServerConfigurationObject
    identity: MailIdentityConfigurationObject

