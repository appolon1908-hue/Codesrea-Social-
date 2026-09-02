# Repository Profile — Codestra Social Control Plane

## Identity

- **Stable GitHub repository ID:** `1351353723`
- **Current operational repository:** `appolon1908-hue/Codesrea-Social-`
- **Approved target after controlled rename:** `appolon1908-hue/Codestra-Social-Control-Plane`
- **Rename state:** `PREPARED_NOT_RENAMED`
- **Category:** Provider-neutral platform control plane — social
- **Visibility:** `public`
- **Default branch:** `main`
- **Authority:** Social coordination, contracts, and control-plane architecture; the existing application/runtime remains `appolon1908-hue/social.codestra.co`.

The current full name remains authoritative for clone, workflow, package, source-lock, and automation use until GitHub readback proves the same repository ID at the approved target name.

## Purpose

Provide a provider-neutral control plane for social campaigns, content calendars, approvals, publishing commands, engagement normalization, account health, analytics, audit, and operator workflows.

## Ownership

- Cross-provider social campaign and approval model
- Provider-neutral scheduling and publishing command contracts
- Normalized social read models and event contracts
- Operator views for accounts, content, approvals, engagement, failures, audit, and reconciliation
- Release and compatibility coordination with the deployed social platform

## Must not own

- A second Postiz/social runtime that competes with `social.codestra.co`
- Direct provider credentials or browser-to-provider calls
- Marketing, identity, gateway, Middleware, SDK, or provider runtime source
- Production publication authority merely because a branch or documentation change merges

## Integrations

- `social.codestra.co`
- `SDK-repository`
- `Middleware-`
- `Codestra-Marketing-`
- Keycloak, Kong, Caddy, Superset, and Grafana

## Milestones

1. Merge and validate the stable-ID rename preparation.
2. Preserve the boundary with `social.codestra.co` and `Codestra-Marketing-`.
3. Define APIs/events, tenancy, RBAC, idempotency, audit, account health, and reconciliation.
4. Add operator UI, generated SDK integration, CI, staging, rollback, and activation gates.
5. Execute the GitHub slug rename only through the controlled account-wide runbook.

## Governance and safety

- This repository has no direct provider runtime or production publishing authority.
- Never commit social-provider tokens, account credentials, customer content, private keys, or secret-bearing evidence.
- Every provider effect must be routed through Middleware and the actual runtime adapters and proven by read-back.
- A repository rename must not connect accounts, publish posts, activate schedules, build images, deploy software, or change production traffic.

## Account-wide migration authority

Until the documentation repository completes its own controlled rename, use:

- `appolon1908-hue/documentaions:repository-name-migration.v1.json`
- `appolon1908-hue/documentaions:REPOSITORY_NAME_MIGRATION_2026-09-02.md`

Historical evidence retains the name valid at capture time and is not rewritten.