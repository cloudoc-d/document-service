from typing import Optional
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from datetime import datetime
from typing import Annotated
from enum import Enum

from .user import User
from .common import PyObjectId



class DocElement(BaseModel):
    type: str   # maybe enum
    attrs: dict
    content: list[dict]


class DocumentAccessRole(Enum):
    READER = 'reader'
    EDITOR = 'editor'


class DocumentAccessRestriction(BaseModel):
    user_id: str
    role: DocumentAccessRole


class DocumentInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    owner_id: str
    name: str
    is_public: bool = Field(default=False)
    access_restrictions: list[DocumentAccessRestriction] = Field(default=list())
    created_at: datetime
    edited_at: Optional[datetime] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True,
    )


class Document(DocumentInfo):
    content: list[DocElement] = Field(default=[])


class DocumentInfoCollection(BaseModel):
    documents: list[DocumentInfo]
    presented_amount: int
    total_amount: int


class DocumentCreate(BaseModel):
    name: str


class DocumentUpdate(BaseModel):
    name: str | None
