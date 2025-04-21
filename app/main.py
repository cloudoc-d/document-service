from fastapi import FastAPI
from app.routers.documents import router as documents_router
from app.routers.styles import router as styles_router
from contextlib import asynccontextmanager
from app.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(router=documents_router)
app.include_router(router=styles_router)
