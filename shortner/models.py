import hashlib

from django.db import models

from config.settings import ZOOKEEPER_HOST, ZOOKEEPER_PORT
from config.zookeeper import ZookeeperCounter

# Create your models here.


class ShortenManagerUtil(models.Manager):
    def _hash_url(self, url: str) -> str:
        url_bytes = url.encode("utf-8")
        sha256_hash = hashlib.sha256()
        sha256_hash.update(url_bytes)
        hashed_url = sha256_hash.hexdigest()
        return hashed_url

    def shorten(self, url: str) -> str:
        zookeeper_hosts = f"{ZOOKEEPER_HOST}:{ZOOKEEPER_PORT}"
        counter_path = "/counters/short_urls"
        counter = ZookeeperCounter(hosts=zookeeper_hosts, counter_path=counter_path)
        counter.connect()

        # Increment the counter
        new_value = counter.increment_counter()
        print(f"New counter value: {new_value}")

        # Get the current counter value
        current_value = counter.get_counter_value()
        print(f"Current counter value: {current_value}")

        # Close the Zookeeper connection
        counter.close()


class UrlsManager(ShortenManagerUtil):
    pass


class URLS(models.Model):
    id = models.AutoField(primary_key=True)
    original_url = models.CharField(max_length=2048)
    shortcode = models.CharField(max_length=7, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UrlsManager()

    class Meta:
        db_table = '"shortner"."urls"'
        indexes = [models.Index(fields=["shortcode"], name="shortner_urls_shortcode_idx")]
