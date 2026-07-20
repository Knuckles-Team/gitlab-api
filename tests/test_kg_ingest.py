"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_projects`` seam with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
GitLab project → :Project/:GitLabGroup mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

from gitlab_api.kg_ingest import ingest_entities, ingest_pipeline_runs, ingest_projects


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, src, dst, props):
        self.edges.append((src, dst, props))

    def commit(self, txn):
        self.committed = True
        return True


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Project", "name": "p"},
            {"id": "b", "node_type": "GitLabGroup"},
        ],
        [{"source": "a", "target": "b", "relationship": "partOfGroup"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "gitlab-api"
    assert c.txn.nodes["a"]["domain"] == "gitlab"
    assert c.txn.edges == [("a", "b", {"relationship": "partOfGroup"})]


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
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.nodes["gitlab:project:42"]["node_type"] == "Project"
    assert c.txn.nodes["gitlab:project:42"]["path_with_namespace"] == "grp/demo"
    assert c.txn.nodes["gitlab:project:42"]["externalToolId"] == "42"
    assert c.txn.nodes["gitlab:group:7"]["node_type"] == "GitLabGroup"
    assert c.txn.edges == [
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
        graph="__commons__",
    )
    assert res == {"nodes": 4, "edges": 5}

    pipe_node = c.txn.nodes["gitlab:pipelinerun:42:101"]
    # Same class name github-agent uses, so both CI systems unify.
    assert pipe_node["node_type"] == "PipelineRun"
    assert pipe_node["status"] == "failed"
    assert pipe_node["sha"] == "abc123"
    assert pipe_node["triggerSource"] == "push"
    assert pipe_node["externalToolId"] == "101"
    # GitLab's own "source" field is renamed so provenance stamping isn't clobbered.
    assert pipe_node["source"] == "gitlab-api"
    assert pipe_node["domain"] == "gitlab"

    job_node = c.txn.nodes["gitlab:checkrun:42:101:501"]
    assert job_node["node_type"] == "CheckRun"
    assert job_node["failureReason"] == "script_failure"
    assert job_node["logUrl"] == "https://gl/grp/demo/-/jobs/501/raw"
    assert job_node["externalToolId"] == "501"

    commit_node = c.txn.nodes["gitlab:commit:42:abc123"]
    assert commit_node["node_type"] == "Commit"

    runner_node = c.txn.nodes["gitlab:runner:9"]
    assert runner_node["node_type"] == "Runner"
    assert runner_node["name"] == "shared-runner"

    # ranFor / hasJob edge names match github-agent's twin producer.
    edges = {(s, t, p["relationship"]) for s, t, p in c.txn.edges}
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
