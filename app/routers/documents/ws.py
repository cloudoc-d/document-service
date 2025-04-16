from fastapi import (
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status
)
from bson import ObjectId

from app.models.editor_events import Event
from app.database import documents_collection as collection
from app.models.document import (
    Document,
    DocumentAccessRestriction,
    DocumentAccessRole,
)
from app.models.user import User
from app.broadcast import broadcast
from app.auth_utils import ActiveUserAnnotation

from .router import router

import anyio


async def get_document(document_id: str) -> Document:
    # raises WebSocketException
    doc = await collection.find_one(
        {'_id': ObjectId(document_id)}
    )
    if doc is None:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="document not found"
        )

    return Document.validate(doc)

async def get_access_role_to_document(
    document: Document,
    user: User
) -> DocumentAccessRole:
    # raises WebSocketException

    if document.owner_id == user.id:
        return DocumentAccessRole.EDITOR

    for rule in document.access_restrictions:
        if user.id == rule.user_id:
            return rule.role

    raise WebSocketException(
        code=status.WS_1008_POLICY_VIOLATION,
        reason="access forbidden"
    )


def get_document_channel_name(document: Document) -> str:
    return f'doc-{document.id}'


@router.websocket("/{document_id}/ws")
async def edit_document_ws(
    websocket: WebSocket,
    user: ActiveUserAnnotation,
    document_id: str,
):
    document = await get_document(document_id)
    role = await get_access_role_to_document(document, user)

    channel_name = get_document_channel_name(document)

    async with anyio.create_task_group() as task_group:
        async def run_ws_receiver() -> None:
            await ws_receiver(
                websocket=websocket,
                channel_name=channel_name
            )
            task_group.cancel_scope.cancel()

        if role == DocumentAccessRole.EDITOR:
            task_group.start_soon(run_ws_receiver)
        await ws_sender(websocket)


async def ws_receiver(
    websocket: WebSocket,
    channel_name: str,
):
    async for message in websocket.iter_text():
        event = Event.model_validate_json(message)
        await broadcast.publish(
            channel=channel_name,
            message=event.model_dump(by_alias=True)
        )


async def ws_sender(
    websocket: WebSocket,
    channel_name: str
):
    async with broadcast.subscribe(channel=channel_name) as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)
