# Codestra Social Runtime Completion V2

## Authority

This branch starts from `development@23d73c7f213ebd1319a4c67ba5deeaadec6f645f`, which contains the reviewed Social API-completion contract. It implements that contract in the existing Social control-plane repository. `social.codestra.co` remains the provider-facing publishing runtime and Codestra Middleware remains the only durable cross-system write boundary.

This document is an implementation mission, not evidence that the implementation is already complete.

## Required operational API

- `GET /health/live`
- `GET /health/ready`
- `GET /version`
- private authenticated `GET /metrics`
- `GET /v1/social/capabilities`

Liveness must check only the process. Readiness must use bounded dependency checks and must never call a social provider or mutate state. Version readback must expose the service name, semantic version, exact source SHA, immutable image digest, environment, deployment identity and migration head.

## Accounts

- `POST /v1/social/accounts`
- `GET /v1/social/accounts`
- `GET /v1/social/accounts/{account_id}`
- `PATCH /v1/social/accounts/{account_id}`

Account records contain only provider-neutral identity, tenancy, status and protected credential-reference metadata. Provider OAuth tokens may not enter this service, n8n, logs, metrics, OpenAPI examples or test fixtures.

## Posts, revisions and approval

- `POST /v1/social/posts`
- `GET /v1/social/posts`
- `GET /v1/social/posts/{post_id}`
- `PATCH /v1/social/posts/{post_id}`
- `POST /v1/social/posts/{post_id}/submit-for-approval`
- `POST /v1/social/posts/{post_id}/approve`
- `POST /v1/social/posts/{post_id}/reject`
- `POST /v1/social/posts/{post_id}/schedule`

Every content change creates an immutable revision. Approval binds the exact revision digest. An approval is invalidated by later content, account, schedule, audience or policy changes. Separation of duties prevents a requester from approving the same revision where policy requires independent approval.

## Publication operations

- `POST /v1/social/posts/{post_id}/publication-requests`
- `GET /v1/social/publications/{publication_id}`
- `GET /v1/social/publications/{publication_id}/events`
- `POST /v1/social/publications/{publication_id}/cancel`

Publication requests must be durable, tenant-scoped and idempotent. The Social control plane persists the request and submits a canonical command to Middleware; it never calls a provider directly. Unknown submission outcomes enter reconciliation and cannot be blindly retried. Terminal events are immutable and lifecycle transitions are monotonic.

## Engagement and runtime readback

- `GET /v1/social/engagement`
- `GET /v1/social/runtime/posts/{runtime_post_id}`
- `GET /v1/social/runtime/posts/{runtime_post_id}/metrics`
- `POST /v1/social/runtime/sync-requests`
- `GET /v1/social/runtime/sync-requests/{operation_id}`

Read and synchronization operations must use bounded date ranges and pagination. Read sync remains disabled unless the explicit capability is approved. Provider/runtime failures must be represented as sanitized state, not raw provider responses.

## Authentication and authorization

Every protected request verifies:

- issuer;
- signature and algorithm allowlist;
- expiry and not-before;
- exact audience;
- authorized party or machine client;
- exact operation scope;
- tenant claim and tenant-header equality;
- correlation identifier bounds;
- semantic idempotency for mutations.

No browser-stored service credential is allowed. Spoofable trusted-identity headers are rejected or stripped at the gateway. Tenant identity is enforced in both service queries and database constraints.

## Persistence

Add PostgreSQL migrations and models for:

- social accounts;
- social posts;
- immutable content revisions;
- approval records;
- schedules;
- publication operations;
- publication lifecycle events;
- engagement snapshots;
- runtime synchronization operations;
- inbox/outbox or command receipts as required by the Middleware boundary;
- tenant-scoped idempotency records.

Migrations must pass clean-database apply, apply-twice, upgrade from the current released schema and rollback/restore certification. Released migrations may not be rewritten.

## Contracts

Commit OpenAPI 3.1 and AsyncAPI 3.0 documents and fail CI on runtime drift. Each operation requires an operation ID, authentication, audience/scope, tenant behavior, idempotency behavior, standard error envelope, pagination where applicable and external-effect classification.

Compatibility `/v1/posts/*` aliases may remain only when a current consumer is proven. They must emit deprecation, warning, link and sunset metadata and must call the canonical implementation rather than duplicate business logic.

## Observability

Expose privacy-safe metrics for:

- request count and duration;
- authentication failures and authorization denials;
- idempotency conflicts;
- database and dependency latency;
- approval requests, approvals and rejections;
- scheduled publication backlog and oldest age;
- publication submissions, failures and reconciliation;
- engagement and runtime-read failures;
- worker failures, inbox/outbox backlog and dead letters;
- deployment version and capability state.

Allowed metric labels are bounded dimensions such as operation, method, status class, environment, service, deployment and aggregate tenant scope. Tenant IDs, customer/account IDs, post/publication IDs, emails, phone numbers, request IDs, correlation IDs, trace IDs, provider payloads, tokens and secrets are prohibited labels.

Emit structured logs and W3C traces with redaction. Correlation and trace IDs may be fields but not metric labels.

## Required tests

- exact issuer/audience/client/scope authorization;
- tenant isolation and cross-tenant denial;
- semantic idempotency replay and conflicting-key behavior;
- concurrent post/revision mutations;
- approval separation of duties;
- approval invalidation after revision changes;
- schedule/timezone validation;
- publication operation lifecycle and cancellation;
- unknown-outcome reconciliation before retry;
- no direct provider or product-database bypass;
- capability kill switches on every mutation and worker path;
- OpenAPI/AsyncAPI/runtime parity;
- migration apply, apply twice, upgrade and rollback/restore;
- privacy and cardinality checks;
- deterministic dependency lock;
- immutable non-root container build, SBOM, provenance and HIGH/CRITICAL vulnerability policy;
- backup and isolated restore evidence.

## Fail-closed safety baseline

```text
BUSINESS_WRITES_ENABLED=false
SOCIAL_PUBLISHING_ENABLED=false
SOCIAL_READ_SYNC_ENABLED=false
TELEMETRY_EXPORT_ENABLED=false
CONTENT_PUBLISHED=0
RUNTIME_DEPLOYED=false
PRODUCTION_CHANGED=false
```

Source tests must prove that every write, worker dispatch, provider operation and read-sync path remains denied when its capability is false. No provider credential, runtime mutation, publication, read-sync activation or production deployment is authorized by this branch.

## Completion gate

The PR may leave draft only when the actual runtime, migrations, contracts, tests, recovery and immutable image source are present; all exact-head and merge-result checks are green; every review thread is resolved; and an independent reviewer with repository write access approves the unchanged head.

Merging source into `development` is not staging deployment or production activation. A later protected promotion must use exact immutable artifacts, staging migration/rollback evidence, private Keycloak/Kong integration, observability evidence and a separate zero-write canary.