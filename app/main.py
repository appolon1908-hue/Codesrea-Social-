import os
import asyncio
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .db import get_session
from .models import SocialPostModel
from .runtime_adapter import SocialRuntimeReadClient

app = FastAPI(title="Codestra Social API", version="0.2.0")
SOCIAL_PUBLISHING_ENABLED = os.getenv("SOCIAL_PUBLISHING_ENABLED", "false").lower() == "true"
SOCIAL_READ_SYNC_ENABLED = os.getenv("SOCIAL_READ_SYNC_ENABLED", "false").lower() == "true"
SERVICE = "codestra-social"


@app.middleware("http")
async def operational_headers(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid4())
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Correlation-ID"] = correlation_id
    return response

class PostState(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SCHEDULED = "scheduled"

class PostCreate(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=128)
    account_id: str = Field(min_length=1, max_length=128)
    body: str = Field(min_length=1, max_length=10000)

class Post(BaseModel):
    id: UUID
    account_id: str
    body: str
    state: str
    model_config = {"from_attributes": True}

@app.get("/health")
def health(request: Request = None) -> dict[str, object]:
    correlation_id = getattr(getattr(request, "state", None), "correlation_id", str(uuid4()))
    return {"status": "ok", "service": SERVICE, "timestamp": datetime.now(timezone.utc).isoformat(), "correlation_id": correlation_id}

@app.get("/ready")
async def ready(request: Request, session: AsyncSession = Depends(get_session)):
    try:
        await asyncio.wait_for(session.execute(select(1)), timeout=2.0)
    except Exception:
        return JSONResponse(status_code=503, content={"status": "not_ready", "service": SERVICE, "dependencies": {"database": "unavailable"}, "correlation_id": request.state.correlation_id})
    return {"status": "ready", "service": SERVICE, "dependencies": {"database": "ready", "configuration": "ready"}, "correlation_id": request.state.correlation_id}

@app.get("/version")
def version(request: Request = None) -> dict[str, object]:
    correlation_id = getattr(getattr(request, "state", None), "correlation_id", str(uuid4()))
    return {"service": SERVICE, "application_version": app.version, "api_versions": ["v1"], "git_sha": os.getenv("CODESTRA_GIT_SHA", "unknown"), "image_digest": os.getenv("CODESTRA_IMAGE_DIGEST", "unknown"), "build_timestamp": os.getenv("CODESTRA_BUILD_TIMESTAMP", "unknown"), "migration_revision": os.getenv("CODESTRA_MIGRATION_REVISION", "unknown"), "environment": os.getenv("CODESTRA_ENVIRONMENT", "unknown"), "correlation_id": correlation_id}

@app.get("/capabilities")
@app.get("/v1/capabilities")
def capabilities(request: Request = None) -> dict[str, object]:
    correlation_id = getattr(getattr(request, "state", None), "correlation_id", str(uuid4()))
    return {"service": SERVICE, "maintenance_mode": os.getenv("MAINTENANCE_MODE", "false").lower() == "true", "degraded_mode": False, "business_writes_enabled": False, "external_delivery_enabled": SOCIAL_PUBLISHING_ENABLED, "live_social_publish_enabled": SOCIAL_PUBLISHING_ENABLED, "read_only_mode": not SOCIAL_PUBLISHING_ENABLED, "simulation_enabled": not SOCIAL_PUBLISHING_ENABLED, "supported_api_versions": ["v1"], "accounts": True, "posts": True, "scheduling": True, "approvals": True, "engagement_sync": SOCIAL_READ_SYNC_ENABLED, "publishing": SOCIAL_PUBLISHING_ENABLED, "correlation_id": correlation_id}

@app.post("/v1/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(body: PostCreate, session: AsyncSession = Depends(get_session)) -> SocialPostModel:
    row = SocialPostModel(**body.model_dump(), state=PostState.DRAFT.value)
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row

@app.get("/v1/posts/{post_id}", response_model=Post)
async def get_post(post_id: UUID, session: AsyncSession = Depends(get_session)) -> SocialPostModel:
    row = await session.get(SocialPostModel, post_id)
    if row is None:
        raise HTTPException(status_code=404, detail="post_not_found")
    return row

@app.post("/v1/posts/{post_id}/publish")
async def publish(post_id: UUID, session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    row = await session.get(SocialPostModel, post_id)
    if row is None:
        raise HTTPException(status_code=404, detail="post_not_found")
    if row.state != PostState.APPROVED.value:
        raise HTTPException(status_code=409, detail="post_not_approved")
    if not SOCIAL_PUBLISHING_ENABLED:
        raise HTTPException(status_code=423, detail="social_publishing_disabled")
    raise HTTPException(status_code=501, detail="runtime_publish_not_implemented")

@app.get("/v1/runtime/posts/{runtime_post_id}")
async def runtime_post_snapshot(runtime_post_id: str, correlation_id: str | None = None) -> dict[str, object] | None:
    if not SOCIAL_READ_SYNC_ENABLED:
        return None
    return await SocialRuntimeReadClient().get_post(runtime_post_id, correlation_id)

@app.get("/v1/runtime/posts/{runtime_post_id}/metrics")
async def runtime_post_metrics(runtime_post_id: str, correlation_id: str | None = None) -> dict[str, object] | None:
    if not SOCIAL_READ_SYNC_ENABLED:
        return None
    return await SocialRuntimeReadClient().get_metrics(runtime_post_id, correlation_id)
