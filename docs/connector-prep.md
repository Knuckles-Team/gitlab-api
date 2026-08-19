# Governed connector preparation

The GitLab connector's preparation contract is version `1`. It is the narrow
boundary between untrusted GitLab API pages and the existing native
`ApplyChangeEnvelope` ingestion path.

## Contract

`gitlab_api.connector_prep` exposes strict, immutable Pydantic projections for
three source record kinds:

- `GitLabProjectPayload`
- `GitLabIssuePayload`
- `GitLabMergeRequestPayload`

The models reject unknown fields, implicit type coercion, blank required text,
unsafe paths and URLs, non-timezone timestamps, oversized text, and secret
bearing fields or values. Existing permissive API response models remain
unchanged; this contract is intentionally a smaller projection selected for
materialization.

Preparation is declared as an Arrow IPC hand-off (`arrow_prep_plan`). The plan
records profiling, deterministic cleaning, strict validation, deduplication,
lineage mapping, and commit operations. The connector does not import pandas,
polars, or pyarrow and does not become a dataframe runtime. A future compatible
adapter can materialize the validated projection as Arrow IPC at the boundary.

## Evidence and lineage

Every terminal row result carries bounded `PrepEvidence` with:

- contract version, source kind, stable record reference, page and ordinal;
- opaque cursor and accepted-input SHA-256 digests;
- tenant, ACL, retention, classification, provenance, and source-instance
  references required by the GitLab governance shapes;
- validation and deterministic cleaning operation codes; and
- quarantine error codes/field paths with no validation messages or raw input.

Rejected payloads are never placed in evidence, exceptions, logs, or the
returned result. Secret-bearing rows use only the generic
`secret_bearing_payload` code. Raw payloads are not retained by the in-memory
fixture checkpoint store either.

## Native commit and replay

`ExistingNativeCommitter` is the only production adapter. It calls
`gitlab_api.kg_ingest.ingest_entities` once for the accepted graph slice. That
wrapper is the existing connector path into the engine-native
`ApplyChangeEnvelope`; this module does not open an engine transaction or copy
the envelope implementation. The optional `NativeCommitter` protocol is a
small compatibility seam for NE-110 and focused fixtures.

Node identifiers are deterministic:

```text
gitlab:project:<id>
gitlab:issue:<project_id>:<iid>
gitlab:mr:<project_id>:<iid>
```

Relationships use the existing ontology names (`partOfGroup` and
`belongsToProject`). The entire page digest is passed as the adapter's
idempotency key. The existing native path also derives content identity from
the complete deterministic graph slice, so a crash after the native commit but
before checkpoint persistence can be retried safely.

`CheckpointStore` is a CAS protocol. `MemoryCheckpointStore` exists only for
focused fixtures; production wiring must use a durable implementation. A page
is advanced only after all selected records are terminal and the single native
commit succeeds. A repeated page with the same digest returns `replayed` for
committed rows without invoking the committer. A changed digest, missing page,
or CAS version conflict fails closed. Oversized pages are returned as one
bounded page-level quarantine and are not advanced, so an operator can
redrive them after correcting pagination.

Malformed records are quarantined individually when within page bounds. All
duplicate stable IDs are quarantined (none is committed). Valid records in a
mixed page are still submitted in one atomic native call; a commit failure
leaves the checkpoint unchanged.

## Operational hand-off

The source fetcher should select only the declared fields, call
`ConnectorPrep.process_page`, persist the returned checkpoint through a durable
CAS implementation, and treat quarantine as an explicit terminal outcome.
Engine-side SHACL/ICV remains authoritative: the native path performs its
existing final validation before durable materialization. A shape violation or
engine failure is never acknowledged as a successful source checkpoint.
