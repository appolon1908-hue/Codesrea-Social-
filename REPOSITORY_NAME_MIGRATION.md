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

Capture all of the following without secret values:

- default-branch SHA, visibility, history, tags, releases, issues, and open pull-request refs;
- rulesets, branch protection, required checks, CODEOWNERS, and GitHub Environments;
- Actions workflow definitions, reusable-workflow references, and active dispatch policy;
- deploy-key fingerprints and access level;
- GitHub App installations and webhook bindings;
- package and GHCR identities, provenance source URLs, and attestations;
- current authority matrices, infrastructure and source-lock references;
- every mutable consumer in Marketing, Communication, AI, Middleware, SDK, documentation, infrastructure, monitoring, and production-evidence repositories.

Record a checksum-bound pre-change packet so success and rollback can be compared against the same inventory.

## Controlled cutover

1. Merge stable-ID alias mappings into every active consumer.
2. Preserve dated release and source-lock evidence unchanged.
3. Freeze merges, release dispatches, and workflow dispatches for this repository; record exactly what was frozen.
4. Rename only this repository through an authorized owner or administrator action.
5. Before updating any consumer, prove unchanged repository ID, visibility, default branch and SHA, history, rulesets, branch protection, required checks, CODEOWNERS, issues, pull requests, tags, releases, Actions workflows, Environments, package and GHCR identities, deploy keys, GitHub Apps, webhooks, and reusable-workflow resolution.
6. Stop and execute rollback when any item from the pre-cutover inventory is missing, weakened, or unresolved.
7. Update mutable current-state references to `Codestra-Social-Control-Plane`, using repository ID `1351353723` to prove continuity.
8. Re-run every downstream authority, workflow-resolution, package, webhook, application-installation, source-lock, and release preflight that consumed the old slug.
9. Verify the deployed `social.codestra.co` repository and runtime are untouched.
10. Verify no social-provider credential, publishing capability, schedule, image, deployment, or traffic state changed.
11. After all success-path checks pass, restore the recorded merge, release-dispatch, and workflow-dispatch state. Do not leave the repository frozen.
12. Rehearse the documented rollback procedure and retain its evidence.

## Rollback and unfreeze

If a rename or downstream-reference update fails:

1. stop further mutable-reference changes;
2. rename the repository back to the previous slug when safe;
3. restore mutable references from the checksum-bound pre-change packet;
4. re-run the complete repository, Actions, checks, Environments, package, deploy-key, GitHub App, webhook, and downstream-consumer readback;
5. confirm `social.codestra.co` and every publishing capability remain unchanged;
6. restore the recorded merge, release-dispatch, and workflow-dispatch state only after rollback validation passes.

A successful rollback must not leave normal repository operations frozen.

Required result:

```text
POST_RENAME_INTEGRATION_READBACK=PASS
ACTIONS_AND_REQUIRED_CHECKS=PASS
PACKAGES_AND_GHCR=PASS|N/A
DEPLOY_KEYS_APPS_WEBHOOKS=PASS|N/A
DOWNSTREAM_CONSUMERS=PASS
MERGES_UNFROZEN=PASS
RELEASE_DISPATCH_UNFROZEN=PASS
WORKFLOW_DISPATCH_UNFROZEN=PASS
ROLLBACK_UNFREEZE=PASS|N/A
SOCIAL_RUNTIME_REPOSITORY_CHANGED=NO
SOCIAL_POSTS_PUBLISHED=0
PROVIDER_WRITES_ENABLED=NO_CHANGE
IMAGES_REBUILT=0
WORKLOADS_RESTARTED=0
PRODUCTION_TRAFFIC_CHANGED=NO
```

The account-wide mapping is governed by `appolon1908-hue/documentaions:repository-name-migration.v1.json` until that documentation repository completes its own controlled rename.
