"""Native epistemic-graph ingestion for GitLab records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the package natively pushes its data into the
epistemic-graph knowledge graph as **typed OWL nodes** (`:Project`, `:GitLabGroup`,
`:MergeRequest`, `:Issue`, …) + links through the required
``agent_utilities.knowledge_graph.memory.native_ingest`` authority. Nodes carry shared
provenance (``domain``/``source``) and match the classes federated by
``gitlab_api.ontology``.
"""

from __future__ import annotations

from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

_SOURCE = "gitlab-api"
_DOMAIN = "gitlab"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships through native ingestion."""
    return _native_ingest_entities(
        entities,
        relationships,
        source=_SOURCE,
        domain=_DOMAIN,
        client=client,
        graph=graph,
    )


def ingest_projects(
    projects: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
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
                "node_type": "Project",
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
                    "node_type": "GitLabGroup",
                    "name": namespace.get("name") or namespace.get("full_path"),
                }
            )
            relationships.append(
                {
                    "source": f"gitlab:project:{pid}",
                    "target": f"gitlab:group:{gid}",
                    "relationship": "partOfGroup",
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
) -> dict[str, int]:
    """Map GitLab pipeline runs (+ their jobs) → ``:PipelineRun``/``:CheckRun`` nodes.

    This is the substrate the autonomous-SDLC loop needs to observe CI (closes gap #2,
    "CI has no graph representation", of ``reports/autonomous-sdlc-loop-design.md``).

    Uses the SAME ``:PipelineRun``/``:CheckRun`` classes and ``ranFor``/``hasJob`` edge
    names as github-agent's ingestion so GitLab CI/CD and GitHub Actions unify under one
    CI node shape in the knowledge graph. ``ranFor`` is emitted once per known target —
    the ``:Project``, the head ``:Commit``, and (if resolved) the triggering
    ``:MergeRequest``. Stable ids: ``gitlab:pipelinerun:<project>:<id>`` /
    ``gitlab:checkrun:<project>:<pipeline>:<job>``.

    ``pipelines``: raw GitLab pipeline records (``id``, ``status``, ``ref``, ``sha``,
    ``source``, ``web_url``, ``name``, timestamps, ``duration``; optionally
    ``merge_request_iid`` if the caller has resolved the triggering merge request).
    ``jobs_by_pipeline``: maps a pipeline ``id`` to its list of raw GitLab job records
    (``id``, ``name``, ``stage``, ``status``, ``failure_reason``, ``web_url``,
    timestamps, ``duration``, optional ``runner``); each becomes a child ``:CheckRun``
    linked via ``hasJob`` (and, when known, its ``:Runner`` via the GitLab-specific
    ``ranOnRunner``).
    """
    pipelines = pipelines or []
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
                "node_type": "PipelineRun",
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
            {
                "source": pipe_node,
                "target": project_node,
                "relationship": "ranFor",
            }
        )

        sha = pipe.get("sha")
        if sha:
            commit_node = f"gitlab:commit:{project_id}:{sha}"
            entities.append({"id": commit_node, "node_type": "Commit", "sha": sha})
            relationships.append(
                {
                    "source": pipe_node,
                    "target": commit_node,
                    "relationship": "ranFor",
                }
            )

        mr_iid = pipe.get("merge_request_iid")
        if mr_iid is not None:
            mr_node = f"gitlab:mr:{project_id}:{mr_iid}"
            relationships.append(
                {
                    "source": pipe_node,
                    "target": mr_node,
                    "relationship": "ranFor",
                }
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
                    "node_type": "CheckRun",
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
                {
                    "source": pipe_node,
                    "target": job_node,
                    "relationship": "hasJob",
                }
            )
            runner = job.get("runner") or {}
            runner_id = runner.get("id")
            if runner_id is not None:
                runner_node = f"gitlab:runner:{runner_id}"
                entities.append(
                    {
                        "id": runner_node,
                        "node_type": "Runner",
                        "name": runner.get("description") or runner.get("name"),
                    }
                )
                relationships.append(
                    {
                        "source": job_node,
                        "target": runner_node,
                        "relationship": "ranOnRunner",
                    }
                )

    return ingest_entities(entities, relationships, client=client, graph=graph)
