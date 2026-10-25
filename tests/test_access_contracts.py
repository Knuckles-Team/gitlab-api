"""GitLab's read-only source access contracts stay source-local."""

from __future__ import annotations

from pathlib import Path

from agent_connector_sdk.access_contract import parse_access_contracts


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "gitlab_api" / "ontology" / "access_contracts.ttl"
KG = "http://knuckles.team/kg#"

EXPECTED = {
    "GitLabGroup": ("gitlab_groups", "group", "id"),
    "Project": ("gitlab_projects", "project", "id"),
    "MergeRequest": ("gitlab_merge_requests", "merge_request", "id"),
    "Pipeline": ("gitlab_pipelines", "pipeline", "id"),
    "PipelineRun": ("gitlab_pipelines", "pipeline", "id"),
    "Job": ("gitlab_jobs", "job", "id"),
    "CheckRun": ("gitlab_jobs", "job", "id"),
    "Issue": ("gitlab_issues", "issue", "id"),
    "Epic": ("gitlab_epics", "epic", "id"),
    "Milestone": ("gitlab_milestones", "milestone", "id"),
    "Commit": ("gitlab_commits", "commit", "id"),
    "Branch": ("gitlab_branches", "branch", "name"),
    "Release": ("gitlab_releases", "release", "tag_name"),
    "Runner": ("gitlab_runners", "runner", "id"),
}


def _contracts():
    return parse_access_contracts(CONTRACTS.read_text(encoding="utf-8"))


def test_every_declared_gitlab_class_has_a_typed_read_contract() -> None:
    contracts = _contracts()
    by_class = {contract.class_iri.rsplit("#", 1)[-1]: contract for contract in contracts}

    assert set(by_class) == set(EXPECTED)
    for class_name, (operation, entity, key_field) in EXPECTED.items():
        contract = by_class[class_name]
        assert contract.class_iri == KG + class_name
        assert contract.source_id == "gitlab-api"
        assert contract.access_kind == "mcp_tool"
        assert contract.operation == operation
        assert contract.entity == entity
        assert contract.key_field == key_field
        assert contract.parameters == ("action", "params_json")
        assert contract.auth_ref == "env://GITLAB_TOKEN"
        assert contract.pagination == "page"
        assert contract.pushdown == frozenset({"filter", "limit", "sort"})


def test_gitlab_contracts_do_not_promote_draft_crosswalks() -> None:
    contracts = _contracts()

    assert all(contract.class_iri.startswith(KG) for contract in contracts)
    assert all(
        contract.class_iri not in {KG + "Incident", KG + "SoftwareProject"}
        for contract in contracts
    )
    assert all(contract.source_id == "gitlab-api" for contract in contracts)


def test_gitlab_contract_artifact_is_packaged_under_ontology() -> None:
    assert CONTRACTS.is_file()


def test_gitlab_contract_bindings_use_declared_fields() -> None:
    contracts = {contract.class_iri.rsplit("#", 1)[-1]: contract for contract in _contracts()}

    assert (KG + "webUrl", "web_url") in contracts["Project"].predicates
    assert (KG + "pipelineStatus", "status") in contracts["Pipeline"].predicates
    assert (KG + "sha", "sha") in contracts["Commit"].predicates
