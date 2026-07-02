from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.verification_record import VerificationRecordCreate, VerificationRecordRead
from app.services import verification_record_service

router = APIRouter(tags=["verification-records"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/verification-records",
    response_model=VerificationRecordRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_verification_record(
    payload: VerificationRecordCreate,
    request: Request,
    session: SessionDep,
) -> VerificationRecordRead:
    record = await verification_record_service.create_verification_record(
        session, payload, request.state.correlation_id
    )
    return VerificationRecordRead.model_validate(record)


@router.get("/verification-records", response_model=list[VerificationRecordRead])
async def list_verification_records(
    session: SessionDep,
    news_item_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[VerificationRecordRead]:
    records = await verification_record_service.list_verification_records(
        session, news_item_id=news_item_id, limit=limit, offset=offset
    )
    return [VerificationRecordRead.model_validate(record) for record in records]


@router.get("/news/{news_id}/verification-records", response_model=list[VerificationRecordRead])
async def list_news_verification_records(
    news_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[VerificationRecordRead]:
    records = await verification_record_service.list_verification_records(
        session, news_item_id=news_id, limit=limit, offset=offset
    )
    return [VerificationRecordRead.model_validate(record) for record in records]


@router.get("/verification-records/{verification_record_id}", response_model=VerificationRecordRead)
async def get_verification_record(
    verification_record_id: str,
    session: SessionDep,
) -> VerificationRecordRead:
    record = await verification_record_service.get_verification_record(
        session, verification_record_id
    )
    return VerificationRecordRead.model_validate(record)
