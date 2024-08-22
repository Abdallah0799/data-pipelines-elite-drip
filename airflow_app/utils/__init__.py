from typing import List
import pandas as pd

import settings
from data_engineering.data_schemas import load_schema


def get_data_types_to_fetch(source: str, database: str) -> dict:
    """ """
    data_to_fetch = settings.data_to_fetch

    return data_to_fetch[source][database]


def align_dataframe_to_bq_schema(
        data: pd.DataFrame,
        data_entity: str
        ) -> pd.DataFrame:
    """Parses the input DataFrame to match the corresponding BigQuery
    schema for a given data entity.This function ensures that the
    DataFrame has the necessary columns as defined by the BigQuery schema
    for the specified data entity. It retains only the required columns and
    converts them to the appropriate data types based on the schema.
    Specifically, date and timestamp fields are converted to `datetime`
    objects.

    :param data: The input data, typically loaded from a CSV file via
    `pd.read_csv`, that needs to be aligned with the BigQuery schema.
    :param data_entity: The name of the data entity whose schema should
    be applied to the DataFrame.

    :return: A Dataframe aligned with the Bigquery Schema
    """
    # Getting corresponding schema
    schema = load_schema(data_entity)

    # Ensure all BigQuery columns are present in the DataFrame
    df_columns = data.columns
    products_columns = [p.name for p in schema]

    missing_columns = set(products_columns) - set(df_columns)
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {missing_columns}")

    # Keep only the fields we want
    data = data[products_columns]

    # Convert date fields
    for field in schema:
        if "DATE" in field.field_type or "TIMESTAMP" in field.field_type:
            data[field.name] = pd.to_datetime(data[field.name])

    return data
