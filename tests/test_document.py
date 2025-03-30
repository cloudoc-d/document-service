import os

os.environ['MONGODB_URL'] = "mongodb://localhost:27017/"

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

document_id: str | None = None


def test_document_creation():
    response = client.post(
        url='/documents',
        json={
            "name": "Test Document",
        },
        params={
            "access_token": "asdfasdf"
        }
    )
    assert response.status_code == 201, response.text
    global document_id
    document_id = response.json()["_id"]


def test_document_update():
    global document_id

    response = client.put(
        url=f'/documents/{document_id}',
        json={
            "name": "New Document Name"
        },
        params={
            "access_token": "asdfasdf"
        }
    )
    assert response.status_code == 200, response.text
    assert response.json()['name'] == 'New Document Name'
