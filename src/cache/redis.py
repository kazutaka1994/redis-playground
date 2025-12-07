import redis

from ..config import RedisConfig
from .base import CacheInterface


class RedisCache(CacheInterface):
    def __init__(self, config: RedisConfig):
        self.config = config
        self.client = redis.Redis(unix_socket_path=config.unix_socket_path, decode_responses=True)

    def get(self, key: str) -> str | None:
        return self.client.get(key)

    def set(self, key: str, value: str, ttl: int) -> None:
        self.client.setex(key, ttl, value)

    def delete(self, key: str) -> None:
        self.client.delete(key)

    def clear(self) -> None:
        self.client.flushdb()
