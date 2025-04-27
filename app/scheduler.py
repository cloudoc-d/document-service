from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler(timezone='UTC')


from app.redis import redis_client
from app.models.document import Document
from app.database import documents_collection
from bson import ObjectId


@scheduler.scheduled_job('interval', minutes=10)
async def push_cache_to_db():
    for key in redis_client.scan(match="document:*"):
        doc_str = redis_client.get(key)
        doc = Document.model_validate_json(doc_str)
        assert doc.id is not None
        await documents_collection.replace_one(
            filter={"_id": doc.id},
            replacement=doc.model_dump(by_alias=True, exclude=["id"])
        )
        redis_client.delete(key)
