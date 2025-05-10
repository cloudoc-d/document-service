from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field
import app.core.crud_router.models as crud_models
from .common import PyObjectId


StyleContent = Annotated[str, Field(max_length=1024)]


NameField = Field(max_length=32)


class StyleInfo(crud_models.ReadInfoModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = NameField
    owner_id: str
    created_at: datetime
    is_deleted: bool = Field(default=False)
    deleted_at: datetime | None = Field(default=None)

    public: bool = Field(default=False)
    updated_at: Optional[datetime] = Field(default=None)
    popularity: int = Field(default=0)


class Style(StyleInfo, crud_models.ReadContentModel):
    content: StyleContent = Field(default="")


class StyleInfoCollection(crud_models.CollectionModel):
    content: list[StyleInfo]
    presented_amount: int
    total_amount: int


class StyleCreate(crud_models.CreateModel):
    name: str = NameField

class StyleUpdate(BaseModel):
    name: str | None = Field(default=None)
    content: StyleContent | None = Field(default=None)
