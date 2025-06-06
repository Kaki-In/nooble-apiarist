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
    
    async def get_html(self, file:bytes, database: _nooble_database.NoobleDatabase, account:_nooble_database.NoobleAccount) -> str:
        account_role = await account.get_role()

        data = _json.loads(file)

        if account_role == _nooble_database_objects.Role.STUDENT:
            given_file = None
            student_homework = None

            for homework in data['homework']:
                if account.get_id() == homework['sender_id']:
                    given_file = await database.get_files().get_file(homework['file_id']).ensure_object()
                    student_homework = homework
            
            if given_file is not None and student_homework is not None:
                return f"""
<h2> Rendre un devoir </h2>
<div id="homework-giveback">
    <span>Devoir rendu</span>
    <a href='{self.get_file_url(student_homework["file_id"])}' target='_blank'>
        {given_file['filename']}
    </a>
    <button id="delete-button">Supprimer le devoir</button>
</div>
"""
            else:

                return """
<h2> Rendre un devoir </h2>
<div id="homework-giveback">
    <input type="file" id="homework-file">
    </input>
</div>
"""
        else:
            result = """
<h2>Devoirs rendus</h2>
<ul class='homework-list'>
"""
            for homework in data['homework']:
                sender = database.get_accounts().get_account(homework['sender_id'])

                if await sender.exists():
                    profile = await sender.get_profile().ensure_object()
                    sender_name = profile['last_name'] + ' ' + profile['first_name']
                else:
                    sender_name = "Unknown Student"
                
                student_file = await database.get_files().get_file(homework['file_id']).get_object()
                
                result += f"""
    <li class='homework'>
        <span class='homework_student'>
            {sender_name}
        </span>
        <a href='{self.get_file_url(homework["file_id"])}&type=section file' target='_blank'>
            {student_file['filename']}
        </a>
    </li>
"""
            result += """
</ul>"""

            return result
        
    async def get_editable_html(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> str:
        return """
<h2> Rendre un devoir </h2>
<div class='homework-edit'>
    <span>
        Rien à éditer ici
    </span>
</div>
"""

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
        return {
            "student": await account.get_role() == _nooble_database_objects.Role.STUDENT
        }

    async def get_used_files(self, file: bytes, database: _nooble_database.NoobleDatabase) -> list[str]:
        data = _json.loads(file)

        files = []

        for homework in data:
            files.append(homework['file_id'])

        return files



