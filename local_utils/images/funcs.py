from .images import _Image, Image
from .translations_keeper import *

import base64 as _base64
import asyncio as _asyncio

async def from_bytes(bytes: bytes) -> _Image:
    return await _asyncio.get_event_loop().run_in_executor(None, long_from_bytes, bytes)

async def from_string(data: str) -> _Image:
    return await _asyncio.get_event_loop().run_in_executor(None, long_from_string, data)

def long_from_bytes(bytes: bytes) -> _Image:
    return DEFAULT_TRANSLATION_KEEPER.long_from_bytes(bytes)

def long_from_string(data: str) -> _Image:
    return DEFAULT_TRANSLATION_KEEPER.long_from_string(data)


