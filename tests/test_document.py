import pytest
import fastapi
from fastapi.testclient import TestClient
from app.main import app as target_app

@pytest.fixture(scope="module")
def client():
    with TestClient(target_app) as client:
        yield client


def setup_module():
    client
