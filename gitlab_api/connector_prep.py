"""Governed GitLab payload preparation and checkpointed native ingestion.

This module is deliberately a small boundary adapter.  It owns the untrusted
GitLab payload (strict validation, bounded cleaning, and deterministic mapping)
but it does not implement a graph transaction.  Successful rows are handed to
the existing :func:`gitlab_api.kg_ingest.ingest_entities` path, which is the
connector's one native ``ApplyChangeEnvelope`` authority.

``ARROW_IPC`` is the declared hand-off format for the shared connector-prep
contract.  The connector does not import pandas, polars, or pyarrow: an
upstream adapter may materialize the validated rows as Arrow IPC before the
next preparation stage without making a dataframe runtime part of this
package.

The public result and evidence types intentionally contain no raw rejected
payloads.  They carry only bounded error codes, safe field paths, opaque
digests, and stable lineage references.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from enum import StrEnum
from threading import RLock
from typing import Any, Literal, NamedTuple, Protocol, cast
from urllib.parse import urlsplit

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    StrictStr,
    ValidationError,
    field_validator,
    model_validator,
)

PREP_CONTRACT_VERSION = "1"
ARROW_IPC = "arrow_ipc"
SOURCE = "gitlab-api"
DOMAIN = "gitlab"

MAX_PAGE_RECORDS = 100
MAX_SELECTED_RECORDS = 100
MAX_PAGES = 100_000
MAX_FIELDS = 48
MAX_ERRORS = 16
MAX_TEXT_LENGTH = 8_192
MAX_URL_LENGTH = 2_048
MAX_PATH_LENGTH = 1_024
MAX_REFERENCE_LENGTH = 256
MAX_LABELS = 64
MAX_LABEL_LENGTH = 256
MAX_IDENTIFIER = 2**63 - 1

RecordKind = Literal["project", "issue", "merge_request"]


class PrepDisposition(StrEnum):
    """Terminal state of one selected source record."""

    COMMITTED = "committed"
    REPLAYED = "replayed"
    QUARANTINED = "quarantined"


class PrepErrorCode(StrEnum):
    """Stable, privacy-safe quarantine reasons."""

    EXTRA_FIELD = "extra_field"
    FIELD_LIMIT = "field_limit"
    PAGE_LIMIT = "page_too_large"
    RECORD_LIMIT = "record_limit"
    SECRET = "secret_bearing_payload"
    TEXT_LIMIT = "text_limit"
    DUPLICATE_ID = "duplicate_id"
    PATH_ABUSE = "path_or_url_abuse"
    INVALID_PAYLOAD = "invalid_payload"
    CHECKPOINT_CONFLICT = "checkpoint_conflict"
    SHAPE_VIOLATION = "shape_violation"


class PrepError(RuntimeError):
    """A bounded, non-sensitive preparation or checkpoint failure."""

    def __init__(self, code: PrepErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code


class CheckpointConflict(PrepError):
    """The source page cannot be safely advanced or replayed."""

    def __init__(self, message: str = "checkpoint conflict") -> None:
        super().__init__(PrepErrorCode.CHECKPOINT_CONFLICT, message)


class ConnectorCommitError(RuntimeError):
    """A native commit failed; the checkpoint remains unchanged."""

    def __init__(self) -> None:
        super().__init__("native GitLab connector commit failed")


class _PrepModel(BaseModel):
    """Strict immutable DTO base; response models remain permissive elsewhere."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        validate_assignment=True,
    )


def _bounded_string(value: object, *, field: str, limit: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    if len(value) > limit:
        raise ValueError(f"{field} exceeds its bounded length")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{field} contains a control character")
    return value


def _required_text(value: object, *, field: str, limit: int = MAX_TEXT_LENGTH) -> str:
    value = _bounded_string(value, field=field, limit=limit).strip()
    if not value:
        raise ValueError(f"{field} must not be blank")
    return value


def _optional_text(
    value: object, *, field: str, limit: int = MAX_TEXT_LENGTH
) -> str | None:
    if value is None:
        return None
    value = _bounded_string(value, field=field, limit=limit).strip()
    return value or None


def _parse_safe_url(value: str, *, field: str):
    try:
        parsed = urlsplit(value)
        _ = parsed.hostname
        _ = parsed.port
    except ValueError as exc:
        raise ValueError(f"{field} is not a safe URL") from exc
    return parsed


def _check_url_scheme_and_host(parsed, *, field: str) -> None:
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"{field} must use an HTTP(S) URL")


def _check_url_credentials_and_fragment(parsed, *, field: str) -> None:
    if parsed.username is not None or parsed.password is not None:
        raise ValueError(f"{field} may not contain credentials")
    if parsed.fragment:
        raise ValueError(f"{field} may not contain a fragment")


def _check_url_path_traversal(parsed, *, field: str) -> None:
    path = parsed.path.lower()
    if "\\" in path or any(part in {".", ".."} for part in path.split("/")):
        raise ValueError(f"{field} contains path traversal")
    if "%2e" in path or "%2f" in path or "%5c" in path:
        raise ValueError(f"{field} contains encoded path traversal")


_SENSITIVE_QUERY_TOKENS = (
    "token=",
    "secret=",
    "password=",
    "apikey=",
    "api_key=",
    "access_key=",
    "authorization=",
)


def _check_url_sensitive_query(parsed, *, field: str) -> None:
    query = parsed.query.lower()
    if any(token in query for token in _SENSITIVE_QUERY_TOKENS):
        raise ValueError(f"{field} contains sensitive query data")


def _safe_url(value: object, *, field: str = "web_url") -> str:
    value = _bounded_string(value, field=field, limit=MAX_URL_LENGTH).strip()
    parsed = _parse_safe_url(value, field=field)
    _check_url_scheme_and_host(parsed, field=field)
    _check_url_credentials_and_fragment(parsed, field=field)
    _check_url_path_traversal(parsed, field=field)
    _check_url_sensitive_query(parsed, field=field)
    return value


def _safe_path(value: object, *, field: str, allow_slash: bool = True) -> str:
    value = _required_text(value, field=field, limit=MAX_PATH_LENGTH)
    if "\\" in value or value.startswith("/"):
        raise ValueError(f"{field} is not a safe path")
    if not allow_slash and "/" in value:
        raise ValueError(f"{field} may not contain a path separator")
    if any(part in {".", ".."} for part in value.split("/")):
        raise ValueError(f"{field} contains traversal")
    if "//" in value:
        raise ValueError(f"{field} contains an empty path component")
    return value


def _state(value: object) -> str:
    value = _required_text(value, field="state", limit=128)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ValueError("state contains unsafe characters")
    return value


def _timestamp(value: object, *, field: str) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        text = value.strip()
        if not text or len(text) > 64:
            raise ValueError(f"{field} is not a valid timestamp")
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"{field} is not a valid timestamp") from exc
    else:
        raise ValueError(f"{field} must be an ISO timestamp")
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed.astimezone(UTC)


