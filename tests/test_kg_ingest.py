"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_projects`` seam with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
GitLab project → :Project/:GitLabGroup mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from gitlab_api.kg_ingest import ingest_entities, ingest_pipeline_runs, ingest_projects


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [{"id": "a", "type": "Project", "name": "p"}, {"id": "b", "type": "GitLabGroup"}],
        [{"source": "a", "target": "b", "type": "partOfGroup"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "gitlab-api"
    assert c.txn.nodes["a"]["domain"] == "gitlab"
    assert c.edges.edges == [("a", "b", {"type": "partOfGroup"})]


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
    assert c.txn.nodes["gitlab:project:42"]["type"] == "Project"
    assert c.txn.nodes["gitlab:project:42"]["path_with_namespace"] == "grp/demo"
    assert c.txn.nodes["gitlab:project:42"]["externalToolId"] == "42"
    assert c.txn.nodes["gitlab:group:7"]["type"] == "GitLabGroup"
    assert c.edges.edges == [
        ("gitlab:project:42", "gitlab:group:7", {"type": "partOfGroup"})
    ]


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Project"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_projects([], client=_FakeClient()) is None


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
    assert pipe_node["type"] == "Pipeline"
    assert pipe_node["status"] == "failed"
    assert pipe_node["sha"] == "abc123"
    assert pipe_node["triggerSource"] == "push"
    assert pipe_node["externalToolId"] == "101"
    # GitLab's own "source" field is renamed so provenance stamping isn't clobbered.
    assert pipe_node["source"] == "gitlab-api"
    assert pipe_node["domain"] == "gitlab"

    job_node = c.txn.nodes["gitlab:checkrun:42:101:501"]
    assert job_node["type"] == "Job"
    assert job_node["failureReason"] == "script_failure"
    assert job_node["logUrl"] == "https://gl/grp/demo/-/jobs/501/raw"
    assert job_node["externalToolId"] == "501"

    commit_node = c.txn.nodes["gitlab:commit:42:abc123"]
    assert commit_node["type"] == "Commit"

    runner_node = c.txn.nodes["gitlab:runner:9"]
    assert runner_node["type"] == "Runner"
    assert runner_node["name"] == "shared-runner"

    edges = {(s, t, p["type"]) for s, t, p in c.edges.edges}
    assert ("gitlab:pipelinerun:42:101", "gitlab:project:42", "belongsToProject") in edges
    assert (
        "gitlab:commit:42:abc123",
        "gitlab:pipelinerun:42:101",
        "triggeredPipeline",
    ) in edges
    assert (
        "gitlab:mr:42:7",
        "gitlab:pipelinerun:42:101",
        "triggeredPipeline",
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


def test_ingest_pipeline_runs_empty_is_noop():
    assert ingest_pipeline_runs(42, [], client=_FakeClient()) is None
