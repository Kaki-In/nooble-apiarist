from ..templates import NoobleSection

import nooble_database.database as _nooble_database
import nooble_database.objects as _nooble_database_objects

class NoobleFileSectionData():
    def __init__(self, filename:str, description:str, src_id:str) -> None:
        self._filename = filename
        self._description = description
        self._src = src_id

    def get_filename(self) -> str:
        return self._filename
    
    def get_description(self) -> str:
        return self._description
    
    def get_source(self) -> str:
        return self._src

class NoobleFileSection(NoobleSection[NoobleFileSectionData, _nooble_database_objects.section_objects.FileSectionDataObject, _nooble_database_objects.section_objects.FileSectionDataObject]):
    def __init__(self, filename:str, description:str, src_id:str) -> None:
        super().__init__("file", NoobleFileSectionData(filename, description, src_id))
    
    async def get_used_files(self, database: _nooble_database.NoobleDatabase) -> list[str]:
        return [ self.get_data().get_source() ]
    
    async def export_to_client_json_data(self, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> _nooble_database_objects.section_objects.FileSectionDataObject:
        data = self.get_data()

        return {
            "description": data.get_description(),
            "filename": data.get_filename(),
            "src": data.get_source()
        }
    
    async def export_to_database_json_data(self, database: _nooble_database.NoobleDatabase) -> _nooble_database_objects.section_objects.FileSectionDataObject:
        data = self.get_data()

        return {
            "description": data.get_description(),
            "filename": data.get_filename(),
            "src": data.get_source()
        }
    


