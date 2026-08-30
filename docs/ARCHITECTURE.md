# Codestra Social Architecture

## Role
Codestra Social is the Codestra-facing control plane for social account abstractions, content scheduling, approvals, engagement, social inbox normalization, analytics ingestion, and integration with the existing social publishing platform.

## Owns
- connected social account references
- content calendar
- posts and variants
- approval workflow
- publishing intent and publish state
- engagement normalization
- comments/inbox abstraction
- social analytics snapshots
- adapter contract to the existing social platform

## Does not own
- campaign spend or paid-media authority: Codestra Marketing
- CRM records: Odoo
- customer-channel delivery: Codestra Communication CC
- model routing: Codestra AI
- integration durability: Middleware
- workflow orchestration: n8n

## Initial APIs
- POST /v1/social/posts
- GET /v1/social/posts
- POST /v1/social/posts/{id}/submit-for-approval
- POST /v1/social/posts/{id}/approve
- POST /v1/social/posts/{id}/schedule
- POST /v1/social/posts/{id}/publish
- GET /v1/social/calendar
- GET /v1/social/accounts
- GET /v1/social/engagement
- GET /v1/social/inbox

## Safety
- live publishing disabled by default until adapter and approval policy are certified
- publishing is idempotent
- external account IDs are references, never secret credentials
- privileged account connection/disconnection is audited
- AI-generated social content remains draft until approved by policy
