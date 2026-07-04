from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.metric_snapshot import MetricSnapshotCreate, MetricSnapshotRead
from app.services import metrics_memory_knowledge_service as mmk_service

router = APIRouter(tags=["metric-snapshots"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/metric-snapshots",
    response_model=MetricSnapshotRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_metric_snapshot(
    payload: MetricSnapshotCreate,
    request: Request,
    session: SessionDep,
) -> MetricSnapshotRead:
    snapshot = await mmk_service.create_metric_snapshot(
        session, payload, request.state.correlation_id
    )
    return MetricSnapshotRead.model_validate(snapshot)


@router.get("/metric-snapshots", response_model=list[MetricSnapshotRead])
async def list_metric_snapshots(
    session: SessionDep,
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    news_item_id: str | None = Query(default=None),
    content_piece_id: str | None = Query(default=None),
    distribution_plan_id: str | None = Query(default=None),
    publication_record_id: str | None = Query(default=None),
    workflow_run_id: str | None = Query(default=None),
    workflow_task_id: str | None = Query(default=None),
    agent_execution_id: str | None = Query(default=None),
    agent_output_id: str | None = Query(default=None),
    metric_category: str | None = Query(default=None),
    channel: str | None = Query(default=None),
    measurement_window: str | None = Query(default=None),
    metric_name: str | None = Query(default=None),
    data_quality: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[MetricSnapshotRead]:
    snapshots = await mmk_service.list_metric_snapshots(
        session,
        entity_type=entity_type,
        entity_id=entity_id,
        news_item_id=news_item_id,
        content_piece_id=content_piece_id,
        distribution_plan_id=distribution_plan_id,
        publication_record_id=publication_record_id,
        workflow_run_id=workflow_run_id,
        workflow_task_id=workflow_task_id,
        agent_execution_id=agent_execution_id,
        agent_output_id=agent_output_id,
        metric_category=metric_category,
        channel=channel,
        measurement_window=measurement_window,
        metric_name=metric_name,
        data_quality=data_quality,
        limit=limit,
        offset=offset,
    )
    return [MetricSnapshotRead.model_validate(snapshot) for snapshot in snapshots]


@router.get("/metric-snapshots/{metric_snapshot_id}", response_model=MetricSnapshotRead)
async def get_metric_snapshot(
    metric_snapshot_id: str,
    session: SessionDep,
) -> MetricSnapshotRead:
    snapshot = await mmk_service.get_metric_snapshot(session, metric_snapshot_id)
    return MetricSnapshotRead.model_validate(snapshot)


@router.get("/news/{news_id}/metric-snapshots", response_model=list[MetricSnapshotRead])
async def list_news_metric_snapshots(
    news_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[MetricSnapshotRead]:
    snapshots = await mmk_service.list_metric_snapshots(
        session, news_item_id=news_id, limit=limit, offset=offset
    )
    return [MetricSnapshotRead.model_validate(snapshot) for snapshot in snapshots]


@router.get(
    "/publication-records/{publication_record_id}/metric-snapshots",
    response_model=list[MetricSnapshotRead],
)
async def list_publication_metric_snapshots(
    publication_record_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[MetricSnapshotRead]:
    snapshots = await mmk_service.list_metric_snapshots(
        session, publication_record_id=publication_record_id, limit=limit, offset=offset
    )
    return [MetricSnapshotRead.model_validate(snapshot) for snapshot in snapshots]


@router.get(
    "/workflows/{workflow_run_id}/metric-snapshots",
    response_model=list[MetricSnapshotRead],
)
async def list_workflow_metric_snapshots(
    workflow_run_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[MetricSnapshotRead]:
    snapshots = await mmk_service.list_metric_snapshots(
        session, workflow_run_id=workflow_run_id, limit=limit, offset=offset
    )
    return [MetricSnapshotRead.model_validate(snapshot) for snapshot in snapshots]
