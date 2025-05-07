from tests.crud_suite import CRUDTestingSuite
from tests.utils.style import create_style, insert_style
import typing


if typing.TYPE_CHECKING:
    from app.models.style import Style


class TestStyleCRUD(CRUDTestingSuite):
    model_name = "style"
    creation_payload = {"name": "New Style"}
    update_payload = {"name": "New Style Name"}
    model_content_data = ".paragraph {color: red;}"

    def create_model(
        self,
        owner_id: str,
        content: str | None = None
    ) -> 'Style':
        f = create_style(owner_id=owner_id, content=content)
        print(f)
        return f

    def insert_model(self, model: 'Style') -> None:
        insert_style(model)

    additional_required_fields = ('public', 'updated_at', 'popularity')
