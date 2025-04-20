import redis
from app.config import Config


redis_client = redis.Redis.from_url(
    Config.REDIS_STORAGE_URL,
    decode_responses=True,
)
