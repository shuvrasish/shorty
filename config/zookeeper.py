import ast
import sys

from django.core.cache import cache
from kazoo.client import KazooClient, KazooState

from config.constants import CACHE_RANGE_KEY, ZOOKEEPER_COUNT_RANGES_PATH
from config.settings import ZOOKEEPER_HOST, ZOOKEEPER_PORT
from logger import logger


def my_listener(state):
    if state == KazooState.LOST:
        logger.warning("Zookeeper session was lost")
    elif state == KazooState.SUSPENDED:
        logger.warning("Disconnected from Zookeeper")
    else:
        logger.info("Connected/reconnected to Zookeeper")


class ZookeeperCounter:
    def __init__(self):
        self.zk = KazooClient(hosts=f"{ZOOKEEPER_HOST}:{ZOOKEEPER_PORT}")
        self.zk.add_listener(my_listener)
        range_key = cache.get(CACHE_RANGE_KEY)
        self.counter_path = f"{ZOOKEEPER_COUNT_RANGES_PATH}/{range_key}"

    def connect(self) -> None:
        self.zk.start()

    def increment_counter(self) -> None:
        try:
            range_data, _ = self.zk.get(self.counter_path)
            range_data = ast.literal_eval(range_data.decode("utf-8"))
            current_value = range_data["current_count"]
            max_value = range_data["end"]
            new_value = int(current_value) + 1 if current_value else 1
            if new_value > max_value:
                raise Exception("Server has reached its limit in counter. Shutting down.")
            range_data["current_count"] = new_value
            self.zk.set(self.counter_path, bytes(str(range_data), "utf-8"))
        except Exception as e:
            logger.error(f"Error incrementing counter: {str(e)}")
            sys.exit("Exiting...")

    def get_counter_value(self) -> int:
        # Retrieve the current value of the counter
        try:
            range_data, _ = self.zk.get(self.counter_path)
            range_data = ast.literal_eval(range_data.decode("utf-8"))
            current_value = range_data["current_count"]
            return int(current_value)
        except Exception as e:
            # Handle connection errors or other exceptions
            logger.error(f"Error getting counter value: {str(e)}")
            return None

    def close(self) -> None:
        self.zk.stop()
