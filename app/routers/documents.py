from fastapi import APIRouter

from database import documents_collection as collection
from models.document import Document


router = APIRouter()

@router.get(
    path='/',
    response_model=list[Document],
)
async def read_documents(self):
