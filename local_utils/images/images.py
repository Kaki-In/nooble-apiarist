import io as _io
import time as _time
import typing as _T
import base64 as _base64
import asyncio as _asyncio
import PIL.Image as _pil_image

import typing as _T

_image_types = _T.TypeVar("_image_types")

try:
    import pyvips as _pyvips

    PYVIPS_INSTALLED = True
except Exception as exc:
    PYVIPS_INSTALLED = False

    print("Warning: could not use the pyvips package because of the following error", exc)
    print("We will use the PIL library, that could be slow. Sorry for that issue. Please install the libvips module, and the libvips42 package. ")

class _Image(_T.Generic[_image_types]):
    def __init__(self, image: _image_types | None):
        self._image = image

    def __str__(self) -> str:
            return _base64.b64encode(bytes(self)).decode()
    
    def __bytes__(self) -> bytes:
        raise NotImplementedError("not implemented for "+ repr(self))
    
    def get_width(self) -> int:
        raise NotImplementedError("not implemented for "+ repr(self))

    def get_height(self) -> int:
        raise NotImplementedError("not implemented for "+ repr(self))

    def get_size(self) -> tuple[int, int]:
        return self.get_width(), self.get_height()
    
    def resize(self, width:int, height:int) -> '_Image[_image_types]':
        raise NotImplementedError("not implemented for "+ repr(self))
    
    def copy(self) -> '_Image[_image_types]':
        raise NotImplementedError("not implemented for "+ repr(self))

if PYVIPS_INSTALLED:
    import pyvips as _pyvips

    class _pyvipsImage(_Image[_pyvips.Image]): 
        def __init__(self, image: _T.Optional[_pyvips.Image] = None):
            self._image = image or _pyvips.Image.black(10, 10)                  #type:ignore

        def __str__(self) -> str:
            return _base64.b64encode(bytes(self)).decode()
        
        def __bytes__(self) -> bytes:
            return self._image.write_to_buffer('.png')                          #type:ignore
        
        def get_width(self) -> int:
            return self._image.width                                            #type:ignore
        
        def get_height(self) -> int:
            return self._image.height                                            #type:ignore
        
        def get_size(self) -> tuple[int, int]:
            return self.get_width(), self.get_height()
        
        def resize(self, width: int, height: int) -> '_pyvipsImage':
            image = self._image

            image_width: int = image.width                                      #type:ignore
            image_height: int = image.height                                    #type:ignore

            resize_factor = min(256 / image_width, 256 / image_height)

            resized_image = image.resize(resize_factor)                         #type:ignore
            
            new_width: int = width                                              #type:ignore
            new_height: int = height                                            #type:ignore

            left = (new_width - 256) // 2
            top = (new_height - 256) // 2

            cropped_image = resized_image.crop(left, top, 256, 256)             #type:ignore

            return _pyvipsImage(cropped_image)
        
        def copy(self) -> '_pyvipsImage':
            return _pyvipsImage(self._image.copy())                                           #type:ignore


class _pillowImage(_Image[_pil_image.Image]):
    def __init__(self, image: _T.Optional[_pil_image.Image] = None):
        self._image = image or _pil_image.new('RGB', (10, 10))

    def __str__(self) -> str:
        return _base64.b64encode(bytes(self)).decode()
    
    def __bytes__(self) -> bytes:
        file  = _io.BytesIO()
        self._image.save(file, '.png')
        
        return file.getvalue()
    
    def get_width(self) -> int:
        return self._image.width
    
    def get_height(self) -> int:
        return self._image.height
    
    def get_size(self) -> tuple[int, int]:
        return self.get_width(), self.get_height()
    
    def resize(self, width: int, height: int) -> '_pillowImage':
        image = self._image

        resized_image = image.resize((width, height))
        
        new_width: int = width
        new_height: int = height

        left = (new_width - 256) // 2
        top = (new_height - 256) // 2

        cropped_image = resized_image.crop((left, top, 256, 256))

        return _pillowImage(cropped_image)
    
    def copy(self) -> '_pillowImage':
        return _pillowImage(self._image.copy())

def Image(image) -> _Image:
    if PYVIPS_INSTALLED:
        if image is None:
            return _pyvipsImage()
        
        if type(image) is _pyvips.Image: #type:ignore
            return _pyvipsImage(image)
        
    return _pillowImage(image)


