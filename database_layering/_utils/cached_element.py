import asyncio as _asyncio

class _CachedElement():
    def __init__(self) -> None:
        self.__autorefreshes__ = False

    def refresh(self) -> None:
        self.upload_updates()
        self.download_updates()
    
    def is_auto_refreshing(self) -> bool:
        return self.__autorefreshes__

    def download_updates(self) -> None:
        raise NotImplementedError()
    
    def upload_updates(self) -> None:
        raise NotImplementedError()
    
    async def main_refresh(self, interval: float) -> None:
        self.__autorefreshes__ = True

        try:
            while True:
                await _asyncio.sleep(interval)
                self.refresh()
        
        finally:
            self.__autorefreshes__ = False


