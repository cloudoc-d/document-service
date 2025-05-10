from abc import ABC, abstractmethod
import typing


class BaseRepository(ABC):
    @abstractmethod
    async def get_documents(
        self,
        owner_id: typing.Any,
        limit: int,
        offset: int,
        name: str | None,
        exclude_fields: list[str] | None,
    ) -> list[dict]:
        ...

    @abstractmethod
    async def count_documents(
        self,
        owner_id: typing.Any,
        name: str | None,
    ) -> int:
        ...

    @abstractmethod
    async def get_document(
        self,
        id: typing.Any,
        owner_id: typing.Any | None,
    ) -> dict | None:
        ...

    @abstractmethod
    async def insert_document(
        self,
        document: dict,
    ) -> dict:
        ...

    @abstractmethod
    async def update_document(
        self,
        id: typing.Any,
        changes: dict[str, typing.Any],
        owner_id: typing.Any
    ) -> dict | None:
        ...

    @abstractmethod
    async def delete_document(
        self,
        id: typing.Any,
        owner_id: typing.Any,
    ) -> bool:
        ...

    @abstractmethod
    async def mark_document_as_deleted(
        self,
        id: typing.Any,
        owner_id: typing.Any,
    ) -> dict | None:
        ...
