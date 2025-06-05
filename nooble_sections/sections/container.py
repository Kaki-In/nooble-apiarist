from ..templates import NoobleSection

import nooble_database.database as _nooble_database
import nooble_database.objects as _nooble_objects

class NoobleContainerSectionData():
    def __init__(self, is_horizontal: bool, is_wrapping: bool, children: list[NoobleSection]) -> None:
        self._is_horizontal = is_horizontal
        self._is_wrapping = is_wrapping
        self._children = children

    def is_horizontal(self) -> bool:
        return self._is_horizontal
    
    def is_wrapping(self) -> bool:
        return self._is_wrapping
    
    def get_children(self) -> list[NoobleSection]:
        return self._children

class NoobleContainerSection(NoobleSection[NoobleContainerSectionData, _nooble_objects.section_objects.ContainerSectionDataObject, _nooble_objects.section_objects.ContainerSectionDataObject]):
    def __init__(self, is_horizontal: bool, is_wrapping: bool, children: list[NoobleSection]) -> None:
        super().__init__("container", NoobleContainerSectionData(is_horizontal, is_wrapping, children))

    async def get_used_files(self, database: _nooble_database.NoobleDatabase) -> list[str]:
        return []
    
    async def get_recursive_used_files(self, database: _nooble_database.NoobleDatabase) -> list[str]:
        files:list[str] = []

        for child in self.get_data().get_children():
            files += await child.get_recursive_used_files(database)

        return files

    async def export_to_client_json_data(self, database: _nooble_database.NoobleDatabase, account: _nooble_database.NoobleAccount) -> _nooble_objects.section_objects.ContainerSectionDataObject:
        return {
            "is_horizontal": self.get_data().is_horizontal(),
            "is_wrapping": self.get_data().is_wrapping(),
            "children": [
                await child.export_to_client_json(database, account) for child in self.get_data().get_children()
            ]
        }
    
    async def export_to_database_json_data(self, database: _nooble_database.NoobleDatabase) -> _nooble_objects.section_objects.ContainerSectionDataObject:
        return {
            "is_horizontal": self.get_data().is_horizontal(),
            "is_wrapping": self.get_data().is_wrapping(),
            "children": [
                await child.export_to_database_json(database) for child in self.get_data().get_children()
            ]
        }
    

