from typing import Annotated
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/documents")


from .http import *
from .ws import *
