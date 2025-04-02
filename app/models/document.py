from typing import Optional
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from datetime import datetime
from typing import Annotated

from .user import User

PyObjectId = Annotated[str, BeforeValidator(str)]


class DocElement(BaseModel):
    type: str   # maybe enum
    attrs: dict
    content: list[dict]


class DocumentInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    owner_id: str
    name: str
    created_at: datetime
    edited_at: Optional[datetime] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True,
    )


class Document(DocumentInfo):
    content: list[DocElement] = Field(default=[])


class DocumentInfoCollection(BaseModel):
    documents: list[DocumentInfo]


class DocumentCreate(BaseModel):
    name: str


class DocumentUpdate(BaseModel):
    name: str
