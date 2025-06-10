from ..templates import NoobleSection

import nooble_database.database as _nooble_database
import nooble_database.objects as _nooble_database_objects

class NoobleIntegrationSectionData():
    def __init__(self, width:str|int, height:str|int, source:str, permissions:list[str]) -> None:
        self._width = width
        self._height = height
        self._source = source
        self._permissions = permissions
    
    def get_width(self) -> str|int:
        return self._width
    
    def get_height(self) -> str|int:
        return self._height
    
    def get_source(self) -> str:
        return self._source
    
    def get_permissions(self) -> list[str]:
        return self._permissions

class NoobleIntegrationSection(NoobleSection[NoobleIntegrationSectionData, _nooble_database_objects.section_objects.IntegrationSectionDataObject, _nooble_database_objects.section_objects.IntegrationSectionDataObject]):
    def __init__(self, width:str|int, height:str|int, source:str, permissions:list[str]) -> None:
        super().__init__("integration", NoobleIntegrationSectionData(width, height, source, permissions))
    
    async def get_used_files(self, database: _nooble_database.NoobleDatabase) -> list[str]:
        return []
    
    async def export_to_client_json_data(self, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> _nooble_database_objects.section_objects.IntegrationSectionDataObject:
        data = self.get_data()

        return {
            "width": data.get_width(),
            "height": data.get_height(),
            "src": data.get_source(),
            "permissions": data.get_permissions()
        }
    
    async def export_to_database_json_data(self, database: _nooble_database.NoobleDatabase) -> _nooble_database_objects.section_objects.IntegrationSectionDataObject:
        data = self.get_data()

        return {
            "width": data.get_width(),
            "height": data.get_height(),
            "src": data.get_source(),
            "permissions": data.get_permissions()
        }
    


