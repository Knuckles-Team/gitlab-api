"""Focused NE-111 connector boundary fixtures.

These tests use a recording committer only.  They never construct an engine:
the production adapter remains ``ExistingNativeCommitter`` → ``kg_ingest`` →
the native ``ApplyChangeEnvelope`` path.
"""

from __future__ import annotations

from typing import Any

import pytest

from gitlab_api.connector_prep import (
    CheckpointConflict,
    ConnectorCommitError,
    ConnectorPrep,
    GitLabProjectPayload,
    MemoryCheckpointStore,
    NativeCommitResult,
    PrepContext,
    PrepDisposition,
    PrepErrorCode,
    arrow_prep_plan,
)


@pytest.fixture
def context() -> PrepContext:
    return PrepContext(
        tenant_reference="tenant:opaque:gitlab",
        access_policy_reference="acl:opaque:gitlab-read",
        retention_reference="retention:gitlab-default",
        provenance_reference="provenance:gitlab-api",
        source_instance_reference="gitlab:instance:synthetic",
    )


class RecordingCommitter:
    def __init__(self, *, fail: bool = False) -> None:
        self.calls: list[tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]] = []
        self.fail = fail

    def commit(
        self,
        entities: Any,
        relationships: Any,
        *,
        client: Any = None,
        graph: str | None = None,
        idempotency_key: str | None = None,
    ) -> NativeCommitResult:
        del client, graph
        if self.fail:
            raise RuntimeError("synthetic engine failure")
        self.calls.append((list(entities), list(relationships), idempotency_key))
        return NativeCommitResult(nodes=len(entities), edges=len(relationships))


def _project(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": 42,
        "name": " Demo ",
        "path_with_namespace": "group/demo",
        "web_url": "https://gitlab.example/group/demo",
        "state": "active",
        "visibility": "private",
        "last_activity_at": "2026-08-19T12:00:00Z",
        "namespace": {"id": 7, "name": "group", "full_path": "group"},
    }
    payload.update(overrides)
    return payload


def _issue(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": 1001,
        "iid": 11,
        "project_id": 42,
        "title": " Fix the governed ingest path ",
        "state": "opened",
        "web_url": "https://gitlab.example/group/demo/-/issues/11",
        "created_at": "2026-08-19T12:00:00Z",
        "labels": ["backend"],
    }
    payload.update(overrides)
    return payload


def _merge_request(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": 2001,
        "iid": 21,
        "project_id": 42,
        "title": " Add bounded source preparation ",
        "state": "opened",
        "source_branch": "feature/prep",
        "target_branch": "main",
        "web_url": "https://gitlab.example/group/demo/-/merge_requests/21",
        "created_at": "2026-08-19T12:00:00Z",
    }
    payload.update(overrides)
    return payload


def _prep(committer: RecordingCommitter | None = None) -> tuple[ConnectorPrep, RecordingCommitter]:
    recorder = committer or RecordingCommitter()
    return ConnectorPrep(committer=recorder, checkpoints=MemoryCheckpointStore()), recorder


def test_versioned_models_are_strict_and_plan_is_arrow_first() -> None:
    model = GitLabProjectPayload.model_validate(_project())
    assert model.schema_version == "1"
    with pytest.raises(ValueError):
        GitLabProjectPayload.model_validate({**_project(), "unexpected": True})
    with pytest.raises(ValueError):
        GitLabProjectPayload.model_validate({**_project(), "schema_version": "2"})

    plan = arrow_prep_plan("project")
    assert plan.handoff_format == "arrow_ipc"
    assert "commit_change_envelope" in plan.operations
    assert all(field.data_type != "pandas" for field in plan.arrow_schema)


def test_project_mapping_carries_governance_lineage_and_one_commit(context: PrepContext) -> None:
    prep, recorder = _prep()
    result = prep.process_page(
        "project",
        [_project()],
        stream="gitlab:projects",
        page=1,
        cursor="cursor-1",
        context=context,
    )

    assert result.checkpoint_advanced is True
    assert result.outcomes[0].disposition is PrepDisposition.COMMITTED
    assert result.outcomes[0].evidence.input_digest is not None
    assert len(recorder.calls) == 1
    entities, relationships, idempotency_key = recorder.calls[0]
    assert idempotency_key == result.page_digest
    project = next(item for item in entities if item["id"] == "gitlab:project:42")
    assert project["tenantReference"] == context.tenant_reference
    assert project["sourceRecordRef"] == "gitlab:project:42"
    assert relationships[0]["relationship"] == "partOfGroup"


@pytest.mark.parametrize(
    ("kind", "payload", "record_ref"),
    [
        ("issue", _issue(), "gitlab:issue:42:11"),
        ("merge_request", _merge_request(), "gitlab:mr:42:21"),
    ],
)
def test_issue_and_merge_request_mapping_is_project_scoped(
    context: PrepContext,
    kind: str,
    payload: dict[str, object],
    record_ref: str,
) -> None:
    prep, recorder = _prep()
    result = prep.process_page(
        kind,  # type: ignore[arg-type]
        [payload],
        stream=f"gitlab:{kind}",
        page=1,
        cursor=None,
        context=context,
    )
    assert result.outcomes[0].record_ref == record_ref
    assert len(recorder.calls) == 1
    entities, relationships, _ = recorder.calls[0]
    assert {item["id"] for item in entities} >= {record_ref, "gitlab:project:42"}
    assert relationships == [
        {
            "source": record_ref,
            "target": "gitlab:project:42",
            "relationship": "belongsToProject",
        }
    ]


