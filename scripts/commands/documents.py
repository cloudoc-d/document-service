from argparse import Namespace
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.document import (
    Document,
    DocElement,
    DocElementType,
    DocumentAccessRestriction,
    DocumentAccessRole,
)
from bson import ObjectId
from datetime import timedelta
import asyncio
import faker
import os
import random


fake = faker.Faker()


def generate_doc_element() -> DocElement:
    element_type = random.choice(list(DocElementType))

    attrs = {}
    data = {}

    if element_type == DocElementType.PARAGRAPH:
        attrs = {"align": random.choice(['left', 'right', 'center'])}
        data = {"text": fake.text(max_nb_chars=500)}
    elif element_type == DocElementType.HEADER:
        attrs = {"level": random.randint(1, 6)}
        data = {"text": fake.sentence()}

    return DocElement(
        type=element_type,
        attrs=attrs,
        data=data
    )


def generate_access_restriction() -> DocumentAccessRestriction:
    return DocumentAccessRestriction(
        user_id=str(ObjectId()),
        role=random.choice(list(DocumentAccessRole))
    )


def generate_document(
    user_id: str | None,
    style_id: ObjectId | None
) -> Document:
    created_at = fake.date_time_between(start_date="-1y", end_date="now")
    edited_at = created_at + timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23)
    ) if random.choice([True, False]) else None

    owner_id = user_id if user_id else str(ObjectId())
    style_id = style_id if style_id else str(ObjectId())

    return Document(
        owner_id=owner_id,
        name=fake.catch_phrase(),
        style_id=style_id,
        is_public=random.choice([True, False]),
        access_restrictions=[
            generate_access_restriction()
            for _ in range(random.randint(0, 5))
        ],
        created_at=created_at,
        edited_at=edited_at,
        content=[
            generate_doc_element()
            for _ in range(random.randint(1, 15))
        ]
    )


async def _fill_documents_collection(
    mongodb_url: str | None,
    user_id: str | None,
    database: str,
    collection: str,
    style_collection: str | None,
    assign_existing_style: bool,
    count: int,
):
    if mongodb_url is None:
        print('url to mongodb not provided. finishing')
        return -1

    mongo_client = AsyncIOMotorClient(mongodb_url)
    database = mongo_client.get_database(database)
    collection = database.get_collection(collection)

    style_ids_cursor = None
    if assign_existing_style:
        s_collection = database.get_collection(style_collection)
        style_ids_cursor = s_collection.find({}, {'_id': 1})

    for _ in range(count):
        try:
            style_id = str((await style_ids_cursor.next())['_id']) \
                if assign_existing_style else None
        except StopAsyncIteration:
            style_id = None
        document = generate_document(
            user_id=user_id,
            style_id=style_id
        )

        await collection.insert_one(
            document.model_dump(by_alias=True, exclude=["id"])
        )

    print('Done!')


def fill_documents_collection(args):
    asyncio.run(
        _fill_documents_collection(
            mongodb_url=args.mongodb_url,
            user_id=args.user_id,
            database=args.database,
            collection=args.collection,
            style_collection=args.collection,
            assign_existing_style=args.assign_existing_style,
            count=args.count
        )
    )
