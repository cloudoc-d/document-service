from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal, Union, Annotated
from app.models.document import DocElementType as BlockType


class BlockChangedData(BaseModel):
    index: int
    data: dict
    id: str
    type: BlockType


class BlockAddedData(BaseModel):
    index: int
    id: str
    type: BlockType


class BlockMovedData(BaseModel):
    from_index: int = Field(alias='fromIndex')
    to_index: int = Field(alias='toIndex')
    id: str

class BlockRemovedData(BaseModel):
    index: int
    id: str


class BlockChangedEvent(BaseModel):
    type: Literal["block-changed"]
    data: BlockChangedData


class BlockAddedEvent(BaseModel):
    type: Literal["block-added"]
    data: BlockAddedData


class BlockMovedEvent(BaseModel):
    type: Literal["block-moved"]
    data: BlockMovedData


class BlockRemovedEvent(BaseModel):
    type: Literal["block-removed"]
    data: BlockRemovedData


class Event(BaseModel):
    event: Annotated[
        Union[
            BlockChangedEvent,
            BlockAddedEvent,
            BlockMovedEvent,
            BlockRemovedEvent
        ],
        Field(discriminator='type')
    ]


class EventsCollection(BaseModel):
    events: list[Event]
