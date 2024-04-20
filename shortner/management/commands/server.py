import sys

from django.core.management.base import BaseCommand

from shortner.register_app_server import deregister_server, register_server


class Command(BaseCommand):
    help = "Register and deregister the server with ZooKeeper"

    def add_arguments(self, parser):
        parser.add_argument("action", type=str, choices=["register", "deregister"])

    def handle(self, *args, **options):
        action = options["action"]
        if action == "register":
            registered = register_server()
            if not registered:
                sys.exit("Could not register app server. Exiting...")
        elif action == "deregister":
            deregister_server()
