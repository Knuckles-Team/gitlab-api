"""Native epistemic-graph ingestion for GitLab records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the package natively pushes its data into the
epistemic-graph knowledge graph as **typed OWL nodes** (`:Project`, `:GitLabGroup`,
`:MergeRequest`, `:Issue`, …) + links, using the lightweight engine client
(``GraphComputeEngine()._client`` + ``txn``) — the same fast client the blob
``MediaStore`` uses, NOT the heavy in-process ingestion engine.

Entirely best-effort and dependency-/engine-guarded: with no agent-utilities KG stack
or no reachable engine, every entry point **no-ops** (returns ``None``), so the
connector keeps working with zero KG infrastructure. Nodes carry the shared provenance
(``domain``/``source``) and match the classes federated by ``gitlab_api.ontology``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("gitlab_api.kg")

_SOURCE = "gitlab-api"
_DOMAIN = "gitlab"


def _client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        graph = getattr(engine, "graph_name", None) or "__commons__"
        return client, graph
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed nodes (+ edges) into epistemic-graph via the fast engine client.

    ``entities``: ``[{"id":..., "type":..., ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":rel}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    ``client``/``graph`` may be injected (tests); otherwise resolved on demand.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    if client is None:
        client, graph = _client()
    if client is None:
        return None
    graph = graph or "__commons__"

    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {
                k: v for k, v in ent.items() if k != "id" and v is not None
            }
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


def ingest_projects(
    projects: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map GitLab project records → ``:Project`` (+ ``:GitLabGroup``) nodes and ingest."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for proj in projects or []:
        pid = proj.get("id")
        if pid is None:
            continue
        entities.append(
            {
                "id": f"gitlab:project:{pid}",
                "type": "Project",
                "name": proj.get("name"),
                "path_with_namespace": proj.get("path_with_namespace"),
                "web_url": proj.get("web_url"),
                "state": proj.get("state"),
                "last_activity_at": proj.get("last_activity_at"),
                "externalToolId": str(pid),
            }
        )
        namespace = proj.get("namespace") or {}
        gid = namespace.get("id") or namespace.get("full_path")
        if gid is not None:
            entities.append(
                {
                    "id": f"gitlab:group:{gid}",
                    "type": "GitLabGroup",
                    "name": namespace.get("name") or namespace.get("full_path"),
                }
            )
            relationships.append(
                {
                    "source": f"gitlab:project:{pid}",
                    "target": f"gitlab:group:{gid}",
                    "type": "partOfGroup",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)
