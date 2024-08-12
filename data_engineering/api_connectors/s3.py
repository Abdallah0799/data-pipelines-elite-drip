import boto3
import awswrangler as wr
from io import StringIO
import pandas as pd

from . import BaseApiConnector
import settings


class S3Connector(BaseApiConnector):
    def __init__(self) -> None:
        ACCESS_KEY = settings.AWS_S3_ACCESS_KEY
        SECRET_KEY = settings.AWS_S3_ACCESS_SECRET

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
            bucket_name: str,
            file_name: str
            ) -> None:
        """Upload a CSV file to an S3 bucket

        :param data: Data to upload
        :param bucket: Bucket to upload to
        :param file_name: Name of the file in s3
        """
        # Convert DataFrame to CSV
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)

        # Upload the CSV file to S3
        self.s3_client.put_object(Bucket=bucket_name,
                                  Key=file_name,
                                  Body=csv_buffer.getvalue())

    def fetch_data(
            self,
            bucket_name: str,
            file_name: str
            ) -> pd.DataFrame:
        """Fetch a CSV file from an S3 bucket

        :param bucket_name: Name of the bucket
        :param file_name: Name of the bucket
        :return: The chosen CSV file as a Dataframe
        """
        # Specify the S3 path to your CSV file
        s3_path = f"s3://{bucket_name}/{file_name}"

        # Read the CSV file from S3 into a Pandas DataFrame using the session
        data = wr.s3.read_csv(s3_path,
                              boto3_session=self.session)

        return data
