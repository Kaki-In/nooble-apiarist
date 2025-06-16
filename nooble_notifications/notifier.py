import nooble_database.database as _nooble_database
import nooble_database.objects as _nooble_database_objects
import datetime as _datetime
import bson as _bson

class NoobleAccountsNotifier():
    def __init__(self, database: _nooble_database.NoobleDatabase) -> None:
        self._database = database

    async def notify(self, icon:str, title:str, message:str, creator: str, people: list[str]) -> None:
        activity = await self._database.get_activities().create_activity(title, message, creator, _datetime.datetime.now(), icon)

        await self._database.get_accounts().update(
            {
                "_id":
                {
                    "$in": [
                        _bson.ObjectId(account) for account in people
                    ]
                }
            },
            {
                "$push": {
                    "activities": {
                        "activity": activity.get_id(),
                        "read": False
                    }
                }
            }
        )
    
    async def notify_class_edit(self, nooble_class: _nooble_database.NoobleClass, editor: _nooble_database.NoobleAccount) -> None:
        class_object = await nooble_class.get_object()
        editor_object = await editor.get_object()

        class_accounts = [self._database.get_accounts().get_account(account_id) for account_id in class_object['accounts']]

        await self.notify(
            "class",
            f"{editor_object['profile']['first_name']} {editor_object['profile']['last_name']} a modifié votre cours",
            f"Votre cours {class_object['name']} vient d'être modifié par {editor_object['profile']['first_name']} {editor_object['profile']['last_name']}. ",
            editor.get_id(),
            [account.get_id() for account in class_accounts if (await account.get_role()).is_teacher()]
        )

    async def notify_profile_edit(self, profiled_account: _nooble_database.NoobleAccount, editor: _nooble_database.NoobleAccount) -> None:
        editor_object = await editor.get_object()

        await self.notify(
            "account",
            f"{editor_object['profile']['first_name']} {editor_object['profile']['last_name']} a modifié votre profil",
            f"{editor_object['profile']['first_name']} {editor_object['profile']['last_name']} vient d'apporter des modifications à votre profil. Merci de votre compréhension",
            editor.get_id(),
            [profiled_account.get_id()]
        )

    async def notify_mail_address_changed(self, last:str, new:str, changed_account: _nooble_database.NoobleAccount, editor: _nooble_database.NoobleAccount) -> None:
        editor_object = await editor.get_object()

        await self.notify(
            "account",
            f"{editor_object['profile']['first_name']} {editor_object['profile']['last_name']} a modifié votre adresse mail",
            f"Votre adresse mail, anciennement {last}, a été définie comme {new} par {editor_object['profile']['first_name']} {editor_object['profile']['last_name']}. N'hésitez pas à intervenir si vous pensez que c'est une erreur",
            editor.get_id(),
            [changed_account.get_id()]
        )

    async def notify_role_changed(self, new_role: _nooble_database_objects.Role, changed_account: _nooble_database.NoobleAccount, editor: _nooble_database.NoobleAccount) -> None:
        editor_object = await editor.get_object()

        if new_role == _nooble_database_objects.Role.ADMIN:
            role_name = "administrateur"
        elif new_role == _nooble_database_objects.Role.ADMIN_TEACHER:
            role_name = "enseignant administrateur"
        elif new_role == _nooble_database_objects.Role.STUDENT:
            role_name = "étudiant"
        elif new_role == _nooble_database_objects.Role.TEACHER:
            role_name = "enseignant"
        else:
            raise ValueError("invalid role given. Where did you find it exactly?")

        await self.notify(
            "role",
            f"{editor_object['profile']['first_name']} {editor_object['profile']['last_name']} a modifié vos privilèges",
            f"Vous êtes maintenant {role_name}. N'hésitez pas à intervenir si vous pensez que c'est une erreur",
            editor.get_id(),
            [changed_account.get_id()]
        )


