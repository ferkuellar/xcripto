from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.editorial_readiness import EditorialReadinessScoreRead
from app.services import editorial_readiness_service, operational_audit_service

router = APIRouter(prefix="/editorial-readiness", tags=["editorial-readiness"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/news/{news_id}/calculate",
    response_model=EditorialReadinessScoreRead,
    status_code=201,
    dependencies=[Depends(require_permission("readiness.calculate"))],
)
async def calculate_editorial_readiness(
    news_id: str,
    request: Request,
    session: SessionDep,
) -> EditorialReadinessScoreRead:
    score = await editorial_readiness_service.calculate_editorial_readiness(
        session, news_id, request.state.correlation_id
    )
    response = EditorialReadinessScoreRead.model_validate(score)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="readiness_event",
        action="readiness.calculate",
        permission="readiness.calculate",
        decision="calculated",
        entity_type="EditorialReadinessScore",
        entity_id=score.id,
        news_item_id=score.news_item_id,
        workflow_run_id=score.workflow_run_id,
        metadata={
            "score": score.score,
            "score_band": score.score_band,
            "readiness_status": score.readiness_status,
        },
    )
    return response


@router.get("/news/{news_id}/latest", response_model=EditorialReadinessScoreRead)
async def get_latest_editorial_readiness(
    news_id: str,
    session: SessionDep,
) -> EditorialReadinessScoreRead:
    score = await editorial_readiness_service.get_latest_readiness_score(session, news_id)
    return EditorialReadinessScoreRead.model_validate(score)


@router.get("", response_model=list[EditorialReadinessScoreRead])
async def list_editorial_readiness_scores(
    session: SessionDep,
    news_item_id: str | None = Query(default=None),
    workflow_run_id: str | None = Query(default=None),
    score_band: str | None = Query(default=None),
    readiness_status: str | None = Query(default=None),
    next_agent: str | None = Query(default=None),
    human_review_required: bool | None = Query(default=None),
    publication_block_recommended: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[EditorialReadinessScoreRead]:
    scores = await editorial_readiness_service.list_readiness_scores(
        session,
        news_item_id=news_item_id,
        workflow_run_id=workflow_run_id,
        score_band=score_band,
        readiness_status=readiness_status,
        next_agent=next_agent,
        human_review_required=human_review_required,
        publication_block_recommended=publication_block_recommended,
        limit=limit,
        offset=offset,
    )
    return [EditorialReadinessScoreRead.model_validate(score) for score in scores]


@router.get("/{score_id}", response_model=EditorialReadinessScoreRead)
async def get_editorial_readiness_score(
    score_id: str,
    session: SessionDep,
) -> EditorialReadinessScoreRead:
    score = await editorial_readiness_service.get_readiness_score(session, score_id)
    return EditorialReadinessScoreRead.model_validate(score)


@router.get("/news/{news_id}/explain", response_model=EditorialReadinessScoreRead)
async def explain_editorial_readiness(
    news_id: str,
    session: SessionDep,
) -> EditorialReadinessScoreRead:
    payload = await editorial_readiness_service.explain_editorial_readiness(session, news_id)
    payload["id"] = "not-persisted"
    payload["created_at"] = payload["updated_at"] = datetime.now(UTC)
    return EditorialReadinessScoreRead.model_validate(payload)
