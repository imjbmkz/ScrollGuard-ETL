import sys
import json
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add(sys.stderr, level="ERROR")
logger.add("logs/std_out_{time:YYYY_MM_DD}.log", rotation="1 day", level="DEBUG")
logger.add("logs/std_err_{time:YYYY_MM_DD}.log", rotation="1 day", level="ERROR")

def get_config() -> dict:
    with open("config/config.json") as fp:
        return json.load(fp)