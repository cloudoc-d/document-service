from fastapi import Depends
from broadcaster import Broadcast
from app.broadcast import broadcast
import typing


def broadcast_dependency() -> Broadcast:
    return broadcast


BroadcastAnnotation = typing.Annotated[
    Broadcast,
    Depends(broadcast_dependency)
]
