from bson.objectid import ObjectId
from app.models.document import (
    Document,
    DocumentAccessRestriction,
    DocumentAccessRole,
)
from app.database import DOCUMENTS_COLLECTION
from datetime import datetime
from .common import (
    generate_rand_str,
    insert_model_in_database
)


def create_document(
    owner_id: str | None = None,
    name: str | None = None,
    style_id: str | None = None,
    is_public: bool = False,
    is_deleted: bool = False,
    reader_ids: list[str] | None = None,
    editor_ids: list[str] | None = None,
    created_at: datetime | None = None,
    edited_at: datetime | None = None,
    content: list[dict] | None = None
) -> Document:
    access_restrictions = list()
    if reader_ids:
        access_restrictions += _get_access_restrictions(
            user_ids=reader_ids,
            role=DocumentAccessRole.READER
        )
    if editor_ids:
        access_restrictions += _get_access_restrictions(
            user_ids=editor_ids,
            role=DocumentAccessRole.EDITOR
        )

    document = Document(
        id=ObjectId(),
        name=name if name else generate_rand_str(),
        owner_id=owner_id if owner_id else generate_rand_str(),
        created_at=created_at if created_at else datetime.now(),
        is_deleted=is_deleted,
        style_id=ObjectId(style_id) if style_id else None,
        is_public=is_public,
        access_restrictions=access_restrictions,
        edited_at=edited_at,
        content=content if content else list()
    )

    return document


def _get_access_restrictions(
    user_ids: list[str],
    role: DocumentAccessRole,
) -> list[DocumentAccessRestriction]:
    result = list()
    for id in user_ids:
        result.append(
            DocumentAccessRestriction(
                user_id=id,
                role=role
            )
        )
    return result


def insert_document(document: Document) -> None:
    insert_model_in_database(document, DOCUMENTS_COLLECTION)


def insert_documents_in_bulk(documents: list[Document]) -> None:
    for doc in documents:
        insert_document(doc)
