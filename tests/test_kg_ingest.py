"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_projects`` seam with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
GitLab project → :Project/:GitLabGroup mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from gitlab_api.kg_ingest import ingest_entities, ingest_projects


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
