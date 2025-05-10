from typing import Protocol, Type, Callable, Annotated, Optional, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from ..repository.base import BaseRepository
from .models import (
    ReadContentModel,
    CreateModel,
    ReadInfoModel,
    CollectionModel,
)


class UserProtocol(Protocol):
    @property
    def id() -> str: ...


class CRUDRouter:
    def __init__(
        self,
        prefix: str,
        tags: list[str],
        repository: BaseRepository,
        user_dependency: Callable[..., UserProtocol],
        read_schema: Type[ReadContentModel],
        create_schema: Type[CreateModel],
        update_schema: Type[BaseModel],
        read_info_schema: Type[ReadInfoModel],
        collection_schema: Type[CollectionModel],
        schema_name: str = "document",
        default_content: Any | None = None,
        id_type: Type = str,
    ) -> None:
        self._repository = repository
        self._user_dependency = user_dependency

        self._create_schema = create_schema
        self._update_schema = update_schema
        self._read_info_schema = read_info_schema
        self._base_schema = read_schema
        self._collection_schema = collection_schema

        self._default_content = default_content
        self._schema_name = schema_name
        self._id_type = id_type

        self.router = APIRouter(prefix=prefix, tags=tags)
        self.router.add_api_route

        self._add_routes()

    def _add_routes(self):
        self._add_read_all_route()
        self._add_create_route()
        self._add_update_route()
        self._add_read_route()
        self._add_delete_route()


    def _add_read_all_route(self):
        @self.router.get(
            path='/',
            response_model=self._collection_schema,
            response_model_by_alias=False,
        )
        async def read_all(
            user: Annotated[UserProtocol, Depends(self._user_dependency)],
            repository: Annotated[BaseRepository, Depends(self._get_repository)],
            limit: Annotated[int, Query(gt=-1)] = 25,
            offset: Annotated[int, Query(gt=-1)] = 0,
            name: Optional[str] = None,
            is_deleted: bool = False,
        ):
            documents = await repository.get_documents(
                limit=limit,
                offset=offset,
                name=name,
                owner_id=user.id,
                is_deleted=is_deleted,
            )
            total_amount = await repository.count_documents(
                name=name,
                owner_id=user.id
            )

            return self._collection_schema(
                total_amount=total_amount,
                presented_amount=len(documents),
                content=documents
            )

    def _add_create_route(self):
        @self.router.post(
            path='/',
            response_model=self._base_schema,
            status_code=status.HTTP_201_CREATED,
            response_model_by_alias=False,
        )
        async def create(
            user: Annotated[UserProtocol, Depends(self._user_dependency)],
            repository: Annotated[BaseRepository, Depends(self._get_repository)],
            data: self._create_schema,   # type: ignore
        ):
            document = self._base_schema(
                name=data.name,
                owner_id=user.id,
                created_at=datetime.now(),
                is_deleted=False,
                content=self._default_content,
                deleted_at=None,
            )
            return await repository.insert_document(
                document=document.model_dump(by_alias=True, exclude=['id'])
            )

    def _add_update_route(self):
        @self.router.patch(
            path='/{id}',
            response_model=self._base_schema,
            response_model_by_alias=False,
        )
        async def update(
            user: Annotated[UserProtocol, Depends(self._user_dependency)],
            repository: Annotated[BaseRepository, Depends(self._get_repository)],
            data: self._update_schema,   # type: ignore
            id: self._id_type,  # type: ignore
        ):
            document = await repository.update_document(
                id=id,
                changes=data.model_dump(by_alias=True),
                owner_id=user.id,
            )
            if document is None:
                self._raise_not_found_exception(id)
            return document

    def _add_read_route(self):
        @self.router.get(
            path='/{id}',
            response_model=self._base_schema,
            response_model_by_alias=False,
        )
        async def read(
            user: Annotated[UserProtocol, Depends(self._user_dependency)],
            repository: Annotated[BaseRepository, Depends(self._get_repository)],
            id: self._id_type,  # type: ignore
        ):
            document = await repository.get_document(id=id, owner_id=user.id)
            if document is None:
                self._raise_not_found_exception(id)
            return document

    def _add_delete_route(self):
        @self.router.delete(
            path='/{id}',
            status_code=status.HTTP_204_NO_CONTENT,
        )
        async def delete(
            user: Annotated[UserProtocol, Depends(self._user_dependency)],
            repository: Annotated[BaseRepository, Depends(self._get_repository)],
            id: self._id_type,  # type: ignore
        ):
            is_deleted = await repository.mark_document_as_deleted(id=id, owner_id=user.id)
            if not is_deleted:
                self._raise_not_found_exception(id)

    def _raise_not_found_exception(self, id) -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{self._schema_name.capitalize()} {id} not found",
        )

    def _get_repository(self) -> BaseRepository:
        return self._repository