@pytest.mark.parametrize(
    ("kind", "payload", "code"),
    [
        ("project", _project(id="42"), PrepErrorCode.SHAPE_VIOLATION.value),
        ("project", _project(path_with_namespace="../escape"), PrepErrorCode.PATH_ABUSE.value),
        (
            "project",
            _project(web_url="https://user:pass@gitlab.example/group/demo"),
            PrepErrorCode.PATH_ABUSE.value,
        ),
        ("issue", _issue(title="  "), PrepErrorCode.SHAPE_VIOLATION.value),
        ("merge_request", _merge_request(source_branch="../main"), PrepErrorCode.PATH_ABUSE.value),
    ],
)
def test_malformed_records_are_quarantined_without_commit(
    context: PrepContext,
    kind: str,
    payload: dict[str, object],
    code: str,
) -> None:
    prep, recorder = _prep()
    result = prep.process_page(
        kind,  # type: ignore[arg-type]
        [payload],
        stream=f"gitlab:{kind}",
        page=1,
        cursor=None,
        context=context,
    )
    assert result.outcomes[0].disposition is PrepDisposition.QUARANTINED
    assert code in result.outcomes[0].evidence.error_codes
    assert recorder.calls == []
    assert result.checkpoint_advanced is True


def test_secret_payload_is_redacted_from_evidence(context: PrepContext) -> None:
    prep, recorder = _prep()
    secret = "glpat-should-never-be-retained"
    result = prep.process_page(
        "project",
        [{**_project(), "private_token": secret}],
        stream="gitlab:projects",
        page=1,
        cursor=None,
        context=context,
    )
    evidence = result.outcomes[0].evidence.model_dump_json()
    assert result.outcomes[0].evidence.error_codes == (
        PrepErrorCode.SECRET.value,
    )
    assert secret not in evidence
    assert recorder.calls == []


def test_duplicate_ids_quarantine_all_duplicates(context: PrepContext) -> None:
    prep, recorder = _prep()
    result = prep.process_page(
        "issue",
        [_issue(), _issue(id=1002)],
        stream="gitlab:issues",
        page=1,
        cursor=None,
        context=context,
    )
    assert all(item.disposition is PrepDisposition.QUARANTINED for item in result.outcomes)
    assert all(
        PrepErrorCode.DUPLICATE_ID.value in item.evidence.error_codes
        for item in result.outcomes
    )
    assert recorder.calls == []


def test_mixed_page_commits_once_and_replays_without_second_commit(context: PrepContext) -> None:
    prep, recorder = _prep()
    records = [_issue(), {**_issue(iid=12), "title": ""}]
    first = prep.process_page(
        "issue",
        records,
        stream="gitlab:issues",
        page=1,
        cursor="cursor-1",
        context=context,
    )
    assert len(recorder.calls) == 1
    assert [item.disposition for item in first.outcomes] == [
        PrepDisposition.COMMITTED,
        PrepDisposition.QUARANTINED,
    ]

    replay = prep.process_page(
        "issue",
        records,
        stream="gitlab:issues",
        page=1,
        cursor="cursor-1",
        context=context,
    )
    assert len(recorder.calls) == 1
    assert replay.commit is not None and replay.commit.replayed is True
    assert replay.outcomes[0].disposition is PrepDisposition.REPLAYED
    assert replay.outcomes[1].disposition is PrepDisposition.QUARANTINED

    with pytest.raises(CheckpointConflict):
        prep.process_page(
            "issue",
            [{**_issue(), "title": "changed"}],
            stream="gitlab:issues",
            page=1,
            cursor="cursor-1",
            context=context,
        )


def test_commit_failure_does_not_advance_checkpoint(context: PrepContext) -> None:
    recorder = RecordingCommitter(fail=True)
    prep, _ = _prep(recorder)
    with pytest.raises(ConnectorCommitError):
        prep.process_page(
            "merge_request",
            [_merge_request()],
            stream="gitlab:merge-requests",
            page=1,
            cursor=None,
            context=context,
        )
    assert prep.checkpoints.latest("gitlab:merge-requests") is None


def test_oversized_page_is_bounded_and_not_checkpointed(context: PrepContext) -> None:
    prep, recorder = _prep()
    result = prep.process_page(
        "project",
        [_project(id=index + 1) for index in range(101)],
        stream="gitlab:projects",
        page=1,
        cursor=None,
        context=context,
    )
    assert len(result.outcomes) == 1
    assert result.outcomes[0].evidence.error_codes == (PrepErrorCode.PAGE_LIMIT.value,)
    assert result.checkpoint_advanced is False
    assert recorder.calls == []


def test_page_gaps_are_rejected(context: PrepContext) -> None:
    prep, _ = _prep()
    with pytest.raises(CheckpointConflict):
        prep.process_page(
            "project",
            [_project()],
            stream="gitlab:projects",
            page=2,
            cursor=None,
            context=context,
        )
