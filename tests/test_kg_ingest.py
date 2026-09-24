"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises ``gitlab_api.kg_ingest``'s structural validation (still enforced locally) and
its no-op commit contract. CONCEPT:AU-KG.ingest.enterprise-source-extractor.

SDK GAP (EH-481/SDK-GAPS.md): ``_native_ingest_entities`` is a stub (no SDK equivalent
yet for the old dependency-injected ``agent_utilities.knowledge_graph.memory.
native_ingest`` ChangeEnvelope committer — see ``gitlab_api/kg_ingest.py``'s module
docstring). Every ``ingest_*`` call below is therefore exercised for its validation +
no-op-commit contract rather than real graph writes; the DI-based ``_FakeClient``
coverage of the retired real-commit path (node/edge shape assertions) is dropped with it.
"""

from __future__ import annotations

import pytest

from gitlab_api.kg_ingest import (
    NativeIngestError,
    ingest_entities,
    ingest_pipeline_runs,
    ingest_projects,
)


def test_ingest_entities_validates_then_noops():
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Project", "name": "p"},
            {"id": "b", "node_type": "GitLabGroup"},
        ],
        [{"source": "a", "target": "b", "relationship": "partOfGroup"}],
    )
    assert res == {"nodes": 0, "edges": 0}


def test_ingest_projects_maps_then_noops():
    res = ingest_projects(
        [
            {
                "id": 42,
                "name": "demo",
                "path_with_namespace": "grp/demo",
                "web_url": "https://gl/grp/demo",
                "namespace": {"id": 7, "name": "grp"},
            }
        ],
    )
    assert res == {"nodes": 0, "edges": 0}


def test_ingest_rejects_legacy_structural_fields():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "legacy", "type": "Legacy"}])


def test_ingest_empty_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([])


def test_ingest_pipeline_runs_maps_then_noops():
    res = ingest_pipeline_runs(
        42,
        [
            {
                "id": 101,
                "status": "failed",
                "ref": "main",
                "sha": "abc123",
                "source": "push",
                "web_url": "https://gl/grp/demo/-/pipelines/101",
                "created_at": "2026-07-10T00:00:00Z",
                "duration": 120.5,
                "merge_request_iid": 7,
            }
        ],
        jobs_by_pipeline={
            101: [
                {
                    "id": 501,
                    "name": "test",
                    "stage": "test",
                    "status": "failed",
                    "failure_reason": "script_failure",
                    "web_url": "https://gl/grp/demo/-/jobs/501",
                    "duration": 30.0,
                    "runner": {"id": 9, "description": "shared-runner"},
                }
            ]
        },
    )
    assert res == {"nodes": 0, "edges": 0}


def test_ingest_pipeline_runs_empty_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_pipeline_runs(42, [])
