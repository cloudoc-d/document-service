from typing import Annotated
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/documents")


from .endpoints import *
from .endpoints_ws import *
