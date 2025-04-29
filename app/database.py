import motor.motor_asyncio
from app.config import Config


DOCUMENTS_COLLECTION = "documents"
STYLES_COLLECTION = "styles"


client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGODB_URL)

database = client.get_database(Config.DATABASE_NAME)

documents_collection = database.get_collection(DOCUMENTS_COLLECTION)
styles_collection = database.get_collection(STYLES_COLLECTION)
