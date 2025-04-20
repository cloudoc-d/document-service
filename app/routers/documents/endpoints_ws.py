from fastapi import (
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status
)
from bson import ObjectId

from app.models.editor_events import Event, EventsCollection
from app.database import documents_collection as collection
from app.models.document import (
    Document,
    DocumentAccessRestriction,
    DocumentAccessRole,
)
from app.models.user import User
from app.broadcast import broadcast
from app.routers.auth_utils import ActiveUserAnnotation
from app.redis import redis_client
from app.routers.cache import get_document, set_document_in_cache

from .router import router

import anyio


@router.websocket("/{document_id}/ws")
async def edit_document_ws(
    websocket: WebSocket,
    user: ActiveUserAnnotation,
    document_id: str,
):
    document = await get_document(document_id)
    if document is None:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="document not found"
        )

    role = get_access_role_to_document(document, user)
    if role is None:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="access forbidden"
        )

    channel_name = get_document_channel_name(document)

    async with anyio.create_task_group() as task_group:
        async def run_ws_receiver() -> None:
            await ws_receiver(
                document_id=document_id,
                websocket=websocket,
                channel_name=channel_name
            )
            task_group.cancel_scope.cancel()

        if role == DocumentAccessRole.EDITOR:
            task_group.start_soon(run_ws_receiver)
        await ws_sender(websocket)


def get_access_role_to_document(
    document: Document,
    user: User
) -> DocumentAccessRole | None:
    # raises WebSocketException

    if document.owner_id == user.id:
        return DocumentAccessRole.EDITOR

    for rule in document.access_restrictions:
        if user.id == rule.user_id:
            return rule.role


def get_document_channel_name(document: Document) -> str:
    return f'doc-{document.id}'


async def ws_receiver(
    websocket: WebSocket,
    channel_name: str,
    document_id: str,
):
    async for message in websocket.iter_text():
        event = Event.model_validate_json(message)
        await push_event_to_stack(document_id, event)
        await apply_event_to_document(document_id, event)
        await broadcast.publish(
            channel=channel_name,
            message=event.model_dump(by_alias=True)
        )

async def apply_event_to_document(document_id: str, event: Event) -> None:
    document: Document = await get_document(document_id)

    # TODO add some kind of validation. Not edit straightforward
    from app.models.document import DocElement

    if event.type == "block-removed":
        document.content.pop(event.data.index)
    elif event.type == "block-changed":
        document.content[event.data.index].data = event.data.data
    elif event.type == "block-added":
        document.content.insert(
            event.data.index,
            DocElement(
                type=event.data.type.value,
                attrs={},
                data={},
            )
        )
    elif event.type == "block-moved":
        document.content.insert(
            event.data.to_index,
            document.content.pop(event.data.from_index)
        )

    set_document_in_cache(document_id, document)


async def push_event_to_stack(document_id: str, event: Event) -> None:
    event_stack_name = get_event_stack_name(document_id)
    event_stack_str: str | None = redis_client.get(event_stack_name)

    events_collection = None
    if event_stack_str is None:
        events_collection = EventsCollection(events=[])
    else:
        events_collection = EventsCollection \
            .model_validate_json(event_stack_str)

    events_collection.append(event)
    redis_client.set(event_stack_name, events_collection.json())


def get_event_stack_name(document_id: str) -> str:
    return f"event_stack:{document_id}"


async def ws_sender(
    websocket: WebSocket,
    channel_name: str
):
    async with broadcast.subscribe(channel=channel_name) as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)
