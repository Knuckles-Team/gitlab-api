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
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
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


def ingest_pipeline_runs(
    project_id: str | int,
    pipelines: list[dict[str, Any]],
    *,
    jobs_by_pipeline: dict[Any, list[dict[str, Any]]] | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map GitLab pipeline runs (+ their jobs) → ``:Pipeline``/``:Job`` nodes and ingest.

    This is the substrate the autonomous-SDLC loop needs to observe CI (closes gap #2,
    "CI has no graph representation", of ``reports/autonomous-sdlc-loop-design.md``).

    ``pipelines``: raw GitLab pipeline records (``id``, ``status``, ``ref``, ``sha``,
    ``source``, ``web_url``, ``name``, timestamps, ``duration``; optionally
    ``merge_request_iid`` if the caller has resolved the triggering merge request).
    ``jobs_by_pipeline``: maps a pipeline ``id`` to its list of raw GitLab job records
    (``id``, ``name``, ``stage``, ``status``, ``failure_reason``, ``web_url``,
    timestamps, ``duration``, optional ``runner``).

    Builds one ``:Pipeline`` node per pipeline (id
    ``gitlab:pipelinerun:<project>:<id>``, aliased ``:PipelineRun`` in the ontology),
    linked to the owning ``:Project`` (``belongsToProject``) and, when known, the
    triggering ``:Commit``/``:MergeRequest`` (``triggeredPipeline``); one child
    ``:Job`` node per job (id ``gitlab:checkrun:<project>:<pipeline>:<job>``, aliased
    ``:CheckRun``), linked to its ``:Pipeline`` (``hasJob``) and, when known, its
    ``:Runner`` (``ranOnRunner``).
    """
    pipelines = pipelines or []
    if not pipelines:
        return None
    jobs_by_pipeline = jobs_by_pipeline or {}
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    project_node = f"gitlab:project:{project_id}"

    for pipe in pipelines:
        pid = pipe.get("id")
        if pid is None:
            continue
        pipe_node = f"gitlab:pipelinerun:{project_id}:{pid}"
        entities.append(
            {
                "id": pipe_node,
                "type": "Pipeline",
                "status": pipe.get("status"),
                "ref": pipe.get("ref"),
                "sha": pipe.get("sha"),
                "triggerSource": pipe.get("source"),
                "webUrl": pipe.get("web_url"),
                "name": pipe.get("name"),
                "createdAt": pipe.get("created_at"),
                "startedAt": pipe.get("started_at"),
                "finishedAt": pipe.get("finished_at"),
                "duration": pipe.get("duration"),
                "externalToolId": str(pid),
            }
        )
        relationships.append(
            {"source": pipe_node, "target": project_node, "type": "belongsToProject"}
        )

        sha = pipe.get("sha")
        if sha:
            commit_node = f"gitlab:commit:{project_id}:{sha}"
            entities.append({"id": commit_node, "type": "Commit", "sha": sha})
            relationships.append(
                {
                    "source": commit_node,
                    "target": pipe_node,
                    "type": "triggeredPipeline",
                }
            )

        mr_iid = pipe.get("merge_request_iid")
        if mr_iid is not None:
            mr_node = f"gitlab:mr:{project_id}:{mr_iid}"
            relationships.append(
                {"source": mr_node, "target": pipe_node, "type": "triggeredPipeline"}
            )

        for job in jobs_by_pipeline.get(pid, []) or []:
            jid = job.get("id")
            if jid is None:
                continue
            job_node = f"gitlab:checkrun:{project_id}:{pid}:{jid}"
            web_url = job.get("web_url")
            entities.append(
                {
                    "id": job_node,
                    "type": "Job",
                    "name": job.get("name"),
                    "stage": job.get("stage"),
                    "status": job.get("status"),
                    "failureReason": job.get("failure_reason"),
                    "webUrl": web_url,
                    "logUrl": f"{web_url}/raw" if web_url else None,
                    "triggerSource": job.get("source"),
                    "createdAt": job.get("created_at"),
                    "startedAt": job.get("started_at"),
                    "finishedAt": job.get("finished_at"),
                    "duration": job.get("duration"),
                    "externalToolId": str(jid),
                }
            )
            relationships.append(
                {"source": pipe_node, "target": job_node, "type": "hasJob"}
            )
            runner = job.get("runner") or {}
            runner_id = runner.get("id")
            if runner_id is not None:
                runner_node = f"gitlab:runner:{runner_id}"
                entities.append(
                    {
                        "id": runner_node,
                        "type": "Runner",
                        "name": runner.get("description") or runner.get("name"),
                    }
                )
                relationships.append(
                    {
                        "source": job_node,
                        "target": runner_node,
                        "type": "ranOnRunner",
                    }
                )

    return ingest_entities(entities, relationships, client=client, graph=graph)
