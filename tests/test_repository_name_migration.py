from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "repository-name-migration.v1.json"
README = ROOT / "README.md"
PROFILE = ROOT / "REPOSITORY_PROFILE.md"
RUNBOOK = ROOT / "REPOSITORY_NAME_MIGRATION.md"


def test_repository_name_migration_is_stable_and_pre_cutover() -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert document["schema_version"] == "1.0"
    assert document["repository_id"] == 1351353723
    assert document["current_repository"] == "appolon1908-hue/Codesrea-Social-"
    assert document["target_repository_after_cutover"] == (
        "appolon1908-hue/Codestra-Social-Control-Plane"
    )
    assert document["status"] == "PREPARED_NOT_RENAMED"
    assert document["runtime_critical"] is False
    assert document["runtime_repository"] == "appolon1908-hue/social.codestra.co"

    policy = document["policy"]
    assert policy["current_repository_remains_operational"] is True
    assert policy["target_repository_forbidden_in_automation_before_cutover"] is True
    assert policy["same_repository_id_required_after_cutover"] is True
    assert policy["historical_evidence_immutable"] is True
    assert policy["all_inventoried_integrations_require_post_rename_readback"] is True
    assert policy["runtime_repository_must_remain_separate"] is True
    assert policy["runtime_repository_must_remain_unchanged"] is True
    assert policy["success_path_must_restore_freeze_state"] is True
    assert policy["rollback_path_must_restore_freeze_state"] is True
    assert policy["rename_authorizes_deployment"] is False
    assert policy["rename_authorizes_publishing"] is False


def test_human_authority_documents_preserve_runtime_boundary() -> None:
    readme = README.read_text(encoding="utf-8")
    profile = PROFILE.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")

    for text in (readme, profile):
        assert "1351353723" in text
        assert "appolon1908-hue/Codesrea-Social-" in text
        assert "appolon1908-hue/Codestra-Social-Control-Plane" in text
        assert "PREPARED_NOT_RENAMED" in text
        assert "appolon1908-hue/social.codestra.co" in text

    for required in (
        "POST_RENAME_INTEGRATION_READBACK=PASS",
        "ACTIONS_AND_REQUIRED_CHECKS=PASS",
        "PACKAGES_AND_GHCR=PASS|N/A",
        "DEPLOY_KEYS_APPS_WEBHOOKS=PASS|N/A",
        "DOWNSTREAM_CONSUMERS=PASS",
        "MERGES_UNFROZEN=PASS",
        "RELEASE_DISPATCH_UNFROZEN=PASS",
        "WORKFLOW_DISPATCH_UNFROZEN=PASS",
        "ROLLBACK_UNFREEZE=PASS|N/A",
        "SOCIAL_RUNTIME_REPOSITORY_CHANGED=NO",
        "SOCIAL_POSTS_PUBLISHED=0",
        "PROVIDER_WRITES_ENABLED=NO_CHANGE",
        "PRODUCTION_TRAFFIC_CHANGED=NO",
    ):
        assert required in runbook

    assert "Do not leave the repository frozen." in runbook
    assert "A successful rollback must not leave normal repository operations frozen." in runbook
