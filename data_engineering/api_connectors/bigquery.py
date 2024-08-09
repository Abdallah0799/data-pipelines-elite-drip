import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from typing import List

from . import BaseApiConnector


class BigQueryConnector(BaseApiConnector):
    def __init__(self, service_account_infos: str, scopes: List[str] = None) -> None:
        if scopes is None:
            scopes = ["https://www.googleapis.com/auth/cloud-platform"]

        try:
            self.credentials = service_account.Credentials.from_service_account_info(
                info=service_account_infos,
                scopes=scopes,
            )

            self.bigquery_client = bigquery.Client(
                credentials=self.credentials, project=self.credentials.project_id
            )
        except Exception as e:
            print(f"Erreur lors de l'initialisation du client BigQuery : {e}")
            raise

    def verify(self, dataset_id: str, table_id: str, schema):

        # check existence of dataset
        try:
            self.bigquery_client.get_dataset(dataset_id)
            print("☑️ Dataset {} already exists".format(dataset_id))
        except NotFound:
            print("🧑‍🎨 Dataset {} is not found, creating it".format(dataset_id))
            self.bigquery_client.create_dataset(dataset_id)

        # check existence of table id
        table_id = ".".join([self.bigquery_client.project, dataset_id, table_id])
        try:
            table = self.bigquery_client.get_table(table_id)
            print("☑️ Table {} already exists.".format(table_id))
        except NotFound:
            print("🧑‍🎨Table {} is not found, creating it".format(table_id))
            table = bigquery.Table(table_id, schema=schema)
            self.bigquery_client.create_table(table)

        # check if schema has not changed/new colums
        original_schema = table.schema
        if len(original_schema) != len(schema):
            table.schema = schema
            table = self.bigquery_client.update_table(table, ["schema"])
            print("✳️ A new column has been added.")

    def insert_data(
        self, df: pd.DataFrame, dataset_id: str, table_id: str, schema,
        duplicate_columns: List[str],
        order_columns: List[str]
    ):

        # check that dataset + table exist
        self.verify(dataset_id, table_id, schema)

        # configs
        dataset_ref = self.bigquery_client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.schema = schema

        job = self.bigquery_client.load_table_from_dataframe(
            df, table_ref, job_config=job_config
        )
        job.result()

        print(
            "\n ✅ Loaded {} rows into {}:{}.".format(
                job.output_rows, dataset_id, table_id
            )
        )
        self.drop_duplicates(dataset_id,
                             table_id,
                             duplicate_columns,
                             order_columns)

    def drop_duplicates(
        self,
        dataset_id: str,
        table_id: str,
        duplicate_columns: List[str],
        order_columns: List[str],
    ):

        table_id = ".".join([self.bigquery_client.project, dataset_id, table_id])

        table = self.bigquery_client.get_table(table_id)
        print("\n❕number rows before = ", table.num_rows)

        query_job = self.bigquery_client.query(
            f"""
        create or replace table `{table_id}` as (
        select * except(row_num) from (
        SELECT
        *,
        ROW_NUMBER() OVER (
        PARTITION BY
        {", ".join(duplicate_columns)}
        ORDER BY
        {", ".join(order_columns)} desc
        ) row_num
        FROM
        `{table_id}`) t
        WHERE row_num=1
        )"""
        )

        query_job.result()
        table = self.bigquery_client.get_table(table_id)
        print("❕number rows after = ", table.num_rows)

    def delete_table(self, table_id: str):

        self.bigquery_client.delete_table(
            table_id, not_found_ok=True
        )  # Make an API request.
        print("Deleted table '{}'.".format(table_id))

    def fetch_data(self, query_string: str) -> pd.DataFrame:
        query_job = self.bigquery_client.query(query_string)
        results = query_job.result()
        df_results = results.to_dataframe()
        return df_results.to_dict("records")
