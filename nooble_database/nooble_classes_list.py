from .templates.nooble_collection import NoobleCollection
from .objects.class_object import ClassObject
from .nooble_class import NoobleClass

import re as _regex

class NoobleClassesList(NoobleCollection[ClassObject]):
    
    def get_class(self, id: int) -> NoobleClass:
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
    
    async def get_account_classes(self, account_id: int) -> list[NoobleClass]:
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
    
    




