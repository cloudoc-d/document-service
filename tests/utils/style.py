from app.models.style import Style
from datetime import datetime
from bson.objectid import ObjectId
from tests.utils.common import (
    generate_rand_str,
    insert_model_in_database,
)
from app.database import STYLES_COLLECTION


def _default_content() -> str:
    return """
    .paragraph {
        font-family: Georgia, serif;
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 400;
    }

    .header {
        font-family: Arial, sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    """


def create_style(
    content: str | None = None,
    name: str | None = None,
    owner_id: str | None = None,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
    is_deleted: bool = False,
    public: bool = False,
    popularity: int = 0,
) -> Style:
    return Style(
        _id=ObjectId(), # TODO почему по алиасу ???
        content=content if content else _default_content(),
        public=public,
        name=name if name else generate_rand_str(),
        owner_id=owner_id if owner_id else generate_rand_str(),
        created_at=created_at if created_at else datetime.now(),
        updated_at=updated_at if updated_at else None,
        popularity=popularity,
        is_deleted=False,
    )


def insert_style(style: Style) -> None:
    insert_model_in_database(style, STYLES_COLLECTION)


def insert_styles_in_bulk(styles: list[Style]) -> None:
    for sty in styles:
        insert_style(sty)
