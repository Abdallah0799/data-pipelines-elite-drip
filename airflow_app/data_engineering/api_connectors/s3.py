import boto3
import awswrangler as wr
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
from typing import List

from . import BaseApiConnector
from .cloud_storage import CloudStorageConnector
from utils import align_dataframe_to_bq_schema
import settings


cloud_storage_conn = CloudStorageConnector('airflow_task_communication',
                                           settings.SERVICE_ACCOUNT_STORAGE_ADMIN)


class S3Connector(BaseApiConnector):
    name = "s3"

    def __init__(self,
                 database: str) -> None:
        """Initialize the connection to AWS. We need to create a
        s3_client with the credentials of our S3 service (with
        access et secret key).

        :param database: Name of the bucket
        """
        ACCESS_KEY = settings.AWS_S3_ACCESS_KEY
        SECRET_KEY = settings.AWS_S3_ACCESS_SECRET

        self.bucket_name = database
        self.database = database

        # initialize a Boto client and session
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
            )
        self.session = boto3.Session(
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
            )

    def insert_data(
            self,
            data_entity: str,
            file_name: str,
            data: pd.DataFrame
            ) -> None:
        """Upload a CSV file to a folder of an S3 bucket

        :param data: Data to upload
        :param data_entity: Folder to upload in
        :param file_name: Name of the file in s3
        """
        # Convert DataFrame to CSV
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)

        # Define key
        key = f"{data_entity}/{file_name}.csv"

        # Upload the CSV file to S3
        self.s3_client.put_object(Bucket=self.bucket_name,
                                  Key=key,
                                  Body=csv_buffer.getvalue())

    def fetch_data(
            self,
            data_entity: str,
            datetime_window_filter: float,
            save_res_to_s3: bool = False
            ) -> pd.DataFrame:
        """Fetch a CSV file from an S3 bucket

        :param data_entity: The name of the folder where we want
        to fetch data in the bucket
        :param datetime_window_filter: see docstring of
        get_file_names function

        :return: The chosen files of the chosen folder as a
        dataframe
        """
        # Specify the S3 path to your CSV file
        S3_PATH_BASE = f"s3://{self.bucket_name}/{data_entity}/"

        # Get file names we want to fetch
        file_names = self.get_file_names(data_entity,
                                         datetime_window_filter)
        dfs = []
        # Fetch data
        for file_name in file_names:

            s3_path = S3_PATH_BASE + file_name
            # Read the CSV file from S3 into a Pandas DataFrame using the
            # session
            data = wr.s3.read_csv(s3_path,
                                  boto3_session=self.session)

            # Transform raw data from the csv
            data = align_dataframe_to_bq_schema(data, data_entity)
            dfs.append(data)

        if save_res_to_s3:
            cloud_storage_conn.insert_data(data_entity + '.csv',
                                           pd.concat(dfs))

        return pd.concat(dfs)

    def get_file_names(
            self,
            data_entity: str,
            datetime_window_filter: float
    ) -> List[str]:
        """Retrieve the names of CSV files from a specified S3 folder that
        were uploaded within a given time window.

        :param data_entity: The name of the S3 folder (data entity)
        from which to fetch data.

        :param datetime_window_filter:The time window (in days) for
        filtering files based on their last modification date. Only
        files modified within this window are returned.

        :return: A list of file names (as strings) that match the criteria.
        """
        folder_path = f"{data_entity}/"

        # List all objects in the specified S3 folder
        # We will need to update this function later
        # because list_objects_v2 only list 1000 files
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name,
                                                  Prefix=folder_path)

        csv_files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                last_modified = obj['LastModified']

                # Check if the file is a CSV and was uploaded within the window
                if (last_modified >= (datetime.now(last_modified.tzinfo) - timedelta(datetime_window_filter))
                    and obj['Key'].endswith('.csv')):
                    csv_files.append(obj['Key'].split(folder_path)[-1])

        return csv_files
