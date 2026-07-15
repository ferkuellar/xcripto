from __future__ import annotations

import base64
import hashlib
import hmac
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from secrets import token_bytes, token_urlsafe

from fastapi import Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.permissions import ROLE_PERMISSIONS
from app.models import AuthSession, OperationalAuditLog, UserAccount

_PASSWORD_HASH_ITERATIONS = 390_000
_PASSWORD_HASH_ALGORITHM = "sha256"
_PASSWORD_HASH_PREFIX = "pbkdf2_sha256"
_LOGIN_FAILURE_WINDOW = timedelta(minutes=15)
_LOGIN_FAILURE_LIMIT = 5


@dataclass(slots=True)
class AuthPrincipal:
    user: UserAccount
    actor_id: str
    actor_role: str
    actor_source: str
    permissions: set[str]
    session: AuthSession | None = None


def hash_password(password: str) -> str:
    salt = token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        _PASSWORD_HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        _PASSWORD_HASH_ITERATIONS,
    )
    salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
    hash_b64 = base64.urlsafe_b64encode(derived).decode("ascii").rstrip("=")
    return f"{_PASSWORD_HASH_PREFIX}${_PASSWORD_HASH_ITERATIONS}${salt_b64}${hash_b64}"


def verify_password(password: str, password_hash: str | None) -> bool:
    if not password_hash:
        return False
    try:
        prefix, iterations, salt_b64, expected_b64 = password_hash.split("$", 3)
    except ValueError:
        return False
    if prefix != _PASSWORD_HASH_PREFIX:
        return False
    try:
        salt = _decode_base64(salt_b64)
        expected = _decode_base64(expected_b64)
        rounds = int(iterations)
    except (ValueError, TypeError):
        return False
    derived = hashlib.pbkdf2_hmac(
        _PASSWORD_HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        rounds,
    )
    return hmac.compare_digest(derived, expected)


def normalize_login_identifier(identifier: str) -> str:
    return identifier.strip().lower()


def session_token_hash(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def generate_session_token() -> str:
    return token_urlsafe(48)


async def get_user_by_identifier(session: AsyncSession, identifier: str) -> UserAccount | None:
    normalized = normalize_login_identifier(identifier)
    stmt = select(UserAccount).where(
        func.lower(func.coalesce(UserAccount.email, "")) == normalized
    )
    user = (await session.execute(stmt.limit(1))).scalar_one_or_none()
    if user is not None:
        return user

    stmt = select(UserAccount).where(
        func.lower(func.coalesce(UserAccount.handle, "")) == normalized
    )
    return (await session.execute(stmt.limit(1))).scalar_one_or_none()


async def authenticate_user(
    session: AsyncSession,
    identifier: str,
    password: str,
) -> UserAccount | None:
    user = await get_user_by_identifier(session, identifier)
    if user is None or not user.is_active or user.status != "active":
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def get_active_session_by_token(
    session: AsyncSession,
    token: str,
) -> AuthSession | None:
    token_hash = session_token_hash(token)
    stmt = select(AuthSession).where(
        AuthSession.token_hash == token_hash,
        AuthSession.revoked_at.is_(None),
        AuthSession.expires_at > datetime.now(UTC),
    )
    return (await session.execute(stmt.limit(1))).scalar_one_or_none()


async def create_session(
    session: AsyncSession,
    user: UserAccount,
    *,
    request: Request | None = None,
) -> tuple[AuthSession, str]:
    settings = get_settings()
    token = generate_session_token()
    now = datetime.now(UTC)
    auth_session = AuthSession(
        user_id=user.id,
        token_hash=session_token_hash(token),
        expires_at=now + timedelta(seconds=settings.session_ttl_seconds),
        last_seen_at=now,
        user_agent=(request.headers.get("user-agent") if request else None),
        client_ip=_client_ip(request),
    )
    session.add(auth_session)
    user.last_login_at = now
    user.last_seen_at = now
    await session.commit()
    await session.refresh(auth_session)
    await session.refresh(user)
    return auth_session, token


async def revoke_session(session: AsyncSession, auth_session: AuthSession) -> AuthSession:
    auth_session.revoked_at = datetime.now(UTC)
    await session.commit()
    await session.refresh(auth_session)
    return auth_session


async def revoke_session_by_token(
    session: AsyncSession,
    token: str,
) -> AuthSession | None:
    auth_session = await get_active_session_by_token(session, token)
    if auth_session is None:
        return None
    return await revoke_session(session, auth_session)


async def resolve_request_principal(
    request: Request,
    session: AsyncSession,
) -> AuthPrincipal | None:
    settings = get_settings()
    session_token = request.cookies.get(settings.session_cookie_name)
    if session_token:
        auth_session = await get_active_session_by_token(session, session_token)
        if auth_session is not None:
            user = await session.get(UserAccount, auth_session.user_id)
            if user is not None and user.is_active and user.status == "active":
                auth_session.last_seen_at = datetime.now(UTC)
                user.last_seen_at = datetime.now(UTC)
                await session.commit()
                await session.refresh(auth_session)
                await session.refresh(user)
                role = user.role
                permissions = set(ROLE_PERMISSIONS.get(role, set()))
                actor_id = user.handle or user.email or user.id
                return AuthPrincipal(
                    user=user,
                    actor_id=actor_id,
                    actor_role=role,
                    actor_source="session",
                    permissions=permissions,
                    session=auth_session,
                )

    return None


async def count_recent_failed_logins(
    session: AsyncSession,
    identifier: str,
    *,
    window: timedelta = _LOGIN_FAILURE_WINDOW,
) -> int:
    normalized = normalize_login_identifier(identifier)
    since = datetime.now(UTC) - window
    stmt = select(func.count()).select_from(OperationalAuditLog).where(
        OperationalAuditLog.event_type == "auth_event",
        OperationalAuditLog.action == "auth.login",
        OperationalAuditLog.outcome == "failed",
        OperationalAuditLog.actor_id == normalized,
        OperationalAuditLog.created_at >= since,
    )
    return int((await session.execute(stmt)).scalar_one())


def login_rate_limit_exceeded(failure_count: int) -> bool:
    return failure_count >= _LOGIN_FAILURE_LIMIT


def cookie_settings() -> dict[str, object]:
    settings = get_settings()
    return {
        "httponly": True,
        "secure": settings.session_cookie_secure,
        "samesite": settings.session_cookie_samesite,
        "path": settings.session_cookie_path,
        "max_age": settings.session_ttl_seconds,
    }


def _client_ip(request: Request | None) -> str | None:
    if request is None or request.client is None:
        return None
    return request.client.host


def _decode_base64(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)
