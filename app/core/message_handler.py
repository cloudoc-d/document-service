from enum import Enum, auto
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json


class ResponseType(Enum):
    UNICAST = auto()
    BROADCAST = auto()


@dataclass
class Response:
    message: str
    response_type: ResponseType


class RequestHandlingException(Exception):
    """Special exception which get sent to client by connection manager"""
    exception_id: str = ...

    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(*args)

    def get_response(self) -> Response:
        return Response(
            message=json.dumps(
                {"error": {"type": self.exception_id, "detail": self.message}}
            ),
            response_type=ResponseType.UNICAST
        )


class BaseMessageHandler(ABC):
    @abstractmethod
    async def handle_message(self, message: str) -> Response: ...
