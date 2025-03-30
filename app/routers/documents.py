from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated
from bson.objectid import ObjectId

from app.database import documents_collection as collection
from app.models.document import (
    Document,
    DocumentCollection,
    DocumentCreate,
    DocumentUpdate,
)
from app.models.user import User
from app.auth_utils import get_active_user

import datetime


ActiveUser = Annotated[User, Depends(get_active_user)]

router = APIRouter()


@router.get(
    path='/',
    response_model=DocumentCollection,
)
async def get_all_documents(user: ActiveUser):
    return DocumentCollection(
        documents=await collection.find({'owner': user.id})
    )


@router.post(
    path='/',
    response_model=Document,
    status_code=status.HTTP_201_CREATED,
)
async def create_document(user: ActiveUser, document_create: DocumentCreate):
    doc = Document(
        owner_id=user.id,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        name=document_create.name
    )
    new_doc = await collection.insert_one(
        doc.model_dump(by_alias=True, exclude=["id"])
    )
    created_doc = await collection.find_one(
        filter={
            "_id": new_doc.inserted_id
        }
    )
    return created_doc


@router.put(
    path='/{document_id}',
    response_model=Document,
)
async def update_document(
    user: ActiveUser,
    document_id: str,
    document_update: DocumentUpdate,
):
    id = ObjectId(document_id)
    doc_fields = {
        k: v for k, v in \
            document_update.model_dump(by_alias=True).items() \
        if v is not None
    }

    doc = None
    doc_query = {
        "_id": ObjectId(document_id),
        "owner_id": user.id
    }

    if len(doc_fields) >= 1:
        doc = await collection.find_one_and_update(
            filter=doc_query,
            update={"$set": doc_fields},
            return_document=True,
        )
    else:
        doc = await collection.find_one(doc_query)

    if doc is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document {id} not found"
        )

    return doc


@router.get(
    path='/{document_id}',
    response_model=Document,
)
async def get_document(user: ActiveUser, document_id: str):
    ...

@router.delete(
    path='/{document_id}'
)
async def delete_document(user: ActiveUser, document_id: str):
    ...
