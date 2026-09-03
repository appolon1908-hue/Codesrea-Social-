import json
import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import (
    SOCIAL_PUBLISHING_ENABLED,
    SOCIAL_READ_SYNC_ENABLED,
    TELEMETRY_EXPORT_ENABLED,
    app,
    capabilities,
)
from app.runtime_adapter import SocialRuntimeReadClient
from app.telemetry import (
    audit_event,
    correlation_id_context,
    install_correlation_middleware,
    private_otlp_endpoint,
)


def test_telemetry_is_default_off_and_does_not_enable_effects():
    assert TELEMETRY_EXPORT_ENABLED is False
    assert SOCIAL_PUBLISHING_ENABLED is False
    assert SOCIAL_READ_SYNC_ENABLED is False
    assert capabilities()["telemetry_export"] is False
    assert capabilities()["correlation_ids"] is True


@pytest.mark.parametrize(
    "endpoint",
    (
        "http://alloy:4318",
        "http://alloy.monitoring.svc:4318",
        "http://127.0.0.1:4318",
        "https://10.20.30.40:4318/v1/traces",
    ),
)
def test_private_otlp_authorities_are_accepted(endpoint):
    assert private_otlp_endpoint(endpoint) == endpoint


@pytest.mark.parametrize(
    "endpoint",
    (
        "https://telemetry.example.com:4318",
        "https://user:secret@alloy:4318",
        "file:///tmp/traces",
        "alloy:4318",
        "https://alloy:4318?token=secret",
    ),
)
def test_external_or_credential_bearing_otlp_authorities_are_rejected(endpoint):
    with pytest.raises(RuntimeError):
        private_otlp_endpoint(endpoint)


def test_correlation_id_is_preserved_or_generated_and_invalid_values_fail_closed():
    test_app = FastAPI()
    install_correlation_middleware(test_app)

    @test_app.get("/")
    def root():
        return {"correlation_id": correlation_id_context.get()}

    client = TestClient(test_app)
    supplied = "social:018f4f7a-1234"
    response = client.get("/", headers={"X-Correlation-ID": supplied})
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == supplied
    assert response.json() == {"correlation_id": supplied}

    generated = client.get("/")
    assert generated.status_code == 200
    assert generated.headers["X-Correlation-ID"] == generated.json()["correlation_id"]

    rejected = client.get("/", headers={"X-Correlation-ID": "secret value invalid"})
    assert rejected.status_code == 400
    assert rejected.json() == {"detail": "invalid_correlation_id"}


def test_runtime_read_adapter_propagates_request_correlation(monkeypatch):
    monkeypatch.setattr("app.runtime_adapter.SOCIAL_RUNTIME_TOKEN", "test-token")
    token = correlation_id_context.set("corr-social-read-123")
    try:
        headers = SocialRuntimeReadClient(client=object())._headers()  # type: ignore[arg-type]
    finally:
        correlation_id_context.reset(token)
    assert headers["X-Correlation-ID"] == "corr-social-read-123"
    assert headers["Authorization"] == "Bearer test-token"


def test_audit_log_excludes_content_account_tenant_and_credentials(caplog):
    original_propagate = logging.getLogger("codestra.social.audit").propagate
    logging.getLogger("codestra.social.audit").propagate = True
    token = correlation_id_context.set("corr-social-123")
    try:
        with caplog.at_level(logging.INFO, logger="codestra.social.audit"):
            audit_event("post_recorded", post_id="post-123", state="draft")
    finally:
        correlation_id_context.reset(token)
        logging.getLogger("codestra.social.audit").propagate = original_propagate
    record = json.loads(caplog.records[-1].message)
    assert record == {
        "correlation_id": "corr-social-123",
        "event": "post_recorded",
        "post_id": "post-123",
        "service": "codestra-social",
        "state": "draft",
    }
    serialized = caplog.records[-1].message.lower()
    for forbidden in ("authorization", "body", "account", "tenant", "token"):
        assert forbidden not in serialized


def test_audit_logger_is_enabled_without_uvicorn_logger_configuration():
    logger = logging.getLogger("codestra.social.audit")
    assert logger.level == logging.INFO
    assert logger.propagate is False
    assert logger.handlers


def test_unhandled_errors_return_a_correlation_id():
    test_app = FastAPI()
    install_correlation_middleware(test_app)

    @test_app.get("/failure")
    def failure():
        raise RuntimeError("sensitive failure detail")

    response = TestClient(test_app, raise_server_exceptions=False).get(
        "/failure", headers={"X-Correlation-ID": "failure-correlation"}
    )
    assert response.status_code == 500
    assert response.headers["X-Correlation-ID"] == "failure-correlation"
    assert response.json() == {"detail": "internal_server_error"}


def test_existing_application_exposes_correlation_header_without_effects():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"]
    assert response.json()["social_publishing_enabled"] is False
    assert response.json()["social_read_sync_enabled"] is False
