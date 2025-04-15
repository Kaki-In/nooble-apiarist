from .elements import NoobleDatabase

import database as _database
import database_layering.enums as _database_layering_enums
import database_layering.cached_elements as _database_layering_cached

class CachedNoobleDatabase(NoobleDatabase):
    def __init__(self, configuration: _database.DatabaseConfiguration) -> None:
        super().__init__(_database_layering_cached.CachedDatabase(configuration, 
            accounts = (_database_layering_enums.CachedTableType.AUTO_INCREMENT_TABLE, 'id', 
                [
                    'id',
                    'surname',
                    'name',
                    'password',
                    'image',
                    'mail',
                    'description',
                    'is-admin',
                    'verified'
                ]
            ),
            activity_savefiles = (_database_layering_enums.CachedTableType.AUTO_INCREMENT_TABLE, 'id', 
                [
                    'id',
                    'type',
                    'content',
                    'section'
                ]
            ),
            classes = (_database_layering_enums.CachedTableType.AUTO_INCREMENT_TABLE, 'id', 
                [
                    'id',
                    'name',
                    'thumbnail',
                    'section'
                ]
            ),
            class_sections = (_database_layering_enums.CachedTableType.AUTO_INCREMENT_TABLE, 'id', 
                [
                    'id',
                    'type',
                    'content',
                ]
            ),
            class_subscriptions = (_database_layering_enums.CachedTableType.ASSOCIATIVE_TABLE, ('account', 'class'),
                [
                    'account',
                    'class',
                    'as teacher'
                ]
            ),
        ))


