from fastapi.testclient import TestClient
from app.main import app

ACCESS_TOKEN = "asdfasdf"

client = TestClient(app)

document_id: str | None = None


def test_document_creation():
    response = client.post(
        url='/documents',
        json={
            "name": "Test Document",
        },
        params={
            "access_token": ACCESS_TOKEN
        }
    )
    assert response.status_code == 201, response.text
    global document_id
    document_id = response.json()["id"]


def test_document_list():
    response = client.get(
        url='/documents',
        params={
            "access_token": ACCESS_TOKEN
        }
    )
    assert response.status_code == 200, response.text
    resp_json = response.json()
    assert len(resp_json['documents']) > 0


def test_document_update():
    global document_id

    response = client.put(
        url=f'/documents/{document_id}',
        json={
            "name": "New Document Name"
        },
        params={
            "access_token": ACCESS_TOKEN
        }
    )
    assert response.status_code == 200, response.text
    assert response.json()['name'] == 'New Document Name'

def test_document_view():
    global document_id

    response = client.get(
        url=f'/documents/{document_id}',
        params={
            "access_token": ACCESS_TOKEN
        }
    )
    assert response.status_code == 200, response.text
    assert response.json()['content'] != None

def test_document_delete():
    global document_id

    response = client.delete(
        url=f'/documents/{document_id}',
        params={
            "access_token": ACCESS_TOKEN
        }
    )
    assert response.status_code == 204, response.text
