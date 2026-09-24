"""EH-410: GitLab pipeline EVENTS -- signed internal webhook + polling fallback.

A :PipelineRun node is a pipeline's latest state; a ``:PipelineRunEvent`` is
one status transition as GitLab reported it (coordinator ruling 2026-09-24):

* **Webhook** (primary): GitLab's pipeline hook POSTs to this server's internal
  route ``/webhooks/gitlab/pipeline``. Only a request SIGNED with the shared
  signing key (Standard Webhooks: ``webhook-id``/``webhook-timestamp``/
  ``webhook-signature`` = ``v1,<base64 HMAC-SHA256 of "id.timestamp.body">``,
  within :data:`TOLERANCE_S`) is accepted; the key comes from OpenBao
  (``GITLAB_WEBHOOK_SIGNING_KEY_REF``). Unsigned, stale or forged -> 401.
* **Polling** (fallback): ``gitlab_ingest_pipeline_events`` lists pipelines
  updated after the caller's cursor and maps each to the same event.

Both paths key an event by (project, pipeline, status, updated_at), so a
webhook delivery and a later poll of the same transition write one node.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from collections.abc import Mapping
from typing import Any

#: The internal route GitLab's pipeline hook is pointed at.
WEBHOOK_PATH = "/webhooks/gitlab/pipeline"
#: How far a signed timestamp may be from now (replay window), seconds.
TOLERANCE_S = 300


class WebhookSignatureError(ValueError):
    """The delivery is unsigned, stale, or signed with another key."""


def _signing_key(secret: str) -> bytes:
    """A Standard Webhooks secret (``whsec_<base64>``) or a raw shared key."""
    if secret.startswith("whsec_"):
        return base64.b64decode(secret.removeprefix("whsec_"))
    return secret.encode("utf-8")


def verify_signature(
    headers: Mapping[str, str], body: bytes, secret: str, *, now: float | None = None
) -> None:
    """Raise :class:`WebhookSignatureError` unless ``body`` is signed with ``secret``."""
    if not secret:
        raise WebhookSignatureError("no webhook signing key is configured")
    delivery = headers.get("webhook-id", "")
    stamp = headers.get("webhook-timestamp", "")
    offered = headers.get("webhook-signature", "").split()
    if not delivery or not stamp.isdigit() or not offered:
        raise WebhookSignatureError("the delivery is unsigned")
    if abs((now if now is not None else time.time()) - int(stamp)) > TOLERANCE_S:
        raise WebhookSignatureError("the signed timestamp is outside the window")
    signed = f"{delivery}.{stamp}.".encode() + body
    digest = hmac.new(_signing_key(secret), signed, hashlib.sha256).digest()
    expected = "v1," + base64.b64encode(digest).decode()
    if not any(hmac.compare_digest(expected, sig) for sig in offered):
        raise WebhookSignatureError("no signature matches the signing key")


def normalized_time(value: Any) -> str:
    """GitLab reports ``2026-09-24 10:00:00 UTC`` in hooks and ISO-8601 in the
    API; both become ``2026-09-24T10:00:00Z`` so a hook and a poll of the same
    transition key the same event. Unparseable text is kept as given."""
    import datetime as dt

    text = str(value or "").strip()
    if not text:
        return ""
    try:
        if text.endswith(" UTC"):
            moment = dt.datetime.strptime(text, "%Y-%m-%d %H:%M:%S UTC")
            moment = moment.replace(tzinfo=dt.UTC)
        else:
            moment = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return text
    return moment.astimezone(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _event(project_id: Any, pipe: Mapping[str, Any]) -> list[dict[str, Any]] | None:
    """The event node + its run node for one pipeline record, or ``None``."""
    pid, updated = pipe.get("id"), normalized_time(pipe.get("updated_at"))
    if pid is None or not updated:
        return None
    status = str(pipe.get("status") or "")
    run_node = f"gitlab:pipelinerun:{project_id}:{pid}"
    event = {
        "id": f"gitlab:pipelineevent:{project_id}:{pid}:{status}:{updated}",
        "node_type": "PipelineRunEvent",
        "status": status,
        "reportedAt": updated,
        "runId": str(pid),
        "sha": pipe.get("sha"),
        "ref": pipe.get("ref"),
        "epistemic_class": "observation",
    }
    run = {
        "id": run_node,
        "node_type": "PipelineRun",
        "status": status,
        "externalToolId": str(pid),
    }
    return [event, run]


def events_from_hook(payload: Mapping[str, Any]) -> tuple[Any, list[Mapping[str, Any]]]:
    """``(project_id, [pipeline record])`` from a pipeline hook body."""
    if payload.get("object_kind") != "pipeline":
        return None, []
    project = payload.get("project") or {}
    attributes = dict(payload.get("object_attributes") or {})
    attributes.setdefault(
        "updated_at", attributes.get("finished_at") or attributes.get("created_at")
    )
    return project.get("id"), [attributes]


def ingest_pipeline_events(
    project_id: Any,
    pipelines: list[Mapping[str, Any]],
    *,
    since: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, Any]:
    """One ``:PipelineRunEvent`` per pipeline updated after ``since``; returns
    the write counts and the next ``cursor``."""
    from gitlab_api.kg_ingest import ingest_entities

    floor = normalized_time(since)
    fresh = [p for p in pipelines if normalized_time(p.get("updated_at")) > floor]
    mapped = [m for m in (_event(project_id, p) for p in fresh) if m]
    cursor = max((event["reportedAt"] for event, _ in mapped), default=since)
    if project_id is None or not mapped:
        return {"nodes": 0, "edges": 0, "cursor": cursor}
    entities = [node for pair in mapped for node in pair]
    relationships = [
        {"source": event["id"], "target": run["id"], "relationship": "pipelineEventOf"}
        for event, run in mapped
    ]
    written = ingest_entities(entities, relationships, client=client, graph=graph)
    return {**written, "cursor": cursor}


def _configured_secret() -> str:
    from agent_utilities.core.config import setting
    from agent_utilities.security.secrets_client import create_secrets_client

    reference = str(setting("GITLAB_WEBHOOK_SIGNING_KEY_REF", "") or "")
    return (
        str(create_secrets_client().resolve_ref(reference) or "") if reference else ""
    )


async def handle_webhook(headers: Mapping[str, str], body: bytes) -> tuple[int, dict]:
    """Verify, parse and ingest one pipeline-hook delivery -> (status, body)."""
    import json

    try:
        verify_signature(headers, body, _configured_secret())
    except WebhookSignatureError as exc:
        return 401, {"error": str(exc)}
    try:
        payload = json.loads(body)
    except ValueError:
        return 400, {"error": "the delivery is not JSON"}
    import asyncio

    project_id, pipelines = events_from_hook(payload)
    written = await asyncio.to_thread(ingest_pipeline_events, project_id, pipelines)
    return 200, {"ingested": written}


def register_webhook_route(mcp: Any) -> None:
    """Mount :data:`WEBHOOK_PATH` on the server's HTTP app (internal ingress)."""
    from starlette.requests import Request
    from starlette.responses import JSONResponse

    @mcp.custom_route(WEBHOOK_PATH, methods=["POST"])
    async def gitlab_pipeline_webhook(request: Request) -> JSONResponse:
        headers = {k.lower(): v for k, v in request.headers.items()}
        status, answer = await handle_webhook(headers, await request.body())
        return JSONResponse(answer, status_code=status)


__all__ = [
    "TOLERANCE_S",
    "WEBHOOK_PATH",
    "WebhookSignatureError",
    "events_from_hook",
    "handle_webhook",
    "ingest_pipeline_events",
    "register_webhook_route",
    "verify_signature",
]
