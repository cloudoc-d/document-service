import pymongo
from app.config import Config


DOCUMENTS_COLLECTION = "documents"
STYLES_COLLECTION = "styles"


client = pymongo.AsyncMongoClient(Config.MONGODB_URL)

database = client.get_database(Config.DATABASE_NAME)

documents_collection = database.get_collection(DOCUMENTS_COLLECTION)
styles_collection = database.get_collection(STYLES_COLLECTION)


from app.core.repository.mongo import MongoRepository

documents_repository = MongoRepository(documents_collection)
styles_repository = MongoRepository(styles_collection)
