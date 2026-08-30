# Codestra Social — Role and Integration Contract

## Mission
Codestra Social is the Codestra-facing social control plane. It exposes stable enterprise APIs for social accounts, publishing, approvals, engagement and analytics while insulating business systems from the implementation details of the social publishing runtime.

## Owns
- Social account/channel registry
- Post drafts, approvals and scheduling intent
- Social content calendar
- Publishing state abstraction
- Engagement normalization and social inbox abstraction
- Organic social analytics
- Adapter contract to social.codestra.co

## Does Not Own
- Paid advertising budgets/campaigns: Codestra Marketing
- AI provider credentials or model routing: Codestra AI
- CRM master: Odoo
- Cross-system durable integration: Middleware
- Identity: Keycloak

## Runtime Boundary
Codestra Social -> Middleware/integration adapter -> social.codestra.co -> social networks.
No Odoo, website, or business service should couple directly to social.codestra.co internals.

## Core Domains
SocialAccount, Channel, Post, MediaAssetReference, Schedule, Approval, Publication, Engagement, Comment, SocialConversation, PerformanceSnapshot.

## Required APIs
- /v1/social/accounts
- /v1/social/posts
- /v1/social/schedules
- /v1/social/approvals
- /v1/social/publications
- /v1/social/engagement
- /v1/social/analytics

## Required Events
social.post.created, social.post.approved, social.post.scheduled, social.post.published, social.post.failed, social.engagement.received, social.metrics.updated.

## Implementation Order
1. Provider-neutral social model
2. Account and authorization boundary
3. Draft/approval/schedule state machine
4. Adapter to social.codestra.co
5. Webhook/event normalization
6. Odoo and Marketing integrations
7. AI-assisted content via Codestra AI
8. Analytics and observability