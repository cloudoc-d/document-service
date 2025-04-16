from bson import ObjectId
from .router import router

from fastapi import status, HTTPException
from app.models.style import (
    StyleInfo,
    StyleInfoCollection,
    StyleCreate,
    StyleUpdate,
    Style,
)
from app.auth_utils import ActiveUserAnnotation
from app.database import styles_collection as collection
from app.routers.utils import update_record_from_model
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

    total_amount = await collection.count_documents(
        filter=filter_conditions
    )

    return StyleInfoCollection(
        styles=styles,
        presented_amount=len(styles),
        total_amount=total_amount
    )


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


@router.patch(
    path='/{style_id}',
    response_model=Style,
    response_model_by_alias=False,
)
async def update_style(
    user: ActiveUserAnnotation,
    style_id: str,
    style_update: StyleUpdate,
):
    style = update_record_from_model(
        collection=collection,
        update_model=style_update,
        filter={
            "_id": ObjectId(style_id),
            "owner_id": user.id
        }
    )
    if style is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="style not found"
        )

    return style


@router.get(
    path='/{style_id}',
    response_model=Style,
    response_model_by_alias=False,
)
async def get_style(user: ActiveUserAnnotation, style_id: str):
    style = await collection.find({"_id": ObjectId(style_id)})
    if style is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="style not found"
        )
    if not (style.public or style.owner_id == user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you have not access to this style"
        )

    return style


@router.delete(
    path='/{style_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_style(user: ActiveUserAnnotation, style_id: str):
    deleted_style = await collection.delete_one(
        {"_id": ObjectId(style_id), "owner_id": user.id}
    )

    if deleted_style.deleted_count == 0:
        raise HTTPException(status_code=404, detail="style not found")
