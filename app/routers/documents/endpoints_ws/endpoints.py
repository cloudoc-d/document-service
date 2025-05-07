from fastapi import WebSocket

from app.dependencies.user import ActiveUserAnnotation
from app.dependencies.document import DocumentAnnotation, DocumentUserRoleAnnotation
from app.dependencies.repository import DocumentsRepositoryAnnotation
from app.dependencies.broadcast import BroadcastAnnotation

from .ws_connection_manager import WSConnectionManager

from ..router import router


@router.websocket("/{document_id}/ws")
async def edit_document_ws(
    websocket: WebSocket,
    user: ActiveUserAnnotation,
    document: DocumentAnnotation,
    user_role: DocumentUserRoleAnnotation,
    repository: DocumentsRepositoryAnnotation,
    broadcast: BroadcastAnnotation,
):
    await websocket.accept()

    connection_manager = WSConnectionManager(
        websocket=websocket,
        broadcast=broadcast,
        document=document,
    )
    await connection_manager.perform()
