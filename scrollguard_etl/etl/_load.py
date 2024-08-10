import os
import pandas as pd
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from ..utils import logger, get_blob_service_client_connection_string

def load_to_csv(df: pd.DataFrame, destination: str | Path):
    try:
        # Create parent directories if not yet available
        destination.parent.mkdir(parents=True, exist_ok=True)

        # Drop duplicate records
        df = df.drop_duplicates().copy()

        df.to_csv(destination, index=False)
        logger.info(f"{destination} has been saved.")

    # Log any errors; no exceptions will be raised
    except Exception as e:
        logger.error(f"Error occured in saving {destination}. {e}")

def upload_blob_file(blob_service_client: BlobServiceClient, file_path: Path):
    try:
        container_name = os.getenv("CONTAINER_NAME")
        container_client = blob_service_client.get_container_client(container=container_name)
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=file_path.name, data=data, overwrite=True)
        file_path.unlink()
        logger.info(f"{file_path} has been upload to Blob Storage.")

    except Exception as e:
        logger.error(f"Error occured in uploading file {file_path} to Blob Storage. {e}")