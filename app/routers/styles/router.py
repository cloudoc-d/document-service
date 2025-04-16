from fastapi import APIRouter


router = APIRouter(prefix="styles")

from .http import *
