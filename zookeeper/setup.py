import sys

from kazoo.client import KazooClient

from config.constants import ZOOKEEPER_COUNT_RANGES_PATH
from config.settings import ZOOKEEPER_PORT
from logger import logger


def initialize_zookeeper_state():
    # Connect to ZooKeeper ensemble
    hosts = f"zookeeper:{ZOOKEEPER_PORT}"
    zk = KazooClient(hosts=hosts)
    zk.start()

    logger.success(f"Connected to zookeeper running at port: {ZOOKEEPER_PORT} successfully")

    # Create parent znode for count ranges
    path_to_check = ZOOKEEPER_COUNT_RANGES_PATH

    # Check if the path already exists in ZooKeeper
    if zk.exists(path_to_check):
        logger.warning(f"The path {path_to_check} already exists. Stopping further execution.")
        zk.stop()  # Close connection
        sys.exit()
    else:
        logger.info(f"The path {path_to_check} does not exist. Proceeding with creating the znodes.")
        zk.ensure_path(f"{path_to_check}")

        # Define count ranges and their statuses
        count_ranges = {
            "R1": {"start": 1, "end": 10000000, "in_use": False, "current_count": 0},
            "R2": {"start": 10000001, "end": 20000000, "in_use": False, "current_count": 10000000},
            "R3": {"start": 20000001, "end": 30000000, "in_use": False, "current_count": 20000000},
            "R4": {"start": 30000001, "end": 40000000, "in_use": False, "current_count": 30000000},
            "R5": {"start": 40000001, "end": 50000000, "in_use": False, "current_count": 40000000},
            "R6": {"start": 50000001, "end": 60000000, "in_use": False, "current_count": 50000000},
            "R7": {"start": 60000001, "end": 70000000, "in_use": False, "current_count": 60000000},
            "R8": {"start": 70000001, "end": 80000000, "in_use": False, "current_count": 70000000},
            "R9": {"start": 80000001, "end": 90000000, "in_use": False, "current_count": 80000000},
        }

        # Create child znodes for each count range
        for range_name, range_info in count_ranges.items():
            range_path = f"{path_to_check}/{range_name}"
            zk.ensure_path(range_path)
            zk.set(range_path, bytes(str(range_info), "utf-8"))

        # Close connection
        logger.success(f"Znodes created successfully at path: {path_to_check}")
        zk.stop()


if __name__ == "__main__":
    initialize_zookeeper_state()
