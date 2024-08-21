import requests
import pandas as pd
import time
from datetime import datetime

from . import BaseApiConnector
from .cloud_storage import CloudStorageConnector
from data_engineering.parsers import get_parsing_functions
import settings

cloud_storage_conn = CloudStorageConnector("airflow_task_communication",
                                           settings.SERVICE_ACCOUNT_STORAGE_ADMIN)
PARSING_FUNCTIONS = get_parsing_functions("balldontlie")


class BallDontLie(BaseApiConnector):
    name = "balldontlie"

    def __init__(self, database: str) -> None:
        API_KEY = settings.BALLDONTLIE_API_KEY
        self.headers = {"Authorization": API_KEY}
        self.BASE_URL = "https://api.balldontlie.io/v1/"
        self.database = database

    def fetch_data(
        self, data_entity: str, params: dict, save_res_to_s3: bool = False
    ) -> pd.DataFrame:
        """
        Fetch data from the BallDontLie database.

        :param data_entity: The name of the data entity we want to
        fetch in the source.
        :param params: Parameters we want to send to the API call.
        Have a look at the balldontlie documentation to see
        all possible parameters.
        :save_res_to_s3: If True it saves the result to cloud
        storage as a csv.

        :return: the fetched data as a DataFrame
        """
        # initialize key variables
        endpoint = self.BASE_URL + data_entity
        cursor = 0
        res = []
        parser = PARSING_FUNCTIONS[data_entity]

        # while there is still data to fetch (meaning that there is a
        # next_cursor)
        while True:
            # update cursor
            params["cursor"] = str(cursor)

            # send request
            r = requests.get(endpoint, params=params, headers=self.headers)

            # get request result
            try:
                response = r.json()
                data = response["data"]
                res += [parser(elt) for elt in data]
                try:
                    cursor = response["meta"]["next_cursor"]
                except Exception:
                    cursor = None
                if cursor is None:
                    if save_res_to_s3:
                        cloud_storage_conn.insert_data(
                            data_entity + ".csv", pd.DataFrame(res)
                        )
                    return pd.DataFrame(res)

            # catching exception if we are out of request
            except Exception as e:
                if r.status_code == 429:  # 429 means we are out of request
                    time.sleep(2)
                else:
                    print(f"An error has occured: {str(e)}")
                    return pd.DataFrame(res)
