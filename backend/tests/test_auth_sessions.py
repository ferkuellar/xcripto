from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models import AuthSession, UserAccount
from app.services.auth_service import hash_password, session_token_hash


async def _create_user(
    email: str = "owner@example.com",
    handle: str = "owner-admin",
    password: str = "CorrectHorseBatteryStaple!123",
    role: str = "owner",
) -> UserAccount:
    async with AsyncSessionLocal() as session:
        user = UserAccount(
            email=email,
            handle=handle,
            display_name="Owner Admin",
            role=role,
            status="active",
            is_active=True,
            password_hash=hash_password(password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def test_password_hash_is_not_plaintext():
    password = "S3curePassword!"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("pbkdf2_sha256$")


async def test_login_me_and_logout_flow(client):
    user = await _create_user()

    login = await client.post(
        "/api/v1/auth/login",
        json={"identifier": user.email, "password": "CorrectHorseBatteryStaple!123"},
    )

    assert login.status_code == 200
    payload = login.json()
    assert payload["user"]["id"] == user.id
    assert payload["user"]["role"] == "owner"
    assert payload["user"]["roles"] == ["owner"]
    assert "password_hash" not in login.text
    assert payload["session"]["authenticated"] is True
    assert payload["session"]["session_expires_at"]

    me = await client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["user"]["id"] == user.id
    assert me.json()["user"]["email"] == user.email

    logout = await client.post("/api/v1/auth/logout")
    assert logout.status_code == 204

    me_after_logout = await client.get("/api/v1/auth/me")
    assert me_after_logout.status_code == 401


async def test_invalid_login_rejected(client):
    await _create_user()

    response = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "owner@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["error"] == "Invalid credentials"


async def test_expired_session_is_rejected(client):
    user = await _create_user()

    login = await client.post(
        "/api/v1/auth/login",
        json={"identifier": user.email, "password": "CorrectHorseBatteryStaple!123"},
    )
    assert login.status_code == 200

    async with AsyncSessionLocal() as session:
        token = client.cookies.get("xmip_session")
        assert token is not None
        auth_session = (
            await session.execute(
                select(AuthSession).where(AuthSession.token_hash == session_token_hash(token))
            )
        ).scalar_one()
        auth_session.expires_at = datetime.now(UTC) - timedelta(minutes=1)
        await session.commit()

    me = await client.get("/api/v1/auth/me")
    assert me.status_code == 401


async def test_production_rejects_spoofed_actor_headers_without_session(client, monkeypatch):
    from app.core.config import get_settings

    settings = get_settings()
    monkeypatch.setattr(settings, "environment", "production")
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "cors_allow_credentials", True)
    monkeypatch.setattr(settings, "session_cookie_secure", True)

    response = await client.post(
        "/api/v1/news/intake",
        json={
            "title": "Spoof test",
            "summary": "Spoof test",
            "category": "markets",
            "priority": "P1",
            "source_url": "https://example.com/spoof",
            "source_name": "Example Wire",
        },
        headers={"X-API-Key": "dev-secret", "X-Actor-Role": "owner", "X-Actor-Id": "fake"},
    )

    assert response.status_code == 401


async def test_authenticated_limited_role_cannot_escalate_with_spoofed_header(client, monkeypatch):
    user = await _create_user(role="viewer", handle="viewer-user", email="viewer@example.com")
    login = await client.post(
        "/api/v1/auth/login",
        json={"identifier": user.email, "password": "CorrectHorseBatteryStaple!123"},
    )
    assert login.status_code == 200

    from app.core.config import get_settings

    settings = get_settings()
    monkeypatch.setattr(settings, "environment", "production")
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "cors_allow_credentials", True)
    monkeypatch.setattr(settings, "session_cookie_secure", True)

    response = await client.get(
        "/api/v1/admin/audit/summary",
        headers={"X-Actor-Role": "owner", "X-Actor-Id": "fake-owner"},
    )

    assert response.status_code == 403
