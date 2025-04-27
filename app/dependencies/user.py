from fastapi import Depends, HTTPException
from typing import Annotated

from app.models.user import User, UserRole


def get_user(access_token: str | None = None) -> User:
    # raises HTTPException
    if access_token is None:
        raise HTTPException(
            status_code=403,
            detail="access_token must be provided"
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
    raise HTTPException(
        status_code=403,
        detail="access_token is invalid"
    )


UserAnnotation = Annotated[User, Depends(get_user)]


def get_active_user(user: UserAnnotation) -> User:
    # raises HTTPException
    if not user.is_active:
        raise HTTPException(status_code=403, details="inactive user")
    return user


ActiveUserAnnotation = Annotated[User, Depends(get_active_user)]


def get_admin_user(user: UserAnnotation) -> User:
    # raises HTTPException
    if UserRole.ADMIN not in user.roles:
        raise HTTPException(status_code=403, details="not an admin")
    return user


AdminUserAnnotation = Annotated[User, Depends(get_admin_user)]
