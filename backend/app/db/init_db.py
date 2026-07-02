from app.db.base import Base
from app.db.session import engine
from app.models import AgentExecution, AuditCheck, NewsItem, SourceReference


async def init_db() -> None:
    # Importing models above registers metadata for create_all in local/test mode.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

