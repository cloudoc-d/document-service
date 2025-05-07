# module for applying incoming event's to Document model.

from app.models.editor_events import (
    Event,
    BlockAddedEvent,
    BlockMovedEvent,
    BlockRemovedEvent,
)
from app.models.document import Document, DocElement
import typing
import pydantic


_event_handlers = dict()


def event_handler(
    event_type: typing.Type,
) -> typing.Callable:
    def wrapper(func: typing.Callable[[typing.Any, Document], Document]):
        _event_handlers[event_type] = func
        return func
    return wrapper


@event_handler(BlockAddedEvent)
def handle_added_event(event: BlockAddedEvent, document: Document) -> Document:
    document.content.insert(
        event.data.index,
        DocElement(
            type=event.data.type.value,
            attrs={},
            data={},
        )
    )
    return document


@event_handler(BlockMovedEvent)
def handle_moved_event(event: BlockMovedEvent, document: Document) -> Document:
    document.content.insert(
        event.data.to_index,
        document.content.pop(event.data.from_index)
    )
    return document


@event_handler(BlockRemovedEvent)
def handle_remove_event(event: BlockRemovedEvent, document: Document) -> Document:
    document.content.pop(event.data.index)
    return document


def apply_event_to_document(event: Event, document: Document) -> Document:
    return _event_handlers[type(event.event)](event.event, document)
