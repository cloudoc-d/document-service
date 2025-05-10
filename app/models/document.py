from typing import Optional
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from datetime import datetime
from typing import Annotated
from enum import Enum
import app.core.crud_router.models as crud_models

from .user import User
from .common import PyObjectId


class DocElementType(str, Enum):
    PARAGRAPH = 'paragraph'
    HEADER = 'header'


class DocElement(BaseModel):
    type: DocElementType
    attrs: dict
    data: dict  # NOTE No validation ? (


class DocumentAccessRole(str, Enum):
    READER = 'reader'
    EDITOR = 'editor'


class DocumentAccessRestriction(BaseModel):
    user_id: str
    role: DocumentAccessRole


class DocumentInfo(crud_models.ReadInfoModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    owner_id: str
    created_at: datetime
    is_deleted: bool = Field(default=False)
    deleted_at: datetime | None = Field(default=None)

    style_id: Optional[PyObjectId] = Field(default=None)
    is_public: bool = Field(default=False)
    access_restrictions: list[DocumentAccessRestriction] = Field(default=list())
    edited_at: Optional[datetime] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True,
    )


class Document(DocumentInfo, crud_models.ReadContentModel):
    content: list[DocElement] = Field(default=[])


class DocumentInfoCollection(crud_models.CollectionModel):
    content: list[DocumentInfo]
    presented_amount: int
    total_amount: int


class DocumentCreate(crud_models.CreateModel):
    name: str


class DocumentUpdate(BaseModel):
    name: str | None = Field(default=None)
    style_id: str | None = Field(default=None)
