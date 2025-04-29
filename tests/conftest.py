import pytest
import typing
from app.main import app as target_app
from fastapi.testclient import TestClient
from tests.utils.user import (
    create_user,
    override_target_app_user
)

if typing.TYPE_CHECKING:
    from app.models.user import User


@pytest.fixture(scope="session")
def client():
    with TestClient(app=target_app) as client:
        yield client


@pytest.fixture(scope="function")
def active_user() -> 'User':
    user = create_user(is_active=True)
    override_target_app_user(user)
    return user
