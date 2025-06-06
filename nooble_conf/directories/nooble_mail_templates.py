from ..base_objects.directory import NoobleSettingsDirectory
from ..base_objects.asset import NoobleSettingsAsset
from ..base_objects.sub_file import NoobleSettingsSubFile

from ..default_assets import get_default_asset_content

from ..objects.mail_identity import MailIdentityConfigurationObject

import nooble_database.objects as _database_objects
import local_utils.images as _local_utils_images

import typing as _T

class NoobleMailTemplatesConfiguration(NoobleSettingsDirectory):
    def __init__(self, pathname: str, identity: NoobleSettingsSubFile[_T.Any, MailIdentityConfigurationObject]) -> None:
        super().__init__(pathname)

        self._identity = identity

        self._base_template = NoobleSettingsAsset(
            self._create_sub_element_path("base_template.html"), 
            get_default_asset_content("mail_base_template.html")
        )

        self._mail_style = NoobleSettingsAsset(
            self._create_sub_element_path("style.css"),
            get_default_asset_content("mail_style.css")
        )

        self._send_password_template = NoobleSettingsAsset(
            self._create_sub_element_path("send_password_template.html"),
            get_default_asset_content("mail_send_password_template.html")
        )

        self._edited_address_template = NoobleSettingsAsset(
            self._create_sub_element_path("edited_address_template.html"),
            get_default_asset_content("mail_edited_address_template.html")
        )

        self._edited_profile_template = NoobleSettingsAsset(
            self._create_sub_element_path("edited_profile_template.html"),
            get_default_asset_content("mail_edited_profile_template.html")
        )

        self._edited_class_template = NoobleSettingsAsset(
            self._create_sub_element_path("edited_class_template.html"),
            get_default_asset_content("mail_edited_class_template.html")
        )

        self._edited_role_template = NoobleSettingsAsset(
            self._create_sub_element_path("edited_role_template.html"),
            get_default_asset_content("mail_edited_role_template.html")
        )

        self._icon = NoobleSettingsAsset(
            self._create_sub_element_path("icon.png"),
            get_default_asset_content("mail_icon.png")
        )

    def get_mail_template(self, receiver: _database_objects.AccountObject, content:str) -> str:
        return self._base_template.get_content().decode().format(
            receiver = receiver,
            content = content,
            style = self._mail_style.get_content().decode(),
            identity = self._identity.get_data(),
        )
    
    def get_send_password_mail_template(self, receiver: _database_objects.AccountObject, password: str) -> str:
        return self.get_mail_template(
            receiver,
            self._send_password_template.get_content().decode().format(
                receiver = receiver,
                sent_password = password,
                identity = self._identity.get_data()
            ),
        )
    
    def get_edited_class_mail_template(self, receiver: _database_objects.AccountObject, nooble_class: _database_objects.ClassObject, modifier: _database_objects.AccountObject) -> str:
        return self.get_mail_template(
            receiver, 
            self._edited_class_template.get_content().decode().format(
                receiver = receiver,
                modified_class = nooble_class,
                modifier = modifier,
                identity = self._identity.get_data()
            )
        )
    
    def get_edited_profile_mail_template(self, receiver: _database_objects.AccountObject, modifier: _database_objects.AccountObject) -> str:
        return self.get_mail_template(
            receiver, 
            self._edited_profile_template.get_content().decode().format(
                receiver = receiver,
                modifier = modifier,
                identity = self._identity.get_data()
            )
        )
    
    def get_edited_role_mail_template(self, receiver: _database_objects.AccountObject, modifier: _database_objects.AccountObject) -> str:
        if receiver["role"] == "admin":
            role_name = "Administrateur"
            role_description = "vous pouvez dorénavant administrer les cours, utilisateurs et décorations de la plateforme"
        elif receiver["role"] ==  "student":
            role_name = "Étudiant"
            role_description = "vous êtes à présent un simple étudiant"
        elif receiver["role"] == "teacher":
            role_name = "Enseignant"
            role_description = "vous pouvez modifier les cours qui vous seront associés"
        elif receiver["role"] == "teacher_admin":
            role_name = "Enseignant administrateur"
            role_description = "vous pouvez à la fois proposer des cours à des élèves, à la fois administrer les autres cours, utilisateurs et décorations de la plateforme. "
        else:
            raise ValueError("invalid role given in receiver")

        return self.get_mail_template(
            receiver, 
            self._edited_role_template.get_content().decode().format(
                receiver = receiver,
                modifier = modifier,
                role_name = role_name,
                role_description = role_description,
                identity = self._identity.get_data()
            )
        )
    
    def get_edited_address_mail_template(self, receiver: _database_objects.AccountObject, modifier: _database_objects.AccountObject, new_address:str) -> str:
        return self.get_mail_template(
            receiver, 
            self._edited_address_template.get_content().decode().format(
                receiver = receiver,
                modifier = modifier,
                new_address = new_address,
                identity = self._identity.get_data()
            )
        )
    
    def get_icon_bytes(self) -> bytes:
        return self._icon.get_content()
    
    async def get_icon(self) -> _local_utils_images.Image:
        return await _local_utils_images.from_bytes(self._icon.get_content())



