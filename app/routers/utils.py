from pydantic import BaseModel
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

import pydantic


def _get_model_fields(model: BaseModel, by_alias=True) -> dict:
    return {
        k: v for k, v in \
            model.model_dump(by_alias=by_alias).items() \
        if v is not None
    }


async def update_record_from_model(
    collection: AsyncIOMotorCollection,
    filter: dict,
    update_model: BaseModel,
) -> dict | None:
    # NOTE: model field names should correspond to db record fields
    update_fields = _get_model_fields(update_model)

    result = None

    if len(update_fields) == 0:
        result = await collection.find_one(filter)
    else:
        result = await collection.find_one_and_update(
            filter=filter,
            update={"$set": update_fields},
            return_document=True
        )

    return result
