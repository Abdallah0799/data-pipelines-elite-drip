from pymongo import MongoClient
import pandas as pd
from importlib import import_module

from . import BaseApiConnector
import settings


class MongoDbConnector(BaseApiConnector):
    name = "mongodb"

    def __init__(
            self,
            db_name
            ) -> None:
        # Connection to the MongoDB database
        CONNECTION_STRING = settings.mongo_db["CONNECTION_STRING"]
        self.dataset = db_name
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[db_name]

    def insert_data(
            self,
            data_type: str,
            data,
            single: bool = True
            ) -> None:
        """Insert data in a MongoDB collection.

        :param data_type: The name of the MongoDB collection 
        from which to fetch data.

        :param data: The data to insert. It could be either a list of
                    multiple elements to insert (i.e multiple dictionnairies) 
                    or a single element to insert (i.e one dictionnary)

        :param single: if True then data is a dictionnary, if False
                    then data is a list of dictionnaries
        """
        collection = self.db[data_type]

        if single:
            collection.insert_one(document=data)
        else:
            collection.insert_many(documents=data)

    def fetch_data(
            self,
            data_type: str,
            filters: dict = {}
            ) -> pd.DataFrame:
        """Fetch data from a specified MongoDB collection with applied filters,
        parse the result, and convert it into a pandas DataFrame.

        :param data_type: The name of the MongoDB collection
        from which to fetch data.

        :param filters: A dictionary of filters to apply to the MongoDB query.
                        The filters should be in the format required by
                        MongoDB's query language.

        :return: A pandas DataFrame containing the parsed data from
        the MongoDB collection.
        """
        data = list(self.db[data_type].find(filters))

        # Getting the coresponding parsing function
        module = import_module('data_engineering.parsing.' + data_type)
        parser = getattr(module, 'parse_raw_' + data_type)

        # Parse Data
        data = [parser(elt) for elt in data]

        return pd.DataFrame(data)
