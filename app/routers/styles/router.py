from fastapi import APIRouter
from app.crud_router import CRUDRouter
from app.models.style import (
    StyleInfo,
    Style,
    StyleInfoCollection,
    StyleCreate,
    StyleUpdate,
)
from app.database import styles_repository
from app.dependencies.user import active_user_dependency


_crud_router = CRUDRouter(
    prefix="/styles",
    tags=["styles"],
    repository=styles_repository,
    user_dependency=active_user_dependency,
    read_schema=Style,
    read_info_schema=StyleInfo,
    collection_schema=StyleInfoCollection,
    create_schema=StyleCreate,
    update_schema=StyleUpdate,
    schema_name="style",
    default_content="",
)

router = _crud_router.router
