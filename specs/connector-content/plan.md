# CONN-GITLAB-API-CONNECTOR-CONTENT — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

`pyproject.toml` declares `gitlab-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `gitlab_api` from it.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest; the proof level each row names
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; shared capabilities come from the SDK
- **Scale/Scope**: 4 rows

## Constitution Check

- One owner per concept: pass. The connector owns one external system's calls, mappings and tools only.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
pyproject.toml  existing
tests/test_ontology_parent_link.py  existing
gitlab_api/ontology/gitlab.ttl  existing
tests/test_cq_paths.py  existing
```

## Phase 0: Research

No unknowns. Each row names the code it touches.

## Phase 1: Design

The rows are delivered in place; the design is the caller chain below.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `tests-fast`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

1. `CONN-GITLAB-API-CONNECTOR-CONTENT-R001`: the `gitlab-mcp` console script (`scion_sdk.cli:serve`) loads the `scion_sdk.connector` entry point `gitlab_api:connector` (`gitlab_api/__init__.py:9`), which the SDK `build_server` turns into the served MCP server and its resources and prompts.
2. `CONN-GITLAB-API-CONNECTOR-CONTENT-R002`: the `gitlab-mcp` console script (`scion_sdk.cli:serve`) loads `gitlab_api:connector` (`gitlab_api/__init__.py:9`) whose packaged `gitlab_api/ontology/gitlab.ttl` is served as the `ontology://` resource and ingested into medulla.
3. `CONN-GITLAB-API-CONNECTOR-CONTENT-R004`: `gitlab_api:connector` (`gitlab_api/__init__.py:9`) serves `gitlab_api/ontology/gitlab.ttl` and the `SCHEMA_MAPPINGS` of `gitlab_api/connector_sources.py:107`, which medulla uses to answer competency-question paths.
4. `CONN-GITLAB-API-CONNECTOR-CONTENT-R005`: `gitlab_api:connector` (`gitlab_api/__init__.py:9`) serves `SOURCES` in `gitlab_api/connector_sources.py:11` whose `edges` lists (lines 27 and 66) are turned into owner, author and assignee edges by SDK ingest.

## Cross-repo seams

none. The cited owner rows are library capabilities the connector calls in process; spec.md names them.
