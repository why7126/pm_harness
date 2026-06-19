"""Root test fixtures shared across unit and integration tests."""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Ensure backend package importable when running from repo root
os.environ.setdefault("APP_ENV", "test")


@pytest.fixture()
def tmp_sqlite_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    db_path = tmp_path / "test.db"
    url = f"sqlite:///{db_path}"
    monkeypatch.setenv("SQLITE_DATABASE_URL", url)
    monkeypatch.setenv("ADMIN_INITIAL_PASSWORD", "AdminPass123!")
    monkeypatch.setenv("APP_SECRET_KEY", "test-secret-key")
    return url


@pytest.fixture()
def api_client(tmp_sqlite_url: str, monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.core.config import settings
    from app.db.seed import seed_admin_user
    from app.db.session import get_db, get_session_factory, init_database, reset_engine
    from app.main import app

    reset_engine()
    settings.sqlite_database_url = tmp_sqlite_url
    settings.admin_initial_password = "AdminPass123!"
    settings.app_secret_key = "test-secret-key"
    init_database()

    session = get_session_factory()()
    seed_admin_user(session)
    session.close()

    def override_get_db() -> Generator[Session, None, None]:
        db = get_session_factory()()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    reset_engine()
