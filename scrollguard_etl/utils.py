import sys
import json
import requests
import urllib3
import ssl
from loguru import logger

logger.remove(0)
logger.add(sys.stdout, level="INFO")
logger.add(sys.stderr, level="ERROR")
logger.add("logs/{time:YYYY_MM_DD}/std_out_.log", rotation="1 day", level="DEBUG")
logger.add("logs/{time:YYYY_MM_DD}/std_err.log", rotation="1 day", level="ERROR")

class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount("https://", CustomHttpAdapter(ctx))
    return session

def get_config() -> dict:
    with open("config/config.json") as fp:
        return json.load(fp)