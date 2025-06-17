from nooble_conf.files.nooble_mail_sender import NoobleMailSenderSettings
from nooble_conf.directories.nooble_mail_templates import NoobleMailTemplatesConfiguration

import nooble_database.objects as _nooble_database_objects
import smtplib as _smtplib
import email.mime.multipart as _email_multipart
import email.mime.text as _email_text
import email.mime.image as _email_image
import email.utils as _email_utils
import asyncio as _asyncio

import ssl as _ssl

class NoobleMailSender():
    def __init__(self, conf: NoobleMailSenderSettings, templates: NoobleMailTemplatesConfiguration) -> None:
        self._conf = conf
        self._templates = templates
    
    def get_configuration(self) -> NoobleMailSenderSettings:
        return self._conf
    
    def get_templates(self) -> NoobleMailTemplatesConfiguration:
        return self._templates
    
    def create_smtp_conn(self) -> _smtplib.SMTP:
        smtp_conf = self._conf.get_smtp_server_configuration()

        if smtp_conf.uses_ssl():
            smtp = _smtplib.SMTP_SSL(smtp_conf.get_host())
        else:
            smtp = _smtplib.SMTP(smtp_conf.get_host())

        smtp.connect(smtp_conf.get_host(), smtp_conf.get_port())

        if smtp_conf.uses_starttls():
            smtp.starttls(context=_ssl.SSLContext(_ssl.PROTOCOL_TLS))

        smtp.login(smtp_conf.get_username(), smtp_conf.get_password())

        return smtp
    
    async def send_email(self, account: _nooble_database_objects.AccountObject, subject:str, content: str) -> None:
        sender_address = "{} <{}>".format(
            self._conf.get_identity_configuration().get_name(),
            self._conf.get_identity_configuration().get_address()
        )
        receiver_address = "{} {} <{}>".format(
            account['profile']['first_name'],
            account['profile']['last_name'],
            account['mail']
        )

        # Message principal : multipart/related
        msg_root = _email_multipart.MIMEMultipart('related')
        msg_root['Subject'] = subject
        msg_root['From'] = sender_address
        msg_root['To'] = receiver_address
        msg_root["Date"] = _email_utils.formatdate(localtime=True)

        # Partie alternative : text/plain + text/html
        msg_alternative = _email_multipart.MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)

        # HTML (ou ajouter aussi un plain text si nécessaire)
        part_html = _email_text.MIMEText(content, 'html')
        msg_alternative.attach(part_html)

        # Image inline
        icon = _email_image.MIMEImage(self._templates.get_icon_bytes())
        icon.add_header('Content-ID', '<nooble_icon>')
        icon.add_header("Content-Disposition", "inline", filename="logo.png")
        msg_root.attach(icon)

        # Envoi
        try:
            smtp = await _asyncio.get_event_loop().run_in_executor(None, self.create_smtp_conn)
            await _asyncio.get_event_loop().run_in_executor(
                None, smtp.sendmail, sender_address, receiver_address, msg_root.as_string()
            )
            smtp.quit()
        except Exception as exc:
            print("[ MAIL_SENDER ] an error occured!", repr(exc))

    async def send_new_password_mail(self, account: _nooble_database_objects.AccountObject, new_password: str) -> None:
        html_content = self._templates.get_send_password_mail_template(account, new_password)
        _asyncio.create_task(self.send_email(account, "Votre nouveau mot de passe", html_content))

    async def send_edited_address_mail(self, account: _nooble_database_objects.AccountObject, new_mail: str, admin: _nooble_database_objects.AccountObject) -> None:
        html_content = self._templates.get_edited_address_mail_template(account, admin, new_mail)
        _asyncio.create_task(self.send_email(account, "Votre adresse mail a été modifiée", html_content))

    async def send_edited_role_mail(self, account: _nooble_database_objects.AccountObject, admin: _nooble_database_objects.AccountObject) -> None:
        html_content = self._templates.get_edited_role_mail_template(account, admin)
        _asyncio.create_task(self.send_email(account, "Votre rôle a été modifié", html_content))

    async def send_edited_profile_mail(self, account: _nooble_database_objects.AccountObject, admin: _nooble_database_objects.AccountObject) -> None:
        html_content = self._templates.get_edited_profile_mail_template(account, admin)
        _asyncio.create_task(self.send_email(account, "Votre profil a été modifié", html_content))

    async def send_edited_class_mail(self, account: _nooble_database_objects.AccountObject, nooble_class: _nooble_database_objects.ClassObject, admin: _nooble_database_objects.AccountObject) -> None:
        html_content = self._templates.get_edited_class_mail_template(account, nooble_class, admin)
        _asyncio.create_task(self.send_email(account, "Votre cours a été modifié", html_content))

    
