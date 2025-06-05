class NoobleFileResource():
    def __init__(self, base_directory: str, path:str) -> None:
        self._base_directory = base_directory
        self._path = path

    def get_path(self) -> str:
        return self._path
    
    def get_content(self) -> bytes:
        file = open(self._path, "rb")
        data = file.read()
        file.close()

        return data
    
    def overwrite(self, data:bytes) -> None:
        file = open(self._path, "rb")
        file.write(data)
        file.close()



