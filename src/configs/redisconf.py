import os

from django.conf import settings
from redis import Redis

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")


def get_connection() -> Redis:
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
        decode_responses=True,
        unix_socket_path="/tmp/redis.sock",
    )
