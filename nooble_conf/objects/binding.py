import typing as _T

class BindingConfigurationObject(_T.TypedDict):
    host: str
    port: int
    use_ssl: bool
    public_key_file: _T.Optional[str]
    private_key_file: _T.Optional[str]


