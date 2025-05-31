import typing as _T

class SmtpServerConfigurationObject(_T.TypedDict):
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

    uses_ssl: bool
    uses_starttls: bool