def _positive_id(value: object, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    if value <= 0 or value > MAX_IDENTIFIER:
        raise ValueError(f"{field} is outside the supported range")
    return value


class NamespacePayload(_PrepModel):
    """The deliberately small namespace subset used for project lineage."""

    id: StrictInt | None = Field(default=None, ge=1, le=MAX_IDENTIFIER)
    name: StrictStr | None = None
    full_path: StrictStr | None = None

    @field_validator("name", mode="before")
    @classmethod
    def _name(cls, value: object) -> str | None:
        return _optional_text(value, field="namespace.name", limit=MAX_REFERENCE_LENGTH)

    @field_validator("full_path", mode="before")
    @classmethod
    def _full_path(cls, value: object) -> str | None:
        if value is None:
            return None
        return _safe_path(value, field="namespace.full_path")

    @model_validator(mode="after")
    def _has_identity(self) -> NamespacePayload:
        if self.id is None and self.full_path is None:
            raise ValueError("namespace requires id or full_path")
        return self


class GitLabProjectPayload(_PrepModel):
    """Versioned strict projection of the GitLab project response."""

    schema_version: Literal[PREP_CONTRACT_VERSION] = PREP_CONTRACT_VERSION
    id: StrictInt = Field(gt=0, le=MAX_IDENTIFIER)
    name: StrictStr
    path_with_namespace: StrictStr
    web_url: StrictStr
    description: StrictStr | None = None
    state: StrictStr | None = None
    visibility: StrictStr | None = None
    last_activity_at: datetime | None = None
    namespace: NamespacePayload | None = None

    @field_validator("id", mode="before")
    @classmethod
    def _id(cls, value: object) -> int:
        return _positive_id(value, field="id")

    @field_validator("name", mode="before")
    @classmethod
    def _name(cls, value: object) -> str:
        return _required_text(value, field="name")

    @field_validator("path_with_namespace", mode="before")
    @classmethod
    def _path(cls, value: object) -> str:
        return _safe_path(value, field="path_with_namespace")

    @field_validator("web_url", mode="before")
    @classmethod
    def _url(cls, value: object) -> str:
        return _safe_url(value)

    @field_validator("description", mode="before")
    @classmethod
    def _description(cls, value: object) -> str | None:
        return _optional_text(value, field="description")

    @field_validator("state", "visibility", mode="before")
    @classmethod
    def _state_or_visibility(cls, value: object, info: Any) -> str | None:
        if value is None:
            return None
        return (
            _state(value)
            if info.field_name == "state"
            else _required_text(value, field=info.field_name, limit=128)
        )

    @field_validator("last_activity_at", mode="before")
    @classmethod
    def _last_activity(cls, value: object) -> datetime | None:
        return None if value is None else _timestamp(value, field="last_activity_at")


class GitLabIssuePayload(_PrepModel):
    """Versioned strict projection of the GitLab issue response."""

    schema_version: Literal[PREP_CONTRACT_VERSION] = PREP_CONTRACT_VERSION
    id: StrictInt = Field(gt=0, le=MAX_IDENTIFIER)
    iid: StrictInt = Field(gt=0, le=MAX_IDENTIFIER)
    project_id: StrictInt = Field(gt=0, le=MAX_IDENTIFIER)
    title: StrictStr
    state: StrictStr
    web_url: StrictStr
    created_at: datetime
    updated_at: datetime | None = None
    description: StrictStr | None = None
    labels: tuple[StrictStr, ...] = ()

    @field_validator("id", "iid", "project_id", mode="before")
    @classmethod
    def _ids(cls, value: object, info: Any) -> int:
        return _positive_id(value, field=info.field_name)

    @field_validator("title", mode="before")
    @classmethod
    def _title(cls, value: object) -> str:
        return _required_text(value, field="title")

    @field_validator("state", mode="before")
    @classmethod
    def _state(cls, value: object) -> str:
        return _state(value)

    @field_validator("web_url", mode="before")
    @classmethod
    def _url(cls, value: object) -> str:
        return _safe_url(value)

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def _dates(cls, value: object, info: Any) -> datetime | None:
        return None if value is None else _timestamp(value, field=info.field_name)

    @field_validator("description", mode="before")
    @classmethod
    def _description(cls, value: object) -> str | None:
        return _optional_text(value, field="description")

    @field_validator("labels", mode="before")
    @classmethod
    def _labels(cls, value: object) -> tuple[str, ...]:
        if value is None:
            return ()
        if not isinstance(value, (list, tuple)) or len(value) > MAX_LABELS:
            raise ValueError("labels exceed the bounded shape")
        labels: list[str] = []
        for label in value:
            labels.append(_required_text(label, field="labels", limit=MAX_LABEL_LENGTH))
        return tuple(labels)


class GitLabMergeRequestPayload(_PrepModel):
    """Versioned strict projection of the GitLab merge-request response."""

    schema_version: Literal[PREP_CONTRACT_VERSION] = PREP_CONTRACT_VERSION
    id: StrictInt = Field(gt=0, le=MAX_IDENTIFIER)
    iid: StrictInt = Field(gt=0, le=MAX_IDENTIFIER)
    project_id: StrictInt = Field(gt=0, le=MAX_IDENTIFIER)
    title: StrictStr
    state: StrictStr
    source_branch: StrictStr
    target_branch: StrictStr
    web_url: StrictStr
    created_at: datetime
    updated_at: datetime | None = None
    merged_at: datetime | None = None
    description: StrictStr | None = None
    sha: StrictStr | None = None

    @field_validator("id", "iid", "project_id", mode="before")
    @classmethod
    def _ids(cls, value: object, info: Any) -> int:
        return _positive_id(value, field=info.field_name)

    @field_validator("title", mode="before")
    @classmethod
    def _title(cls, value: object) -> str:
        return _required_text(value, field="title")

    @field_validator("state", mode="before")
    @classmethod
    def _state(cls, value: object) -> str:
        return _state(value)

    @field_validator("source_branch", "target_branch", mode="before")
    @classmethod
    def _branches(cls, value: object, info: Any) -> str:
        branch = _safe_path(value, field=info.field_name)
        if ".." in branch:
            raise ValueError(f"{info.field_name} contains unsafe traversal")
        return branch

    @field_validator("web_url", mode="before")
    @classmethod
    def _url(cls, value: object) -> str:
        return _safe_url(value)

    @field_validator("created_at", "updated_at", "merged_at", mode="before")
    @classmethod
    def _dates(cls, value: object, info: Any) -> datetime | None:
        return None if value is None else _timestamp(value, field=info.field_name)

    @field_validator("description", "sha", mode="before")
    @classmethod
    def _optional(cls, value: object, info: Any) -> str | None:
        return _optional_text(value, field=info.field_name)


PayloadModel = GitLabProjectPayload | GitLabIssuePayload | GitLabMergeRequestPayload
_PAYLOAD_MODELS: dict[RecordKind, type[BaseModel]] = {
    "project": GitLabProjectPayload,
    "issue": GitLabIssuePayload,
    "merge_request": GitLabMergeRequestPayload,
}


class PrepLimits(_PrepModel):
    """Operator-tunable bounds.  Every limit is finite and positive."""

    max_page_records: StrictInt = Field(
        default=MAX_PAGE_RECORDS, gt=0, le=MAX_PAGE_RECORDS
    )
    max_selected_records: StrictInt = Field(
        default=MAX_SELECTED_RECORDS, gt=0, le=MAX_SELECTED_RECORDS
    )
    max_pages: StrictInt = Field(default=MAX_PAGES, gt=0, le=MAX_PAGES)
    max_fields: StrictInt = Field(default=MAX_FIELDS, gt=0, le=MAX_FIELDS)
    max_errors: StrictInt = Field(default=MAX_ERRORS, gt=0, le=MAX_ERRORS)
    max_text_length: StrictInt = Field(
        default=MAX_TEXT_LENGTH, gt=0, le=MAX_TEXT_LENGTH
    )


def _safe_reference(
    value: object, *, field: str, limit: int = MAX_REFERENCE_LENGTH
) -> str:
    value = _required_text(value, field=field, limit=limit)
    if "://" in value or value.startswith(("/", "\\")):
        raise ValueError(f"{field} must be an opaque reference")
    if any(
        marker in value.lower() for marker in ("token", "secret", "password", "bearer")
    ):
        raise ValueError(f"{field} is not an opaque reference")
    return value


class PrepContext(_PrepModel):
    """Governance references required before a row can reach graph materialization."""

    tenant_reference: StrictStr
    access_policy_reference: StrictStr
    classification: Literal["public", "internal", "confidential", "restricted"] = (
        "internal"
    )
    retention_reference: StrictStr
    provenance_reference: StrictStr
    source_instance_reference: StrictStr

    @field_validator(
        "tenant_reference",
        "access_policy_reference",
        "retention_reference",
        "provenance_reference",
        "source_instance_reference",
        mode="before",
    )
    @classmethod
    def _references(cls, value: object, info: Any) -> str:
        return _safe_reference(value, field=info.field_name)


class ArrowField(_PrepModel):
    name: StrictStr
    data_type: StrictStr


class ArrowPrepPlan(_PrepModel):
    """A versioned declaration of the Arrow boundary, not an Arrow runtime."""

    schema_version: Literal[PREP_CONTRACT_VERSION] = PREP_CONTRACT_VERSION
    record_kind: RecordKind
    handoff_format: Literal[ARROW_IPC] = ARROW_IPC
    operations: tuple[StrictStr, ...]
    arrow_schema: tuple[ArrowField, ...]
    engine_dependencies: tuple[StrictStr, ...] = ()


_PLAN_FIELDS: dict[RecordKind, tuple[tuple[str, str], ...]] = {
    "project": (
        ("id", "int64"),
        ("name", "utf8"),
        ("path_with_namespace", "utf8"),
        ("web_url", "utf8"),
        ("last_activity_at", "timestamp[us, tz=UTC]"),
    ),
    "issue": (
        ("id", "int64"),
        ("iid", "int64"),
        ("project_id", "int64"),
        ("title", "utf8"),
        ("state", "utf8"),
        ("created_at", "timestamp[us, tz=UTC]"),
    ),
    "merge_request": (
        ("id", "int64"),
        ("iid", "int64"),
        ("project_id", "int64"),
        ("title", "utf8"),
        ("state", "utf8"),
        ("source_branch", "utf8"),
        ("target_branch", "utf8"),
        ("created_at", "timestamp[us, tz=UTC]"),
    ),
}


def arrow_prep_plan(record_kind: RecordKind) -> ArrowPrepPlan:
    """Return the deterministic preparation declaration for ``record_kind``."""

    return ArrowPrepPlan(
        record_kind=record_kind,
        operations=(
            "profile",
            "clean_names",
            "drop_null_required",
            "coerce_types",
            "dedupe",
            "validate_strict",
            "map_lineage",
            "commit_change_envelope",
        ),
        arrow_schema=tuple(
            ArrowField(name=name, data_type=data_type)
            for name, data_type in _PLAN_FIELDS[record_kind]
        ),
    )


class PrepEvidence(_PrepModel):
    """Safe lineage and validation evidence; never stores a source row."""

    schema_version: Literal[PREP_CONTRACT_VERSION] = PREP_CONTRACT_VERSION
    source: Literal[SOURCE] = SOURCE
    record_kind: RecordKind
    record_ref: StrictStr
    disposition: PrepDisposition
    page: StrictInt = Field(ge=1, le=MAX_PAGES)
    ordinal: StrictInt = Field(ge=0, lt=MAX_PAGE_RECORDS)
    cursor_digest: StrictStr | None = None
    source_instance_reference: StrictStr
    tenant_reference: StrictStr
    access_policy_reference: StrictStr
    retention_reference: StrictStr
    provenance_reference: StrictStr
    classification: Literal["public", "internal", "confidential", "restricted"]
    validation_codes: tuple[StrictStr, ...] = ()
    clean_operations: tuple[StrictStr, ...] = ()
    input_digest: StrictStr | None = None
    error_codes: tuple[StrictStr, ...] = ()
    error_fields: tuple[StrictStr, ...] = ()

    @field_validator("record_ref", mode="before")
    @classmethod
    def _record_ref(cls, value: object) -> str:
        return _safe_reference(value, field="record_ref", limit=MAX_REFERENCE_LENGTH)

    @field_validator(
        "source_instance_reference",
        "tenant_reference",
        "access_policy_reference",
        "retention_reference",
        "provenance_reference",
        mode="before",
    )
    @classmethod
    def _context_ref(cls, value: object, info: Any) -> str:
        return _safe_reference(value, field=info.field_name)

    @field_validator("cursor_digest", "input_digest", mode="before")
    @classmethod
    def _digest(cls, value: object, info: Any) -> str | None:
        if value is None:
            return None
        digest = _bounded_string(value, field=info.field_name, limit=64)
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"{info.field_name} must be a SHA-256 digest")
        return digest

    @field_validator(
        "validation_codes", "clean_operations", "error_codes", "error_fields"
    )
    @classmethod
    def _bounded_codes(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) > MAX_ERRORS:
            raise ValueError("evidence error list is too large")
        return tuple(
            _safe_reference(item, field="evidence_code", limit=128) for item in value
        )


