from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime | None = None

    class Config:
        from_attributes = True

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: int) -> int:
        """
        Validate that ID is a positive integer (>= 1).
        """
        if v < 1:
            raise ValueError("ID must be a positive integer (>= 1)")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        Validate name:
        - Cannot be empty or whitespace only
        - Cannot contain control characters (ASCII 0-31, 127)
        - Must be 50 characters or less
        - Automatically trims leading/trailing whitespace
        """
        # Check for control characters before trimming
        # ASCII control characters: 0-31 (except space, tab, newline, carriage return) and 127 (DEL)
        for c in v:
            code = ord(c)
            if (code < 32 and c not in (" ", "\t", "\n", "\r")) or code == 127:
                raise ValueError("Name cannot contain control characters")

        # Trim whitespace
        trimmed = v.strip()

        # Check if empty after trimming
        if not trimmed:
            raise ValueError("Name cannot be empty or whitespace only")

        # Check length
        if len(trimmed) > 50:
            raise ValueError("Name must be 50 characters or less")

        return trimmed

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
