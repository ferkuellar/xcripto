from __future__ import annotations

import argparse
import asyncio
import sys
from getpass import getpass
from pathlib import Path

from sqlalchemy import or_, select

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import get_settings  # noqa: E402
from app.db.session import AsyncSessionLocal  # noqa: E402
from app.models import UserAccount  # noqa: E402
from app.services.auth_service import hash_password  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create the initial XMIP admin user.")
    parser.add_argument("--email", required=True, help="Admin email address")
    parser.add_argument("--handle", required=False, help="Admin username/handle")
    parser.add_argument("--display-name", required=True, help="Admin display name")
    parser.add_argument("--role", default="owner", help="Admin role (default: owner)")
    parser.add_argument("--password", required=False, help="Admin password")
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    password = args.password or getpass("Admin password: ")
    if not password:
        raise SystemExit("Password cannot be empty")

    settings = get_settings()

    async with AsyncSessionLocal() as session:
        duplicate_filter = UserAccount.email == args.email
        if args.handle:
            duplicate_filter = or_(duplicate_filter, UserAccount.handle == args.handle)
        existing = (
            await session.execute(select(UserAccount).where(duplicate_filter))
        ).scalar_one_or_none()
        if existing is not None:
            raise SystemExit(
                f"User already exists for email/handle {args.email!r}/{args.handle!r}"
            )

        user = UserAccount(
            email=args.email,
            handle=args.handle,
            display_name=args.display_name,
            role=args.role,
            status="active",
            is_active=True,
            is_system_user=False,
            password_hash=hash_password(password),
            correlation_id=f"bootstrap:{settings.environment}",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    print(f"Created admin user {user.id} ({user.email or user.handle})")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
