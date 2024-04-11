import logging

from kazoo.client import KazooClient, KazooState

logging.basicConfig()


def my_listener(state):
    if state == KazooState.LOST:
        logging.warning("Zookeeper session was lost")
    elif state == KazooState.SUSPENDED:
        logging.warning("Disconnected from Zookeeper")
    else:
        logging.info("Connected/reconnected to Zookeeper")


class ZookeeperCounter:
    def __init__(self, hosts, counter_path):
        self.zk = KazooClient(hosts=hosts)
        self.zk.add_listener(my_listener)
        self.counter_path = counter_path

    def connect(self):
        self.zk.start()

    def increment_counter(self):
        # Increment the counter value atomically using Zookeeper's transactional operations
        while True:
            try:
                self.zk.ensure_path(self.counter_path)
                current_value, _ = self.zk.get(self.counter_path)
                new_value = int(current_value) + 1 if current_value else 1
                self.zk.set(self.counter_path, str(new_value).encode())
                return new_value
            except Exception as e:
                # Handle connection errors or other exceptions
                # Implement retry logic if necessary
                logging.error(f"Error incrementing counter: {str(e)}")

    def get_counter_value(self):
        # Retrieve the current value of the counter
        try:
            self.zk.ensure_path(self.counter_path)
            current_value, _ = self.zk.get(self.counter_path)
            return int(current_value) if current_value else 0
        except Exception as e:
            # Handle connection errors or other exceptions
            logging.error(f"Error getting counter value: {str(e)}")
            return None

    def close(self):
        self.zk.stop()
