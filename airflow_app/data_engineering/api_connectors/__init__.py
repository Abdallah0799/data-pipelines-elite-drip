from abc import ABCMeta
import pandas as pd
from typing import Any

from data_engineering.data_schemas import load_schema


class BaseApiConnector(metaclass=ABCMeta):
    def __init__(self, database: str, **kwargs: Any) -> None:
        """Initialize the connection with the connector.
        :param database: Name of the database we want to use
        in the source.
        """
        pass

    def insert_data(self, data: Any, **kwargs: Any) -> None:
        """Insert data in the class destination.

        :param data: Data to insert.
        """
        pass

    def fetch_data(self, data_entity: str, **kwargs: Any) -> pd.DataFrame:
        """Fetch data from the class source.

        :param data_entity: The name of the data entity we want to
        fetch in the source.

        :return: The fetched data as a DataFrame.
        """
        pass
