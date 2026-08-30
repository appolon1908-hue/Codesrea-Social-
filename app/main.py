from enum import StrEnum
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Codestra Social API", version="0.1.0")

SOCIAL_PUBLISHING_ENABLED = False

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
    state: PostState

_posts: dict[UUID, Post] = {}

@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "social_publishing_enabled": SOCIAL_PUBLISHING_ENABLED}

@app.get("/v1/capabilities")
def capabilities() -> dict[str, object]:
    return {
        "accounts": True,
        "posts": True,
        "scheduling": True,
        "approvals": True,
        "engagement_sync": True,
        "publishing": SOCIAL_PUBLISHING_ENABLED,
    }

@app.post("/v1/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(body: PostCreate) -> Post:
    post = Post(id=uuid4(), account_id=body.account_id, body=body.body, state=PostState.DRAFT)
    _posts[post.id] = post
    return post

@app.post("/v1/posts/{post_id}/publish")
def publish(post_id: UUID) -> dict[str, str]:
    if post_id not in _posts:
        raise HTTPException(status_code=404, detail="post_not_found")
    if not SOCIAL_PUBLISHING_ENABLED:
        raise HTTPException(status_code=423, detail="social_publishing_disabled")
    raise HTTPException(status_code=501, detail="runtime_adapter_not_implemented")
