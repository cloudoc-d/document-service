from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal, Union


class BlockType(Enum):
    PARAGRAPH = 'paragraph'



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
    type: Literal["block-removec"]
    data: BlockRemovedData


Event = Union[
    BlockChangedEvent,
    BlockAddedEvent,
    BlockMovedEvent,
    BlockRemovedEvent
]
