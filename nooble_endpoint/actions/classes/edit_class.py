import quart.wrappers as _quart_wrappers

import nooble_database.objects as _nooble_database_objects
import datetime as _datetime

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class EditClassAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "id" in args
        and "title" in args
        and "description" in args
        and "content" in args
        ):
            return False
        
        if not (
            type(args["id"]) is str
        and type(args["title"]) is str
        and type(args["description"]) is str
        ):
            return False
        
        try:
            wrapped_section = configuration.get_sections().export(args["content"])

            if not wrapped_section.is_valid(configuration.get_database()):
                return False

        except Exception as exc:
            return False
        
        nooble_class = configuration.get_database().get_classes().get_class(args["id"])

        if not await nooble_class.exists():
            return False
        
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False

        role = await account.get_role()

        if role.is_admin():
            return True
        
        elif role.is_teacher():
            args = await self.get_request_args(request)

            nooble_class = configuration.get_database().get_classes().get_class(args["id"])

            return account.get_id() in await nooble_class.get_accounts_ids()
        
        return False

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)

        args = await self.get_request_args(request)

        nooble_class = configuration.get_database().get_classes().get_class(args["id"])

        previous_class_content = configuration.get_sections().export(await nooble_class.get_content())
        actual_used_files = await previous_class_content.get_recursive_used_files(configuration.get_database())

        title:str = args["title"]
        description:str = args["description"]
        content:_nooble_database_objects.SectionObject = args["content"]

        ensured_content = configuration.get_sections().export(content)
        new_used_files = await ensured_content.get_recursive_used_files(configuration.get_database())

        for file_id in actual_used_files:
            if not file_id in new_used_files:
                file = configuration.get_database().get_files().get_file(file_id)

                configuration.get_resources().get_file(await file.get_filepath()).destroy()
                await file.destroy()

        await nooble_class.update(
            {
                "$set": {
                    "name": title,
                    "description": description,
                    "last_modification": _datetime.datetime.now().timestamp(),
                    "last_modifier": account.get_id(),
                    "content": await ensured_content.export_to_database_json_data(configuration.get_database())
                }
            }
        )

        class_accounts = await nooble_class.get_accounts_ids()

        if not account.get_id() in class_accounts:
            for teacher_id in class_accounts:
                teacher_object = await configuration.get_database().get_accounts().get_account(teacher_id).get_object()

                if teacher_object["role"] in "student":
                    continue

                await configuration.get_mail_service().send_edited_class_mail(teacher_object, await nooble_class.ensure_object(), await account.get_object())


        return await self.make_response(None, configuration)



