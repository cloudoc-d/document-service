import typing
from bson import ObjectId
import pytest
from app.main import app as target_app
from tests.utils.document import (
    create_document,
    insert_document,
    insert_documents_in_bulk,
)
from fastapi import status


if typing.TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from app.models.user import User
    from app.models.document import Document


@pytest.fixture
def mock_document(active_user: 'User') -> 'Document':
    return create_document(owner_id=active_user.id)


@pytest.fixture
def persisted_document(mock_document: 'Document') -> 'Document':
    insert_document(mock_document)
    return mock_document


DOCUMENTS_URL = '/documents'


def document_detail_url(document_id: str) -> str:
    return f"{DOCUMENTS_URL}/{document_id}"


def test_document_creation(
    client: 'TestClient',
    active_user: 'User',
):
    document_name = "New Document"

    response = client.post(
        url=DOCUMENTS_URL,
        json={
            "name": document_name,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data.get('name') == document_name
    assert response_data.get('owner_id') == active_user.id


@pytest.mark.parametrize(
    "doc_num,limit,offset,expected_presented",
    [
        (5, 10, 0, 5),
        (5, 3, 0, 3),
        (5, 10, 2, 3),
        (0, 10, 10, 0),
        (1, 0, 0, 0),
        (1, 0, 3, 0),
    ],
    ids=[
        "limit_bigger_than_total",
        "limit_less_than_total",
        "offset_with_limit",
        "offset_exceeds_total",
        "zero_limit",
        "zero_limit_with_offset",
    ]
)
def test_document_list_normal_behavior(
    client: 'TestClient',
    active_user: 'User',
    doc_num: int,
    limit: int,
    offset: int,
    expected_presented: int,
):
    documents = [create_document(owner_id=active_user.id) for _ in range(doc_num)]
    insert_documents_in_bulk(documents)

    response = client.get(
        url=DOCUMENTS_URL,
        params={
            'limit': limit,
            'offset': offset,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data.get('presented_amount') == expected_presented
    assert response_data.get('total_amount') == doc_num

    documents = response_data['documents']

    assert len(documents) == expected_presented

    for document in documents:
        assert document.get('owner_id') == active_user.id


@pytest.mark.parametrize(
    'limit,offset',
    ((-5, 5), (5, -5), (-5, -5)),
    ids=[
        "negative_limit_positive_offset",
        "positive_limit_negative_offset",
        "negative_limit_negative_offset",
    ]
)
def test_document_list_negative_params(
    client: 'TestClient',
    active_user: 'User',
    limit: int,
    offset: int
):
    resp = client.get(
        url=DOCUMENTS_URL,
        params={
            'limit': limit,
            'offset': offset,
        }
    )

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    resp_data = resp.json()

    assert 'documents' not in resp_data
    assert 'presented_amount' not in resp_data
    assert 'total_amount' not in resp_data


@pytest.mark.parametrize(
    'document_name,document_style_id',
    (
        ('New Name', str(ObjectId())),
        (None, str(ObjectId())),
        ('Name', None),
        (None, None),
    ),
    ids=[
        "name_and_style",
        "only_style",
        "only_name",
        "no_name_no_style",
    ]
)
def test_document_update(
    client: 'TestClient',
    active_user: 'User',
    persisted_document: 'Document',
    document_name: str,
    document_style_id: str,
):
    response = client.patch(
        url=document_detail_url(persisted_document.id),
        json={
            'name': document_name,
            'style_id': document_style_id,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    if document_name is not None:
        assert response_data['name'] == document_name
    if document_style_id is not None:
        assert response_data['style_id'] == document_style_id


def test_document_content(
    client: 'TestClient',
    active_user: 'User',
):
    content = [
        {
            "type": "paragraph",
            "attrs": {},
            "data": {"text": "First Paragraph"}
        }
    ]

    document = create_document(
        owner_id=active_user.id,
        content=content
    )
    insert_document(document)

    response = client.get(
        url=document_detail_url(document.id)
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data['name'] == document.name
    assert response_data['owner_id'] == active_user.id
    assert response_data['content'] == content


def test_document_deletion(
    client: 'TestClient',
    active_user: 'User',
    persisted_document: 'Document',
):
    response = client.delete(
        url=document_detail_url(persisted_document.id)
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_resp = client.get(
        url=document_detail_url(persisted_document.id)
    )

    assert get_resp.status_code == status.HTTP_404_NOT_FOUND
