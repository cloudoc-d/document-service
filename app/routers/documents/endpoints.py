from .router import router

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    WebSocket,
    WebSocketException,
    status
)

from typing import Annotated
from bson import ObjectId
from typing import Optional
import datetime

from app.models.document import (
    Document,
    DocumentInfo,
    DocumentInfoCollection,
    DocumentCreate,
    DocumentUpdate,
)
from app.models.user import User
from app.dependencies.user import ActiveUserAnnotation
from app.dependencies.database import DocumentsCollectionAnnotation
from app.routers.utils import update_record_from_model


@router.get(
    path='/',
    response_model=DocumentInfoCollection,
    response_model_by_alias=False,
)
async def get_documents(
    user: ActiveUserAnnotation,
    collection: DocumentsCollectionAnnotation,
    limit: int = 25,
    offset: int = 0,
    name: Optional[str] = None,
):
    filter_conditions = {
        "owner_id": user.id,
    }

    if name:
        filter_conditions["name"] = {
            "$regex": f".*{name}.*",
            "$options": "i"
        }

    documents = await collection.find(
        filter_conditions,
        {'content': 0}
    ).skip(offset).limit(limit).to_list(None)

    total_amount = await collection.count_documents(
        filter=filter_conditions
    )

    return DocumentInfoCollection(
        documents=documents,
        presented_amount=len(documents),
        total_amount=total_amount
    )


@router.post(
    path='/',
    response_model=Document,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_document(
    collection: DocumentsCollectionAnnotation,
    user: ActiveUserAnnotation,
    document_create: DocumentCreate
):
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


@router.patch(
    path='/{document_id}',
    response_model=Document,
    response_model_by_alias=False,
)
async def update_document(
    collection: DocumentsCollectionAnnotation,
    user: ActiveUserAnnotation,
    document_id: str,
    document_update: DocumentUpdate,
):
    document = update_record_from_model(
        collection=collection,
        update_model=document_update,
        filter={
            "_id": ObjectId(document_id),
            "owner_id": user.id,
        }
    )
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detayil="document not found"
        )

    return document


@router.get(
    path='/{document_id}',
    response_model=Document,
    response_model_by_alias=False,
)
async def get_document(
    collection: DocumentsCollectionAnnotation,
    user: ActiveUserAnnotation,
    document_id: str
):
    doc = await collection.find_one(
        {'_id': ObjectId(document_id), 'owner_id': user.id}
    )
    if doc is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document {document_id} not found"
        )

    return doc


@router.delete(
    path='/{document_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    collection: DocumentsCollectionAnnotation,
    user: ActiveUserAnnotation,
    document_id: str
):
    del_result = await collection.delete_one(
        {'_id': ObjectId(document_id), 'owner_id': user.id}
    )

    if del_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Document {id} not found")


from renderer_definition.tasks import render_pdf_task
from renderer_definition.models import (
    Document as DocumentIR,
    RenderedDocument
)


@router.get(
    path='/{document_id}/render',
    response_model=RenderedDocument
)
async def render_document(user: ActiveUserAnnotation, document_id: str):
    result = render_pdf_task.delay(
        DocumentIR(
            name="asdfsadf",
            content=[],
            style="",
        ).dict()
    )
    return RenderedDocument(**result.get(timeout=10))