class PreparedOutcome(_PrepModel):
    """Bounded terminal result for one selected row."""

    record_kind: RecordKind
    ordinal: StrictInt = Field(ge=0, lt=MAX_PAGE_RECORDS)
    record_ref: StrictStr
    disposition: PrepDisposition
    evidence: PrepEvidence


class NativeCommitResult(_PrepModel):
    """Small adapter result; no engine response is exposed to the connector."""

    nodes: StrictInt = Field(ge=0)
    edges: StrictInt = Field(ge=0)
    replayed: bool = False
    transaction_reference: StrictStr | None = None


class NativeCommitter(Protocol):
    """Compatible seam for NE-110 or the existing native connector path."""

    def commit(
        self,
        entities: Sequence[Mapping[str, Any]],
        relationships: Sequence[Mapping[str, Any]],
        *,
        client: Any | None = None,
        graph: str | None = None,
        idempotency_key: str | None = None,
    ) -> NativeCommitResult:
        """Commit one already-mapped graph slice atomically."""


def _commit_result(value: object) -> NativeCommitResult:
    if isinstance(value, NativeCommitResult):
        return value
    if not isinstance(value, Mapping):
        raise ConnectorCommitError
    try:
        return NativeCommitResult(
            nodes=int(value.get("nodes", 0)),
            edges=int(value.get("edges", 0)),
            replayed=bool(value.get("replayed", False)),
            # Engine transaction/envelope identifiers are intentionally not
            # surfaced unless a future adapter proves they are opaque.
            transaction_reference=None,
        )
    except (TypeError, ValueError):
        raise ConnectorCommitError from None


