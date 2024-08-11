from pymongo import MongoClient
import pandas as pd
from importlib import import_module

from . import BaseApiConnector
import settings


class MongoDbConnector(BaseApiConnector):
    def __init__(
            self,
            db_name
            ) -> None:
        # Connection to the MongoDB database
        CONNECTION_STRING = settings.mongo_db["CONNECTION_STRING"]
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[db_name]

    def insert_data(
            self,
            collection_name: str,
            data,
            single: bool = True
            ) -> None:
        """Insert data in a MongoDB collection.

        :param collection_name: The name of the MongoDB collection 
        from which to fetch data.

        :param data: The data to insert. It could be either a list of
                    multiple elements to insert (i.e multiple dictionnairies) 
                    or a single element to insert (i.e one dictionnary)

        :param single: if True then data is a dictionnary, if False
                    then data is a list of dictionnaries
        """
        collection = self.db[collection_name]

        if single:
            collection.insert_one(document=data)
        else:
            collection.insert_many(documents=data)

    def fetch_data(
            self,
            collection_name: str,
            filters: dict = {}
            ) -> pd.DataFrame:
        """Fetch data from a specified MongoDB collection with applied filters,
        parse the result, and convert it into a pandas DataFrame.

        :param collection_name: The name of the MongoDB collection
        from which to fetch data.

        :param filters: A dictionary of filters to apply to the MongoDB query.
                        The filters should be in the format required by
                        MongoDB's query language.

        :return: A pandas DataFrame containing the parsed data from
        the MongoDB collection.
        """
        data = list(self.db[collection_name].find(filters))

        # Getting the coresponding parsing function
        module = import_module('data_engineering.data_schemas.' + collection_name)
        parser = getattr(module, 'parse_raw_' + collection_name)

        # Parse Data
        data = [parser(elt) for elt in data]

        return pd.DataFrame(data)
