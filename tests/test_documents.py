from tests.crud_suite import CRUDTestingSuite
from tests.utils.document import create_document, insert_document
import typing


if typing.TYPE_CHECKING:
    from app.models.document import Document


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

    def create_model(
        self,
        owner_id: str,
        content: dict | None = None
    ) -> 'Document':
        return create_document(owner_id=owner_id, content=content)

    def insert_model(self, model: 'Document') -> None:
        insert_document(model)

    additional_required_fields = (
        'style_id', 'is_public', 'access_restrictions', 'edited_at'
    )
