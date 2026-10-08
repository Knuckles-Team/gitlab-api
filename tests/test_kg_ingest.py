"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_projects`` seam with a fake
ChangeEnvelope-capable engine client (no engine required), asserting the
committed nodes/edges and the GitLab project → :Project/:GitLabGroup mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.

The fake client mirrors agent-utilities' own sanctioned test double
(``agent-utilities/tests/knowledge_graph/test_native_ingest.py``) — the
``txn``-only fake is retired; ``native_ingest`` now hard-requires an injected
client exposing ``.changes``/``.nodes``/``.rdf``/``.supports()``.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.actor_identity import ActorType
from agent_utilities.security.brain_context import ActorContext, use_actor

from gitlab_api.kg_ingest import ingest_entities, ingest_pipeline_runs, ingest_projects


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Project", "name": "p"},
            {"id": "b", "node_type": "GitLabGroup"},
        ],
        [{"source": "a", "target": "b", "relationship": "partOfGroup"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "gitlab-api"
    assert c.nodes.values["a"]["domain"] == "gitlab"
    assert c.changes.edges == [("a", "b", {"relationship": "partOfGroup"})]


def test_ingest_projects_maps_project_and_group():
    c = _FakeClient()
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
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.nodes.values["gitlab:project:42"]["node_type"] == "Project"
    assert c.nodes.values["gitlab:project:42"]["path_with_namespace"] == "grp/demo"
    assert c.nodes.values["gitlab:project:42"]["externalToolId"] == "42"
    assert c.nodes.values["gitlab:group:7"]["node_type"] == "GitLabGroup"
    assert c.changes.edges == [
        ("gitlab:project:42", "gitlab:group:7", {"relationship": "partOfGroup"})
    ]


def test_ingest_rejects_legacy_structural_fields():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "legacy", "type": "Legacy"}], client=_FakeClient())


def test_ingest_empty_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())


def test_ingest_pipeline_runs_maps_pipeline_job_commit_and_runner():
    c = _FakeClient()
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
        client=c,
    )
    assert res == {"nodes": 4, "edges": 5}

    pipe_node = c.nodes.values["gitlab:pipelinerun:42:101"]
    # Same class name github-agent uses, so both CI systems unify.
    assert pipe_node["node_type"] == "PipelineRun"
    assert pipe_node["status"] == "failed"
    assert pipe_node["sha"] == "abc123"
    assert pipe_node["triggerSource"] == "push"
    assert pipe_node["externalToolId"] == "101"
    # GitLab's own "source" field is renamed so provenance stamping isn't clobbered.
    assert pipe_node["source"] == "gitlab-api"
    assert pipe_node["domain"] == "gitlab"

    job_node = c.nodes.values["gitlab:checkrun:42:101:501"]
    assert job_node["node_type"] == "CheckRun"
    assert job_node["failureReason"] == "script_failure"
    assert job_node["logUrl"] == "https://gl/grp/demo/-/jobs/501/raw"
    assert job_node["externalToolId"] == "501"

    commit_node = c.nodes.values["gitlab:commit:42:abc123"]
    assert commit_node["node_type"] == "Commit"

    runner_node = c.nodes.values["gitlab:runner:9"]
    assert runner_node["node_type"] == "Runner"
    assert runner_node["name"] == "shared-runner"

    # ranFor / hasJob edge names match github-agent's twin producer.
    edges = {(s, t, p["relationship"]) for s, t, p in c.changes.edges}
    assert ("gitlab:pipelinerun:42:101", "gitlab:project:42", "ranFor") in edges
    assert (
        "gitlab:pipelinerun:42:101",
        "gitlab:commit:42:abc123",
        "ranFor",
    ) in edges
    assert (
        "gitlab:pipelinerun:42:101",
        "gitlab:mr:42:7",
        "ranFor",
    ) in edges
    assert (
        "gitlab:pipelinerun:42:101",
        "gitlab:checkrun:42:101:501",
        "hasJob",
    ) in edges
    assert (
        "gitlab:checkrun:42:101:501",
        "gitlab:runner:9",
        "ranOnRunner",
    ) in edges


def test_ingest_pipeline_runs_empty_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_pipeline_runs(42, [], client=_FakeClient())
