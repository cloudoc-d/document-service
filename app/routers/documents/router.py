from typing import Annotated
from fastapi import APIRouter, Depends

from app.models.user import User
from app.auth_utils import get_active_user


ActiveUser = Annotated[User, Depends(get_active_user)]

router = APIRouter()

from .http import *
from .ws import *
