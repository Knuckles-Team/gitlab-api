# CONN-GITLAB-API — GitLab ingestible sources and merge-request delivery

Owner: gitlab-api. Cross-repo IDs: SCION-SOURCE-INGEST-R004.19, SCION-SOURCE-INGEST-R004.21, ARBORA-OPS-R020.6.
Component: Connector

An operator syncs GitLab records into the knowledge graph. The connector declares which records it can ingest and which read-only tool pages them. It also serves one tool per GitLab API operation that autonomous delivery of a change proposal needs.

## User Scenarios & Testing

### User Story 1 - Ingestible sources (Priority: P1)

An operator syncs GitLab projects and issues into the knowledge graph through declared read-only tools.

**Acceptance Scenarios**:

1. **Given** the packaged declaration, **When** the SDK loads it, **Then** each source names a mapped record type and a read-only operation tool.

### User Story 2 - Merge-request delivery tools (Priority: P1)

The platform delivers a spec row as a merge request on its own. It reads discussions, pipelines and approvals, answers review feedback and asks to set auto-merge. Each step uses one tool per GitLab API operation.

**Acceptance Scenarios**:

1. **Given** an open merge request, **When** arbora calls the discussion, pipeline and approval tools, **Then** each reply maps to one typed change-proposal record.
2. **Given** an auto-merge request without an owner approval reference, **When** the tool runs, **Then** it refuses and arms nothing.
3. **Given** a webhook with a valid token, **When** arbora passes it to the normalizer, **Then** one feedback event of one closed kind results.

### Edge Cases

- An auto-merge request with a stale `sha` refuses with `head_mismatch`.
- A resolve call on a resolved discussion writes nothing new.
- A webhook of an unsupported event refuses with `SCM_EVENT_UNSUPPORTED`.

## Requirements

- **FR-001**: The connector declares the `projects` and `issues` sources in its ontology pack. Rows: `CONN-GITLAB-API-R001`.
- **FR-002**: The connector is filed under its fleet name and uses the shared GraphQL client. Rows: `CONN-GITLAB-API-R002`, `CONN-GITLAB-API-R003`.
- **FR-003**: The connector serves one tool per merge-request operation and a webhook normalizer. Rows: `CONN-GITLAB-API-R004`.

## Success Criteria

- **SC-001**: The packaged declaration validates, and its tool is a served read-only operation tool. Rows: `CONN-GITLAB-API-R001`.
- **SC-002**: Each of the eleven merge-request operations has exactly one served tool. Rows: `CONN-GITLAB-API-R004.14`.
- **SC-003**: Both merge tools refuse in 100% of calls without an approval reference. Rows: `CONN-GITLAB-API-R004.7`.

## Assumptions

- The SDK provides the change-proposal records, the normalizer protocol and the approval flag of `SCION-SCM`.
- Arbora owns the webhook route, the admission of feedback and the approval receipt.
- The engine owns the delivery records and every merge verdict.

## Why a new spec

This spec is not new. The search `git grep -n -iE "merge request|discussion|pipeline" -- specs` found this spec and the content spec. This spec owns the connector's served GitLab operations. The merge-request tools extend it as rollup `R004`.

## Scope and interfaces

The connector ships `gitlab_api/ontology/ingest_sources.json` and the merge-request operation tools. Non-goals: the webhook route and admission (arbora), merge verdicts (the engine), scheduling and storage.

## Traceability

| Label | Rows | Design section | Test |
|---|---|---|---|
| FR-001 | `CONN-GITLAB-API-R001` | [plan.md](plan.md) | `tests/test_ingest_sources.py::test_declares_ingestible_sources` |
| FR-003 | `CONN-GITLAB-API-R004` | [plan.md](plan.md) | `tests/test_merge_request_served.py::test_served_tools_and_normalizer_round_trip` |
