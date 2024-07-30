import requests
from pathlib import Path
from ..utils import logger

def extract_source(url: str, destination_file: str | Path):

    # Create parent directories if not yet available
    destination_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Download the file in the desired format specified in config.json
        response = requests.get(url)
        response.raise_for_status()

        with open(destination_file, "wb") as fp:
            fp.write(response.content)

        logger.info(f"{url} has been downloaded.")

    # Log any errors; no exceptions will be raised 
    except Exception as e:
        logger.error(f"Error occured in downloading {url}. {e}")