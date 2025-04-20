from fastapi import APIRouter


router = APIRouter(prefix="/styles")

from .endpoints import *
