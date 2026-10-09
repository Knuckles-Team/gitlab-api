"""Epistemic-graph ingestion for GitLab records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the package pushes its data into the ONE
epistemic-graph knowledge graph as **typed OWL nodes** (`:Project`, `:GitLabGroup`,
`:MergeRequest`, `:Issue`, …) + links through ``agent_connector_sdk.ingest`` -- the
generated ``SourceIngest`` client, not a local ingestion helper. Nodes carry shared
provenance (via ``IngestBinding``) and match the classes federated by
``gitlab_api.ontology``.
"""

from __future__ import annotations

from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

_BINDING = IngestBinding(connector="gitlab-api", stream="gitlab")

_ENTITY_RESERVED_KEYS = frozenset({"id", "node_type"})
_RELATIONSHIP_RESERVED_KEYS = frozenset({"source", "target", "relationship"})


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={
            key: value
            for key, value in record.items()
            if key not in _ENTITY_RESERVED_KEYS
        },
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    properties = {
        key: value
        for key, value in record.items()
        if key not in _RELATIONSHIP_RESERVED_KEYS
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=properties or None,
    )


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships through the SDK ingest facade."""
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    change_set = ChangeSet(
        entities=tuple(_to_entity(entity) for entity in entities),
        relationships=tuple(
            _to_relationship(relationship) for relationship in relationships or ()
        ),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_projects(
    projects: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
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
    return await ingest_entities(entities, relationships, ingest=ingest)


def _map_pipeline_run(
    project_id: str | int, pipe: dict[str, Any]
) -> tuple[str | None, list[dict[str, Any]], list[dict[str, Any]]]:
    """Map one raw pipeline record to its ``:PipelineRun`` node + ``ranFor`` edges.

    Returns ``(pipe_node, entities, relationships)``; ``pipe_node`` is ``None``
    (with empty entities/relationships) when the record carries no ``id``.
    """
    pid = pipe.get("id")
    if pid is None:
        return None, [], []

    project_node = f"gitlab:project:{project_id}"
    pipe_node = f"gitlab:pipelinerun:{project_id}:{pid}"
    entities: list[dict[str, Any]] = [
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
    ]
    relationships: list[dict[str, Any]] = [
        {"source": pipe_node, "target": project_node, "relationship": "ranFor"}
    ]

    sha = pipe.get("sha")
    if sha:
        commit_node = f"gitlab:commit:{project_id}:{sha}"
        entities.append({"id": commit_node, "node_type": "Commit", "sha": sha})
        relationships.append(
            {"source": pipe_node, "target": commit_node, "relationship": "ranFor"}
        )

    mr_iid = pipe.get("merge_request_iid")
    if mr_iid is not None:
        mr_node = f"gitlab:mr:{project_id}:{mr_iid}"
        relationships.append(
            {"source": pipe_node, "target": mr_node, "relationship": "ranFor"}
        )

    return pipe_node, entities, relationships


def _map_pipeline_job(
    project_id: str | int, pid: Any, pipe_node: str, job: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Map one raw job record to its ``:CheckRun`` node + ``hasJob``/``ranOnRunner`` edges."""
    jid = job.get("id")
    if jid is None:
        return [], []

    job_node = f"gitlab:checkrun:{project_id}:{pid}:{jid}"
    web_url = job.get("web_url")
    entities: list[dict[str, Any]] = [
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
    ]
    relationships: list[dict[str, Any]] = [
        {"source": pipe_node, "target": job_node, "relationship": "hasJob"}
    ]

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

    return entities, relationships


def _map_pipeline_jobs(
    project_id: str | int,
    pid: Any,
    pipe_node: str,
    jobs_by_pipeline: dict[Any, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Map every job of one pipeline via `_map_pipeline_job`, flattening the results."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for job in jobs_by_pipeline.get(pid, []) or []:
        job_entities, job_relationships = _map_pipeline_job(
            project_id, pid, pipe_node, job
        )
        entities.extend(job_entities)
        relationships.extend(job_relationships)
    return entities, relationships


async def ingest_pipeline_runs(
    project_id: str | int,
    pipelines: list[dict[str, Any]],
    *,
    jobs_by_pipeline: dict[Any, list[dict[str, Any]]] | None = None,
    ingest: KnowledgeIngest | None = None,
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

    for pipe in pipelines:
        pipe_node, pipe_entities, pipe_relationships = _map_pipeline_run(
            project_id, pipe
        )
        if pipe_node is None:
            continue
        entities.extend(pipe_entities)
        relationships.extend(pipe_relationships)

        job_entities, job_relationships = _map_pipeline_jobs(
            project_id, pipe.get("id"), pipe_node, jobs_by_pipeline
        )
        entities.extend(job_entities)
        relationships.extend(job_relationships)

    return await ingest_entities(entities, relationships, ingest=ingest)
