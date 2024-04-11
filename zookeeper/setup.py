from kazoo.client import KazooClient

from config.settings import ZOOKEEPER_PORT

# Connect to ZooKeeper ensemble
hosts = f"zookeeper:{ZOOKEEPER_PORT}"
zk = KazooClient(hosts=hosts)
zk.start()

# Create parent znode for count ranges
zk.ensure_path("/count_ranges")

# Define count ranges and their statuses
count_ranges = {
    "R1": {"start": 1, "end": 10000000, "status": "unused", "current_count": 0},
    "R2": {"start": 10000001, "end": 20000000, "status": "unused", "current_count": 0},
    "R3": {"start": 20000001, "end": 30000000, "status": "unused", "current_count": 0},
    "R4": {"start": 30000001, "end": 40000000, "status": "unused", "current_count": 0},
    "R5": {"start": 40000001, "end": 50000000, "status": "unused", "current_count": 0},
    "R6": {"start": 50000001, "end": 60000000, "status": "unused", "current_count": 0},
    "R7": {"start": 60000001, "end": 70000000, "status": "unused", "current_count": 0},
    "R8": {"start": 70000001, "end": 80000000, "status": "unused", "current_count": 0},
    "R9": {"start": 80000001, "end": 90000000, "status": "unused", "current_count": 0},
    "R10": {"start": 90000001, "end": 100000000, "status": "unused", "current_count": 0},
}

# Create child znodes for each count range
for range_name, range_info in count_ranges.items():
    range_path = f"/count_ranges/{range_name}"
    zk.ensure_path(range_path)
    zk.set(range_path, bytes(str(range_info), "utf-8"))

# Close connection
zk.stop()
