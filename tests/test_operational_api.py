import httpx
import pytest
from fastapi import HTTPException
from types import SimpleNamespace
from unittest.mock import AsyncMock

from app import main, runtime_adapter
from app.main import PostCreate, app, capabilities, create_post, health, ready, version


def test_operational_endpoints_are_attributable_and_fail_closed():
    assert {"/health", "/ready", "/version", "/capabilities"}.issubset(
        app.openapi()["paths"]
    )
    assert health()["service"] == "codestra-social"
    assert version()["service"] == "codestra-social"
    value = capabilities()
    assert value["business_writes_enabled"] is False
    assert value["live_social_publish_enabled"] is False
    assert value["read_only_mode"] is True


def test_version_does_not_invent_runtime_attribution():
    value = version()
    assert value["git_sha"] == "unknown"
    assert value["image_digest"] == "unknown"


def test_unimplemented_publishing_cannot_be_advertised(monkeypatch):
    monkeypatch.setattr(main, "SOCIAL_PUBLISHING_ENABLED", True)
    monkeypatch.setattr(main, "SOCIAL_PUBLISHING_AVAILABLE", False)
    value = capabilities()
    assert value["external_delivery_enabled"] is False
    assert value["live_social_publish_enabled"] is False


@pytest.mark.asyncio
async def test_create_post_is_blocked_before_database_mutation(monkeypatch):
    monkeypatch.setattr(main, "BUSINESS_WRITES_ENABLED", False)
    session = AsyncMock()
    with pytest.raises(HTTPException) as blocked:
        await create_post(
            PostCreate(tenant_id="tenant", account_id="account", body="draft"),
            session,
        )
    assert blocked.value.status_code == 423
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_readiness_rejects_enabled_sync_without_token(monkeypatch):
    monkeypatch.setattr(main, "SOCIAL_READ_SYNC_ENABLED", True)
    monkeypatch.setattr(runtime_adapter, "SOCIAL_RUNTIME_TOKEN", None)
    session = AsyncMock()
    response = await ready(
        SimpleNamespace(state=SimpleNamespace(correlation_id="test-correlation")),
        session,
    )
    assert response.status_code == 503


@pytest.mark.asyncio
async def test_operational_headers_and_content_type():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/health", headers={"X-Correlation-ID": "contract-id"}
        )
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-correlation-id"] == "contract-id"
    assert response.headers["content-type"].startswith("application/json")
