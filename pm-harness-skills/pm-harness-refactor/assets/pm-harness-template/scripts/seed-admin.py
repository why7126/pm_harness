#!/usr/bin/env python3
"""Seed default admin user from ADMIN_INITIAL_PASSWORD."""

from __future__ import annotations

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "src" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import settings  # noqa: E402
from app.db.seed import seed_admin_user  # noqa: E402
from app.db.session import get_session_factory, init_database  # noqa: E402


def main() -> int:
    if not settings.admin_initial_password:
        print("ADMIN_INITIAL_PASSWORD is not set; skipping admin seed.")
        return 0

    init_database()
    session = get_session_factory()()
    try:
        created = seed_admin_user(session)
        if created:
            print(f"Created admin user '{settings.admin_username}'.")
        else:
            print(f"Admin user '{settings.admin_username}' already exists.")
    finally:
        session.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
