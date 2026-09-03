# Codestra Social API Completion V1

This branch completes the tenant-governed Social control plane while preserving `social.codestra.co` as the publishing runtime and Middleware as the only cross-system write boundary.

## Canonical surface

- `GET /health/live`, `GET /health/ready`, `GET /version`, private `GET /metrics`
- account create/list/detail/update
- post create/list/detail/update
- content-revision-bound submit/approve/reject
- validated scheduling
- durable publication request/status/events/cancel
- engagement read API
- runtime post/metric readback
- read-sync request/status

`/v1/social/*` is canonical. Existing `/v1/posts/*` routes remain only as explicit deprecated compatibility aliases when tests prove they are still required.

## Security and durability

Every tenant mutation requires verified Keycloak issuer, audience, client, scope and tenant claims plus correlation and semantic idempotency. Approval binds the exact immutable content revision and enforces separation of duties. Unknown publication outcomes enter reconciliation before retry.

Publishing requests are durable Middleware operations. Social does not call Postly/Postiz or social providers directly, and provider OAuth tokens remain within the runtime/OpenBao boundary. n8n receives no provider token and performs no direct provider or product-database write.

## Required source evidence

- PostgreSQL migrations and reversible rollback/restore evidence
- tenant and idempotency concurrency tests
- OpenAPI 3.1 and AsyncAPI 3.0 runtime parity
- request/auth/idempotency/approval/scheduling/publication/reconciliation/provider-sync/safety metrics
- no customer or tenant identifiers in metric labels

## Safety baseline

```text
BUSINESS_WRITES_ENABLED=false
SOCIAL_PUBLISHING_ENABLED=false
SOCIAL_READ_SYNC_ENABLED=false
TELEMETRY_EXPORT_ENABLED=false
CONTENT_PUBLISHED=0
RUNTIME_DEPLOYED=false
PRODUCTION_CHANGED=false
```
