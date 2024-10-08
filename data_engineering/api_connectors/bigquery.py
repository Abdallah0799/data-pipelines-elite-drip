import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from typing import List

import settings
from . import BaseApiConnector
from utils import align_dataframe_to_bq_schema
from .cloud_storage import CloudStorageConnector

cloud_storage_conn = CloudStorageConnector('airflow_task_communication',
                                           settings.SERVICE_ACCOUNT_STORAGE_ADMIN)


class BigQueryConnector(BaseApiConnector):
    def __init__(
            self, database: str,
            service_account_infos: str,
            scopes: List[str] = None
            ) -> None:
        """Initialize the connection to BigQuery. We need to create a
        bigquery_client with the credentials of a service account.

        :param service_account_infos: Service account informations. The json
        uploaded from GCP but converted in str format.
        :param database: The name of the BigQuery dataset containing the tables
        we want to use
        """
        self.database = database
        if scopes is None:
            scopes = ["https://www.googleapis.com/auth/cloud-platform"]

        # Connection to the BigQuery Admin Service Account
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

    def verify(
        self, data_entity: str, schema: List[bigquery.SchemaField]
    ) -> None:
        """
        Verify the existence of a BigQuery dataset and table, creating
        them if necessary, and ensure the table schema is up to date.

        :param data_entity: The name of the BigQuery table to verify or create.
        This will be combined with the dataset_id and project ID to
        form a fully-qualified table ID.

        :param schema: The schema to apply to the BigQuery table if it is
        created or if the existing schema differs.
        """
        # check existence of dataset
        try:
            self.bigquery_client.get_dataset(self.database)
        except NotFound:
            self.bigquery_client.create_dataset(self.database)

        # check existence of table id
        table_id = f"{self.bigquery_client.project}.{self.database}.{data_entity}"

        try:
            table = self.bigquery_client.get_table(table_id)

            # check if schema has not changed/new colums
            original_schema = table.schema
            if len(original_schema) != len(schema):
                table.schema = schema
                table = self.bigquery_client.update_table(table, ["schema"])

        except NotFound:
            table = bigquery.Table(table_id, schema=schema)
            self.bigquery_client.create_table(table)

    def insert_data(
        self,
        data: pd.DataFrame,
        data_entity: str,
        schema: List[bigquery.SchemaField],
        duplicate_columns: List[str],
        order_columns: List[str],
        order: str = "DESC",
    ) -> None:
        """
        Insert data from a pandas DataFrame into a BigQuery table, verifying
        the table's existence and schema, and optionally removing duplicates
        after insertion.

        :param data: The pandas DataFrame containing the data to be inserted
        into the BigQuery table.

        :param data_entity: The name of the BigQuery table into which the data
        will be inserted.

        :param schema: The schema of the BigQuery table.
        This schema is used to verify the table structure
        before insertion.

        :param duplicate_columns: see docstring of drop_duplicates()

        :param order_columns: see docstring of drop_duplicates()

        :param order: see docstring of drop_duplicates()

        """
        # if data is empty we go fetch data in s3
        if data is None:
            data = cloud_storage_conn.fetch_data(data_entity + '.csv')
            data = align_dataframe_to_bq_schema(data, data_entity)

        # Checking dataset and table
        self.verify(data_entity, schema)

        # Job config then run job
        table_id = f"{self.bigquery_client.project}.{self.database}.{data_entity}"
        job_config = bigquery.LoadJobConfig(schema=schema)
        job = self.bigquery_client.load_table_from_dataframe(
            data, table_id, job_config=job_config
        )
        job.result()

        # Drop duplicates if a duplicate columns is given
        if len(duplicate_columns) > 0:
            self.drop_duplicates(
                data_entity, duplicate_columns, order_columns, order
            )

    def drop_duplicates(
        self,
        data_entity: str,
        duplicate_columns: List[str],
        order_columns: List[str],
        order: str = "DESC",
    ) -> None:
        """
        Remove duplicate rows from a BigQuery table based on specified columns.
        This function uses a SQL query to create or replace the table with a
        version that has duplicates removed

        :param data_entity: The name of the BigQuery table from which to remove
        duplicates.

        :param duplicate_columns: A list of columns used to identify duplicate
        rows.

        :param order_columns: A list of columns used to determine which row to
        keep when duplicates are found.

        :param order: The order used to determine which rows are kept. It can
        be DESC (descending) or ASC (ascending)
        """
        table_id = f"{self.bigquery_client.project}.{self.database}.{data_entity}"

        # Constructing SQL query with parameters
        duplicate_columns_str = ", ".join(duplicate_columns)
        if len(order_columns) > 0:
            partition_order_str = f"ORDER BY {', '.join(order_columns)} {order}"

        else:
            partition_order_str = ""

        sql_query = f"""
            CREATE OR REPLACE TABLE `{table_id}` AS (
                SELECT * EXCEPT(row_num)
                FROM (
                    SELECT
                        *,
                        ROW_NUMBER() OVER (
                            PARTITION BY {duplicate_columns_str}
                            {partition_order_str}
                        ) AS row_num
                    FROM `{table_id}`
                ) t
                WHERE row_num = 1
            )
        """
        sql_query_job = self.bigquery_client.query(sql_query)
        sql_query_job.result()

    def fetch_data(self, data_entity: str) -> pd.DataFrame:
        """
        Fetch data from a specified table.

        :param data_entity: The name of the BigQuery table to fetch.

        :return: A pandas DataFrame containing the table date.
        """
        table_id = f"{self.bigquery_client.project}.{self.database}.{data_entity}"
        query_str = f"SELECT * FROM `{table_id}`"
        # Run query job
        query_job = self.bigquery_client.query(query_str)
        results = query_job.result()
        # Convert results to dataframe
        df_results = results.to_dataframe()

        return df_results
