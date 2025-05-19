import asyncio
import typing
import json
from fastapi import WebSocket
from broadcaster import Broadcast
from dataclasses import dataclass
from enum import Enum, auto
from .message_handler import (
    BaseMessageHandler,
    Response,
    ResponseType,
    RequestHandlingException,
)



class WSConnectionManager:
    def __init__(
        self,
        websocket: WebSocket,
        broadcast: Broadcast,
        channel_name: str,
        message_handler: BaseMessageHandler,
    ) -> None:
        self._websocket = websocket
        self._broadcast = broadcast
        self._message_handler = message_handler
        self._channel_name = channel_name

    async def perform(self) -> None:
        await self._websocket.accept()
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._ws_recieve())
            tg.create_task(self._ws_send())

    async def _ws_recieve(self) -> None:
        async for message in self._websocket.iter_text():
            try:
                response = await self._message_handler.handle_message(message)
            except RequestHandlingException as e:
                response = e.get_response()
            if response.response_type is ResponseType.BROADCAST:
                await self._publish_message(response.message)
            elif response.response_type is ResponseType.UNICAST:
                await self._send_message(response.message)

    async def _publish_message(self, message: typing.Any):
        await self._broadcast.publish(
            channel=self._channel_name,
            message=message
        )

    async def _send_message(self, message: typing.Any):
        await self._websocket.send_text(message)

    async def _ws_send(self) -> None:
        async with self._broadcast.subscribe(channel=self._channel_name) as subscriber:
            async for event in subscriber:
                await self._websocket.send_text(event.message)
