from .get_messages import GetMessagesActivityAction
from .send_message import SendMessageActivityAction

from ....templates.nooble_activity_pack import NoobleActivityActionsPack


class NoobleMessengerActivityPack(NoobleActivityActionsPack):
    def __init__(self) -> None:
        super().__init__("messenger")

        self.add_action("get-messages", GetMessagesActivityAction("messenger"), 'GET')
        self.add_action("send", SendMessageActivityAction("messenger"), 'POST')

    

