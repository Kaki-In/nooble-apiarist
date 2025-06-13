from ..templates.nooble_collection import NoobleCollection
from .nooble_activity import NoobleActivity
from ..objects.activity_object import ActivityObject

import datetime as _datetime

class NoobleActivitiesList(NoobleCollection[ActivityObject]):

    def get_activity(self, activity_id: str) -> NoobleActivity:
        return NoobleActivity(self.get_collection(), activity_id)
    
    async def get_creator_activities(self, creator_id: str) -> list[NoobleActivity]:
        activities = await self.find({
            "creator": creator_id
        })

        activities_results: list[NoobleActivity] = []

        for activity in activities:
            activities_results.append(
                NoobleActivity(
                    self.get_collection(),
                    activity['_id'],
                    activity
                )
            )

        return activities_results
    
    async def create_activity(self, title: str, content: str, creator: str, date: _datetime.datetime, icon: str) -> NoobleActivity:
        object: ActivityObject = {
            "title": title,
            "content": content,
            "creator": creator,
            "date": int(date.timestamp()),
            "icon": icon
        } #type:ignore

        id = await self.insert_one(object)
        object["_id"] = id
    
        return NoobleActivity(self.get_collection(), id, object)
    


