import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class CacheConfig(ABC):
    @abstractmethod
    def get_ttl(self) -> int:
        pass


@dataclass
class RedisConfig(CacheConfig):
    unix_socket_path: str = os.getenv("REDIS_SOCKET_PATH")
    cache_ttl: int = int(os.getenv("REDIS_CACHE_TTL"))

    def get_ttl(self) -> int:
        return self.cache_ttl


@dataclass
class PostgresConfig:
    host: str = os.getenv("POSTGRES_HOST")
    port: int = int(os.getenv("POSTGRES_PORT"))
    database: str = os.getenv("POSTGRES_DB")
    user: str = os.getenv("POSTGRES_USER")
    password: str = os.getenv("POSTGRES_PASSWORD")
