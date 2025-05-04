from tests.crud_suite import CRUDTestingSuite
from tests.utils.document import create_document, insert_document
import typing


if typing.TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from app.models.user import User


class TestDocumentCRUD(CRUDTestingSuite):
    model_name = "document"
    creation_payload = {"name": "New Document"}
    update_payload = {"name": "New Document Name"}
    model_content_data = [
        {
            "type": "paragraph",
            "attrs": {},
            "data": {"text": "First Paragraph"}
        }
    ]

    create_model = staticmethod(create_document)
    insert_model = staticmethod(insert_document)

    def assert_model_integrity(
        self,
        data: dict,
        owner_id: typing.Any
    ) -> None:
        ...
