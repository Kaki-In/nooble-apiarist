#!/usr/bin/python3.11

from nooble_conf.main_configuration import MAIN_CONFIGURATION
from nooble_database.database import NoobleDatabase
from nooble_mail_service.mail_sender import NoobleMailSender

from nooble_database.objects import *

import sys
import asyncio

import pip

async def main(args):
    mail_configuration = MAIN_CONFIGURATION.get_mail_settings()
    mail_templates = MAIN_CONFIGURATION.get_templates().get_mail_templates()

    mail_sender = NoobleMailSender(mail_configuration, mail_templates)

    account: AccountObject = {
        "_id": -1,
        "activities": [],
        "mail": "kaki@mifamofi.net",
        "password": "undefined",
        "profile": {
            "active_badges": [],
            "active_decoration": 1,
            "description": {
                "data": None,
                "type": "none",
                "uses_files": []
            },
            "first_name": "Kaki",
            "last_name": "in",
            "profile_image": 2
        },
        "role": "admin",
        "safe": {
            "badges": [],
            "decorations": [],
            "quota": 12
        },
        "creation_date": 10
    }

    await mail_sender.send_new_password_mail(account, "azgrobul")

if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv)))
    