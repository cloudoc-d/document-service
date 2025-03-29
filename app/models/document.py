from pydantic import BaseModel, Field
from datetime import datetime

from .user import User


class DocElement(BaseModel):
    type: str   # maybe enum
    attrs: dict
    content: list[dict]


class Document(BaseModel):
    owner: User
    content: list[DocElement]
    created_at: datetime
    edited_at: datetime
