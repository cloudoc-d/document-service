from fastapi import Depends
from app.database import documents_repository, styles_repository
from app.crud_router.repository.mongo import MongoRepository
import typing


def documents_repository_dependency() -> MongoRepository:
    return documents_repository


DocumentsRepositoryAnnotation = typing.Annotated[
    MongoRepository,
    Depends(documents_repository_dependency)
]


def styles_repository_dependency() -> MongoRepository:
    return styles_repository


StylesRepositoryAnnotation = typing.Annotated[
    MongoRepository,
    Depends(styles_repository_dependency)
]
