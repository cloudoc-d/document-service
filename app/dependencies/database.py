from app.database import (
    database,
    documents_collection,
    styles_collection
)
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Annotated
from fastapi import Depends


def get_database() -> AsyncIOMotorDatabase:
    return database


DatabaseAnnotation = Annotated[AsyncIOMotorDatabase, Depends(get_database)]


def get_documents_collection() -> AsyncIOMotorCollection:
    return documents_collection


DocumentsCollectionAnnotation = Annotated[AsyncIOMotorCollection, Depends(get_documents_collection)]


def get_styles_collection() -> AsyncIOMotorCollection:
    return styles_collection


StylesCollectionAnnotation = Annotated[AsyncIOMotorCollection, Depends(get_styles_collection)]
