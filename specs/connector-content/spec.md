# CONN-GITLAB-API-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: gitlab-api. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `gitlab-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Why a new spec

The specs of this repository were read; none owns this capability. This spec states it for this connector only.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - The connector serves its packaged content (Priority: P1)

The `gitlab-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-GITLAB-API-CONNECTOR-CONTENT-R001` (default content) is exercised, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.
2. **Given** the connector is configured, **When** the behaviour of row `CONN-GITLAB-API-CONNECTOR-CONTENT-R002` (ontology joins the parent graph) is exercised, **Then** the test parses each ontology and finds no orphan class beyond the pending list. Test: `tests/test_ontology_parent_link.py::test_ontology_joins_the_parent_graph`.
3. **Given** the connector is configured, **When** the behaviour of row `CONN-GITLAB-API-CONNECTOR-CONTENT-R004` (competency-question paths) is exercised, **Then** the test finds no shared-class declaration, the `state` domain on `Issue` and no null mapping. Test: `tests/test_cq_paths.py::test_shared_concepts_are_not_redeclared`.

### Edge Cases

- If `CONN-GITLAB-API-CONNECTOR-CONTENT-R001` is not met, its proving test fails: default content.
- If `CONN-GITLAB-API-CONNECTOR-CONTENT-R002` is not met, its proving test fails: ontology joins the parent graph.
- If `CONN-GITLAB-API-CONNECTOR-CONTENT-R004` is not met, its proving test fails: competency-question paths.

## Requirements

- **FR-001**: Default content. Rows: `CONN-GITLAB-API-CONNECTOR-CONTENT-R001`.
- **FR-002**: Ontology joins the parent graph. Rows: `CONN-GITLAB-API-CONNECTOR-CONTENT-R002`.
- **FR-003**: Competency-question paths. Rows: `CONN-GITLAB-API-CONNECTOR-CONTENT-R004`.
- **FR-004**: Owner and assignee edges. Rows: `CONN-GITLAB-API-CONNECTOR-CONTENT-R005`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-GITLAB-API-CONNECTOR-CONTENT-R001`.
- **SC-002**: The test parses each ontology and finds no orphan class beyond the pending list. Rows: `CONN-GITLAB-API-CONNECTOR-CONTENT-R002`.
- **SC-003**: The test finds no shared-class declaration, the `state` domain on `Issue` and no null mapping. Rows: `CONN-GITLAB-API-CONNECTOR-CONTENT-R004`.
- **SC-004**: `tests/test_catalog_edges.py::test_every_declared_edge_is_an_ontology_property_of_its_record_type` and `::test_project_and_issue_references_become_owner_and_assignee_edges`. Rows: `CONN-GITLAB-API-CONNECTOR-CONTENT-R005`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-GITLAB-API-CONNECTOR-CONTENT-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-GITLAB-API-CONNECTOR-CONTENT-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-003 | `CONN-GITLAB-API-CONNECTOR-CONTENT-R004` | [plan.md](plan.md) | T-003 | [test-spec.md](test-spec.md) |
| FR-004 | `CONN-GITLAB-API-CONNECTOR-CONTENT-R005` | [plan.md](plan.md) | T-004 | [test-spec.md](test-spec.md) |
