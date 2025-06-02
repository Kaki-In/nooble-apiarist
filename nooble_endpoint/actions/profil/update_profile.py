import quart.wrappers as _quart_wrappers
import nooble_database.objects.file_types as _nooble_database_types

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class UpdateProfileAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if not (
            "first_name" in args 
        and "last_name" in args
        and "active_badges" in args
        and "active_decoration" in args
        and "description" in args
        and "profile_image" in args
        ):
            return False
        
        if not (
            type(args["first_name"]) is str
        and type(args["last_name"]) is str
        and type(args["active_decoration"]) is int
        and type(args["profile_image"]) is int
        and type(args["active_badges"]) is list
        and type(args["description"]) is dict
        ):
            return False
        
        for badge in args['active_badges']:
            if type(badge) is not int:
                return False
            
        # TODO: ensure description sections are valid

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
        
        args = await self.get_request_args(request)
        
        safe = await account.get_safe().get_object()

        badges: list[int] = args["active_badges"]

        for badge in badges:
            if not badge in safe["badges"]:
                return False
        
        decoration: int = args["active_decoration"]

        if not decoration in safe["decorations"]:
            return False
        
        file_image = configuration.get_database().get_files().get_file(args["profile_image"])

        if account.get_id() != await file_image.get_sender_id():
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        first_name: str = args["first_name"]
        last_name: str = args["last_name"]
        active_decoration:str = args["active_decoration"]
        active_badges: list[int] = args["active_badges"]
        description: dict = args["description"]
        profile_image: int = args["profile_image"]

        account = await self.get_account(request, configuration)

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

        return await self.make_response(None, configuration)
