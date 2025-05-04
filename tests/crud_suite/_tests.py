from pydantic.main import BaseModel
import pytest
import typing
from fastapi import status


if typing.TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from tests.crud_suite.base import CRUDTestingSuite
    from app.models.user import User


def test_model_creation(
    self: 'CRUDTestingSuite',
    client: 'TestClient',
    active_user: 'User'
):
    response = client.post(
        url=self.base_url,
        json=self.creation_payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()

    self.assert_model_integrity(
        data=response_data,
        owner_id=active_user.id,
    )


@pytest.mark.parametrize(
    "amount,limit,offset,expected_presented",
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
def test_model_list_normal_behavior(
    self: 'CRUDTestingSuite',
    client: 'TestClient',
    active_user: 'User',
    amount: int,
    limit: int,
    offset: int,
    expected_presented: int,
):
    models = [self.create_model(owner_id=active_user.id) for _ in range(amount)]
    self.insert_models_bulk(models)

    response = client.get(
        url=self.base_url,
        params={
            'limit': limit,
            'offset': offset,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data['presented_amount'] == expected_presented
    assert response_data['total_amount'] == amount

    models = response_data['content']

    assert len(models) == expected_presented

    self.assert_models_integrity_bulk(
        data=models,
        owner_id=active_user.id
    )


@pytest.mark.parametrize(
    'limit,offset',
    ((-5, 5), (5, -5), (-5, -5)),
    ids=[
        "negative_limit_positive_offset",
        "positive_limit_negative_offset",
        "negative_limit_negative_offset",
    ]
)
def test_model_list_negative_params(
    self: 'CRUDTestingSuite',
    client: 'TestClient',
    active_user: 'User',
    limit: int,
    offset: int
) -> dict:
    response = client.get(
        url=self.base_url,
        params={
            'limit': limit,
            'offset': offset,
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response_data = response.json()

    assert 'content' not in response_data
    assert 'presented_amount' not in response_data
    assert 'total_amount' not in response_data

def test_model_update(
    self: 'CRUDTestingSuite',
    client: 'TestClient',
    active_user: 'User',
    persisted_model: 'BaseModel',
):
    response = client.patch(
        url=self.detail_url(persisted_model.id),
        json=self.update_payload
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    self.assert_model_integrity(
        data=response_data,
        owner_id=active_user.id,
    )

def test_model_details(
    self: 'CRUDTestingSuite',
    client: 'TestClient',
    active_user: 'User',
):
    mock_model = self.create_model(
        owner_id=active_user.id,
        content=self.model_content_data,
    )
    self.insert_model(mock_model)

    response = client.get(
        url=self.detail_url(mock_model.id)
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['content'] == self.model_content_data

    self.assert_model_integrity(
        data=response_data,
        owner_id=active_user.id,
    )

def test_model_deletion(
    self: 'CRUDTestingSuite',
    client: 'TestClient',
    active_user: 'User',
    persisted_model: 'BaseModel',
):
    response = client.delete(
        url=self.detail_url(persisted_model.id)
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(
        url=self.detail_url(persisted_model.id)
    )

    assert get_response.status_code == status.HTTP_404_NOT_FOUND
