from pymongo import MongoClient
import pandas as pd
from importlib import import_module

from . import BaseApiConnector
from .cloud_storage import CloudStorageConnector
from data_engineering.parsers import get_parsing_functions
import settings

cloud_storage_conn = CloudStorageConnector('airflow_task_communication',
                                           settings.SERVICE_ACCOUNT_STORAGE_ADMIN)
PARSING_FUNCTIONS = get_parsing_functions('mongodb')


class MongoDbConnector(BaseApiConnector):
    name = "mongodb"

    def __init__(
            self,
            database: str
            ) -> None:
        # Connection to the MongoDB database
        CONNECTION_STRING = settings.mongo_db["CONNECTION_STRING"]
        self.database = database
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[database]

    def insert_data(
            self,
            data_entity: str,
            data,
            single: bool = True
            ) -> None:
        """Insert data in a MongoDB collection.

        :param data_entity: The name of the MongoDB collection
        from which to fetch data.

        :param data: The data to insert. It could be either a list of
                    multiple elements to insert (i.e multiple dictionnairies)
                    or a single element to insert (i.e one dictionnary)

        :param single: if True then data is a dictionnary, if False
                    then data is a list of dictionnaries
        """
        collection = self.db[data_entity]

        if single:
            collection.insert_one(document=data)
        else:
            collection.insert_many(documents=data)

    def fetch_data(
            self,
            data_entity: str,
            filters: dict = {},
            save_res_to_s3: bool = False
            ) -> pd.DataFrame:
        """Fetch data from a specified MongoDB collection with applied filters,
        parse the result, and convert it into a pandas DataFrame.

        :param data_entity: The name of the MongoDB collection
        from which to fetch data.

        :param filters: A dictionary of filters to apply to the MongoDB query.
                        The filters should be in the format required by
                        MongoDB's query language.

        :return: A pandas DataFrame containing the parsed data from
        the MongoDB collection.
        """
        data = list(self.db[data_entity].find(filters))

        # Getting the coresponding parsing function
        parser = PARSING_FUNCTIONS[data_entity]

        # Parse Data
        data = [parser(elt) for elt in data]

        if save_res_to_s3:
            cloud_storage_conn.insert_data(data_entity + '.csv',
                                           pd.DataFrame(data))

        return pd.DataFrame(data)
