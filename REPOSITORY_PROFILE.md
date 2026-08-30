# Repository Profile — `Codesrea-Social-`

## Identity

- **Repository:** `appolon1908-hue/Codesrea-Social-`
- **Category:** Planned platform control plane — social
- **Visibility:** `public`
- **Default branch:** `main`
- **Authority:** Proposed provider-neutral social coordination control plane; existing runtime remains `social.codestra.co`
- **Status:** Empty repository initialized with an architecture outline only; repository name requires review.

## Intended purpose

Provide a provider-neutral control plane for social campaigns, content calendars, approvals, publishing commands, engagement normalization, account health, analytics, audit, and operator workflows.

## Intended ownership

- Cross-provider social campaign and approval model
- Provider-neutral scheduling/publishing command contracts and normalized read models
- Operator views for accounts, content, approvals, engagement, failures, audit, and reconciliation

## Must not own

- A second Postiz/social runtime that competes with `social.codestra.co`
- Direct provider credentials or browser-to-provider calls
- Marketing, identity, gateway, Middleware, or SDK runtime source

## Planned integrations

- `social.codestra.co`
- `SDK-repository`
- Middleware
- `Codestra-Marketing-`
- Keycloak, Kong, Caddy, Superset, and Grafana

## Initial milestones

1. Correct or formally accept the repository name
2. Approve the boundary with `social.codestra.co` and `Codestra-Marketing-`
3. Define APIs/events, tenancy, RBAC, idempotency, audit, account health, and reconciliation
4. Add operator UI, generated SDK integration, CI, staging, rollback, and activation gates

## Governance and safety

- This repository has no provider runtime or production authority yet.
- Never commit social-provider tokens, account credentials, customer content, private keys, or secret-bearing evidence.
- Every provider effect must be routed through Middleware/runtime adapters and proven by read-back.
- This document does not connect accounts, publish posts, activate schedules, or deploy software.

## Account-wide catalog

See `appolon1908-hue/documentaions/REPOSITORY_CATALOG.md`.
