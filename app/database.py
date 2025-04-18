import motor.motor_asyncio
from app.config import Config


_MONGODB_NAME = "cloudoc"
_DOCUMENTS_COLLECTION = "documents"
_STYLES_COLLECTION = "styles"


client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGODB_URL)

database = client.get_database(_MONGODB_NAME)

documents_collection = database.get_collection(_DOCUMENTS_COLLECTION)
styles_collection = database.get_collection(_STYLES_COLLECTION)
