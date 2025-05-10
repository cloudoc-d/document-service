from fastapi import WebSocket

from app.dependencies.user import ActiveUserAnnotation
from app.dependencies.document import DocumentAnnotation, DocumentUserRoleAnnotation
from app.dependencies.repository import DocumentsRepositoryAnnotation
from app.dependencies.broadcast import BroadcastAnnotation

from app.core.ws_connection_manager import WSConnectionManager

from .message_handler import MessageHandler
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
    message_handler = MessageHandler(
        document_id=document.id,
        repository=repository,
        user=user,
    )
    connection_manager = WSConnectionManager(
        websocket=websocket,
        broadcast=broadcast,
        channel_name=f"document-edit:{document.id}",
        message_handler=message_handler,
    )
    await connection_manager.perform()
