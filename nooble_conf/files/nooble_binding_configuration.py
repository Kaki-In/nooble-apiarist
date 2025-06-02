from ..objects.binding import BindingConfigurationObject
from ..objects.endoint import EndpointConfigurationObject
from ..base_objects.sub_file import NoobleSettingsSubFile

class NoobleBindingSettings(NoobleSettingsSubFile[EndpointConfigurationObject, BindingConfigurationObject]):
    def _get_data_from_file(self, file_data: EndpointConfigurationObject) -> BindingConfigurationObject:
        return file_data['binding']
    
    def get_host(self) -> str:
        return self.get_data()['host']
    
    def get_port(self) -> int:
        return self.get_data()["port"]
    
    def get_uses_ssl(self) -> bool:
        return self.get_data()['use_ssl']
    
    def get_certificate_file(self) -> str | None:
        return self.get_data()["cert_file"]
    
    def get_key_file(self) -> str | None:
        return self.get_data()["key_file"]
    

