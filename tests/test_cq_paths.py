"""Competency-question paths of the GitLab pack (CONN-GITLAB-API-CONNECTOR-CONTENT-R004)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

import gitlab_api

pytestmark = pytest.mark.spec("CONN-GITLAB-API-CONNECTOR-CONTENT-R004")

PACKAGE = Path(gitlab_api.__file__).parent
TTL = (PACKAGE / "ontology" / "gitlab.ttl").read_text("utf-8")
# Concepts the epistemic-graph ontology owns: referenced, never declared here.
SHARED = ("Commit", "Branch", "Release", "Runner", "Milestone", "PipelineRun")


def _block(name: str) -> str:
    match = re.search(rf"^:{name} a [^\n]*\n(?:[^\n]+\n)*", TTL, flags=re.M)
    assert match, name
    return match.group(0)


@pytest.mark.parametrize("name", SHARED)
def test_shared_concepts_are_not_redeclared(name: str) -> None:
    assert not re.search(rf"^:{name} a owl:Class", TTL, flags=re.M), name


def test_state_is_declared_on_the_issue_type() -> None:
    block = _block("state")
    assert re.search(r"rdfs:domain \[ a owl:Class ; owl:unionOf \( :Issue ", block)


def test_merge_request_and_check_run_extend_shared_classes() -> None:
    assert "rdfs:subClassOf :PullRequest" in _block("MergeRequest")
    assert "rdfs:subClassOf :PipelineRun" in _block("CheckRun")


def test_no_mapping_has_a_null_ontology_class() -> None:
    manifest = yaml.safe_load(
        (PACKAGE.parent / "connector_manifest.yml").read_text("utf-8")
    )
    unmapped = [
        name
        for name, mapping in manifest["schema_mappings"].items()
        if not mapping["ontology_class"]
    ]
    assert unmapped == []
