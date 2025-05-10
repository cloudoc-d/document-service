from enum import Enum, auto
from dataclasses import dataclass
from abc import ABC, abstractmethod


class ResponseType(Enum):
    UNICAST = auto()
    BROADCAST = auto()


@dataclass
class Response:
    message: str | dict
    response_type: ResponseType


class BaseMessageHandler(ABC):
    @abstractmethod
    async def handle_message(self, message: str) -> Response: ...