class ExistingNativeCommitter:
    """Call the one existing ``kg_ingest`` / ``ApplyChangeEnvelope`` path."""

    def commit(
        self,
        entities: Sequence[Mapping[str, Any]],
        relationships: Sequence[Mapping[str, Any]],
        *,
        client: Any | None = None,
        graph: str | None = None,
        idempotency_key: str | None = None,
    ) -> NativeCommitResult:
        # The import is lazy so model-only tooling does not resolve the engine.
        import asyncio

        from .kg_ingest import ingest_entities

        # ``ingest_entities`` is the only connector write authority.  Its SDK
        # ingest facade is async; this adapter's ``commit`` contract (NE-110)
        # is sync and has no production caller on the engine's own event loop
        # today, so bridging with ``asyncio.run`` is safe here (never bridge a
        # handler that already runs on that loop -- see
        # FLEET-SDK-MIGRATION-RECIPE.md). ``client``/``graph`` are no longer
        # accepted by the SDK facade (process-global ``current_ingest()``);
        # ``idempotency_key`` remains in this adapter contract for NE-110,
        # but is intentionally not routed to a second or private transaction
        # implementation here.
        del client, graph, idempotency_key
        try:
            result = asyncio.run(
                ingest_entities(
                    [dict(entity) for entity in entities],
                    [dict(relationship) for relationship in relationships],
                )
            )
        except Exception as exc:  # noqa: BLE001 - never leak engine details
            raise ConnectorCommitError from exc
        return _commit_result(result)


class CheckpointOutcome(_PrepModel):
    ordinal: StrictInt = Field(ge=0, lt=MAX_PAGE_RECORDS)
    record_ref: StrictStr
    disposition: PrepDisposition
    input_digest: StrictStr | None = None
    error_codes: tuple[StrictStr, ...] = ()
    error_fields: tuple[StrictStr, ...] = ()

    @field_validator("record_ref", mode="before")
    @classmethod
    def _record_ref(cls, value: object) -> str:
        return _safe_reference(value, field="record_ref")

    @field_validator("input_digest", mode="before")
    @classmethod
    def _input_digest(cls, value: object) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError("input_digest must be a SHA-256 digest")
        return value


class Checkpoint(_PrepModel):
    """A page digest plus safe terminal outcomes, suitable for CAS storage."""

    schema_version: Literal[PREP_CONTRACT_VERSION] = PREP_CONTRACT_VERSION
    stream: StrictStr
    page: StrictInt = Field(ge=1, le=MAX_PAGES)
    cursor_digest: StrictStr | None = None
    page_digest: StrictStr
    version: StrictInt = Field(ge=1)
    outcomes: tuple[CheckpointOutcome, ...] = ()

    @field_validator("stream", mode="before")
    @classmethod
    def _stream(cls, value: object) -> str:
        return _safe_reference(value, field="stream")

    @field_validator("cursor_digest", "page_digest", mode="before")
    @classmethod
    def _page_digest(cls, value: object, info: Any) -> str | None:
        if value is None and info.field_name == "cursor_digest":
            return None
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError(f"{info.field_name} must be a SHA-256 digest")
        return value


class CheckpointStore(Protocol):
    """CAS contract implemented by a durable source checkpoint store."""

    def read(self, stream: str, page: int) -> Checkpoint | None:
        """Return the exact page checkpoint, if present."""

    def latest(self, stream: str) -> Checkpoint | None:
        """Return the highest advanced page."""

    def advance(
        self, stream: str, checkpoint: Checkpoint, *, expected_version: int
    ) -> Checkpoint:
        """Atomically advance after all selected rows are terminal."""


