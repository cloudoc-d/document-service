import typing
import json
from abc import ABC, abstractmethod
from app.core import repository
from app.core.message_handler import (
    BaseMessageHandler, ResponseType, Response, RequestHandlingException
)
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


class BlockAlreadyLockedException(RequestHandlingException):
    exception_id = 'block-already-locked'

class BlockAccessDeniedException(RequestHandlingException):
    exception_id = 'block-access-denied'

class BlockReleaseDeniedException(RequestHandlingException):
    exception_id = 'block-release-denied'

class UnableToHandleException(RequestHandlingException):
    exception_id = 'unable-to-handle'

class DocumentDeletedException(RequestHandlingException):
    exception_id = 'document-deleted'

class DocumentNotFoundException(RequestHandlingException):
    exception_id = 'document-not-found'


_event_handlers = {}    # TODO (((


class MessageHandler(BaseMessageHandler):
    _event_handlers = _event_handlers

    def event_handler(
        event_type: str | typing.Iterable[str],
    ) -> typing.Callable:
        def wrapper(func: typing.Awaitable[Response]):
            if isinstance(event_type, str):
                _event_handlers[event_type] = func
            else:
                for etype in event_type:
                    _event_handlers[etype] = func
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
            raise UnableToHandleException("unable to handle event")

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
            raise BlockAlreadyLockedException("block is locked by another user")

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
            raise BlockReleaseDeniedException("block is locked by another user")

    @event_handler(EventType.BLOCK_ADDED)
    async def _handle_block_added_event(self, event_model: Event) -> Response:
        await self._check_block_locked_by_user(event_model.event.data.id)
        document_model = await self._get_not_deleted_document()
        document_model.content.insert(
            event_model.event.data.index,
            DocElement(
                type=event_model.event.data.type.value,
                attrs={},
                data={}
            )
        )
        self._repository.update_document(
            id=self._document_id,
            changes=document_model.model_dump(include=("content"))
        )
        event_model.user = self._event_user_info

        return Response(
            response_type=ResponseType.BROADCAST,
            message=event_model.model_dump_json(),
        )


    @event_handler(EventType.BLOCK_MOVED)
    async def _handle_block_moved_event(self, event_model: Event) -> Response:
        await self._check_block_locked_by_user(event_model.event.data.id)
        document_model = await self._get_not_deleted_document(self._document_id)
        document_model.content.insert(
            event_model.event.data.to_index,
            document_model.content.pop(event_model.event.data.from_index)
        )
        event_model.user = self._event_user_info

        return Response(
            response_type=ResponseType.BROADCAST,
            message=event_model.model_dump_json()
        )


    @event_handler(EventType.BLOCK_REMOVED)
    async def _handle_block_removed_event(self, event_model: Event) -> Response:
        await self._check_block_locked_by_user(event_model.event.data.id)
        document_model = await self._get_not_deleted_document(self._document_id)
        document_model.content.pop(event_model.event.data.index)
        event_model.user = self._event_user_info

        return Response(
            response_type=ResponseType.BROADCAST,
            message=event_model.model_dump_json()
        )

    @event_handler(EventType.BLOCK_CHANGED)
    async def _handle_block_changed_event(self, event_model: Event) -> Response:
        await self._check_block_locked_by_user(event_model.event.data.id)
        document_model = await self._get_not_deleted_document(self._document_id)

        # TODO

    async def _check_block_locked_by_user(self, block_id: str) -> None:
        if not await self._lock_manager.is_locked_by(
            resource_id=block_id,
            user_id=self._user.id
        ):
            raise BlockAccessDeniedException(
                "block must be locked before accessing"
            )

    async def _get_not_deleted_document(self) -> Document:
        document: dict | None = await self._repository.get_document(id=self._document_id)
        if document is None:
            raise DocumentNotFoundException()
        document_model = Document.model_validate(document)
        if document_model.is_deleted:
            raise DocumentDeletedException(
                "Document deleted. Restore it before applying changes"
            )
        return document_model
