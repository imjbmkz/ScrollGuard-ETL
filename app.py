from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from scrollguard_etl.utils import logger, get_config
from scrollguard_etl.etl import extract_source, extract_from_csv, extract_from_excel, extract_xml, load_to_csv, transform_normalize_dict

if __name__=="__main__":

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

    # Iterate through each data source configuration and get details required
    for src in source_config:
        name = src["NAME"]
        fmt = src["FORMAT"]
        source_file = Path("data_dump/raw") / f"{name}.{fmt}"
        destination_file = Path("data_dump/processed") / f"{name}.CSV"

        if fmt=="CSV":
            params = src["PARAMS"]
            df = extract_from_csv(source_file, params)
            load_to_csv(df, destination_file)

        if fmt=="XLSX":
            params = src["PARAMS"]
            df = extract_from_excel(source_file, params)
            load_to_csv(df, destination_file)

        if fmt=="XML":
            output_params = src["OUTPUTS"]
            for oparam in output_params:
                xpath = oparam["XPATH"]
                columns = oparam["COLUMNS"]
                label = oparam["LABEL"]
                destination_file_new = destination_file.parent / f"{label}.CSV"
                df = extract_xml(source_file, xpath, columns)
                if "META" in oparam.keys():
                    meta = oparam["META"]
                    record = oparam["RECORD"]
                    df_new = transform_normalize_dict(df, meta, record)
                    load_to_csv(df_new, destination_file_new)
                else:
                    load_to_csv(df, destination_file_new)