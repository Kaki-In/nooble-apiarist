import nooble_database.database as _nooble_database
import nooble_resources_manager as _nooble_resources_manager
import nooble_database.objects as _nooble_database_objects
import nooble_conf.files as _nooble_conf_files

from ..templates import NoobleActivity

import json as _json
import typing as _T

class HomeworkActivity(NoobleActivity):
    def __init__(self) -> None:
        super().__init__("homework")

    def create_empty_file(self) -> bytes:
        return _json.dumps([]).encode()
    
    def get_css(self, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        return """

div.homework-giveback {
    position: relative;
    border: 1px solid grey;
    padding: clamp(10px, 4vw, 20px);
    border-radius: 4px;
    margin: 10px 0;
    max-width: 100%;
}

ul.homework-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    list-style: none;
    padding: 0;
    margin: 0;
}

ul.homework-list li.homework {
    position: relative;
    padding: 15px;
    background: #ececec;
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    min-height: 120px;
}

div.homework-edit {
    position: relative;
    border: 2px dashed #dbdbdb;
    border-radius: 10px;
    padding: clamp(20px, 6vw, 40px);
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #fafafa;
    text-align: center;
}

.homework-file-input {
    margin: 10px 0;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
    max-width: 300px;
    box-sizing: border-box;
}

.homework-button {
    padding: clamp(8px, 2vw, 12px) clamp(16px, 4vw, 20px);
    margin: 5px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: clamp(12px, 3vw, 14px);
    width: 100%;
    max-width: 200px;
    touch-action: manipulation;
}

.homework-button.upload {
    background: #4CAF50;
    color: white;
}

.homework-button.remove {
    background: #f44336;
    color: white;
}

.homework-button:hover {
    opacity: 0.8;
}

.homework-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.homework-student-name {
    font-weight: bold;
    margin-bottom: 10px;
    font-size: clamp(14px, 3.5vw, 16px);
    text-align: center;
    word-wrap: break-word;
}

.homework-filename {
    font-style: italic;
    color: #666;
    margin-top: 5px;
    font-size: clamp(12px, 3vw, 14px);
    text-align: center;
    word-wrap: break-word;
    max-width: 100%;
}

.homework-download-link {
    color: #2196F3;
    text-decoration: none;
    cursor: pointer;
    padding: 8px 12px;
    border-radius: 4px;
    margin-top: 10px;
    touch-action: manipulation;
    font-size: clamp(12px, 3vw, 14px);
}

.homework-download-link:hover {
    text-decoration: underline;
    background: rgba(33, 150, 243, 0.1);
}

/* Media queries pour les très petits écrans */
@media (max-width: 480px) {
    ul.homework-list {
        grid-template-columns: 1fr;
    }
    
    div.homework-edit {
        padding: 15px;
    }
    
    .homework-file-input {
        font-size: 16px; /* Évite le zoom sur iOS */
    }
}

/* Media queries pour les écrans moyens */
@media (min-width: 481px) and (max-width: 768px) {
    ul.homework-list {
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }
}

"""

    async def get_javascript(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        return """

class Activity {
    constructor(id, args) {
        this._activity_id = id;
        this._activity_args = args;
    }

    onRender(div) {
        if (this._activity_args.is_student) {
            this.onRenderStudent(div);
        } else {
            this.onRenderTeacher(div);
        }
    }

    onRenderStudent(div) {
        div.className = 'homework-giveback';
        
        const editDiv = document.createElement('div');
        editDiv.className = 'homework-edit';
        
        if (this._activity_args.has_given_file) {
            const currentFile = this._activity_args.has_given_file;
            
            const title = document.createElement('h3');
            title.textContent = 'Votre devoir rendu';
            editDiv.appendChild(title);
            
            const filename = document.createElement('a');
            filename.href = `""" + self.get_download_url("${this._activity_args.has_given_file.file_id}", configuration) + """`;
            console.log(filename.href);
            filename.className = 'homework-filename';
            filename.textContent = currentFile.name || 'Fichier sans nom';
            editDiv.appendChild(filename);
            
            const removeBtn = document.createElement('button');
            removeBtn.className = 'homework-button remove';
            removeBtn.textContent = 'Retirer le devoir';
            removeBtn.onclick = () => this.removeHomework(editDiv);
            editDiv.appendChild(removeBtn);
            
        } else {
            const title = document.createElement('h3');
            title.textContent = 'Déposer un devoir';
            editDiv.appendChild(title);
            
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.className = 'homework-file-input';
            editDiv.appendChild(fileInput);
            
            const nameInput = document.createElement('input');
            nameInput.type = 'text';
            nameInput.placeholder = 'Nom du devoir (optionnel)';
            nameInput.className = 'homework-file-input';
            editDiv.appendChild(nameInput);
            
            const uploadBtn = document.createElement('button');
            uploadBtn.className = 'homework-button upload';
            uploadBtn.textContent = 'Uploader le devoir';
            uploadBtn.onclick = () => this.uploadHomework(fileInput, nameInput, editDiv);
            editDiv.appendChild(uploadBtn);
        }
        
        div.appendChild(editDiv);
    }

    onRenderTeacher(div) {
        div.className = 'homework-giveback';
        
        const title = document.createElement('h2');
        title.textContent = 'Devoirs rendus';
        div.appendChild(title);
        
        this.loadHomeworkList(div);
    }

    async uploadHomework(fileInput, nameInput, containerDiv) {
        if (!fileInput.files[0]) {
            alert('Veuillez sélectionner un fichier');
            return;
        }
        
        const formData = new FormData();
        formData.append('file-content', fileInput.files[0]);
        formData.append('name', nameInput.value || fileInput.files[0].name);
        formData.append('activity_id', this._activity_id);
        
        try {
            const response = await fetch(`""" + self.get_resource_url("upload", configuration) + """`, {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });
            
            if (response.ok) {
                const result = await response.json();
                alert('Devoir uploadé avec succès!');
                this._activity_args.has_given_file = { name: nameInput.value || fileInput.files[0].name, file_id: result };
                this.refreshStudentView(containerDiv.parentElement);
            } else {
                alert('Erreur lors de l\\'upload du devoir');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur de connexion');
        }
    }

    async removeHomework(containerDiv) {
        if (!confirm('Êtes-vous sûr de vouloir retirer votre devoir?')) {
            return;
        }
        
        try {
            const response = await fetch(`""" + self.get_resource_url("remove", configuration) + """`, {
                method: 'POST',
                body: JSON.stringify({
                    activity_id: this._activity_id
                }),
                credentials: 'include'
            });
            
            if (response.ok) {
                alert('Devoir retiré avec succès!');
                this._activity_args.has_given_file = null;
                this.refreshStudentView(containerDiv.parentElement);
            } else {
                alert('Erreur lors de la suppression du devoir');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur de connexion');
        }
    }

    async loadHomeworkList(containerDiv) {
        const listContainer = document.createElement('ul');
        listContainer.className = 'homework-list';
        
        const homeworkList = this._activity_args.homework_list || [];
        
        if (homeworkList.length === 0) {
            const noHomework = document.createElement('p');
            noHomework.textContent = 'Aucun devoir rendu pour le moment.';
            containerDiv.appendChild(noHomework);
            return;
        }
        
        homeworkList.forEach(homework => {
            const listItem = document.createElement('li');
            listItem.className = 'homework';
            
            const studentName = document.createElement('div');
            studentName.className = 'homework-student-name';
            studentName.textContent = homework.student_name || 'Étudiant inconnu';
            listItem.appendChild(studentName);
            
            const fileName = document.createElement('div');
            fileName.className = 'homework-filename';
            fileName.textContent = homework.name || 'Fichier sans nom';
            listItem.appendChild(fileName);
            
            const downloadLink = document.createElement('a');
            downloadLink.className = 'homework-download-link';
            downloadLink.textContent = 'Télécharger';
            downloadLink.href = `""" + self.get_download_url("${homework.file_id}", configuration) + """`;
            listItem.appendChild(downloadLink);
            
            listContainer.appendChild(listItem);
        });
        
        containerDiv.appendChild(listContainer);
    }

    refreshStudentView(div) {
        for (let child of div.children)
        {
            if (child.tagName.toUpperCase() !== 'STYLE')
            div.removeChild(child);
        }
        
        this.onRenderStudent(div);
    }
}
"""

    async def get_editable_javascript(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        return """

class Activity {
    constructor(id, args) {
        this._activity_id = id;
        this._activity_args = args;
    }

    onRender(div) {
        div.className = 'homework-giveback';
        
        const editDiv = document.createElement('div');
        editDiv.className = 'homework-edit';
        editDiv.style.minHeight = '100px';
        editDiv.style.textAlign = 'center';
        
        const title = document.createElement('h3');
        title.textContent = 'Activité de dépôt de devoirs';
        title.style.margin = '0 0 15px 0';
        title.style.color = '#333';
        editDiv.appendChild(title);
        
        const description = document.createElement('p');
        description.textContent = 'Les étudiants pourront déposer leurs devoirs ici. Vous pourrez consulter et télécharger les devoirs une fois le cours publié.';
        description.style.color = '#666';
        description.style.fontSize = '14px';
        description.style.lineHeight = '1.4';
        description.style.margin = '0 0 15px 0';
        editDiv.appendChild(description);
        
        if (this._activity_args.homework_count !== undefined) {
            const stats = document.createElement('div');
            stats.style.padding = '10px';
            stats.style.background = '#f0f8ff';
            stats.style.borderRadius = '4px';
            stats.style.fontSize = '13px';
            stats.style.color = '#2c5aa0';
            
            const count = this._activity_args.homework_count || 0;
            stats.textContent = `${count} devoir${count > 1 ? 's' : ''} déjà déposé${count > 1 ? 's' : ''}`;
            
            editDiv.appendChild(stats);
        }
        
        div.appendChild(editDiv);
    }
}"""

    async def get_arguments(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> _T.Any:
        file_data = _json.loads(file)

        if await account.get_role() == _nooble_database_objects.Role.STUDENT:
            given = None
            
            for homework in file_data:
                if homework['sender_id'] == account.get_id():
                    given = homework
            
            if given:

                file_id = given["file_id"]
                homework_file = await database.get_files().get_file(file_id).ensure_object()

                args = {
                    "is_student": True,
                    "has_given_file": {
                        "name": homework_file["name"],
                        "file_id": file_id
                    }
                }
                

            else:
                args = {
                    "is_student": True,
                    "has_given_file": None
                }
                
            
        else:
            args = {
                "is_student": False,
                "homework_list": []
            }

            for homework in file_data:
                homework_file = await database.get_files().get_file(homework["file_id"]).ensure_object()
                
                try :
                    student = (await database.get_accounts().get_account(homework["sender_id"]).ensure_object())["profile"]
                except:
                    student = {
                        'first_name': "Deleted",
                        'last_name': "User"
                    }

                args["homework_list"].append({
                    "student_name": student["first_name"] + " " + student["last_name"],
                    "name": homework_file["name"],
                    "file_id": homework_file['_id']
                })
        
        return args

    async def get_used_files(self, file: bytes, database: _nooble_database.NoobleDatabase) -> list[str]:
        data = _json.loads(file)

        files = []

        for homework in data:
            files.append(homework['file_id'])

        return files



