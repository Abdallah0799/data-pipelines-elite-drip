import unittest
import pandas as pd

from data_engineering.api_connectors.bigquery import BigQueryConnector
from data_engineering.api_connectors.mongodb import MongoDbConnector
from data_engineering.api_connectors.s3 import S3Connector
from data_engineering.data_schemas.orders import orders_schema
import settings

bq_connector = BigQueryConnector(settings.SERVICE_ACCOUNT_BQ_ADMIN)
mongo_connector = MongoDbConnector("center")
s3_connector = S3Connector()


class ConnectorsTest(unittest.TestCase):

    def test_bq_data_fetch(self):
        res = bq_connector.fetch_data("fictive_company", "orders")

    def test_bq_data_insert(self):
        data = pd.read_csv("orders.csv", index_col=False)
        data["order_date"] = pd.to_datetime(data["order_date"])
        bq_connector.insert_data(
            data, "fictive_company", "orders", orders_schema, ["id"], ["id"]
        )

    def test_s3_data_fetch(self):
        res = s3_connector.fetch_data("fictive-company", "orders.csv")

    def test_mongo_data_fetch(self):
        res = mongo_connector.fetch_data("orders")


if __name__ == "__main__":
    unittest.main()
