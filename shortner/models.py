import hashlib

from django.db import models

# Create your models here.


class ShortenManagerUtil(models.Manager):
    def _hash_url(self, url: str) -> str:
        url_bytes = url.encode("utf-8")
        sha256_hash = hashlib.sha256()
        sha256_hash.update(url_bytes)
        hashed_url = sha256_hash.hexdigest()
        return hashed_url

    def shorten(self, url: str) -> str:
        hashed_url = self._hash_url(url)
        return hashed_url[:7]


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
