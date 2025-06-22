import typing as _T

class BindingConfigurationObject(_T.TypedDict):
    host: str
    host_url: str
    port: int
    use_ssl: bool
    cert_file: _T.Optional[str]
    key_file: _T.Optional[str]


