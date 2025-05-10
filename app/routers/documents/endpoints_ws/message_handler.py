import typing
import json
from abc import ABC, abstractmethod
from app.models.editor_events import (
    Event, UserInfo, EventType
)
from app.models.document import Document, DocElement
from app.models.user import User
from app.core.repository.base import BaseRepository
from app.core.lock_manager import (
    LockManager,
    AlreadyLockedException,
    UnauthorizedReleaseException
)
from app.redis import redis_client
from enum import Enum, auto
from dataclasses import dataclass


class ResponseType(Enum):
    UNICAST = auto()
    BROADCAST = auto()


@dataclass
class Response:
    message: str | dict
    response_type: ResponseType


class _ErrorType(Enum):
    BLOCK_ALREADY_LOCKED = 'block-already-locked'
    RELEASE_DENIED = 'release-denied'
    UNABLE_TO_HANDLE = 'unable-to-handle'


class BaseMessageHandler(ABC):
    @abstractmethod
    async def handle_message(self, message: str) -> Response: ...


_event_handlers = {}    # TODO (((
class MessageHandler(BaseMessageHandler):
    _event_handlers = _event_handlers

    def event_handler(
        event_type: str,
    ) -> typing.Callable:
        def wrapper(func: typing.Callable[..., Response]):
            _event_handlers[event_type] = func
            return func
        return wrapper

    def __init__(
        self,
        document_id: str,
        repository: BaseRepository,
        user: User,
    ) -> None:
        self._lock_manager = LockManager(
            resource_namespace=document_id,
            redis_client=redis_client,
        )
        self._user = user
        self._document_id = document_id
        self._repository = repository

        self._event_user_info = UserInfo(
            id=self._user.id,
            name=self._user.name,
        )

    async def handle_message(self, message: str) -> Response:
        event_model = Event.model_validate_json(message)

        handler_function = self._event_handlers.get(event_model.event.type)
        if handler_function is None:
            return Response(
                response_type=ResponseType.UNICAST,
                message=self._get_error_message_json(
                    error_type=_ErrorType.UNABLE_TO_HANDLE,
                    detail="unable to handle event"
                )
            )

        response = await handler_function(self, event_model)
        return response

    @event_handler(EventType.BLOCK_LOCKED)
    async def _handle_block_locked_event(self, event_model: Event) -> Response:
        try:
            await self._lock_manager.lock(
                resource_id=event_model.event.data.id,
                user_id=self._user.id,
            )
            event_model.user = self._event_user_info
            return Response(
                response_type=ResponseType.BROADCAST,
                message=event_model.model_dump_json()
            )
        except AlreadyLockedException:
            return Response(
                response_type=ResponseType.UNICAST,
                message=self._get_error_message_json(
                    error_type=_ErrorType.BLOCK_ALREADY_LOCKED,
                    detail="block is locked by another user",
                )
            )

    @event_handler(EventType.BLOCK_RELEASED)
    async def _handle_block_released_event(self, event_model: Event) -> Response:
        try:
            await self._lock_manager.release(
                resource_id=event_model.event.data.id,
                user_id=self._user.id
            )
            event_model.user = self._event_user_info
            return Response(
                response_type=ResponseType.BROADCAST,
                message=event_model.model_dump_json()
            )
        except UnauthorizedReleaseException:
            return Response(
                response_type=ResponseType.UNICAST,
                message=self._get_error_message_json(
                    error_type=_ErrorType.RELEASE_DENIED,
                    detail="block is locked by another user"
                )
            )

    @event_handler(EventType.BLOCK_ADDED)
    async def _handle_block_added_event(self, event_model: Event) -> Response:
        ...

    def _get_error_message_json(self, error_type: _ErrorType, detail: str) -> str:
        return json.dumps(
            {"error": {"type": error_type.value, "detail": detail}}
        )
