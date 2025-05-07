import bson
from app.models.document import Document
from app.redis import redis_client
from app.database import documents_collection


def _get_document_key(document_id: str):
    return f"document:{document_id}"


async def _get_document_from_mongodb(
    document_id: bson.ObjectId
) -> Document | None:
    # raises pydantic.ValidationError

    mongo_record = await documents_collection.find_one(
        {"_id": document_id}
    )
    return (
        Document.model_validate(mongo_record)
            if mongo_record
            else None
    )


async def get_document(
    document_id: str,
) -> Document | None:
    document_key = _get_document_key(document_id)

    document: Document | None = None
    if doc_redis_record := redis_client.get(document_key):
        document = Document.model_validate_json(doc_redis_record)
    else:
        document = await _get_document_from_mongodb(
            bson.ObjectId(document_id)
        )
        if document is not None:
            redis_client.set(document_key, document.model_dump_json())

    return document


async def set_document_in_cache(
    document_id: str,
    document: Document
) -> None:
    document_key = _get_document_key(document_id)

    redis_client.set(document_key, document.model_dump_json())
