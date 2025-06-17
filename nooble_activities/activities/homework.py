import nooble_database.database as _nooble_database
import nooble_resources_manager as _nooble_resources_manager
import nooble_database.objects as _nooble_database_objects

from ..templates import NoobleActivity

import json as _json
import typing as _T

class HomeworkActivity(NoobleActivity):
    def __init__(self) -> None:
        super().__init__("homework")

    def create_empty_file(self) -> bytes:
        return _json.dumps([]).encode()
    
    def get_css(self) -> str:
        return """

div.homework-giveback {
    position: relative;
    border: 1px solid grey;
    padding: 20ps;
    border_radius: 4px;
}

ul.homework-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}

ul.homework-list li.homework {
    position: relative;
    margin: 5px;
    padding: 5px;
    background: #ececec;

    display: flex;
    flex-direction: column;
    align-items: center;

    width: 200px;
}

div.homework-edit {
    position: relative;

    border: 2px dashed #dbdbdb;
    border-radius: 10px;
    padding: 40px;

    display: flex;
    flex-direction: column;
    align-items: center;
}

"""

    async def get_javascript(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> str:
        return """

class Activity // the Activity name is mandatory
{
    constructor(id, args) // id is the id of the activity, and args the json args given to the activity
    {
        // construction of the actvitiy
    }

    onRender(div)
    {
        // what to do when rendering the div
    }
}

"""

    async def get_editable_javascript(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> str:
        return """

class Activity // the Activity name is mandatory
{
    constructor(id, args) // id is the id of the activity, and args the json args given to the activity
    {
        // construction of the actvitiy
    }

    onRender(div)
    {
        // what to do when rendering the div
    }
}

"""

    async def get_arguments(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> _T.Any:
        file_data = _json.loads(file)

        given = None

        for homework in file_data:
            if homework['sender_id'] == account.get_id():
                given = homework

        return {
            "is_student": await account.get_role() == _nooble_database_objects.Role.STUDENT,
            "has_given_file": given
        }

    async def get_used_files(self, file: bytes, database: _nooble_database.NoobleDatabase) -> list[str]:
        data = _json.loads(file)

        files = []

        for homework in data:
            files.append(homework['file_id'])

        return files



