from fastapi import FastAPI
from app.routers.documents import router as documents_router
from app.routers.styles import router as styles_router


app = FastAPI()

app.include_router(router=documents_router)
app.include_router(router=styles_router)
