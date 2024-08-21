import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from typing import Any
import io
import pandas as pd

from . import BaseApiConnector
from utils import align_dataframe_to_bq_schema


class CloudStorageConnector(BaseApiConnector):
    def __init__(
            self,
            database: str,
            service_account_infos: str
            ) -> None:

        # Connection to the BigQuery Admin Service Account
        try:
            # Load the credentials from the specified JSON file
            self.credentials = service_account.Credentials.from_service_account_info(
                service_account_infos
                )
            # Initialize a client with the credentials
            self.storage_client = storage.Client(
                credentials=self.credentials,
                project=self.credentials.project_id
                )
        except Exception as e:
            print(f"Erreur lors de l'initialisation du client BigQuery : {e}")
            raise

        # Get the bucket
        self.bucket = self.storage_client.bucket(database)

    def insert_data(
            self,
            file_name: str,
            data: Any
    ) -> None:
        # Convert the DataFrame to CSV format in memory
        csv_buffer = io.BytesIO()
        data.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)  # Move the pointer to the start of the stream

        # Create a blob object with the specified name
        blob = self.bucket.blob(file_name)

        # Upload the CSV file from memory
        blob.upload_from_file(csv_buffer, content_type='text/csv')

    def fetch_data(
            self,
            file_name: str,
    ) -> pd.DataFrame:
        # Create a blob object
        blob = self.bucket.blob(file_name)
        # Download the CSV file content as a string and load it into
        # a Pandas DataFrame
        csv_data = blob.download_as_bytes()
        df = pd.read_csv(io.BytesIO(csv_data))
        df = align_dataframe_to_bq_schema(df, file_name.split('.csv')[0])

        return df
