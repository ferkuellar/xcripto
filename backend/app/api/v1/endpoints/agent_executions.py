from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import AGENT_EXECUTION_STATUSES
from app.core.errors import DomainValidationError
from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.agent_execution import AgentExecutionCreate, AgentExecutionRead
from app.services import agent_execution_service

router = APIRouter(prefix="/agents/executions", tags=["agent-executions"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "",
    response_model=AgentExecutionRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_execution(
    payload: AgentExecutionCreate,
    request: Request,
    session: SessionDep,
) -> AgentExecutionRead:
    execution = await agent_execution_service.create_execution(
        session, payload, request.state.correlation_id
    )
    return AgentExecutionRead.model_validate(execution)


@router.get("", response_model=list[AgentExecutionRead])
async def list_executions(
    session: SessionDep,
    agent_name: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[AgentExecutionRead]:
    if status is not None and status not in AGENT_EXECUTION_STATUSES:
        raise DomainValidationError(f"status must be one of {sorted(AGENT_EXECUTION_STATUSES)}")
    executions = await agent_execution_service.list_executions(
        session, agent_name=agent_name, status=status, limit=limit, offset=offset
    )
    return [AgentExecutionRead.model_validate(execution) for execution in executions]


@router.get("/{execution_id}", response_model=AgentExecutionRead)
async def get_execution(execution_id: str, session: SessionDep) -> AgentExecutionRead:
    execution = await agent_execution_service.get_execution(session, execution_id)
    return AgentExecutionRead.model_validate(execution)
