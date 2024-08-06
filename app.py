from datetime import datetime
from prefect import flow
from scrollguard_etl.utils import logger
from scrollguard_etl.tasks import task_extract_sources, task_transform_sources

@flow(name="scrollguard-main-flow")
def flow_main():
    
    start_time = datetime.now()
    logger.info("ScrollGuard Data Pipeline has started.")
    
    task_extract_sources()
    task_transform_sources()
    
    end_time = datetime.now() - start_time
    logger.info(f"ScrollGuard Data Pipeline has ended. Elapsed: {end_time}.")

if __name__=="__main__":

    flow_main()