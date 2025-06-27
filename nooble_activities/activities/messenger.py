import nooble_database.database as _nooble_database
import nooble_resources_manager as _nooble_resources_manager
import nooble_database.objects as _nooble_database_objects
import nooble_conf.files as _nooble_conf_files

from ..templates import NoobleActivity

import json as _json
import typing as _T
import time

class MessengerActivity(NoobleActivity):
    def __init__(self) -> None:
        super().__init__("messenger")

    def create_empty_file(self) -> bytes:
        return _json.dumps({
            "messages": []
        }).encode()
    
    def get_css(self, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        return """
.messenger-container {
    display: flex;
    flex-direction: column;
    height: 400px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.messenger-messages {
    display: flex;
    flex-direction: column;
    align-items: start;

    flex: 1;
    padding: 15px;
    overflow-y: auto;
    background: #f9f9f9;
}

.message-item {
    display: flex;
    margin-bottom: 15px;
    align-items: flex-start;
    max-width: 40%;
    background: lightgrey;
    border-radius: 5px;
    padding: 20px;
}

.message-item.self-message {
    flex-direction: row-reverse;
    justify-content: end;
    text-align: right;
    align-self: end;
    background: #93d575;
}

.message-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin: 10px;
    flex-shrink: 0;
}

.message-content {
    flex: 1;
}

.message-header {
    display: flex;
    align-items: center;
    margin-bottom: 4px;
}

.message-author {
    font-weight: 600;
    color: #333;
    font-size: 14px;
    margin-right: 8px;
}

.message-time {
    font-size: 12px;
    color: #888;
}

.message-text {
    color: #555;
    font-size: 14px;
    line-height: 1.4;
    word-wrap: break-word;
}

.messenger-input {
    border-top: 1px solid #ddd;
    padding: 15px;
    background: white;
    border-radius: 0 0 8px 8px;
}

.messenger-form {
    display: flex;
    gap: 10px;
}

.messenger-form input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 20px;
    outline: none;
    font-size: 14px;
}

.messenger-form input:focus {
    border-color: #4a90e2;
}

.messenger-form button {
    padding: 10px 20px;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
}

.messenger-form button:hover {
    background: #357abd;
}

.messenger-form button:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.messenger-messages::-webkit-scrollbar {
    width: 6px;
}

.messenger-messages::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.messenger-messages::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
}

.messenger-messages::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
"""

    async def get_javascript(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        return """
class Activity
{
    constructor(id, args)
    {
        this.id = id;
        this.args = args;
        this.refreshInterval = null;
        this.lastMessageCount = 0;
    }

    onRender(div)
    {
        let innerDiv = document.createElement("div");
        innerDiv.innerHTML = `
            <div class="messenger-container">
                <div class="messenger-messages" id="messages">
                </div>
                <div class="messenger-input">
                    <form class="messenger-form" id="form">
                        <input type="text" id="input" placeholder="Tapez votre message..." maxlength="500" required>
                        <button type="submit" id="submit-button">Envoyer</button>
                    </form>
                </div>
            </div>
        `;

        div.appendChild(innerDiv.children[0]);

        this.setupEventListeners(div);
        this.loadMessages(div);
        this.startRefresh(div);
    }

    setupEventListeners(div)
    {
        const form = div.querySelector(`#form`);
        const input = div.querySelector(`#input`);

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage(div);
        });

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage(div);
            }
        });
    }

    async sendMessage(div)
    {
        const input = div.querySelector(`#input`);
        const button = div.querySelector(`#submit-button`);
        const message = input.value.trim();

        if (!message) return;

        button.disabled = true;
        input.disabled = true;

        try {
            const response = await fetch('""" + self.get_resource_url("send", configuration) + """', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    activity_id: this.id,
                    message: message
                }),
                credentials: 'include'
            });

            if (response.ok) {
                input.value = '';
                this.loadMessages(div);
            } else {
                console.error('Erreur lors de l\\'envoi du message');
            }
        } catch (error) {
            console.error('Erreur réseau:', error);
        } finally {
            button.disabled = false;
            input.disabled = false;
            input.focus();
        }
    }

    async loadMessages(div)
    {
        try {
            const response = await fetch(`""" + self.get_resource_url("get-messages", configuration) + """?activity_id=${this.id}`, {credentials: 'include'});
            if (response.ok) {
                const data = await response.json();
                this.displayMessages(div, data.messages || []);
            }
        } catch (error) {
            console.error('Erreur lors du chargement des messages:', error);
        }
    }

    displayMessages(div, messages)
    {
        const container = div.querySelector(`#messages`);
        const shouldScrollToBottom = container.scrollTop + container.clientHeight >= container.scrollHeight - 10;
        
        container.innerHTML = '';

        messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message-item';

            if (message.user_id === this.args.user_id)
            {
                messageDiv.classList.add("self-message");
            }

            const avatarImg = document.createElement('img');
            avatarImg.className = 'message-avatar';
            avatarImg.src = `""" + self.get_profile_image_url("${message.user_avatar_id}", configuration) + """`;
            avatarImg.alt = message.user_name;
            avatarImg.onerror = function() {
                this.src = '/images/icons/user.png';
            };

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';

            const headerDiv = document.createElement('div');
            headerDiv.className = 'message-header';

            const authorSpan = document.createElement('span');
            authorSpan.className = 'message-author';
            authorSpan.textContent = message.user_name;

            const timeSpan = document.createElement('span');
            timeSpan.className = 'message-time';
            timeSpan.textContent = this.formatTime(message.timestamp);

            const textDiv = document.createElement('div');
            textDiv.className = 'message-text';
            textDiv.textContent = message.content;

            headerDiv.appendChild(authorSpan);
            headerDiv.appendChild(timeSpan);
            contentDiv.appendChild(headerDiv);
            contentDiv.appendChild(textDiv);
            messageDiv.appendChild(avatarImg);
            messageDiv.appendChild(contentDiv);

            container.appendChild(messageDiv);
        });

        if (shouldScrollToBottom || messages.length !== this.lastMessageCount) {
            container.scrollTop = container.scrollHeight;
        }
        
        this.lastMessageCount = messages.length;
    }

    formatTime(timestamp)
    {
        const date = new Date(timestamp * 1000);
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const messageDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());

        if (messageDate.getTime() === today.getTime()) {
            return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
        } else {
            return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' }) + 
                   ' ' + date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
        }
    }

    startRefresh(div)
    {
        this.refreshInterval = setInterval(() => {
            // Vérifier si le div est toujours dans le DOM
            const container = div.querySelector(`#messages`);
            if (!container || !document.body.contains(container)) {
                // L'activité a été détruite, arrêter le rafraîchissement
                clearInterval(this.refreshInterval);
                return;
            }
            this.loadMessages(div);
        }, 5000); // Rafraîchissement toutes les 5 secondes
    }
}
"""

    async def get_editable_javascript(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> str:
        return """
class Activity
{
    constructor(id, args)
    {
        this.id = id;
        this.args = args;
    }

    onRender(div)
    {
        div.innerHTML = `
            <div class="messenger-container">
                <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #888; font-style: italic;">
                    <div style="text-align: center;">
                        <div>La messagerie n'est pas disponible en mode édition</div>
                    </div>
                </div>
            </div>
        `;
    }
}
"""

    async def get_arguments(self, file: bytes, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount, configuration: _nooble_conf_files.NoobleBindingSettings) -> _T.Any:
        return {
            "user_id": account.get_id()
        }

    async def get_used_files(self, file: bytes, database: _nooble_database.NoobleDatabase) -> list[str]:
        return []