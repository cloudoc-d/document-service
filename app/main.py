from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.documents import router as documents_router
from app.routers.styles import router as styles_router
from app.scheduler import scheduler
from app.database import client as mongo_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
    mongo_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router=documents_router)
app.include_router(router=styles_router)
