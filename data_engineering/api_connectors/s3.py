import boto3
import awswrangler as wr
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
from typing import List
import pytz

from . import BaseApiConnector
from data_engineering.schemas import BigQuerySchemas
import settings

bq_schemas = BigQuerySchemas()


class S3Connector(BaseApiConnector):
    name = "s3"

    def __init__(self,
                 bucket_name: str) -> None:
        """
        :param bucket_name: Name of the bucket
        """
        ACCESS_KEY = settings.AWS_S3_ACCESS_KEY
        SECRET_KEY = settings.AWS_S3_ACCESS_SECRET

        self.bucket_name = bucket_name
        self.dataset = bucket_name

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
            data: pd.DataFrame,
            file_name: str
            ) -> None:
        """Upload a CSV file to an S3 bucket

        :param data: Data to upload
        :param file_name: Name of the file in s3
        """
        # Convert DataFrame to CSV
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)

        # Upload the CSV file to S3
        self.s3_client.put_object(Bucket=self.bucket_name,
                                  Key=file_name,
                                  Body=csv_buffer.getvalue())

    def fetch_data(
            self,
            data_type: str,
            datetime_window_filter: float
            ) -> pd.DataFrame:
        """Fetch a CSV file from an S3 bucket

        :param bucket_name: Name of the bucket
        :param file_name: Name of the bucket
        :return: The chosen CSV file as a Dataframe
        """
        # Specify the S3 path to your CSV file
        S3_PATH_BASE = f"s3://{self.bucket_name}/{data_type}/"

        # Get file names we want to fetch
        file_names = self.get_file_names(data_type,
                                         datetime_window_filter)
        dfs = []
        # Fetch data
        for file_name in file_names:

            s3_path = S3_PATH_BASE + file_name
            # Read the CSV file from S3 into a Pandas DataFrame using the session
            data = wr.s3.read_csv(s3_path,
                                  boto3_session=self.session)

            # Transform raw data from the csv
            data = self.transform_data(data, data_type)
            dfs.append(data)

        return pd.concat(dfs)

    def get_file_names(
            self,
            data_type: str,
            datetime_window_filter: float
    ) -> List[str]:
        folder_path = f"{data_type}/"

        # List all objects in the specified S3 folder
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

    def transform_data(
            self,
            data: pd.DataFrame,
            data_name: str
    ) -> pd.DataFrame:
        """
        """
        # Getting corresponding schema
        schema = getattr(bq_schemas, data_name)

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
            if 'DATE' in field.field_type:
                data[field.name] = pd.to_datetime(data[field.name])

        return data
