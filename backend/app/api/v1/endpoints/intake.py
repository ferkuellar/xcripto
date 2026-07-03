from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key, require_permission
from app.db.session import get_session
from app.schemas.intake import (
    IntakeAdapterRunCreate,
    IntakeAdapterRunRead,
    IntakeSignalCreate,
    IntakeSignalPromote,
    IntakeSignalRead,
    IntakeSignalReject,
)
from app.services import intake_service

router = APIRouter(prefix="/intake", tags=["intake"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/signals",
    response_model=IntakeSignalRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_signal(
    payload: IntakeSignalCreate,
    request: Request,
    session: SessionDep,
) -> IntakeSignalRead:
    signal = await intake_service.create_intake_signal(
        session, payload, request.state.correlation_id
    )
    return IntakeSignalRead.model_validate(signal)


@router.get("/signals", response_model=list[IntakeSignalRead])
async def list_signals(
    session: SessionDep,
    signal_type: str | None = Query(default=None),
    signal_status: str | None = Query(default=None),
    dedupe_status: str | None = Query(default=None),
    source_name: str | None = Query(default=None),
    source_type: str | None = Query(default=None),
    topic: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    linked_news_item_id: str | None = Query(default=None),
    promoted_news_item_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[IntakeSignalRead]:
    signals = await intake_service.list_intake_signals(
        session,
        signal_type=signal_type,
        signal_status=signal_status,
        dedupe_status=dedupe_status,
        source_name=source_name,
        source_type=source_type,
        topic=topic,
        priority=priority,
        linked_news_item_id=linked_news_item_id,
        promoted_news_item_id=promoted_news_item_id,
        limit=limit,
        offset=offset,
    )
    return [IntakeSignalRead.model_validate(signal) for signal in signals]


@router.get("/signals/{signal_id}", response_model=IntakeSignalRead)
async def get_signal(signal_id: str, session: SessionDep) -> IntakeSignalRead:
    signal = await intake_service.get_intake_signal(session, signal_id)
    return IntakeSignalRead.model_validate(signal)


@router.post(
    "/signals/{signal_id}/dedupe",
    response_model=IntakeSignalRead,
    dependencies=[Depends(require_api_key)],
)
async def dedupe_signal(signal_id: str, session: SessionDep) -> IntakeSignalRead:
    signal = await intake_service.recalculate_signal_dedupe(session, signal_id)
    return IntakeSignalRead.model_validate(signal)


@router.post(
    "/signals/{signal_id}/promote",
    response_model=IntakeSignalRead,
    dependencies=[Depends(require_permission("intake.promote"))],
)
async def promote_signal(
    signal_id: str,
    payload: IntakeSignalPromote,
    request: Request,
    session: SessionDep,
) -> IntakeSignalRead:
    signal = await intake_service.promote_intake_signal(
        session,
        signal_id,
        create_workflow=payload.create_workflow,
        workflow_type=payload.workflow_type,
        correlation_id=request.state.correlation_id,
    )
    return IntakeSignalRead.model_validate(signal)


@router.patch(
    "/signals/{signal_id}/reject",
    response_model=IntakeSignalRead,
    dependencies=[Depends(require_api_key)],
)
async def reject_signal(
    signal_id: str,
    payload: IntakeSignalReject,
    session: SessionDep,
) -> IntakeSignalRead:
    signal = await intake_service.reject_intake_signal(session, signal_id, payload.reason)
    return IntakeSignalRead.model_validate(signal)


@router.patch(
    "/signals/{signal_id}/archive",
    response_model=IntakeSignalRead,
    dependencies=[Depends(require_api_key)],
)
async def archive_signal(signal_id: str, session: SessionDep) -> IntakeSignalRead:
    signal = await intake_service.archive_intake_signal(session, signal_id)
    return IntakeSignalRead.model_validate(signal)


@router.post(
    "/adapter-runs",
    response_model=IntakeAdapterRunRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_adapter_run(
    payload: IntakeAdapterRunCreate,
    request: Request,
    session: SessionDep,
) -> IntakeAdapterRunRead:
    run = await intake_service.create_adapter_run(
        session, payload, request.state.correlation_id
    )
    return IntakeAdapterRunRead.model_validate(run)


@router.get("/adapter-runs", response_model=list[IntakeAdapterRunRead])
async def list_adapter_runs(
    session: SessionDep,
    adapter_name: str | None = Query(default=None),
    adapter_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[IntakeAdapterRunRead]:
    runs = await intake_service.list_adapter_runs(
        session,
        adapter_name=adapter_name,
        adapter_type=adapter_type,
        status=status,
        limit=limit,
        offset=offset,
    )
    return [IntakeAdapterRunRead.model_validate(run) for run in runs]


@router.get("/adapter-runs/{adapter_run_id}", response_model=IntakeAdapterRunRead)
async def get_adapter_run(
    adapter_run_id: str,
    session: SessionDep,
) -> IntakeAdapterRunRead:
    run = await intake_service.get_adapter_run(session, adapter_run_id)
    return IntakeAdapterRunRead.model_validate(run)
