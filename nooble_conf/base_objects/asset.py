import os as _os

class NoobleSettingsAsset():
    def __init__(self, path:str, default_content: bytes) -> None:
        self._path = path

        if not _os.path.exists(path):
            self.overwrite(default_content)

    def get_content(self) -> bytes:
        a = open(self._path, "rb")
        data = a.read()
        a.close()

        return data
    
    def overwrite(self, content: bytes) -> None:
        a = open(self._path, "wb")
        a.write(content)
        a.close()


