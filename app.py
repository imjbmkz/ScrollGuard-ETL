from datetime import datetime
from dotenv import load_dotenv
from scrollguard_etl.utils import logger, get_blob_service_client_connection_string
from scrollguard_etl.tasks import task_extract_sources, task_transform_sources, task_upload_files_to_blob

def flow_main():

    load_dotenv()
    
    start_time = datetime.now()
    logger.info("ScrollGuard Data Pipeline has started.")
    
    task_extract_sources()
    task_transform_sources()
    task_upload_files_to_blob()
    
    end_time = datetime.now() - start_time
    logger.info(f"ScrollGuard Data Pipeline has ended. Elapsed: {end_time}.")

if __name__=="__main__":

    flow_main()
    print(get_blob_service_client_connection_string())