class MemoryCheckpointStore:
    """Small deterministic fixture store; production uses a durable CAS store."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._pages: dict[tuple[str, int], Checkpoint] = {}
        self._latest: dict[str, Checkpoint] = {}

    def read(self, stream: str, page: int) -> Checkpoint | None:
        with self._lock:
            return self._pages.get((stream, page))

    def latest(self, stream: str) -> Checkpoint | None:
        with self._lock:
            return self._latest.get(stream)

    def advance(
        self, stream: str, checkpoint: Checkpoint, *, expected_version: int
    ) -> Checkpoint:
        with self._lock:
            current = self._latest.get(stream)
            current_version = current.version if current else 0
            if current_version != expected_version:
                raise CheckpointConflict
            prior_page = self._pages.get((stream, checkpoint.page))
            if prior_page is not None:
                if prior_page.page_digest == checkpoint.page_digest:
                    return prior_page
                raise CheckpointConflict
            if current is not None and checkpoint.page != current.page + 1:
                raise CheckpointConflict
            if checkpoint.version != expected_version + 1:
                raise CheckpointConflict
            self._pages[(stream, checkpoint.page)] = checkpoint
            self._latest[stream] = checkpoint
            return checkpoint


class PrepResult(_PrepModel):
    """Page-level result with bounded evidence and checkpoint state."""

    schema_version: Literal[PREP_CONTRACT_VERSION] = PREP_CONTRACT_VERSION
    record_kind: RecordKind
    stream: StrictStr
    page: StrictInt = Field(ge=1, le=MAX_PAGES)
    page_digest: StrictStr
    plan: ArrowPrepPlan
    outcomes: tuple[PreparedOutcome, ...]
    checkpoint_advanced: bool = False
    checkpoint: Checkpoint | None = None
    commit: NativeCommitResult | None = None

    @field_validator("page_digest", mode="before")
    @classmethod
    def _page_digest(cls, value: object) -> str:
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError("page_digest must be a SHA-256 digest")
        return value


def _digest(value: object) -> str:
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=lambda item: repr(item),
        ).encode("utf-8")
    except Exception:
        encoded = type(value).__name__.encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


_SECRET_FIELD = re.compile(
    r"(?:token|password|secret|private[_-]?key|api[_-]?key|authorization|"
    r"credential|access[_-]?key|ssh[_-]?key)",
    re.IGNORECASE,
)
_SECRET_VALUE = (
    re.compile(r"glpat-[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def _cursor_digest(cursor: str | None) -> str | None:
    """Validate a source cursor without retaining its (possibly sensitive) value."""

    if cursor is None:
        return None
    try:
        _bounded_string(cursor, field="cursor", limit=512)
    except ValueError as exc:
        raise PrepError(PrepErrorCode.INVALID_PAYLOAD, "cursor is not bounded") from exc
    if any(pattern.search(cursor) for pattern in _SECRET_VALUE):
        raise PrepError(PrepErrorCode.SECRET, "secret-bearing cursor rejected")
    return _digest(cursor)


def _walk_payload(value: object, path: str = "") -> Sequence[tuple[str, object]]:
    found: list[tuple[str, object]] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}" if path else key_text
            found.append((child_path, child))
            found.extend(_walk_payload(child, child_path))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            found.extend(_walk_payload(child, f"{path}[{index}]"))
    return found


def _check_field_path_not_secret(path: str) -> None:
    if _SECRET_FIELD.search(path):
        raise PrepError(PrepErrorCode.SECRET, "secret-bearing payload rejected")


def _check_field_value_bounds(value: object, limits: PrepLimits) -> None:
    if not isinstance(value, str):
        return
    if len(value) > limits.max_text_length:
        raise PrepError(PrepErrorCode.TEXT_LIMIT, "record text exceeds the bound")
    if any(pattern.search(value) for pattern in _SECRET_VALUE):
        raise PrepError(PrepErrorCode.SECRET, "secret-bearing payload rejected")


def _check_payload_bounds(payload: object, limits: PrepLimits) -> None:
    if not isinstance(payload, Mapping):
        raise PrepError(PrepErrorCode.INVALID_PAYLOAD, "record must be an object")
    if len(payload) > limits.max_fields:
        raise PrepError(
            PrepErrorCode.FIELD_LIMIT, "record field count exceeds the bound"
        )
    for path, value in _walk_payload(payload):
        _check_field_path_not_secret(path)
        _check_field_value_bounds(value, limits)


def _clean_payload(payload: Mapping[str, object]) -> dict[str, object]:
    """Perform only deterministic boundary cleaning; validation remains strict."""

    def clean(value: object) -> object:
        if isinstance(value, Mapping):
            return {str(key).strip(): clean(child) for key, child in value.items()}
        if isinstance(value, list):
            return [clean(child) for child in value]
        if isinstance(value, tuple):
            return tuple(clean(child) for child in value)
        if isinstance(value, str):
            return value.strip()
        return value

    return cast(dict[str, object], clean(payload))


def _validation_codes(
    error: ValidationError, limits: PrepLimits
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Reduce Pydantic errors to bounded types/paths without inputs or messages."""

    codes: list[str] = []
    fields: list[str] = []
    for item in error.errors()[: limits.max_errors]:
        code = str(item.get("type") or "invalid_payload")[:128]
        path = ".".join(str(part) for part in item.get("loc", ()))[:128]
        if code not in codes:
            codes.append(code)
        if path and path not in fields:
            fields.append(path)
    return tuple(codes), tuple(fields)


def _validation_reason(codes: Sequence[str], fields: Sequence[str]) -> PrepErrorCode:
    if "extra_forbidden" in codes:
        return PrepErrorCode.EXTRA_FIELD
    if any(
        field.split(".", 1)[0]
        in {"web_url", "path_with_namespace", "source_branch", "target_branch"}
        for field in fields
    ):
        return PrepErrorCode.PATH_ABUSE
    return PrepErrorCode.SHAPE_VIOLATION


def _record_ref(
    kind: RecordKind, model: BaseModel | None, page: int, ordinal: int
) -> str:
    if isinstance(model, GitLabProjectPayload):
        return f"gitlab:project:{model.id}"
    if isinstance(model, GitLabIssuePayload):
        return f"gitlab:issue:{model.project_id}:{model.iid}"
    if isinstance(model, GitLabMergeRequestPayload):
        return f"gitlab:mr:{model.project_id}:{model.iid}"
    return f"gitlab:{kind}:page:{page}:ordinal:{ordinal}"


def _base_properties(
    context: PrepContext, *, record_ref: str, page: int, cursor_digest: str | None
) -> dict[str, object]:
    return {
        "sourceRecordRef": record_ref,
        "tenantReference": context.tenant_reference,
        "accessPolicyReference": context.access_policy_reference,
        "retentionReference": context.retention_reference,
        "provenanceReference": context.provenance_reference,
        "classification": context.classification,
        "sourcePage": page,
        "sourceCursorDigest": cursor_digest,
        "sourceInstanceReference": context.source_instance_reference,
    }


def _project_stub(
    project_id: int, context: PrepContext, page: int, cursor_digest: str | None
) -> dict[str, object]:
    ref = f"gitlab:project:{project_id}"
    return {
        "id": ref,
        "node_type": "Project",
        "externalToolId": str(project_id),
        **_base_properties(
            context, record_ref=ref, page=page, cursor_digest=cursor_digest
        ),
    }


