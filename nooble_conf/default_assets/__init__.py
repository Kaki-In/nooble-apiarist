import os as _os

DEFAULT_ASSETS_DIRECTORY = _os.path.abspath(_os.path.dirname(__file__))

def get_default_asset_content(filename: str) -> bytes:
    if not _os.path.exists(DEFAULT_ASSETS_DIRECTORY + _os.path.sep + filename):
        raise FileNotFoundError("no default asset found for " + filename)

    a = open(DEFAULT_ASSETS_DIRECTORY + _os.path.sep + filename, "rb")
    data = a.read()
    a.close()

    return data


