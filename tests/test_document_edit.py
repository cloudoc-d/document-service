import pytest
import typing

from tests.utils.document import create_document, insert_document

if typing.TYPE_CHECKING:
    from app.models.user import User
    from app.models.document import Document
    from fastapi.testclient import TestClient
    from starlette.testclient import WebSocketTestSession

DOCUMENTS_URL = '/documents'

@pytest.fixture
def mock_document(active_user: 'User') -> 'Document':
    return create_document(owner_id=active_user.id)

@pytest.fixture
def persisted_document(mock_document: 'Document') -> 'Document':
    insert_document(mock_document)
    return mock_document

@pytest.fixture
def ws_client(
    client: 'TestClient',
    persisted_document: 'Document',
) -> typing.Generator['WebSocketTestSession', None, None]:
    url = get_documents_edit_ws_url(persisted_document.id)
    with client.websocket_connect(url=url) as client:
        yield client


def get_documents_edit_ws_url(document_id: str) -> str:
    return f"{DOCUMENTS_URL}/{document_id}/ws"


def test_unknown_event(ws_client: 'WebSocketTestSession'):
    event = {
        "event": {
            "type": "unknown-event",
            "data": {},
        }
    }
    ws_client.send_json(event)
    response = ws_client.receive_json()
    assert response["error"]["type"] == "unable-to-handle"
