import quart.wrappers as _quart_wrappers

import nooble_database.objects.file_types as _nooble_database_file_types

from ...configuration import NoobleEndpointConfiguration
from ...templates.nooble_action import NoobleEndpointAction

class GetSelfFilesAction(NoobleEndpointAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        args = await self.get_request_args(request)

        if "type" in args:
            try:
                _nooble_database_file_types.FileType.from_raw_filetype(args["type"])
            except ValueError:
                return False

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return await self.get_account(request, configuration) is not None

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        args = await self.get_request_args(request)

        if "type" in args:
            files_type = args["type"]
        else:
            files_type = None

        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        files = await configuration.get_database().get_files().get_sender_files(account.get_id(), files_type)

        files_result = []

        for file in files:
            file_object = await file.ensure_object()
            
            files_result.append(
                {
                    "id": file.get_id(),
                    "name": file_object["name"],
                    "filename": file_object["filename"],
                    "sent_date": file_object["sent_date"],
                    "sender": file_object["sender"],
                    "size": file_object["size"],
                    "filetype": file_object["filetype"]
                }
            )
        
        return await self.make_response(
            files_result,
            configuration
        )


