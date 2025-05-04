import typing
from typing_extensions import Sequence
import pytest
from fastapi import status


if typing.TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from app.models.user import User
    from pydantic import BaseModel


class CRUDTestingSuite:
    @property
    def model_name(self) -> str:
       raise NotImplementedError()

    @property
    def creation_payload(self) -> dict[str, typing.Any]:
        raise NotImplementedError()

    @property
    def update_payload(self) -> dict[str, typing.Any]:
        raise NotImplementedError()

    @property
    def model_content_data(self) -> typing.Any:
        raise NotImplementedError()

    def create_model(
        self,
        owner_id: typing.Any,
        content: typing.Any | None = None
    ) -> 'BaseModel':
        raise NotImplementedError()

    def insert_model(self, model: 'BaseModel') -> None:
        raise NotImplementedError()

    @property
    def required_fields(self) -> Sequence[str]:
        return ("id", "name", "owner_id", "created_at", "is_deleted")

    @property
    def additional_required_fields(self) -> Sequence[str]:
        return ()

    def insert_models_bulk(self, models: list['BaseModel']) -> None:
        for m in models:
            self.insert_model(m)

    def assert_model_integrity(
        self,
        data: dict,
        owner_id: typing.Any
    ) -> None:
        fields = self.required_fields + self.additional_required_fields
        for field in fields:
            assert field in data, f"Missing required field in response json: {field}"

        if 'owner_id' in self.required_fields:
            assert data['owner_id'] == owner_id, "owner_id doesn't correspond to provided document"

    def assert_models_integrity_bulk(
        self,
        data: list[dict],
        owner_id: typing.Any
    ) -> None:
        for document in data:
            self.assert_model_integrity(document, owner_id)

    @pytest.fixture
    def mock_model(self, active_user: 'User') -> 'BaseModel':
        return self.create_model(owner_id=active_user.id)


    @pytest.fixture
    def persisted_model(self, mock_model: 'BaseModel') -> 'BaseModel':
        self.insert_model(mock_model)
        return mock_model

    @property
    def base_url(self) -> str:
        return f"{self.model_name}s"


    def detail_url(self, id: str) -> str:
        return f'{self.base_url}/{id}'


    from ._tests import (
        test_model_creation,
        test_model_list_normal_behavior,
        test_model_list_negative_params,
        test_model_update,
        test_model_details,
        test_model_deletion,
    )
