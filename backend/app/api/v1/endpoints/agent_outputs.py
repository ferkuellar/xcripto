from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.agent_output import (
    AgentOutputAccept,
    AgentOutputCreate,
    AgentOutputRead,
    AgentOutputReject,
    AgentOutputSupersede,
)
from app.services import agent_output_service

router = APIRouter(tags=["agent-outputs"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/agent-outputs",
    response_model=AgentOutputRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_agent_output(
    payload: AgentOutputCreate,
    request: Request,
    session: SessionDep,
) -> AgentOutputRead:
    output = await agent_output_service.create_agent_output(
        session, payload, request.state.correlation_id
    )
    return AgentOutputRead.model_validate(output)


@router.get("/agent-outputs", response_model=list[AgentOutputRead])
async def list_agent_outputs(
    session: SessionDep,
    agent_name: str | None = Query(default=None),
    output_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    news_item_id: str | None = Query(default=None),
    workflow_run_id: str | None = Query(default=None),
    agent_execution_id: str | None = Query(default=None),
    human_review_required: bool | None = Query(default=None),
    accepted: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[AgentOutputRead]:
    outputs = await agent_output_service.list_agent_outputs(
        session,
        agent_name=agent_name,
        output_type=output_type,
        status=status,
        entity_type=entity_type,
        entity_id=entity_id,
        news_item_id=news_item_id,
        workflow_run_id=workflow_run_id,
        agent_execution_id=agent_execution_id,
        human_review_required=human_review_required,
        accepted=accepted,
        limit=limit,
        offset=offset,
    )
    return [AgentOutputRead.model_validate(output) for output in outputs]


@router.get("/news/{news_id}/agent-outputs", response_model=list[AgentOutputRead])
async def list_news_agent_outputs(
    news_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[AgentOutputRead]:
    outputs = await agent_output_service.list_agent_outputs(
        session, news_item_id=news_id, limit=limit, offset=offset
    )
    return [AgentOutputRead.model_validate(output) for output in outputs]


@router.get("/workflows/{workflow_run_id}/agent-outputs", response_model=list[AgentOutputRead])
async def list_workflow_agent_outputs(
    workflow_run_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[AgentOutputRead]:
    outputs = await agent_output_service.list_agent_outputs(
        session, workflow_run_id=workflow_run_id, limit=limit, offset=offset
    )
    return [AgentOutputRead.model_validate(output) for output in outputs]


@router.patch(
    "/agent-outputs/{agent_output_id}/accept",
    response_model=AgentOutputRead,
    dependencies=[Depends(require_api_key)],
)
async def accept_agent_output(
    agent_output_id: str,
    payload: AgentOutputAccept,
    session: SessionDep,
) -> AgentOutputRead:
    output = await agent_output_service.accept_agent_output(
        session, agent_output_id, payload.accepted_by
    )
    return AgentOutputRead.model_validate(output)


@router.patch(
    "/agent-outputs/{agent_output_id}/reject",
    response_model=AgentOutputRead,
    dependencies=[Depends(require_api_key)],
)
async def reject_agent_output(
    agent_output_id: str,
    payload: AgentOutputReject,
    session: SessionDep,
) -> AgentOutputRead:
    output = await agent_output_service.reject_agent_output(
        session, agent_output_id, payload.rejected_reason
    )
    return AgentOutputRead.model_validate(output)


@router.patch(
    "/agent-outputs/{agent_output_id}/supersede",
    response_model=AgentOutputRead,
    dependencies=[Depends(require_api_key)],
)
async def supersede_agent_output(
    agent_output_id: str,
    payload: AgentOutputSupersede,
    session: SessionDep,
) -> AgentOutputRead:
    output = await agent_output_service.supersede_agent_output(
        session, agent_output_id, payload.superseded_by_output_id
    )
    return AgentOutputRead.model_validate(output)


@router.get("/agent-outputs/{agent_output_id}", response_model=AgentOutputRead)
async def get_agent_output(agent_output_id: str, session: SessionDep) -> AgentOutputRead:
    output = await agent_output_service.get_agent_output(session, agent_output_id)
    return AgentOutputRead.model_validate(output)
