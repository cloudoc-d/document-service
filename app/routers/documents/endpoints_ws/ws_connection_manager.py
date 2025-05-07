import asyncio
from fastapi import WebSocket
from broadcaster import Broadcast
from app.models.document import Document
from app.models.editor_events import Event
from .apply_event import apply_event_to_document


class WSConnectionManager:
    def __init__(
        self,
        websocket: WebSocket,
        broadcast: Broadcast,
        document: Document,
    ) -> None:
        self._websocket = websocket
        self._broadcast = broadcast
        self._document_state = document

        self._channel_name = self._get_document_edit_channel_name()

    def _get_document_edit_channel_name(self) -> str:
        return f"document:{self._document_state.id}"

    async def perform(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._ws_recieve())
            tg.create_task(self._ws_send())

    async def _ws_recieve(self) -> None:
        async for message in self._websocket.iter_text():
            await self._handle_message(message)
            await self._broadcast.publish(
                channel=self._channel_name,
                message=message,
            )

    async def _handle_message(self, message: str) -> None:
        event = Event.model_validate_json(message)
        self._document_state = apply_event_to_document(
            event=event,
            document=self._document_state
        )

    async def _ws_send(self) -> None:
        async with self._broadcast.subscribe(channel=self._channel_name) as subscriber:
            async for event in subscriber:
                await self._websocket.send_text(event.message)
