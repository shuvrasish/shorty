from django.apps import AppConfig

from logger import logger


class ShortnerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shortner"

    def ready(self):
        logger.success(f"Started worker for {self.name}")
