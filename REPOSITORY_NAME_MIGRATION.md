# Repository-name migration record

```text
REPOSITORY_ID=1351353723
CURRENT_FULL_NAME=appolon1908-hue/Codesrea-Social-
TARGET_FULL_NAME=appolon1908-hue/Codestra-Social-Control-Plane
STATUS=PREPARED_NOT_RENAMED
RUNTIME_CRITICAL=NO
```

## Boundary preserved by the target name

This repository coordinates provider-neutral social concepts and control-plane contracts. It is not a replacement for `appolon1908-hue/social.codestra.co`, which remains the application/runtime authority.

Until GitHub proves repository ID `1351353723` at the approved target full name, active validators, source locks, workflow queries, and documentation continue to use the current repository name.

## Pre-cutover inventory

Capture default-branch SHA, rulesets, protection, open PR refs, Actions, required checks, Environments, deploy-key fingerprints, GitHub Apps, webhooks, packages, current authority matrices, infrastructure/source-lock references, and all links from Marketing, Communication, AI, Middleware, SDK, documentation, and production-evidence repositories. Do not capture secret values.

## Controlled cutover

1. Merge stable-ID alias mappings into every active consumer.
2. Preserve dated release/source-lock evidence unchanged.
3. Freeze merges and workflow dispatches for this repository.
4. Rename only this repository through an authorized owner/admin action.
5. Prove unchanged repository ID, visibility, default SHA, history, protection, issues, PRs, tags, releases, and Environments.
6. Update mutable current-state references to `Codestra-Social-Control-Plane`.
7. Verify the deployed `social.codestra.co` repository and runtime are untouched.
8. Verify no social provider credentials or publishing capability changed.
9. Rehearse rollback to the previous slug.

Required result:

```text
SOCIAL_RUNTIME_REPOSITORY_CHANGED=NO
SOCIAL_POSTS_PUBLISHED=0
PROVIDER_WRITES_ENABLED=NO_CHANGE
IMAGES_REBUILT=0
WORKLOADS_RESTARTED=0
PRODUCTION_TRAFFIC_CHANGED=NO
```

The account-wide mapping is governed by `appolon1908-hue/documentaions:repository-name-migration.v1.json` until that documentation repository completes its own controlled rename.