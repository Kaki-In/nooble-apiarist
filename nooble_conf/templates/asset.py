class NoobleSettingsAsset():
    def __init__(self, path:str) -> None:
        self._path = path

    def get_content(self) -> bytes:
        a = open(self._path, "rb")
        data = a.read()
        a.close()

        return data
    
    def overwrite(self, content: bytes) -> None:
        a = open(self._path, "wb")
        a.write(content)
        a.close()


