from .binding import BindingConfigurationObject
from .registrations import RegistrationsConfigurationObject

import typing as _T

class EndpointConfigurationObject(_T.TypedDict):
    binding: BindingConfigurationObject
    registrations: RegistrationsConfigurationObject


