from .images import Image, PYVIPS_INSTALLED

import typing as _T
import base64 as _base64
import PIL.Image as _pil_image

_image_types = _T.TypeVar("_image_types")

class ImagesTranslationKeeper(_T.Generic[_image_types]):
    def __init__(self):
        self._images: list[tuple[bytes, _image_types]] = []
        self._str_decodes: dict[str, bytes] =  {}
    
    def saveImageTranslation(self, bytes: bytes, image: _image_types) -> None:
        self._images.append((bytes, image))
    
    def hasImageTranslation(self, bytes: bytes) -> bool:
        for element in self._images:
            if element[0] == bytes:
                return True
        
        return False
    
    def hasStrDecode(self, data: str) -> bool:
        return data in self._str_decodes
    
    def getImageTranslation(self, bytes: bytes) -> _image_types:
        for element in self._images:
            if element[0] == bytes:
                return element[1]
            
        raise KeyError("no image found for this chain")
    
    def saveStrDecode(self, data: str, bytes: bytes) -> None:
        self._str_decodes[data] = bytes
    
    def getImageTranslationFromString(self, data: str) -> _image_types:
        if not data in self._str_decodes:
            raise KeyError("no decode found for this data")
        
        return self.getImageTranslation(self._str_decodes[data])
    
    def decodeStr(self, data: str) -> bytes:
        return self._str_decodes[data]

    def long_from_bytes(self, bytes: bytes) -> Image[_image_types]:
        raise NotImplementedError("not implemented for "+ repr(self))

    def long_from_string(self, data: str) -> Image[_image_types]:
        raise NotImplementedError("not implemented for "+ repr(self))


if PYVIPS_INSTALLED:
    import pyvips as _pyvips
    from .images import _pyvipsImage

    class _pyvipsImagesTranslationKeeper(ImagesTranslationKeeper[_pyvips.Image]):
        def long_from_bytes(self, bytes: bytes) -> _pyvipsImage:
            if self.hasImageTranslation(bytes):
                image = self.getImageTranslation(bytes)
            else:
                image: _pyvips.Image = _pyvips.Image.new_from_buffer(bytes, "") #type:ignore
                self.saveImageTranslation(bytes, image)
            
            return _pyvipsImage(image)

        def long_from_string(self, data: str) -> _pyvipsImage:
            if self.hasStrDecode(data):
                bytes = self.decodeStr(data)
            else:
                bytes = _base64.b64decode(data.encode())
                self.saveStrDecode(data, bytes)

            return self.long_from_bytes(bytes)

    DEFAULT_TRANSLATION_KEEPER = _pyvipsImagesTranslationKeeper()
else:
    from .images import _pillowImage

    class _pillowImagesTranslationKeeper(ImagesTranslationKeeper[_pil_image.Image]):
        def long_from_bytes(self, bytes: bytes) -> _pillowImage:
            if self.hasImageTranslation(bytes):
                image = self.getImageTranslation(bytes)
            else:
                image = _pil_image.open(bytes)
                self.saveImageTranslation(bytes, image)
            
            return _pillowImage(image)

        def long_from_string(self, data: str) -> _pillowImage:
            if self.hasStrDecode(data):
                bytes = self.decodeStr(data)
            else:
                bytes = _base64.b64decode(data.encode())
                self.saveStrDecode(data, bytes)

            return self.long_from_bytes(bytes)


    DEFAULT_TRANSLATION_KEEPER = _pillowImagesTranslationKeeper()
