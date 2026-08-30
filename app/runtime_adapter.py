import os
from typing import Any
import httpx

SOCIAL_RUNTIME_URL = os.getenv("SOCIAL_RUNTIME_URL", "http://social-runtime:3000")
SOCIAL_RUNTIME_TOKEN = os.getenv("SOCIAL_RUNTIME_TOKEN")
SOCIAL_READ_SYNC_ENABLED = os.getenv("SOCIAL_READ_SYNC_ENABLED", "false").lower() == "true"

class SocialRuntimeReadClient:
    """Read/reconciliation adapter. Publishing methods are intentionally absent."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(timeout=15.0)

    def _headers(self, correlation_id: str | None = None) -> dict[str, str]:
        if not SOCIAL_RUNTIME_TOKEN:
            raise RuntimeError("social_runtime_token_missing")
        headers = {"Authorization": f"Bearer {SOCIAL_RUNTIME_TOKEN}", "Accept": "application/json"}
        if correlation_id:
            headers["X-Correlation-ID"] = correlation_id
        return headers

    async def get_post(self, runtime_post_id: str, correlation_id: str | None = None) -> dict[str, Any] | None:
        if not SOCIAL_READ_SYNC_ENABLED:
            return None
        response = await self._client.get(f"{SOCIAL_RUNTIME_URL}/api/posts/{runtime_post_id}", headers=self._headers(correlation_id))
        response.raise_for_status()
        return response.json()

    async def get_metrics(self, runtime_post_id: str, correlation_id: str | None = None) -> dict[str, Any] | None:
        if not SOCIAL_READ_SYNC_ENABLED:
            return None
        response = await self._client.get(f"{SOCIAL_RUNTIME_URL}/api/posts/{runtime_post_id}/metrics", headers=self._headers(correlation_id))
        response.raise_for_status()
        return response.json()
