import app.models  # noqa: F401
from app.db.base import Base
from app.db.session import engine


async def init_db() -> None:
    # Importing models above registers metadata for create_all in local/test mode.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
