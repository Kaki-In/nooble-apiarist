from ..templates.nooble_collection import NoobleCollection
from ..objects.class_object import ClassObject
from .nooble_class import NoobleClass
from ..objects.section_objects import SectionObject

import re as _regex
import datetime as _datetime

class NoobleClassesList(NoobleCollection[ClassObject]):
    
    def get_class(self, id: str) -> NoobleClass:
        return NoobleClass(self.get_collection(), id)
    
    async def get_class_containing_name(self, name: str) -> list[NoobleClass]:
        return [
            NoobleClass(
                self.get_collection(),
                class_data["_id"],
                class_data
            )

            for class_data in await self.find(
                {
                    "$or": [
                        {
                            "name": {
                                '$regex': _regex.escape(name),
                                '$options': 'i' # case insensitive
                            }
                        },
                        {
                            "description": {
                                '$regex': _regex.escape(name),
                                '$options': 'i' # case insensitive
                            }
                        },
                    ]
                }
            )
        ]
    
    async def get_account_classes(self, account_id: str) -> list[NoobleClass]:
        return [
            NoobleClass(
                self.get_collection(),
                class_data["_id"],
                class_data
            )

            for class_data in await self.find(
                {
                    "accounts": {
                        "$elemMatch": {
                            "$eq": account_id,
                        }
                    }
                }
            )
        ]
    
    async def create_class(self, name: str, description: str, creator: str) -> NoobleClass:
        base_container: SectionObject = {
            "type": "container",
            "data": {
                "children": [],
                "is_horizontal": False,
                "is_wrapping": False,
            }
        }
        object: ClassObject = {
            "accounts": [],
            "content": base_container,
            "description": description,
            "last_modification": int(_datetime.datetime.now().timestamp()),
            "last_modifier": creator,
            "name": name
        } #type:ignore

        id = await self.insert_one(object)
        object["_id"] = id

        return NoobleClass(self.get_collection(), id, object)
    
    




