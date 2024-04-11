import ast
import logging
import sys

from django.apps import AppConfig
from django.core.cache import cache
from kazoo.client import KazooClient
from kazoo.exceptions import KazooException
from redis.exceptions import AuthenticationError

from config.settings import ZOOKEEPER_HOST, ZOOKEEPER_PORT

logging.basicConfig()


class ShortnerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shortner"

    def ready(self):
        # Connect to ZooKeeper
        try:
            zk = KazooClient(hosts=f"{ZOOKEEPER_HOST}:{ZOOKEEPER_PORT}")
            zk.start()

            # Retrieve list of count ranges
            count_ranges = zk.get_children("/count_ranges")

            # Iterate over count ranges and fetch their data
            logging.info("Connected to zookeeper server, iterating over count ranges.")
            for range_name in count_ranges:
                range_data, _ = zk.get(f"/count_ranges/{range_name}")
                range_data = ast.literal_eval(range_data.decode("utf-8"))

                if range_data.get("status") == "unused":
                    cache.set("range_key", range_name)
                    print("key set", range_name)
                    break
        except AuthenticationError as e:
            print(f"Failed to connect to Redis: {e}")
            sys.exit()
        except KazooException as e:
            # Handle the connection error
            print(f"An error occurred while connecting to ZooKeeper: {e}")
            sys.exit()
        finally:
            # Close the connection
            zk.stop()
