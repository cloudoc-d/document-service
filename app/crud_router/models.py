from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any


class ReadInfoModel(BaseModel):
    id: Any | None = Field(default=None)
    name: str
    owner_id: Any
    created_at: datetime
    is_deleted: bool


class ReadContentModel(ReadInfoModel):
    content: Any | None


class CollectionModel(BaseModel):
    total_amount: int
    presented_amount: int
    content: list[ReadInfoModel]


class CreateModel(BaseModel):
    name: str
