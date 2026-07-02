from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.models import AgentExecution
from app.schemas.agent_execution import AgentExecutionCreate


async def create_execution(
    session: AsyncSession, payload: AgentExecutionCreate, correlation_id: str | None = None
) -> AgentExecution:
    execution = AgentExecution(**payload.model_dump())
    if execution.correlation_id is None:
        execution.correlation_id = correlation_id
    session.add(execution)
    await session.commit()
    await session.refresh(execution)
    return execution


async def list_executions(
    session: AsyncSession,
    agent_name: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[AgentExecution]:
    stmt = (
        select(AgentExecution)
        .order_by(AgentExecution.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if agent_name is not None:
        stmt = stmt.where(AgentExecution.agent_name == agent_name)
    if status is not None:
        stmt = stmt.where(AgentExecution.status == status)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_execution(session: AsyncSession, execution_id: str) -> AgentExecution:
    execution = await session.get(AgentExecution, execution_id)
    if execution is None:
        raise NotFoundError("Agent execution")
    return execution
