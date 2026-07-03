from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.models import UserAccount
from app.schemas.user_account import UserAccountCreate, UserAccountUpdate


async def create_user_account(
    session: AsyncSession,
    payload: UserAccountCreate,
    correlation_id: str | None = None,
) -> UserAccount:
    await _ensure_unique_user_fields(session, payload.email, payload.handle)
    user = UserAccount(**payload.model_dump())
    if user.correlation_id is None:
        user.correlation_id = correlation_id
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def list_user_accounts(
    session: AsyncSession,
    role: str | None = None,
    status: str | None = None,
    is_active: bool | None = None,
    email: str | None = None,
    handle: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[UserAccount]:
    stmt = select(UserAccount).order_by(UserAccount.created_at.desc())
    filters = {
        "role": role,
        "status": status,
        "is_active": is_active,
        "email": email,
        "handle": handle,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(UserAccount, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_user_account(session: AsyncSession, user_id: str) -> UserAccount:
    user = await session.get(UserAccount, user_id)
    if user is None:
        raise NotFoundError("User account")
    return user


async def update_user_account(
    session: AsyncSession,
    user_id: str,
    payload: UserAccountUpdate,
) -> UserAccount:
    user = await get_user_account(session, user_id)
    data = payload.model_dump(exclude_unset=True)
    if "email" in data and data["email"] != user.email:
        await _ensure_unique_user_fields(session, data["email"], None, exclude_user_id=user.id)
    if "handle" in data and data["handle"] != user.handle:
        await _ensure_unique_user_fields(session, None, data["handle"], exclude_user_id=user.id)
    for field, value in data.items():
        setattr(user, field, value)
    await session.commit()
    await session.refresh(user)
    return user


async def activate_user_account(session: AsyncSession, user_id: str) -> UserAccount:
    user = await get_user_account(session, user_id)
    user.status = "active"
    user.is_active = True
    await session.commit()
    await session.refresh(user)
    return user


async def deactivate_user_account(session: AsyncSession, user_id: str) -> UserAccount:
    user = await get_user_account(session, user_id)
    user.status = "inactive"
    user.is_active = False
    await session.commit()
    await session.refresh(user)
    return user


async def _ensure_unique_user_fields(
    session: AsyncSession,
    email: str | None,
    handle: str | None,
    exclude_user_id: str | None = None,
) -> None:
    if email:
        stmt = select(UserAccount).where(UserAccount.email == email)
        if exclude_user_id:
            stmt = stmt.where(UserAccount.id != exclude_user_id)
        if (await session.execute(stmt.limit(1))).scalar_one_or_none() is not None:
            raise ConflictError("UserAccount email already exists")
    if handle:
        stmt = select(UserAccount).where(UserAccount.handle == handle)
        if exclude_user_id:
            stmt = stmt.where(UserAccount.id != exclude_user_id)
        if (await session.execute(stmt.limit(1))).scalar_one_or_none() is not None:
            raise ConflictError("UserAccount handle already exists")
