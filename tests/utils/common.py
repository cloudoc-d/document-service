import string
import random
import typing
import pymongo
from bson import ObjectId
from app.config import Config

if typing.TYPE_CHECKING:
    from pydantic import BaseModel


def generate_rand_str(length=10) -> str:
    characters = string.digits + string.ascii_letters
    sequence = ''.join(random.choice(characters) for _ in range(length))
    return sequence


def insert_model_in_database(
    model: 'BaseModel',
    collection_name: str
) -> None:
    with pymongo.MongoClient(Config.MONGODB_URL) as client:
        database = client.get_database(Config.DATABASE_NAME)
        collection = database.get_collection(collection_name)
        model_dump = model.model_dump(by_alias=True)
        model_dump['_id'] = ObjectId(model_dump['_id'])
        collection.insert_one(model_dump)
