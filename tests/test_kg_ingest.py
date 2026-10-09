"""Epistemic-graph typed-node ingestion -- Wire-First coverage for gitlab-api.

Exercises the real ``ingest_entities`` / ``ingest_projects`` / ``ingest_pipeline_runs``
seam against a fake ``agent_connector_sdk.ingest`` transport (no engine required). The
real SDK request builder (``agent_connector_sdk.ingest.request.build_request``) still
runs, so a malformed change set is still caught by the SDK's own contract, not
re-derived here; only the final network commit is faked.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest
from epistemic_graph.generated.source_ingestion import SourceIngestionRequest

from gitlab_api.kg_ingest import ingest_entities, ingest_pipeline_runs, ingest_projects


class _FakeTransport:
    """Records every submitted request; no epistemic-graph engine required."""

    def __init__(self) -> None:
        self.requests: list[SourceIngestionRequest] = []

    async def source_status(self, _connector: str, _stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: SourceIngestionRequest) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, _data: bytes) -> str:
        raise AssertionError("gitlab-api topology ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Project", "name": "p"},
            {"id": "b", "node_type": "GitLabGroup"},
        ],
        [{"source": "a", "target": "b", "relationship": "partOfGroup"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    request = transport.requests[0]
    record_ids = {record.record_id for record in request.records}
    assert record_ids == {"a", "b"}
    a_record = next(r for r in request.records if r.record_id == "a")
    assert a_record.payload["name"] == "p"
    assert a_record.mapping_reference.endswith("schema_mappings/Project")
    assert request.relationships[0].relation_reference.endswith(
        "resources/Project/relations/partOfGroup"
    )


@pytest.mark.asyncio
async def test_ingest_projects_maps_project_and_group(ingest):
    service, transport = ingest
    res = await ingest_projects(
        [
            {
                "id": 42,
                "name": "demo",
                "path_with_namespace": "grp/demo",
                "web_url": "https://gl/grp/demo",
                "namespace": {"id": 7, "name": "grp"},
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    request = transport.requests[0]
    project = next(r for r in request.records if r.record_id == "gitlab:project:42")
    assert project.mapping_reference.endswith("schema_mappings/Project")
    assert project.payload["path_with_namespace"] == "grp/demo"
    assert project.payload["externalToolId"] == "42"
    group = next(r for r in request.records if r.record_id == "gitlab:group:7")
    assert group.mapping_reference.endswith("schema_mappings/GitLabGroup")
    assert request.relationships[0].relation_reference.endswith(
        "resources/Project/relations/partOfGroup"
    )


@pytest.mark.asyncio
async def test_ingest_rejects_legacy_structural_fields(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="node_type"):
        await ingest_entities([{"id": "legacy", "type": "Legacy"}], ingest=service)


@pytest.mark.asyncio
async def test_ingest_empty_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)


@pytest.mark.asyncio
async def test_ingest_pipeline_runs_maps_pipeline_job_commit_and_runner(ingest):
    service, transport = ingest
    res = await ingest_pipeline_runs(
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
        ingest=service,
    )
    assert res == {"nodes": 4, "edges": 5}
    request = transport.requests[0]

    pipe_record = next(
        r for r in request.records if r.record_id == "gitlab:pipelinerun:42:101"
    )
    # Same class name github-agent uses, so both CI systems unify.
    assert pipe_record.mapping_reference.endswith("schema_mappings/PipelineRun")
    assert pipe_record.payload["status"] == "failed"
    assert pipe_record.payload["sha"] == "abc123"
    assert pipe_record.payload["triggerSource"] == "push"
    assert pipe_record.payload["externalToolId"] == "101"

    job_record = next(
        r for r in request.records if r.record_id == "gitlab:checkrun:42:101:501"
    )
    assert job_record.mapping_reference.endswith("schema_mappings/CheckRun")
    assert job_record.payload["failureReason"] == "script_failure"
    assert job_record.payload["logUrl"] == "https://gl/grp/demo/-/jobs/501/raw"
    assert job_record.payload["externalToolId"] == "501"

    commit_record = next(
        r for r in request.records if r.record_id == "gitlab:commit:42:abc123"
    )
    assert commit_record.mapping_reference.endswith("schema_mappings/Commit")

    runner_record = next(r for r in request.records if r.record_id == "gitlab:runner:9")
    assert runner_record.mapping_reference.endswith("schema_mappings/Runner")
    assert runner_record.payload["name"] == "shared-runner"

    # ranFor / hasJob edge names match github-agent's twin producer.
    edges = {
        (
            rel.source.record_id,
            rel.target.record_id,
            rel.relation_reference.rsplit("/", 1)[-1],
        )
        for rel in request.relationships
    }
    assert ("gitlab:pipelinerun:42:101", "gitlab:project:42", "ranFor") in edges
    assert ("gitlab:pipelinerun:42:101", "gitlab:commit:42:abc123", "ranFor") in edges
    assert ("gitlab:pipelinerun:42:101", "gitlab:mr:42:7", "ranFor") in edges
    assert (
        "gitlab:pipelinerun:42:101",
        "gitlab:checkrun:42:101:501",
        "hasJob",
    ) in edges
    assert ("gitlab:checkrun:42:101:501", "gitlab:runner:9", "ranOnRunner") in edges


@pytest.mark.asyncio
async def test_ingest_pipeline_runs_empty_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_pipeline_runs(42, [], ingest=service)
