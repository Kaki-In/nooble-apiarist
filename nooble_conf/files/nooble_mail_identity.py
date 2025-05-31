from ..base_objects.sub_file import NoobleSettingsSubFile
from ..objects.mail_identity import MailIdentityConfigurationObject
from ..objects.mail_sender import MailSenderConfigurationObject

class NoobleMailIdentitySettings(NoobleSettingsSubFile[MailSenderConfigurationObject, MailIdentityConfigurationObject]):
    def _get_data_from_file(self, file_data: MailSenderConfigurationObject) -> MailIdentityConfigurationObject:
        return file_data['identity']
    
    def get_address(self) -> str:
        return self.get_data()['address']
    
    def get_name(self) -> str:
        return self.get_data()['name']
    
    def get_website(self) -> str:
        return self.get_data()['website']

