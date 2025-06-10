from ..templates import NoobleSection

import nooble_database.database as _nooble_database

class NoobleAudioSection(NoobleSection[str, str, str]):
    def __init__(self, data: str) -> None:
        super().__init__("audio", data)
    
    async def get_used_files(self, database: _nooble_database.NoobleDatabase) -> list[str]:
        data = self.get_data()
        if data.startswith("content://"):
            return [ data[len("content://"):] ]
        
        return []
    
    async def export_to_client_json_data(self, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> str:
        return self.get_data()
    
    async def export_to_database_json_data(self, database: _nooble_database.NoobleDatabase) -> str:
        return self.get_data()


