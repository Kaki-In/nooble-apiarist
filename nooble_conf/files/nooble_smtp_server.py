from ..base_objects.sub_file import NoobleSettingsSubFile
from ..objects.smtp_server import SmtpServerConfigurationObject
from ..objects.mail_sender import MailSenderConfigurationObject

class NoobleSmtpServerSettings(NoobleSettingsSubFile[MailSenderConfigurationObject, SmtpServerConfigurationObject]):
    def _get_data_from_file(self, file_data: MailSenderConfigurationObject) -> SmtpServerConfigurationObject:
        return file_data['smtp']
    
    def get_host(self) -> str:
        return self.get_data()['smtp_host']
    
    def get_port(self) -> int:
        return self.get_data()["smtp_port"]
    
    def get_username(self) -> str:
        return self.get_data()["smtp_username"]
    
    def get_password(self) -> str:
        return self.get_data()['smtp_password']
    
    def uses_ssl(self) -> bool:
        return self.get_data()["uses_ssl"]
    
    def uses_starttls(self) -> bool:
        return self.get_data()["uses_starttls"]


