import requests
import pandas as pd
from xmltodict import parse
from pathlib import Path
from ..utils import logger

def extract_source(url: str, destination_file: str | Path):

    # Create parent directories if not yet available
    destination_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Download the file in the desired format specified in config.json
        response = requests.get(url)
        response.raise_for_status()

        # Save the downloaded file in the data_dump/raw folder
        with open(destination_file, "wb") as fp:
            fp.write(response.content)

        logger.info(f"{url} has been downloaded.")

    # Log any errors; no exceptions will be raised 
    except Exception as e:
        logger.error(f"Error occured in downloading {url}. {e}")

def extract_from_csv(file_path: str | Path, params: dict) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, **params)
    
    # Log any errors; no exceptions will be raised
    except Exception as e:
        logger.error(f"Error occured in reading {file_path}. {e}")

def extract_from_excel(file_path: str | Path, params: dict) -> pd.DataFrame:
    try:
        return pd.read_excel(file_path, **params)
    
    # Log any errors; no exceptions will be raised
    except Exception as e:
        logger.error(f"Error occured in reading {file_path}. {e}")

def extract_xml(file_path: str | Path, xpath: str, columns: list) -> pd.DataFrame:
    try:
        with open(file_path, "rb") as fp:
            data = parse(fp)

        if xpath:
            for xp in xpath.split("/"):
                if xp:
                    data = data[xp]

        df = pd.DataFrame(data)
        return df[columns]
    
    # Log any errors; no exceptions will be raised
    except Exception as e:
        logger.error(f"Error occured in reading {file_path}. {e}")