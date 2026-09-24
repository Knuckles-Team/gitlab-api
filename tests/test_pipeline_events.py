"""EH-410: GitLab pipeline events -- signed webhook and polling fallback."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
from typing import Any

import pytest

from gitlab_api import kg_ingest, pipeline_events

SECRET = "whsec_" + base64.b64encode(b"test-only-signing-key").decode()
HOOK = {
    "object_kind": "pipeline",
    "project": {"id": 42, "path_with_namespace": "grp/app"},
    "object_attributes": {
        "id": 7,
        "status": "failed",
        "ref": "main",
        "sha": "abc",
        "finished_at": "2026-09-24 10:00:00 UTC",
    },
}


def _signed(
    body: bytes, *, stamp: int = 1_700_000_000, key: bytes = b"test-only-signing-key"
):
    signed = f"msg-1.{stamp}.".encode() + body
    digest = base64.b64encode(hmac.new(key, signed, hashlib.sha256).digest()).decode()
    return {
        "webhook-id": "msg-1",
        "webhook-timestamp": str(stamp),
        "webhook-signature": f"v1,{digest}",
    }


@pytest.fixture
def written(monkeypatch) -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {}

    def capture(entities, relationships=None, **_kwargs):
        nodes.update({e["id"]: e for e in entities})
        return {"nodes": len(entities), "edges": len(relationships or [])}

    monkeypatch.setattr(kg_ingest, "ingest_entities", capture)
    return nodes


def test_a_signed_delivery_verifies_and_forgeries_do_not() -> None:
    body = json.dumps(HOOK).encode()
    now = 1_700_000_010
    pipeline_events.verify_signature(_signed(body), body, SECRET, now=now)
    bad = [
        ({}, "unsigned"),
        (_signed(body, key=b"other-key"), "no signature"),
        (_signed(body, stamp=now - 3600), "outside"),
        (_signed(body + b" "), "no signature"),
    ]
    for headers, reason in bad:
        with pytest.raises(pipeline_events.WebhookSignatureError, match=reason):
            pipeline_events.verify_signature(headers or {}, body, SECRET, now=now)
    with pytest.raises(pipeline_events.WebhookSignatureError, match="no webhook"):
        pipeline_events.verify_signature(_signed(body), body, "", now=now)


def test_the_webhook_ingests_one_event_and_refuses_unsigned(monkeypatch, written):
    body = json.dumps(HOOK).encode()
    monkeypatch.setattr(pipeline_events, "_configured_secret", lambda: SECRET)
    monkeypatch.setattr(pipeline_events.time, "time", lambda: 1_700_000_000)
    status, answer = asyncio.run(pipeline_events.handle_webhook(_signed(body), body))
    assert status == 200 and answer["ingested"]["nodes"] == 2
    event = written["gitlab:pipelineevent:42:7:failed:2026-09-24T10:00:00Z"]
    assert event["node_type"] == "PipelineRunEvent" and event["status"] == "failed"
    status, _ = asyncio.run(pipeline_events.handle_webhook({}, body))
    assert status == 401


def test_polling_writes_the_same_event_ids_and_advances_the_cursor(written):
    pipes = [
        {"id": 7, "status": "failed", "updated_at": "2026-09-24T10:00:00.000Z"},
        {"id": 6, "status": "success", "updated_at": "2026-09-23 10:00:00 UTC"},
    ]
    res = pipeline_events.ingest_pipeline_events(
        42, pipes, since="2026-09-24T00:00:00Z"
    )
    assert res["cursor"] == "2026-09-24T10:00:00Z", "the hook and the poll agree"
    assert set(written) == {
        "gitlab:pipelineevent:42:7:failed:2026-09-24T10:00:00Z",
        "gitlab:pipelinerun:42:7",
    }
