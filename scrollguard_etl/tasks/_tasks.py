from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from ..utils import get_config, get_blob_service_client_connection_string
from ..etl import extract_source, extract_from_csv, extract_from_excel, extract_xml, transform_normalize_dict, load_to_csv, upload_blob_file

def task_extract_sources():
    source_config = get_config()["SOURCES"]

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

def task_transform_sources():
    source_config = get_config()["SOURCES"]

    # Iterate through each data source configuration and get details required
    for src in source_config:
        # Construct the source raw file and the destination file in CSV format
        name = src["NAME"]
        fmt = src["FORMAT"]
        source_file = Path("data_dump/raw") / f"{name}.{fmt}"
        destination_file = Path("data_dump/processed") / f"{name}.CSV"

        # Preprocessing steps for CSV sources; parameters are pulled from the configuration
        if fmt=="CSV":
            params = src["PARAMS"]
            df = extract_from_csv(source_file, params)
            load_to_csv(df, destination_file)
        
        # Preprocessing steps for XLSX sources; parameters are pulled from the configuration
        if fmt=="XLSX":
            params = src["PARAMS"]
            df = extract_from_excel(source_file, params)
            load_to_csv(df, destination_file)

        # Preprocessing steps for XML sources; configuration consists of details on which ID to keep and what node to parse
        # This is an iterative process since some XML files are nested.
        if fmt=="XML":
            # Get all possible output files from the configuration; iterate through each output config
            output_params = src["OUTPUTS"]
            for oparam in output_params:

                # Get the base details of the main sources; extract the main source as dataframe
                xpath = oparam["XPATH"]
                columns = oparam["COLUMNS"]
                label = oparam["LABEL"]
                destination_file_new = destination_file.parent / f"{label}.CSV"
                df = extract_xml(source_file, xpath)

                # META is the keyword for nested records; if the key META exists in the configuration, it is a nested node
                if "META" in oparam.keys():
                    meta = oparam["META"]
                    record = oparam["RECORD"]
                    df_new = transform_normalize_dict(df, meta, record)
                    load_to_csv(df_new[columns], destination_file_new)
                else:
                    load_to_csv(df[columns], destination_file_new)

def task_upload_files_to_blob():
    blob_client = get_blob_service_client_connection_string()
    files = list(Path("data_dump/processed").glob("SANCTIONS_LIST*.CSV"))

    for f in files:
        upload_blob_file(blob_client, f)