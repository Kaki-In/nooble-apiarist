from .nooble_accounts_list import NoobleAccountsList
from .nooble_files_list import NoobleFilesList
from .nooble_activities_list import NoobleActivitiesList
from .nooble_decorations_list import NoobleDecorationsList
from .nooble_classes_list import NoobleClassesList

import pymongo as _pymongo

import nooble_conf.files.nooble_database_configuration as _nooble_conf

class NoobleDatabase():
    def __init__(self, configuration: _nooble_conf.NoobleDatabaseSettings) -> None:
        self._client = _pymongo.AsyncMongoClient(
            configuration.get_host(),
            configuration.get_port()
        )

        self._database = self._client.get_database(configuration.get_dbname())

        self._configuration = configuration

    def get_accounts(self) -> NoobleAccountsList:
        collection_name = self._configuration.get_tables().get_accounts_name()
        return NoobleAccountsList(self._database.get_collection(collection_name), self._configuration.get_rules())
    
    def get_files(self) -> NoobleFilesList:
        collection_name = self._configuration.get_tables().get_files_name()
        return NoobleFilesList(self._database.get_collection(collection_name))
    
    def get_classes(self) -> NoobleClassesList:
        collection_name = self._configuration.get_tables().get_classes_name()
        return NoobleClassesList(self._database.get_collection(collection_name))
    
    def get_activities(self) -> NoobleActivitiesList:
        collection_name = self._configuration.get_tables().get_activities_name()
        return NoobleActivitiesList(self._database.get_collection(collection_name))
    
    def get_decorations(self) -> NoobleDecorationsList:
        collection_name = self._configuration.get_tables().get_decorations_name()
        return NoobleDecorationsList(self._database.get_collection(collection_name))
    




