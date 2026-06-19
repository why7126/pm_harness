"""API integration baseline tests."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_endpoint(api_client: TestClient) -> None:
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_available(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    payload = response.json()
    assert "paths" in payload
    assert "/api/v1/auth/login" in payload["paths"]
