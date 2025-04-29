import typing
import pytest
from app.main import app as target_app
from tests.utils.document import (
    create_document,
    insert_document_in_database
)


if typing.TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from app.models.user import User
    from app.models.document import Document


def test_document_creation(
    client: 'TestClient',
    active_user: 'User',
):
    document_name = "New Document"

    resp = client.post(
        url='/documents',
        json={
            "name": document_name,
        }
    )
    assert resp.status_code == 201
    resp_data = resp.json()
    assert resp_data.get('name') == document_name
    assert resp_data.get('owner_id') == active_user.id


@pytest.mark.parametrize(
    "doc_num,limit,offset",
    (
        (5, 10, 0),
        (5, 3, 0),
        (5, 10, 2),
        (0, 10, 10),
        (1, 0, 0),
        (1, 0, 3),
    )
)
def test_document_list(
    client: 'TestClient',
    active_user: 'User',
    doc_num: int,
    limit: int,
    offset: int,
):
    documents: list['Document'] = list()
    for _ in range(doc_num):
        doc = create_document(owner_id=active_user.id)
        insert_document_in_database(doc)
        documents.append(doc)

    resp = client.get(
        url='/documents',
        params={
            'limit': limit,
            'offset': offset,
        }
    )

    assert resp.status_code == 200

    resp_data = resp.json()

    presented_amount = min(
        doc_num - offset if doc_num - offset > 0 else 0,
        limit
    )
    assert resp_data.get('presented_amount') == presented_amount
    assert resp_data.get('total_amount') == doc_num

    documents = resp_data['documents']
    assert len(documents) == presented_amount

    for document in documents:
        assert document.get('owner_id') == active_user.id
