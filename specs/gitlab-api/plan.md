# CONN-GITLAB-API — Implementation plan

Governing spec: [spec.md](spec.md).
Component: Connector
Code: ../../gitlab_api/ontology/ingest_sources.json ../../tests/test_ingest_sources.py ../../gitlab_api/api/api_client_merge_requests.py

## Summary

The declaration file lists the `projects` and `issues` sources. The tool `gitlab_get_projects` is the operation tool of the client method `get_projects`. Rollup `R004` adds one tool per GitLab API operation that autonomous delivery needs, plus a webhook normalizer. Each tool is a public method of the `Api` class, so the SDK registers it as its own tool.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp, the GitLab REST client in `gitlab_api/api/`
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest with recorded GitLab replies; served tests through an in-process MCP client
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: one GitLab call per tool call; pages of 100 items at most
- **Constraints**: one tool per API operation; no merge without an owner approval reference
- **Scale/Scope**: 7 new operation tools, 4 reused tools and one normalizer

## Constitution Check

- One owner per concept: pass. The connector owns GitLab calls only; records come from the SDK and verdicts from the engine.
- Connectors depend on the SDK and are called through arbora: pass. Every tool is reached through `fleet.call`.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
gitlab_api/api/api_client_merge_requests.py   existing  discussion, pipeline, auto-merge, close and ready methods
gitlab_api/scm_records.py                     new       reply to record mappers
gitlab_api/scm_events.py                      new       webhook normalizer
tests/test_merge_request_tools.py             new       per-tool tests
tests/test_merge_request_served.py            new       served proof
```

## Phase 0: Research

No unknowns. Each operation maps to one documented GitLab endpoint.

## Phase 1: Design

The `Connector` declaration (`gitlab_api/__init__.py:9`) passes `Api` to the SDK. The SDK registers one tool per public method, named `gitlab_<method>`. A host syncs the sources through the SDK sync runner (SCION-SOURCE-INGEST-R004.21). Mappers in `gitlab_api/scm_records.py` turn replies into the SDK records; see [data-model.md](data-model.md). The auto-merge tool and the existing merge tool declare the owner-approval flag and refuse without an approval reference.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first. Mappers come before tools, and the served proof comes last.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: ruff check and format, `connector-standard`, `secrets`, `spec` and `tests-fast`. Each tool has one recorded-reply test.

## Production caller chain

1. Arbora `fleet.call` reaches the `gitlab-mcp` server over MCP.
2. The `Connector` declaration (`gitlab_api/__init__.py:9`) registered each operation tool.
3. The tool calls the `Api` method in `gitlab_api/api/`.
4. Arbora's SCM intake calls `GitlabEventNormalizer.normalize` for each webhook (row `CONN-GITLAB-API-R004.12`).

## Cross-repo seams

- The change-proposal records and the normalizer protocol come from the SDK. Rows: `CONN-GITLAB-API-R004.12`. Contract: [change-proposal-contract](contracts/change-proposal-contract.md).
- Arbora calls the tools and the normalizer for delivery. Rows: `CONN-GITLAB-API-R004.7`. Contract: [delivery-calls](contracts/delivery-calls.md).
- The engine owns the classes the records map to. Rows: `CONN-GITLAB-API-R004.13`. Contract: [delivery-classes](contracts/delivery-classes.md).
