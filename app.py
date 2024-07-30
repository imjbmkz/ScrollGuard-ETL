from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from scrollguard_etl.utils import logger, get_config
from scrollguard_etl.etl import extract_source

source_config = get_config()["SOURCES"]

if __name__=="__main__":

    # Download the sources in parallel
    with ProcessPoolExecutor() as executor:

        # Iterate through each data source configuration and get details required
        for src in source_config:
            name = src["NAME"]
            fmt = src["FORMAT"]
            url = src["URL"]
            destination_file = Path("data_dump/raw") / f"{name}.{fmt}"
            
            # Save the file in the data_dump/raw folder
            executor.submit(extract_source, url, destination_file)