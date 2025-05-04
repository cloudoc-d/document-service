from datetime import datetime
from app.models.user import User, UserRole
import app.dependencies.user
from app.main import app as target_app
from .common import generate_rand_str


def create_user(
    is_active: bool = True,
    is_admin: bool = False,
    email: str | None = None,
    name: str | None = None,
    id: str | None = None,
    created_at: datetime | None = None,
) -> User:
    return User(
        id=id if id else generate_rand_str(),
        name=name if name else generate_rand_str(),
        is_active=is_active,
        email=email if email else f"{generate_rand_str()}@email.io",
        roles=[UserRole.ADMIN] if is_admin else [],
        created_at=created_at if created_at else datetime.now()
    )


def override_target_app_user(user: User) -> None:
    def get_user() -> User:
        return user

    target_app.dependency_overrides[app.dependencies.user.get_user] = get_user


def clear_target_app_user_override() -> None:
    target_app.dependency_overrides.pop(app.dependencies.user.get_user)