def _map_payload(
    kind: RecordKind,
    model: PayloadModel,
    context: PrepContext,
    *,
    page: int,
    cursor_digest: str | None,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Map only validated fields to canonical nodes and ontology relations."""

    if isinstance(model, GitLabProjectPayload):
        ref = f"gitlab:project:{model.id}"
        node: dict[str, object] = {
            "id": ref,
            "node_type": "Project",
            "name": model.name,
            "path_with_namespace": model.path_with_namespace,
            "web_url": model.web_url,
            "description": model.description,
            "state": model.state,
            "visibility": model.visibility,
            "last_activity_at": model.last_activity_at.isoformat()
            if model.last_activity_at
            else None,
            "externalToolId": str(model.id),
            **_base_properties(
                context, record_ref=ref, page=page, cursor_digest=cursor_digest
            ),
        }
        nodes = [node]
        relationships: list[dict[str, object]] = []
        if model.namespace is not None:
            group_identity = (
                str(model.namespace.id)
                if model.namespace.id is not None
                else model.namespace.full_path
            )
            assert group_identity is not None
            group_ref = f"gitlab:group:{group_identity}"
            nodes.append(
                {
                    "id": group_ref,
                    "node_type": "GitLabGroup",
                    "name": model.namespace.name or model.namespace.full_path,
                    "fullPath": model.namespace.full_path,
                    **_base_properties(
                        context,
                        record_ref=group_ref,
                        page=page,
                        cursor_digest=cursor_digest,
                    ),
                }
            )
            relationships.append(
                {"source": ref, "target": group_ref, "relationship": "partOfGroup"}
            )
        return nodes, relationships

    if isinstance(model, GitLabIssuePayload):
        ref = f"gitlab:issue:{model.project_id}:{model.iid}"
        node = {
            "id": ref,
            "node_type": "Issue",
            "iid": model.iid,
            "projectId": model.project_id,
            "title": model.title,
            "state": model.state,
            "webUrl": model.web_url,
            "createdAt": model.created_at.isoformat(),
            "updatedAt": model.updated_at.isoformat() if model.updated_at else None,
            "description": model.description,
            "labels": list(model.labels),
            "externalToolId": str(model.id),
            **_base_properties(
                context, record_ref=ref, page=page, cursor_digest=cursor_digest
            ),
        }
        project_ref = f"gitlab:project:{model.project_id}"
        return [
            _project_stub(model.project_id, context, page, cursor_digest),
            node,
        ], [{"source": ref, "target": project_ref, "relationship": "belongsToProject"}]

    ref = f"gitlab:mr:{model.project_id}:{model.iid}"
    node = {
        "id": ref,
        "node_type": "MergeRequest",
        "iid": model.iid,
        "projectId": model.project_id,
        "title": model.title,
        "state": model.state,
        "sourceBranch": model.source_branch,
        "targetBranch": model.target_branch,
        "webUrl": model.web_url,
        "createdAt": model.created_at.isoformat(),
        "updatedAt": model.updated_at.isoformat() if model.updated_at else None,
        "mergedAt": model.merged_at.isoformat() if model.merged_at else None,
        "description": model.description,
        "sha": model.sha,
        "externalToolId": str(model.id),
        **_base_properties(
            context, record_ref=ref, page=page, cursor_digest=cursor_digest
        ),
    }
    project_ref = f"gitlab:project:{model.project_id}"
    return [
        _project_stub(model.project_id, context, page, cursor_digest),
        node,
    ], [{"source": ref, "target": project_ref, "relationship": "belongsToProject"}]


def _error_evidence(
    kind: RecordKind,
    ref: str,
    disposition: PrepDisposition,
    *,
    page: int,
    ordinal: int,
    context: PrepContext,
    cursor_digest: str | None,
    input_digest: str | None = None,
    codes: Sequence[str] = (),
    fields: Sequence[str] = (),
) -> PrepEvidence:
    return PrepEvidence(
        record_kind=kind,
        record_ref=ref,
        disposition=disposition,
        page=page,
        ordinal=ordinal,
        cursor_digest=cursor_digest,
        source_instance_reference=context.source_instance_reference,
        tenant_reference=context.tenant_reference,
        access_policy_reference=context.access_policy_reference,
        retention_reference=context.retention_reference,
        provenance_reference=context.provenance_reference,
        classification=context.classification,
        input_digest=input_digest,
        error_codes=tuple(codes)[:MAX_ERRORS],
        error_fields=tuple(fields)[:MAX_ERRORS],
    )


def _checkpoint_outcome(outcome: PreparedOutcome) -> CheckpointOutcome:
    return CheckpointOutcome(
        ordinal=outcome.ordinal,
        record_ref=outcome.record_ref,
        disposition=outcome.disposition,
        input_digest=outcome.evidence.input_digest,
        error_codes=outcome.evidence.error_codes,
        error_fields=outcome.evidence.error_fields,
    )


def _record_identity(model: BaseModel) -> tuple[object, ...]:
    """The de-duplication key for one accepted record within a page."""
    if isinstance(model, GitLabProjectPayload):
        return ("project", model.id)
    if isinstance(model, GitLabIssuePayload):
        return ("issue", model.project_id, model.iid)
    return ("merge_request", model.project_id, model.iid)


class _PageRecordContext(NamedTuple):
    """The per-page values shared by every record processed within one page."""

    kind: RecordKind
    model_cls: type[BaseModel]
    page: int
    cursor_digest: str | None
    context: PrepContext


AcceptedRecord = tuple[
    int, BaseModel, list[dict[str, object]], list[dict[str, object]], str
]


class ConnectorPrep:
    """Strict, bounded, checkpointed GitLab source preparation."""

    def __init__(
        self,
        *,
        committer: NativeCommitter | None = None,
        checkpoints: CheckpointStore | None = None,
        limits: PrepLimits | None = None,
    ) -> None:
        self.committer = committer or ExistingNativeCommitter()
        self.checkpoints = checkpoints or MemoryCheckpointStore()
        self.limits = limits or PrepLimits()

    @staticmethod
    def _validate_kind(kind: str) -> RecordKind:
        if kind not in _PAYLOAD_MODELS:
            raise ValueError("unsupported GitLab preparation record kind")
        return cast(RecordKind, kind)

    def _quarantine(
        self,
        kind: RecordKind,
        *,
        page: int,
        ordinal: int,
        context: PrepContext,
        cursor_digest: str | None,
        code: PrepErrorCode,
        fields: Sequence[str] = (),
        ref: str | None = None,
    ) -> PreparedOutcome:
        record_ref = ref or f"gitlab:{kind}:page:{page}:ordinal:{ordinal}"
        evidence = _error_evidence(
            kind,
            record_ref,
            PrepDisposition.QUARANTINED,
            page=page,
            ordinal=ordinal,
            context=context,
            cursor_digest=cursor_digest,
            codes=(str(code.value),),
            fields=tuple(fields)[: self.limits.max_errors],
        )
        return PreparedOutcome(
            record_kind=kind,
            ordinal=ordinal,
            record_ref=record_ref,
            disposition=PrepDisposition.QUARANTINED,
            evidence=evidence,
        )

    def _replay_result(
        self,
        kind: RecordKind,
        stream: str,
        page: int,
        page_digest: str,
        checkpoint: Checkpoint,
        context: PrepContext,
        plan: ArrowPrepPlan,
    ) -> PrepResult:
        outcomes: list[PreparedOutcome] = []
        for item in checkpoint.outcomes:
            disposition = (
                PrepDisposition.REPLAYED
                if item.disposition is PrepDisposition.COMMITTED
                else PrepDisposition.QUARANTINED
            )
            evidence = _error_evidence(
                kind,
                item.record_ref,
                disposition,
                page=page,
                ordinal=item.ordinal,
                context=context,
                cursor_digest=checkpoint.cursor_digest,
                input_digest=item.input_digest,
                codes=item.error_codes,
                fields=item.error_fields,
            )
            outcomes.append(
                PreparedOutcome(
                    record_kind=kind,
                    ordinal=item.ordinal,
                    record_ref=item.record_ref,
                    disposition=disposition,
                    evidence=evidence,
                )
            )
        return PrepResult(
            record_kind=kind,
            stream=stream,
            page=page,
            page_digest=page_digest,
            plan=plan,
            outcomes=tuple(outcomes),
            checkpoint_advanced=False,
            checkpoint=checkpoint,
            commit=NativeCommitResult(nodes=0, edges=0, replayed=True),
        )

    def _reject_if_oversized_page(
        self,
        kind: RecordKind,
        records: Sequence[Mapping[str, object]],
        *,
        stream: str,
        page: int,
        context: PrepContext,
        cursor_digest: str | None,
    ) -> PrepResult | None:
        """Oversized pages are never enumerated, hashed, or checkpointed.

        The response remains bounded and the caller must quarantine/re-drive
        the source page explicitly.
        """
        if len(records) <= self.limits.max_page_records:
            return None
        digest = _digest(
            {"kind": kind, "page": page, "oversized_records": len(records)}
        )
        ref = f"gitlab:{kind}:page:{page}:oversized"
        outcome = self._quarantine(
            kind,
            page=page,
            ordinal=0,
            context=context,
            cursor_digest=cursor_digest,
            code=PrepErrorCode.PAGE_LIMIT,
            ref=ref,
        )
        return PrepResult(
            record_kind=kind,
            stream=_safe_reference(stream, field="stream"),
            page=page,
            page_digest=digest,
            plan=arrow_prep_plan(kind),
            outcomes=(outcome,),
        )

    def _checkpoint_replay_or_conflict(
        self,
        kind: RecordKind,
        stream: str,
        page: int,
        page_digest: str,
        context: PrepContext,
        plan: ArrowPrepPlan,
    ) -> PrepResult | None:
        """A replay result for an already-checkpointed page, else None to proceed.

        Raises ``CheckpointConflict`` when the page cannot legally be applied
        next (digest drift, a skipped page, or a page behind the stream).
        """
        existing = self.checkpoints.read(stream, page)
        if existing is not None:
            if existing.page_digest != page_digest:
                raise CheckpointConflict("page digest changed after checkpoint")
            return self._replay_result(
                kind, stream, page, page_digest, existing, context, plan
            )
        latest = self.checkpoints.latest(stream)
        if latest is None and page != 1:
            raise CheckpointConflict("first page checkpoint must be page one")
        if latest is not None and page > latest.page + 1:
            raise CheckpointConflict("page checkpoint gap")
        if latest is not None and page <= latest.page:
            raise CheckpointConflict(
                "page checkpoint is missing from an advanced stream"
            )
        return None

    def _prepare_one_record(
        self,
        page_ctx: _PageRecordContext,
        raw: Mapping[str, object],
        ordinal: int,
    ) -> tuple[
        PreparedOutcome | None, AcceptedRecord | None, tuple[object, ...] | None
    ]:
        """Validate, clean, and map one record.

        Returns ``(outcome, None, None)`` when the record is rejected, or
        ``(None, accepted_item, identity)`` when it is accepted.
        """
        ref = f"gitlab:{page_ctx.kind}:page:{page_ctx.page}:ordinal:{ordinal}"
        try:
            _check_payload_bounds(raw, self.limits)
            cleaned = _clean_payload(raw)
            model = page_ctx.model_cls.model_validate(cleaned)
            record_ref = _record_ref(page_ctx.kind, model, page_ctx.page, ordinal)
            nodes, relationships = _map_payload(
                page_ctx.kind,
                cast(PayloadModel, model),
                page_ctx.context,
                page=page_ctx.page,
                cursor_digest=page_ctx.cursor_digest,
            )
            accepted = (ordinal, model, nodes, relationships, record_ref)
            return None, accepted, _record_identity(model)
        except PrepError as exc:
            outcome = self._quarantine(
                page_ctx.kind,
                page=page_ctx.page,
                ordinal=ordinal,
                context=page_ctx.context,
                cursor_digest=page_ctx.cursor_digest,
                code=exc.code,
                ref=ref,
            )
        except ValidationError as exc:
            codes, fields = _validation_codes(exc, self.limits)
            outcome = self._quarantine(
                page_ctx.kind,
                page=page_ctx.page,
                ordinal=ordinal,
                context=page_ctx.context,
                cursor_digest=page_ctx.cursor_digest,
                code=_validation_reason(codes, fields),
                fields=fields,
                ref=ref,
            )
        except (TypeError, ValueError):
            outcome = self._quarantine(
                page_ctx.kind,
                page=page_ctx.page,
                ordinal=ordinal,
                context=page_ctx.context,
                cursor_digest=page_ctx.cursor_digest,
                code=PrepErrorCode.INVALID_PAYLOAD,
                ref=ref,
            )
        return outcome, None, None

    def _validate_and_map_records(
        self,
        page_ctx: _PageRecordContext,
        records: Sequence[Mapping[str, object]],
    ) -> tuple[
        list[PreparedOutcome], list[AcceptedRecord], dict[tuple[object, ...], list[int]]
    ]:
        outcomes: list[PreparedOutcome] = []
        accepted: list[AcceptedRecord] = []
        seen: dict[tuple[object, ...], list[int]] = {}

        for ordinal, raw in enumerate(records):
            outcome, item, identity = self._prepare_one_record(page_ctx, raw, ordinal)
            if outcome is not None:
                outcomes.append(outcome)
                continue
            seen.setdefault(identity, []).append(ordinal)
            accepted.append(item)  # type: ignore[arg-type]
        return outcomes, accepted, seen

    def _drop_duplicate_records(
        self,
        page_ctx: _PageRecordContext,
        accepted: list[AcceptedRecord],
        seen: dict[tuple[object, ...], list[int]],
    ) -> tuple[list[AcceptedRecord], list[PreparedOutcome]]:
        """Quarantine every record whose identity repeats within the page."""
        duplicate_ordinals = {
            ordinal
            for ordinals in seen.values()
            if len(ordinals) > 1
            for ordinal in ordinals
        }
        if not duplicate_ordinals:
            return accepted, []

        outcomes: list[PreparedOutcome] = []
        retained: list[AcceptedRecord] = []
        for item in accepted:
            if item[0] in duplicate_ordinals:
                outcomes.append(
                    self._quarantine(
                        page_ctx.kind,
                        page=page_ctx.page,
                        ordinal=item[0],
                        context=page_ctx.context,
                        cursor_digest=page_ctx.cursor_digest,
                        code=PrepErrorCode.DUPLICATE_ID,
                        ref=item[4],
                    )
                )
            else:
                retained.append(item)
        return retained, outcomes

    def _commit_accepted_records(
        self,
        accepted: list[AcceptedRecord],
        *,
        client: Any | None,
        graph: str | None,
        page_digest: str,
    ) -> NativeCommitResult:
        if not accepted:
            return NativeCommitResult(nodes=0, edges=0)

        entities: list[dict[str, object]] = []
        relationships: list[dict[str, object]] = []
        for _ordinal, _model, nodes, rels, _ref in accepted:
            entities.extend(nodes)
            relationships.extend(rels)
        # A page may include several issues/MRs from the same project.  The
        # native envelope gets each deterministic node exactly once.
        unique_entities = {str(entity["id"]): entity for entity in entities}
        entities = list(unique_entities.values())

        try:
            commit = self.committer.commit(
                entities,
                relationships,
                client=client,
                graph=graph,
                idempotency_key=page_digest,
            )
            return _commit_result(commit)
        except ConnectorCommitError:
            raise
        except Exception as exc:  # noqa: BLE001 - no raw engine detail
            raise ConnectorCommitError from exc

    def _build_committed_outcomes(
        self,
        page_ctx: _PageRecordContext,
        accepted: list[AcceptedRecord],
        commit: NativeCommitResult,
    ) -> list[PreparedOutcome]:
        disposition = (
            PrepDisposition.REPLAYED if commit.replayed else PrepDisposition.COMMITTED
        )
        outcomes: list[PreparedOutcome] = []
        for ordinal, model, _nodes, _rels, record_ref in accepted:
            input_digest = _digest(model.model_dump(mode="json"))
            evidence = PrepEvidence(
                record_kind=page_ctx.kind,
                record_ref=record_ref,
                disposition=disposition,
                page=page_ctx.page,
                ordinal=ordinal,
                cursor_digest=page_ctx.cursor_digest,
                source_instance_reference=page_ctx.context.source_instance_reference,
                tenant_reference=page_ctx.context.tenant_reference,
                access_policy_reference=page_ctx.context.access_policy_reference,
                retention_reference=page_ctx.context.retention_reference,
                provenance_reference=page_ctx.context.provenance_reference,
                classification=page_ctx.context.classification,
                validation_codes=("strict_payload", "shape_context"),
                clean_operations=("trim_strings", "normalize_timestamps"),
                input_digest=input_digest,
            )
            outcomes.append(
                PreparedOutcome(
                    record_kind=page_ctx.kind,
                    ordinal=ordinal,
                    record_ref=record_ref,
                    disposition=evidence.disposition,
                    evidence=evidence,
                )
            )
        return outcomes

    def _advance_page_checkpoint(
        self,
        stream: str,
        page: int,
        cursor_digest: str | None,
        page_digest: str,
        outcomes: list[PreparedOutcome],
    ) -> Checkpoint:
        latest = self.checkpoints.latest(stream)
        expected_version = latest.version if latest else 0
        checkpoint = Checkpoint(
            stream=stream,
            page=page,
            cursor_digest=cursor_digest,
            page_digest=page_digest,
            version=expected_version + 1,
            outcomes=tuple(_checkpoint_outcome(outcome) for outcome in outcomes),
        )
        # The native commit was deterministic; callers can safely retry this
        # page and receive a replay or an explicit CheckpointConflict.
        return self.checkpoints.advance(
            stream, checkpoint, expected_version=expected_version
        )

    def process_page(
        self,
        kind: RecordKind,
        records: Sequence[Mapping[str, object]],
        *,
        stream: str,
        page: int,
        cursor: str | None,
        context: PrepContext,
        client: Any | None = None,
        graph: str | None = None,
    ) -> PrepResult:
        """Prepare one bounded page and atomically submit its accepted rows.

        A page checkpoint is written only after the single native commit returns
        and every selected row has a terminal disposition.  If the process
        crashes after the engine commit but before the checkpoint write, the
        retry submits the same deterministic graph slice; the native authority
        treats the content identity as a replay.
        """

        kind = self._validate_kind(kind)
        if page < 1 or page > self.limits.max_pages:
            raise CheckpointConflict("page is outside the configured bound")
        if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
            raise PrepError(
                PrepErrorCode.INVALID_PAYLOAD, "page must be a record sequence"
            )
        cursor_digest = _cursor_digest(cursor)

        oversized = self._reject_if_oversized_page(
            kind,
            records,
            stream=stream,
            page=page,
            context=context,
            cursor_digest=cursor_digest,
        )
        if oversized is not None:
            return oversized
        if len(records) > self.limits.max_selected_records:
            raise PrepError(
                PrepErrorCode.RECORD_LIMIT, "selected record count exceeds the bound"
            )

        stream = _safe_reference(stream, field="stream")
        page_digest = _digest(records)
        plan = arrow_prep_plan(kind)

        replay = self._checkpoint_replay_or_conflict(
            kind, stream, page, page_digest, context, plan
        )
        if replay is not None:
            return replay

        page_ctx = _PageRecordContext(
            kind=kind,
            model_cls=_PAYLOAD_MODELS[kind],
            page=page,
            cursor_digest=cursor_digest,
            context=context,
        )
        outcomes, accepted, seen = self._validate_and_map_records(page_ctx, records)
        accepted, duplicate_outcomes = self._drop_duplicate_records(
            page_ctx, accepted, seen
        )
        outcomes.extend(duplicate_outcomes)

        commit = self._commit_accepted_records(
            accepted, client=client, graph=graph, page_digest=page_digest
        )
        outcomes.extend(self._build_committed_outcomes(page_ctx, accepted, commit))

        outcomes.sort(key=lambda item: item.ordinal)
        if len(outcomes) != len(records):
            raise ConnectorCommitError

        checkpoint = self._advance_page_checkpoint(
            stream, page, cursor_digest, page_digest, outcomes
        )

        return PrepResult(
            record_kind=kind,
            stream=stream,
            page=page,
            page_digest=page_digest,
            plan=plan,
            outcomes=tuple(outcomes),
            checkpoint_advanced=True,
            checkpoint=checkpoint,
            commit=commit,
        )


__all__ = [
    "ARROW_IPC",
    "Checkpoint",
    "CheckpointConflict",
    "CheckpointOutcome",
    "CheckpointStore",
    "ConnectorCommitError",
    "ConnectorPrep",
    "DOMAIN",
    "ExistingNativeCommitter",
    "GitLabIssuePayload",
    "GitLabMergeRequestPayload",
    "GitLabProjectPayload",
    "MemoryCheckpointStore",
    "NativeCommitResult",
    "NativeCommitter",
    "PrepContext",
    "PrepDisposition",
    "PrepError",
    "PrepErrorCode",
    "PrepEvidence",
    "PrepLimits",
    "PrepResult",
    "PREP_CONTRACT_VERSION",
    "SOURCE",
    "arrow_prep_plan",
]
