from functools import lru_cache

from ..cache.redis import RedisCache
from ..config import PostgresConfig, RedisConfig
from ..repositories.postgres import PostgresUserRepository
from ..services.user_service import UserService


@lru_cache
def get_redis_config() -> RedisConfig:
    return RedisConfig()


@lru_cache
def get_postgres_config() -> PostgresConfig:
    return PostgresConfig()


@lru_cache
def get_cache() -> RedisCache:
    return RedisCache(get_redis_config())


@lru_cache
def get_repository() -> PostgresUserRepository:
    return PostgresUserRepository(get_postgres_config())


@lru_cache
def get_user_service() -> UserService:
    return UserService(
        repository=get_repository(), cache=get_cache(), cache_config=get_redis_config()
    )
