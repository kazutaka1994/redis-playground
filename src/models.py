from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime | None = None

    class Config:
        from_attributes = True

    def __eq__(self, other: object) -> bool:
        """
        Entity identity: Users with the same ID are considered equal.
        """
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Entity hash: ID-based hashing.
        Allows User to be used in Set or as Dict keys.
        """
        return hash(self.id)
