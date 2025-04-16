from .router import router

from fastapi import status
from app.models.style import (
    StyleInfo,
    StyleInfoCollection,
    StyleCreate,
    StyleUpdate,
    Style,
)
from app.auth_utils import ActiveUserAnnotation
from app.database import styles_collection as collection
from datetime import datetime
from typing import Optional


@router.get(
    path='/',
    response_model=StyleInfoCollection,
    response_model_by_alias=False,
)
async def get_styles(
    user: ActiveUserAnnotation,
    limit: int = 10,
    offset: int = 0,
    owned: Optional[bool] = True,
    name: Optional[str] = None,
):
    filter_conditions = {}

    if owned:
        filter_conditions["owner_id"] = user.id
    else:
        filter_conditions["public"] = True
        filter_conditions["owner_id"] = {"$ne": user.id}

    if name:
        filter_conditions["name"] = {
            "$regex": f".*{name}.*",
            "$options": "i"
        }

    styles = await collection.find(
        filter_conditions,
        {'content': 0}
    ).skip(offset).limit(limit).to_list(None)

    return StyleInfoCollection(styles=styles)


@router.post(
    path='/',
    response_model=Style,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_style(
    user: ActiveUserAnnotation,
    document_create: StyleCreate,
):
    style = Style(
        name=StyleCreate.name,
        owner_id=user.id,
        created_at=datetime.now(),
        content=""
    )
    inserted_style = await collection.insert_one(
        style.model_dump(by_alias=True, exclude=["id"])
    )
    new_style = await collection.find(
        {"_id": inserted_style.inserted_id}
    )


@router.put(    # TODO PATCH ???
    path='/{style_id}',
    response_model=Style,
    response_model_by_alias=False,
)
async def update_style(
    user: ActiveUserAnnotation,
    style_id: str,
    style_update: StyleUpdate,
):
    ...


@router.get(
    path='/{style_id}',
    response_model=Style,
    response_model_by_alias=False,
)
async def get_style(user: ActiveUserAnnotation, style_id: str):
    ...


@router.delete(
    path='/{style_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_style(user: ActiveUserAnnotation, style_id: str):
    ...
