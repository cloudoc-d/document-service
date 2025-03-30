from fastapi import FastAPI
from .routers.documents import router as documents_router


app = FastAPI()

app.include_router(router=documents_router, prefix="/documents")
