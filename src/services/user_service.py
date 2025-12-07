import json
from collections.abc import Callable

from ..cache.base import CacheInterface
from ..config import CacheConfig
from ..models import User
from ..repositories.base import UserRepositoryInterface


class UserService:
    def __init__(
        self, repository: UserRepositoryInterface, cache: CacheInterface, cache_config: CacheConfig
    ):
        self.repository = repository
        self.cache = cache
        self.cache_config = cache_config

    def _get_with_cache(
        self, cache_key: str, fetch_func: Callable[[], User | None], use_cache: bool
    ) -> User | None:
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached:
                return User(**json.loads(cached))

        user = fetch_func()

        if user and use_cache:
            self.cache.set(cache_key, user.model_dump_json(), self.cache_config.get_ttl())

        return user

    def get_user_by_id(self, user_id: int, use_cache: bool = True) -> User | None:
        return self._get_with_cache(
            cache_key=f"user:{user_id}",
            fetch_func=lambda: self.repository.get_by_id(user_id),
            use_cache=use_cache,
        )

    def get_user_by_email(self, email: str, use_cache: bool = True) -> User | None:
        return self._get_with_cache(
            cache_key=f"user:email:{email}",
            fetch_func=lambda: self.repository.get_by_email(email),
            use_cache=use_cache,
        )

    def invalidate_cache(self, user_id: int) -> None:
        self.cache.delete(f"user:{user_id}")
