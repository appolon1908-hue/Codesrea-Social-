import os
from enum import StrEnum
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session
from .models import SocialPostModel

app = FastAPI(title="Codestra Social API", version="0.2.0")
SOCIAL_PUBLISHING_ENABLED = os.getenv("SOCIAL_PUBLISHING_ENABLED", "false").lower() == "true"
SOCIAL_READ_SYNC_ENABLED = os.getenv("SOCIAL_READ_SYNC_ENABLED", "false").lower() == "true"

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
def health() -> dict[str, object]:
    return {"status": "ok", "social_publishing_enabled": SOCIAL_PUBLISHING_ENABLED, "social_read_sync_enabled": SOCIAL_READ_SYNC_ENABLED}

@app.get("/v1/capabilities")
def capabilities() -> dict[str, object]:
    return {"accounts": True, "posts": True, "scheduling": True, "approvals": True, "engagement_sync": SOCIAL_READ_SYNC_ENABLED, "publishing": SOCIAL_PUBLISHING_ENABLED}

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
    raise HTTPException(status_code=501, detail="runtime_adapter_not_implemented")
