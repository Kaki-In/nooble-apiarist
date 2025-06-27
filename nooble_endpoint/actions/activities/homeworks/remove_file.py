import quart.wrappers as _quart_wrappers
import nooble_database.objects as _nooble_database_objects
import json as _json

from ....configuration import NoobleEndpointConfiguration
from ....templates.nooble_activity_action import NoobleEndpointActivityAction

class DeleteHomeworkFileActivityAction(NoobleEndpointActivityAction):
    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        file_result = await self.get_activity_file(configuration, request)

        if file_result is None:
            return False

        account = await self.get_account(request, configuration)

        if account is None:
            return True # non-allowed request
        
        file_data = _json.loads(file_result[1])

        gave_back_homework = False
        for homework in file_data:
            if homework['sender_id'] == account.get_id():
                gave_back_homework = True

        if not gave_back_homework:
            return False

        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        account = await self.get_account(request, configuration)

        if account is None:
            return False
        
        if not await account.get_role() == _nooble_database_objects.Role.STUDENT:
            return False
        
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        account = await self.get_account(request, configuration)

        if account is None:
            return await self.make_response(None, configuration, 500)
        
        activity_files = await self.get_activity_file(configuration, request)

        if activity_files is None:
            return await self.make_response(None, configuration, 500)

        file_data = _json.loads(activity_files[1])

        for homework_index in range(len(file_data)):
            homework = file_data[homework_index]
            if homework['sender_id'] == account.get_id():
                file_id = homework['file_id']

                file = configuration.get_database().get_files().get_file(file_id)

                configuration.get_resources().get_file(await file.get_filepath()).destroy()
                await file.destroy()

                file_data.pop(homework_index)

                break
        
        await account.get_safe().decrease(110)

        await self.overwrite_savefile(_json.dumps(file_data).encode(), configuration, request)

        return await self.make_response(None, configuration)
            


