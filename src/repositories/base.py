from abc import ABC, abstractmethod

from ..models import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass
