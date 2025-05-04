from .base import BaseRepository

import pymongo
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection
from typing import Any
from bson import ObjectId


class MongoRepository(BaseRepository):
    def __init__(self, collection: AsyncCollection) -> None:
        self._collection = collection

    async def get_documents(
        self,
        owner_id: str,
        limit: int,
        offset: int,
        name: str | None = None,
        exclude_fields: list[str] | None = None
    ) -> list[dict]:
        if limit > 0:
            return await self._collection.find(
                filter=self._construct_filter(owner_id=owner_id, name=name),
                projection=self._construct_projection(exclude_fields)
            ).skip(offset).limit(limit).to_list(None)
        else:
            return list()

    async def count_documents(
        self,
        owner_id: str,
        name: str | None = None,
    ) ->  int:
        return await self._collection.count_documents(
            filter=self._construct_filter(
                owner_id=owner_id,
                name=name
            )
        )

    async def get_document(
        self,
        id: str | ObjectId,
        owner_id: str | None,
    ) -> dict | None:
        return await self._collection.find_one(
            filter=self._construct_filter(id=id, owner_id=owner_id)
        )

    async def insert_document(
        self,
        document: dict,
    ) -> dict:
        insert_result = await self._collection.insert_one(document)

        return await self.get_document(id=insert_result.inserted_id, owner_id=None)

    async def update_document(
        self,
        id: str,
        changes: dict[str, Any],
        owner_id: str | None,
    ) -> dict:
        valuable_fields = {k: v for k, v in changes.items() if v is not None}

        filter = self._construct_filter(id=id, owner_id=owner_id)
        if len(valuable_fields) == 0:
            document = await self._collection.find_one(filter=filter)
        else:
            document = await self._collection.find_one_and_update(
                filter=filter,
                update={"$set": valuable_fields},
                return_document=True
            )

        return document

    async def delete_document(self, id: str, owner_id: str | None) -> bool:
        delete_result = await self._collection.delete_one(
            filter=self._construct_filter(id=id, owner_id=owner_id)
        )

        return delete_result.deleted_count == 1

    def _construct_filter(
        self,
        id: str | ObjectId | None = None,
        owner_id: str | None = None,
        name: str | None = None,
    ) -> dict:
        filter = dict()
        if id is not None:
            filter["_id"] = id if isinstance(id, ObjectId) else ObjectId(id)
        if owner_id is not None:
            filter["owner_id"] = owner_id
        if name is not None:
           filter["name"] = {
               "$regex": f".*{name}.*",
               "$options": "i"
           }

        return filter

    def _construct_projection(self, exclude_fields: list[str] | None) -> dict:
        if exclude_fields is None:
            return dict()
        return {k: 0 for k in exclude_fields}
