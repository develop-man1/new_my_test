from fastapi import FastAPI
from contextlib import asynccontextmanager

from .core.database import Base, engine
from .routes import auth_router, users_router, admin_router, mock_business_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Auth System",
    description="Система аутентификации и авторизации",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(mock_business_router)