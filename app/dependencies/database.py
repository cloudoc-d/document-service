from app.database import client
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Annotated
from fastapi import Depends


_MONGODB_NAME = "cloudoc"
_DOCUMENTS_COLLECTION = "documents"
_STYLES_COLLECTION = "styles"


def get_database() -> AsyncIOMotorDatabase:
    return client.get_database(_MONGODB_NAME)


DatabaseAnnotation = Annotated[AsyncIOMotorDatabase, Depends(get_database)]


def get_documents_collection(
    database: DatabaseAnnotation
) -> AsyncIOMotorCollection:
    return database.get_collection(_DOCUMENTS_COLLECTION)


DocumentsCollectionAnnotation = Annotated[AsyncIOMotorCollection, Depends(get_documents_collection)]


def get_styles_collection(
    database: DatabaseAnnotation
) -> AsyncIOMotorCollection:
    return database.get_collection(_STYLES_COLLECTION)


StylesCollectionAnnotation = Annotated[AsyncIOMotorCollection, Depends(get_styles_collection)]
