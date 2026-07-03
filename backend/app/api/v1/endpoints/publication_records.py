from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.publication_record import (
    PublicationRecordCreate,
    PublicationRecordRead,
    PublicationRecordStatusUpdate,
)
from app.services import operational_audit_service, publication_record_service

router = APIRouter(tags=["publication-records"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/publication-records",
    response_model=PublicationRecordRead,
    status_code=201,
    dependencies=[Depends(require_permission("publication.create"))],
)
async def create_publication_record(
    payload: PublicationRecordCreate,
    request: Request,
    session: SessionDep,
) -> PublicationRecordRead:
    record = await publication_record_service.create_publication_record(
        session, payload, request.state.correlation_id
    )
    response = PublicationRecordRead.model_validate(record)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="publication_event",
        action="publication.create",
        permission="publication.create",
        decision="created",
        entity_type="PublicationRecord",
        entity_id=record.id,
        news_item_id=record.news_item_id,
        metadata={
            "publication_status": record.publication_status,
            "channel": record.channel,
            "content_piece_id": record.content_piece_id,
            "distribution_plan_id": record.distribution_plan_id,
        },
    )
    return response


@router.get("/publication-records", response_model=list[PublicationRecordRead])
async def list_publication_records(
    session: SessionDep,
    content_piece_id: str | None = Query(default=None),
    news_item_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[PublicationRecordRead]:
    records = await publication_record_service.list_publication_records(
        session,
        content_piece_id=content_piece_id,
        news_item_id=news_item_id,
        limit=limit,
        offset=offset,
    )
    return [PublicationRecordRead.model_validate(record) for record in records]


@router.get(
    "/content-pieces/{content_piece_id}/publication-records",
    response_model=list[PublicationRecordRead],
)
async def list_content_piece_publication_records(
    content_piece_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[PublicationRecordRead]:
    records = await publication_record_service.list_publication_records(
        session, content_piece_id=content_piece_id, limit=limit, offset=offset
    )
    return [PublicationRecordRead.model_validate(record) for record in records]


@router.get("/news/{news_id}/publication-records", response_model=list[PublicationRecordRead])
async def list_news_publication_records(
    news_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[PublicationRecordRead]:
    records = await publication_record_service.list_publication_records(
        session, news_item_id=news_id, limit=limit, offset=offset
    )
    return [PublicationRecordRead.model_validate(record) for record in records]


@router.patch(
    "/publication-records/{publication_record_id}/status",
    response_model=PublicationRecordRead,
    dependencies=[Depends(require_permission("publication.update_status"))],
)
async def update_publication_record_status(
    publication_record_id: str,
    payload: PublicationRecordStatusUpdate,
    request: Request,
    session: SessionDep,
) -> PublicationRecordRead:
    record = await publication_record_service.update_publication_record_status(
        session, publication_record_id, payload.publication_status
    )
    response = PublicationRecordRead.model_validate(record)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="publication_event",
        action="publication.update_status",
        permission="publication.update_status",
        decision="updated",
        entity_type="PublicationRecord",
        entity_id=record.id,
        news_item_id=record.news_item_id,
        after_state={"publication_status": record.publication_status},
    )
    return response


@router.get("/publication-records/{publication_record_id}", response_model=PublicationRecordRead)
async def get_publication_record(
    publication_record_id: str,
    session: SessionDep,
) -> PublicationRecordRead:
    record = await publication_record_service.get_publication_record(
        session, publication_record_id
    )
    return PublicationRecordRead.model_validate(record)
