from .remove_file import DeleteHomeworkFileActivityAction
from .upload_file import UploadHomeworkFileActivityAction

from ....templates.nooble_activity_pack import NoobleActivityActionsPack


class NoobleHomeworkActivityPack(NoobleActivityActionsPack):
    def __init__(self) -> None:
        super().__init__("homework")

        self.add_action("upload", UploadHomeworkFileActivityAction("homework"), 'POST')
        self.add_action("remove", DeleteHomeworkFileActivityAction("homework"), 'POST')

    

