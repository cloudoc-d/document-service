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
from app.dependencies.user import get_active_user


_crud_router = CRUDRouter(
    prefix="/styles",
    tags=["styles"],
    repository=styles_repository,
    user_dependency=get_active_user,
    read_schema=Style,
    read_info_schema=StyleInfo,
    collection_schema=StyleInfoCollection,
    create_schema=StyleCreate,
    update_schema=StyleUpdate,
    schema_name="style",
    default_content="",
    id_type=str
)

router = _crud_router.router
