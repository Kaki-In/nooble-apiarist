import quart.wrappers as _quart_wrappers
import nooble_database.objects.file_types as _nooble_database_types
import nooble_database.objects.roles as _nooble_database_roles

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class ModifyProfileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "user_id" in args
        and "first_name" in args 
        and "last_name" in args
        and "active_badges" in args
        and "active_decoration" in args
        and "description" in args
        and "profile_image" in args
        ):
            return False
        
        if not (
            type(args["user_id"]) is str
        and type(args["first_name"]) is str
        and type(args["last_name"]) is str
        and type(args["active_decoration"]) is str
        and type(args["profile_image"]) is str
        and type(args["active_badges"]) is list
        and type(args["description"]) is str
        ):
            return False
        
        account = configuration.get_database().get_accounts().get_account(args["user_id"])

        if not await account.exists():
            return False

        for badge in args['active_badges']:
            if type(badge) is not str:
                return False
            
            pass
            
        file_image = configuration.get_database().get_files().get_file(args["profile_image"])
        
        if not await file_image.exists():
            return False
        
        if not await file_image.get_filetype() != _nooble_database_types.FileType.PROFILE_ICON:
            return False

        return True
    
    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        if not await account.get_role() in [_nooble_database_roles.Role.ADMIN, _nooble_database_roles.Role.ADMIN_TEACHER]:
            return False
        
        args = await self.get_request_args(request)

        if account.get_id() == args["user_id"]:
            return False
        
        return True


    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        self_account = await self.get_account(request, configuration)

        if self_account is None:
            return await self.make_response(None, configuration, 500)

        args = await self.get_request_args(request)

        user_id: str = args["user_id"]
        first_name: str = args["first_name"]
        last_name: str = args["last_name"]
        active_decoration: str = args["active_decoration"]
        active_badges: list[str] = args["active_badges"]
        description: str = args["description"]
        profile_image: str = args["profile_image"]

        account = configuration.get_database().get_accounts().get_account(user_id)

        if not await account.exists():
            return False

        if account is None:
            return await self.make_response(None, configuration, 500) # should not be the case
        
        await account.update({
            "$set": {
                "profile": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "active_decorations": active_decoration,
                    "active_badges": active_badges,
                    "description": description,
                    "profile_image": profile_image
                }
            }
        })

        await configuration.get_mail_service().send_edited_profile_mail(await account.ensure_object(), await self_account.ensure_object())

        await configuration.get_notifier().notify_profile_edit(account, self_account)

        return await self.make_response(None, configuration)
