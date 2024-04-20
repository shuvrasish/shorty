import ast
import sys

from django.core.cache import cache
from kazoo.client import KazooClient

from config.constants import CACHE_RANGE_KEY, ZOOKEEPER_COUNT_RANGES_PATH
from config.settings import ZOOKEEPER_HOST, ZOOKEEPER_PORT
from logger import logger

zk_client = None


def register_server() -> bool:
    """Register the server with ZooKeeper and cache the assigned range."""
    global zk_client
    zk_client = KazooClient(hosts=f"{ZOOKEEPER_HOST}:{ZOOKEEPER_PORT}")
    zk_client.start()

    count_ranges = zk_client.get_children(ZOOKEEPER_COUNT_RANGES_PATH)
    logger.success("Connected to ZooKeeper server!")
    cache.clear()
    logger.info("Cleared Cache")
    for range_name in count_ranges:
        range_path = f"{ZOOKEEPER_COUNT_RANGES_PATH}/{range_name}"
        try:
            range_data, _ = zk_client.get(range_path)
            range_data = ast.literal_eval(range_data.decode("utf-8"))
            if not range_data.get("in_use"):
                range_data["in_use"] = True
                zk_client.set(range_path, bytes(str(range_data), "utf-8"))
                cache.set(CACHE_RANGE_KEY, range_name)
                logger.info(f"Range Key set: {range_name}")
                return True
        except Exception as e:
            logger.error("Error while registering server: %s", str(e))

    logger.error("No unused ranges available, exiting.")
    zk_client.stop()
    return False


def deregister_server():
    """Deregister the server from ZooKeeper and remove the cached range."""
    logger.info("Deregistering server")

    range_name = cache.get(CACHE_RANGE_KEY)
    if range_name is None:
        logger.info("Range name not found in cache, skipping deregistration.")
        return

    try:
        cache.delete(CACHE_RANGE_KEY)
        range_path = f"{ZOOKEEPER_COUNT_RANGES_PATH}/{range_name}"
        range_data, _ = zk_client.get(range_path)
        range_data = ast.literal_eval(range_data.decode("utf-8"))
        range_data["in_use"] = False
        zk_client.set(range_path, bytes(str(range_data), "utf-8"))
        logger.success("Server deregistered successfully")
    except Exception as e:
        logger.error("Error while deregistering server: %s", str(e))

    zk_client.stop()
    print("Exiting application")
    sys.exit()
