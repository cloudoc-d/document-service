from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field
from .common import PyObjectId


StyleContent = Annotated[str, Field(max_length=1024)]


class StyleInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    public: bool = Field(default=False)
    name: str = Field(max_length=32)
    owner_id: str
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
    poplularity: int = Field(default=0)


class StyleInfoCollection(BaseModel):
    styles: list[StyleInfo]
    presented_amount: int
    total_amount: int


class Style(StyleInfo):
    content: StyleContent


class StyleCreate(BaseModel):
    name: str

class StyleUpdate(BaseModel):
    name: str | None
    content: StyleContent | None
