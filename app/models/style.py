from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field
import app.crud_router.models as crud_models
from .common import PyObjectId


StyleContent = Annotated[str, Field(max_length=1024)]


NameField = Field(max_length=32)


class StyleInfo(crud_models.ReadInfoModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = NameField
    owner_id: str
    created_at: datetime
    is_deleted: bool = Field(default=False)

    public: bool = Field(default=False)
    updated_at: Optional[datetime] = Field(default=None)
    popularity: int = Field(default=0)


class Style(crud_models.ReadContentModel, StyleInfo):
    content: StyleContent


class StyleInfoCollection(crud_models.CollectionModel):
    content: list[StyleInfo]
    presented_amount: int
    total_amount: int


class StyleCreate(crud_models.CreateModel):
    name: str = NameField

class StyleUpdate(BaseModel):
    name: str | None = Field(default=None)
    content: StyleContent | None = Field(default=None)
