from fastapi import (
    Request, WebSocket, HTTPException,
    WebSocketException, Depends
)
import enum
import typing

class ConnectionContext(enum.Enum):
    WEBSOCKET = "websocket"
    HTTP = "http"


def get_context_based_exception(
    context: ConnectionContext,
    http_code: int,
    ws_code: int,
    message: str,
) -> Exception:
    if context is ConnectionContext.WEBSOCKET:
        return WebSocketException(
            code=ws_code,
            reason=message,
        )
    if context is ConnectionContext.HTTP:
        return HTTPException(
            status_code=http_code,
            detail=message,
        )


def _context_dependency(
    request: Request = None,
    websocket: WebSocket = None,
) -> ConnectionContext:
    if websocket:
        return ConnectionContext.WEBSOCKET
    if request:
        return ConnectionContext.HTTP


ContextAnnotation = typing.Annotated[ConnectionContext, Depends(_context_dependency)]
