from .images import *
from .translations_keeper import *

import asyncio as _asyncio

async def from_bytes(bytes: bytes) -> Image:
    return await _asyncio.get_event_loop().run_in_executor(None, long_from_bytes, bytes)

async def from_string(data: str) -> Image:
    return await _asyncio.get_event_loop().run_in_executor(None, long_from_string, data)

def long_from_bytes(bytes: bytes) -> Image:
    return DEFAULT_TRANSLATION_KEEPER.long_from_bytes(bytes)

def long_from_string(data: str) -> Image:
    return DEFAULT_TRANSLATION_KEEPER.long_from_string(data)


