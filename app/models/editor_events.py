from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal, Union, Annotated, Any
from app.models.document import DocElementType as BlockType


class EventType(str, Enum):
    BLOCK_CHANGED = "block-changed"
    BLOCK_ADDED = "block-added"
    BLOCK_MOVED = "block-moved"
    BLOCK_REMOVED = "block-removed"
    BLOCK_LOCKED = "block-locked"
    BLOCK_RELEASED = "block-released"


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

class BlockLockedData(BaseModel):
    id: str

class BlockReleasedData(BaseModel):
    id: str

class BlockChangedEvent(BaseModel):
    type: Literal[EventType.BLOCK_CHANGED]
    data: BlockChangedData


class BlockAddedEvent(BaseModel):
    type: Literal[EventType.BLOCK_ADDED]
    data: BlockAddedData


class BlockMovedEvent(BaseModel):
    type: Literal[EventType.BLOCK_MOVED]
    data: BlockMovedData


class BlockRemovedEvent(BaseModel):
    type: Literal[EventType.BLOCK_REMOVED]
    data: BlockRemovedData


class BlockLockedEvent(BaseModel):
    type: Literal[EventType.BLOCK_LOCKED]
    data: BlockLockedData


class BlockReleasedEvent(BaseModel):
    type: Literal[EventType.BLOCK_RELEASED]
    data: BlockReleasedData


class DefaultEvent(BaseModel):
    """Anything that follows general structure"""
    type: str
    data: Any


class UserInfo(BaseModel):
    id: str
    name: str

class Event(BaseModel):
    event: Annotated[
        Union[
            BlockChangedEvent,
            BlockAddedEvent,
            BlockMovedEvent,
            BlockRemovedEvent,
            DefaultEvent
        ],
        Field(union_mode='left_to_right')
    ]
    user: UserInfo | None = Field(default=None)


class EventsCollection(BaseModel):
    events: list[Event]
