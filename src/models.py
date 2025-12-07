from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime | None = None

    class Config:
        from_attributes = True
