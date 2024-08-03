import sys
import json
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add(sys.stderr, level="ERROR")
logger.add("logs/{time:YYYY_MM_DD}/std_out_.log", rotation="1 day", level="DEBUG")
logger.add("logs/{time:YYYY_MM_DD}/std_err.log", rotation="1 day", level="ERROR")

def get_config() -> dict:
    with open("config/config.json") as fp:
        return json.load(fp)