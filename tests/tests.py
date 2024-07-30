from pathlib import Path
from scrollguard_etl.utils import logger

def test_logger():
    logger.info("Test info log")
    logger.error("Test error log")