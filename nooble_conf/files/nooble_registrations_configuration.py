from ..objects.registrations import RegistrationsConfigurationObject
from ..objects.endoint import EndpointConfigurationObject

from ..base_objects.sub_file import NoobleSettingsSubFile

import datetime as _datetime

class NoobleRegistrationsSettings(NoobleSettingsSubFile[EndpointConfigurationObject, RegistrationsConfigurationObject]):
    def _get_data_from_file(self, file_data: EndpointConfigurationObject) -> RegistrationsConfigurationObject:
        return file_data["registrations"]
    
    def get_tokens_size(self) -> int:
        return self.get_data()["tokens_size"]
    
    def get_tokens_duration(self) -> _datetime.timedelta:
        return _datetime.timedelta(minutes = self.get_data()["token_duration_minutes"])



