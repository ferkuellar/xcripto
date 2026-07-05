from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SOURCE_STATUSES
from app.core.errors import DomainValidationError
from app.core.security import require_api_key
from app.core.source_quality import (
    PRIMARY_OR_TRUSTED_LEVELS,
    is_disqualified,
    source_level_for,
)
from app.db.session import get_session
from app.schemas.source import SourceCreate, SourceRead
from app.services import operational_audit_service, source_service

router = APIRouter(prefix="/sources", tags=["sources"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Niveles que exigen verificación independiente fuerte para publicar (gate S3/S4).
_REQUIRES_STRONG_VERIFICATION_LEVELS = {"S3", "S4"}


@router.post(
    "",
    response_model=SourceRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_source(
    payload: SourceCreate,
    request: Request,
    session: SessionDep,
) -> SourceRead:
    source = await source_service.create_source(session, payload, request.state.correlation_id)
    # Evaluate + audit the source quality at registration (deterministic from the
    # registered source; folds the "quality evaluated" record into the register event).
    disqualified = is_disqualified(source)
    level = source_level_for(source)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="source_event",
        action="source.register",
        decision="created",
        entity_type="SourceReference",
        entity_id=source.id,
        metadata={
            "source_reference_id": source.id,
            "source_name": source.source_name,
            "source_url": operational_audit_service.redact_url(source.source_url),
            "trust_level": source.trust_level,
            "source_status": source.source_status,
            "quality_level": level,
            "disqualified": disqualified,
            "allowed_for_fact_publication": (
                level in PRIMARY_OR_TRUSTED_LEVELS and not disqualified
            ),
            "requires_strong_verification": (
                level in _REQUIRES_STRONG_VERIFICATION_LEVELS and not disqualified
            ),
        },
    )
    return SourceRead.model_validate(source)


@router.get("", response_model=list[SourceRead])
async def list_sources(
    session: SessionDep,
    source_status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[SourceRead]:
    if source_status is not None and source_status not in SOURCE_STATUSES:
        raise DomainValidationError(f"source_status must be one of {sorted(SOURCE_STATUSES)}")
    sources = await source_service.list_sources(
        session, source_status=source_status, limit=limit, offset=offset
    )
    return [SourceRead.model_validate(source) for source in sources]


@router.get("/{source_id}", response_model=SourceRead)
async def get_source(source_id: str, session: SessionDep) -> SourceRead:
    source = await source_service.get_source(session, source_id)
    return SourceRead.model_validate(source)
