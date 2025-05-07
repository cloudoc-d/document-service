from fastapi import (
    WebSocket, Request, Depends,
    WebSocketException, HTTPException, status
)
import typing
import enum

from app.models.user import User, UserRole
from ._context import ContextAnnotation, get_context_based_exception



def user_dependency(
    connection_context: ContextAnnotation,
    access_token: str | None = None,
) -> User:
    # raises HTTPException
    if access_token is None:
        raise get_context_based_exception(
            context=connection_context,
            http_code=status.HTTP_401_UNAUTHORIZED,
            ws_code=status.WS_1008_POLICY_VIOLATION,
            message="access_token must be provided"
        )
    # TODO глушилка, жду доку к сервису авторизации
    from datetime import datetime
    if access_token == "asdfasdf":
        return User(
            id="asdfasdf",
            name="zandari",
            email="asdf@asdf.ru",
            roles=[UserRole.ADMIN],
            created_at=datetime.now(),
            is_active=True
        )

    raise get_context_based_exception(
        context=connection_context,
        http_code=status.HTTP_401_UNAUTHORIZED,
        ws_code=status.WS_1008_POLICY_VIOLATION,
        message="access_token is invalid",
    )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="access_token is invalid"
    )


UserAnnotation = typing.Annotated[User, Depends(user_dependency)]


def active_user_dependency(
    connection_context: ContextAnnotation,
    user: UserAnnotation
) -> User:
    # raises HTTPException
    if not user.is_active:
        raise get_context_based_exception(
            context=connection_context,
            http_code=status.HTTP_403_FORBIDDEN,
            ws_code=status.WS_1008_POLICY_VIOLATION,
            message="inactive user"
        )
    return user


ActiveUserAnnotation = typing.Annotated[User, Depends(active_user_dependency)]


def admin_user_dependency(
    connection_context: ContextAnnotation,
    user: UserAnnotation
) -> User:
    # raises HTTPException
    if UserRole.ADMIN not in user.roles:
        raise get_context_based_exception(
            context=connection_context,
            http_code=status.HTTP_403_FORBIDDEN,
            ws_code=status.WS_1008_POLICY_VIOLATION,
            details="not an admin"
        )
    return user


AdminUserAnnotation = typing.Annotated[User, Depends(admin_user_dependency)]
