from pydantic import BaseModel, EmailStr
from pydantic.fields import Field
from datetime import datetime
from enum import Enum


class UserRole(Enum):
    ADMIN = 'admin'


class User(BaseModel):
    id: str
    name: str = Field(max_length=32)
    is_active: bool
    email: EmailStr
    roles: list[UserRole]
    created_at: datetime
