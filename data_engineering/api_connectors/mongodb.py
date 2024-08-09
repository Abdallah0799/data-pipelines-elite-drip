from pymongo import MongoClient
import pandas as pd
from importlib import import_module

from . import BaseApiConnector
import settings


class MongoDbConnector(BaseApiConnector):
    def __init__(self, db_name) -> None:
        CONNECTION_STRING = settings.mongo_db["CONNECTION_STRING"]
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[db_name]

    def insert_data(self, collection_name: str, data, single=True) -> None:
        collection = self.db[collection_name]

        if single:
            collection.insert_one(document=data)
        else:
            collection.insert_many(documents=data)

    def fetch_data(self, collection_name: str, filters: dict) -> pd.DataFrame:
        data = list(self.db[collection_name].find(filters))

        # Getting the coresponding parsing function
        module = import_module('data_engineering.data_schemas.' + collection_name)
        parser = getattr(module, 'parse_raw_' + collection_name)

        # Parsing Data
        data = [parser(elt) for elt in data]

        return pd.DataFrame(data)
