from app.core.crud_router import CRUDRouter
from app.database import documents_repository
from app.dependencies.user import active_user_dependency
from app.models.document import (
    Document,
    DocumentCreate,
    DocumentUpdate,
    DocumentInfo,
    DocumentInfoCollection,
)

_crud_router = CRUDRouter(
    prefix='/documents',
    tags=['documents'],
    repository=documents_repository,
    user_dependency=active_user_dependency,
    read_schema=Document,
    create_schema=DocumentCreate,
    update_schema=DocumentUpdate,
    read_info_schema=DocumentInfo,
    collection_schema=DocumentInfoCollection,
    default_content=list(),
)

router = _crud_router.router


from .endpoints import *
# from .endpoints_ws import *
from .endpoints_ws import edit_document_ws
