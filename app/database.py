import motor
import os


_MONGODB_URL  = os.environ['MONGODB_URL']
_MONGODB_NAME = "cloudoc"
_DOCUMENTS_COLLECTION = "documents"


client = motor.motor_asyncio.AsyncIOMotorClient()
database = client.get_database(_MONGODB_NAME)
documents_collection = database.get_collection(_DOCUMENTS_COLLECTION)
