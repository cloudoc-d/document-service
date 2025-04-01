import motor.motor_asyncio
import os


_MONGODB_URL  = os.environ['MONGODB_URL']
_MONGODB_NAME = "cloudoc"
_DOCUMENTS_COLLECTION = "documents"


client = motor.motor_asyncio.AsyncIOMotorClient(_MONGODB_URL)
import asyncio
client.get_io_loop = asyncio.get_event_loop #???
database = client.get_database(_MONGODB_NAME)
documents_collection = database.get_collection(_DOCUMENTS_COLLECTION)
