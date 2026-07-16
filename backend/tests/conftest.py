import os

# Ignore any local backend/.env (used for docker/VPS runs) so the suite is hermetic:
# a production-like .env (AUTH_ENABLED=true, custom CORS, Postgres URL) must not leak
# into tests. Must be set before app modules build settings/engine at import time.
os.environ["XMIP_DISABLE_DOTENV"] = "1"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["ENVIRONMENT"] = "test"
os.environ["AUTO_CREATE_TABLES"] = "false"

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def clean_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
