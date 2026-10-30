"""Owner and assignee edges declared on the ingest sources (CONN-GITLAB-API-CONNECTOR-CONTENT-R005)."""

from __future__ import annotations

from pathlib import Path

import pytest
from scion_sdk.ingest.live_declaration import load_declaration
from scion_sdk.ingest.source_sync import _edges  # noqa: PLC2701

import gitlab_api

ONTOLOGY = Path(gitlab_api.__file__).parent / "ontology" / "gitlab.ttl"


def _declaration():
    return load_declaration("gitlab_api")


def _domain_and_range(name: str) -> tuple[str, str]:
    block = ONTOLOGY.read_text(encoding="utf-8").split(f"\n:{name} a owl:ObjectProperty")[1]
    block = block.split(" .\n")[0]
    return block.split("rdfs:domain :")[1].split()[0], block.split("rdfs:range :")[1].split()[0]


@pytest.mark.spec("CONN-GITLAB-API-CONNECTOR-CONTENT-R005")
def test_every_declared_edge_is_an_ontology_property_of_its_record_type() -> None:
    declaration = _declaration()
    seen = set()
    for source in declaration.sources:
        for edge in source.edges:
            assert _domain_and_range(edge.relationship) == (source.record_type, edge.target_type)
            assert edge.target_type in declaration.schema_mappings
            seen.add((source.source_id, edge.relationship))
    assert seen == {
        ("issues", "issueAuthoredBy"),
        ("issues", "issueAssignedTo"),
        ("projects", "projectOwnedBy"),
        ("projects", "partOfGroup"),
    }


@pytest.mark.spec("CONN-GITLAB-API-CONNECTOR-CONTENT-R005")
def test_project_and_issue_references_become_owner_and_assignee_edges() -> None:
    declaration = _declaration()
    project = {"id": 213, "owner": {"id": 5, "username": "ann", "name": "Ann"}, "namespace": {"id": 9, "full_path": "homelab"}}
    issue = {"id": 2, "author": {"id": 5, "username": "ann"}, "assignees": [{"id": 6, "username": "bob"}, {"id": 5}]}
    projects = {(r.relationship, r.target) for _, r in _edges("213", project, declaration.source("projects"))}
    issues = {(r.relationship, r.target) for _, r in _edges("2", issue, declaration.source("issues"))}
    assert projects == {("projectOwnedBy", "user:5"), ("partOfGroup", "group:9")}
    assert issues == {("issueAuthoredBy", "user:5"), ("issueAssignedTo", "user:6"), ("issueAssignedTo", "user:5")}
    owner = next(t for t, r in _edges("213", project, declaration.source("projects")) if r.relationship == "projectOwnedBy")
    assert owner.node_type == "Person" and owner.properties == {"name": "Ann", "username": "ann"}
