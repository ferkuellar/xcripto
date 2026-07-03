from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key, require_permission
from app.db.session import get_session
from app.schemas.memory_item import (
    MemoryItemApprove,
    MemoryItemArchive,
    MemoryItemCreate,
    MemoryItemInvalidate,
    MemoryItemRead,
    MemoryItemReject,
)
from app.services import metrics_memory_knowledge_service as mmk_service

router = APIRouter(tags=["memory-items"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/memory-items",
    response_model=MemoryItemRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_memory_item(
    payload: MemoryItemCreate,
    request: Request,
    session: SessionDep,
) -> MemoryItemRead:
    memory = await mmk_service.create_memory_item(session, payload, request.state.correlation_id)
    return MemoryItemRead.model_validate(memory)


@router.get("/memory-items", response_model=list[MemoryItemRead])
async def list_memory_items(
    session: SessionDep,
    memory_type: str | None = Query(default=None),
    memory_status: str | None = Query(default=None),
    scope: str | None = Query(default=None),
    confidence_level: str | None = Query(default=None),
    persistence_level: str | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    news_item_id: str | None = Query(default=None),
    workflow_run_id: str | None = Query(default=None),
    agent_output_id: str | None = Query(default=None),
    human_review_required: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[MemoryItemRead]:
    memories = await mmk_service.list_memory_items(
        session,
        memory_type=memory_type,
        memory_status=memory_status,
        scope=scope,
        confidence_level=confidence_level,
        persistence_level=persistence_level,
        entity_type=entity_type,
        entity_id=entity_id,
        news_item_id=news_item_id,
        workflow_run_id=workflow_run_id,
        agent_output_id=agent_output_id,
        human_review_required=human_review_required,
        limit=limit,
        offset=offset,
    )
    return [MemoryItemRead.model_validate(memory) for memory in memories]


@router.get("/memory-items/{memory_item_id}", response_model=MemoryItemRead)
async def get_memory_item(memory_item_id: str, session: SessionDep) -> MemoryItemRead:
    memory = await mmk_service.get_memory_item(session, memory_item_id)
    return MemoryItemRead.model_validate(memory)


@router.get("/news/{news_id}/memory-items", response_model=list[MemoryItemRead])
async def list_news_memory_items(
    news_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[MemoryItemRead]:
    memories = await mmk_service.list_memory_items(
        session, news_item_id=news_id, limit=limit, offset=offset
    )
    return [MemoryItemRead.model_validate(memory) for memory in memories]


@router.get("/workflows/{workflow_run_id}/memory-items", response_model=list[MemoryItemRead])
async def list_workflow_memory_items(
    workflow_run_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[MemoryItemRead]:
    memories = await mmk_service.list_memory_items(
        session, workflow_run_id=workflow_run_id, limit=limit, offset=offset
    )
    return [MemoryItemRead.model_validate(memory) for memory in memories]


@router.patch(
    "/memory-items/{memory_item_id}/approve",
    response_model=MemoryItemRead,
    dependencies=[Depends(require_permission("memory.approve"))],
)
async def approve_memory_item(
    memory_item_id: str,
    payload: MemoryItemApprove,
    session: SessionDep,
) -> MemoryItemRead:
    memory = await mmk_service.approve_memory_item(session, memory_item_id, payload.approved_by)
    return MemoryItemRead.model_validate(memory)


@router.patch(
    "/memory-items/{memory_item_id}/reject",
    response_model=MemoryItemRead,
    dependencies=[Depends(require_api_key)],
)
async def reject_memory_item(
    memory_item_id: str,
    payload: MemoryItemReject,
    session: SessionDep,
) -> MemoryItemRead:
    memory = await mmk_service.reject_memory_item(session, memory_item_id, payload.reason)
    return MemoryItemRead.model_validate(memory)


@router.patch(
    "/memory-items/{memory_item_id}/invalidate",
    response_model=MemoryItemRead,
    dependencies=[Depends(require_permission("memory.invalidate"))],
)
async def invalidate_memory_item(
    memory_item_id: str,
    payload: MemoryItemInvalidate,
    session: SessionDep,
) -> MemoryItemRead:
    memory = await mmk_service.invalidate_memory_item(
        session, memory_item_id, payload.invalidated_by, payload.reason
    )
    return MemoryItemRead.model_validate(memory)


@router.patch(
    "/memory-items/{memory_item_id}/archive",
    response_model=MemoryItemRead,
    dependencies=[Depends(require_api_key)],
)
async def archive_memory_item(
    memory_item_id: str,
    payload: MemoryItemArchive,
    session: SessionDep,
) -> MemoryItemRead:
    memory = await mmk_service.archive_memory_item(session, memory_item_id, payload.reason)
    return MemoryItemRead.model_validate(memory)
