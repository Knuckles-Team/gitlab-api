---
name: gitlab-api-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the GitLab REST and GraphQL connector. Use
  this skill when changing API mappings, governed MCP tools, authentication,
  tenant selection, KG ingestion, packaged content, or repository gates.
license: MIT
tags: [gitlab, rest, graphql, mcp, development, connector, test, gates]
tier: repository
metadata:
  author: Genius
  version: '0.1.0'
---

# gitlab-api development

This repository owns the GitLab REST and GraphQL API facades, tenant and
authentication boundary, action-routed MCP tools, GitLab ontology and KG
ingestion mappings, and packaged connector content. Shared connector
contracts, transports, TLS profiles, and credential helpers belong to
`agent-connector-sdk`; admission, serving, and durable graph state belong to
their owning repositories. Read `AGENTS.md` before changing code and keep
credentials, private endpoints, tenant data, and customer records out of
source, logs, fixtures, and skill content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend the
  existing spec before adding requirement text.
- Reuse the single `Connector` in `gitlab_api/__init__.py`, the `Api` facade in
  `gitlab_api/api_client.py`, the modular clients under `gitlab_api/api/`, and
  the action dispatch tables in `gitlab_api/mcp_server.py`. Keep GraphQL
  operations in `gitlab_api/gitlab_gql.py`; do not create a second API, MCP,
  authentication, or transport plane.
- Preserve the multi-tenant resolution in `gitlab_api/instances.py`. A named
  instance, bare URL, or default selection must retain caller entitlement
  checks and the `GITLAB_INSTANCES` shared setting. The legacy
  `GITLAB_URL`/`GITLAB_TOKEN` fallback remains supported.
- Preserve `GITLAB_URL`, `GITLAB_TOKEN`, `GITLAB_TLS_PROFILE`, and
  `ENABLE_DELEGATION` handling in `gitlab_api/auth.py`. Delegated RFC 8693
  token exchange and fixed credentials stay behind the SDK identity/TLS
  helpers. Never print tokens or add a TLS verification bypass.
- Keep the REST resource paths, GraphQL typed-operation boundary, action names,
  pagination, and response models stable. Use `run_blocking` for blocking API
  calls from MCP tools and return typed refusal/error envelopes instead of
  bypassing the shared dispatcher. Keep `MCP_TOOL_MODE` (`condensed`,
  `verbose`, or `both`) and each action group's toggle behavior aligned with
  the generated tool surface.
- Preserve typed KG ingestion through `gitlab_api/kg_ingest.py`, source
  declarations in `gitlab_api/connector_sources.py`, and neutral ontology
  mappings. Project, issue, merge-request, pipeline, job, runner, group, and
  person records use the existing stable IDs and relationship names.
- Mock HTTP, GraphQL, and authentication responses in local tests; never call a
  live GitLab instance or use live credentials in a gate. Every delivered
  requirement needs a bound focused test. Generated `specs/*/status.json` files
  come from shared hooks; never hand-edit them.
- Keep `skills/**`, `ontology/**`, `connectors/**`, prompts, and
  `mcp_config.json` coherent with package data and the
  `agent_connector_sdk.connector` entry point (`gitlab-mcp =
  gitlab_api:connector`). Do not add a second publisher or runtime plane.

## Setup and gates

Use the pinned environment from `uv sync --locked`, then run the shared gates:

```bash
uv sync --locked
uvx pre-commit run --all-files
uvx pre-commit run --all-files --hook-stage pre-push
```

For focused feedback, run the smallest affected tests with the locked
environment, for example:

```bash
uv run --locked --extra test pytest -q tests/test_gitlab_api_development_skill.py
uv run --locked --extra test pytest -q tests/test_pages_workflow.py
uv run --locked --extra test pytest -q tests/test_auth.py tests/test_gitlab_mcp_validation.py
```

The canonical `.pre-commit-config.yaml` delegates connector-standard, secrets,
spec, tests-fast, and dependency-readiness to `Knuckles-Team/pipelines`. Do not
copy those hooks locally or bypass a failing check.

## Connector-specific checks

- Keep REST resource paths, GraphQL operation names, action selectors,
  pagination, and Pydantic response normalization stable. Add focused mocked
  request tests for a changed provider path.
- Keep OIDC token exchange and fixed-token fallback at the existing
  authentication boundary. Resolve TLS policy through the SDK and never bake
  static bearer tokens into the client.
- Preserve identity-scoped tenant discovery and refusal of an instance the
  caller is not entitled to use. Discovery returns names, URLs, and profile
  state only; it never returns tokens.
- Keep projects, issues, merge requests, pipelines, jobs, runners, groups, and
  people as the typed records already mapped by `gitlab_api/kg_ingest.py`.
  Ingestion stays best-effort when the graph engine is unavailable.
- Keep `gitlab_api/skills/`, `gitlab_api/ontology/`,
  `gitlab_api/connectors/`, prompts, and `gitlab_api/mcp_config.json` in package
  data. Keep source metadata tenant-neutral.
- Documentation is published by the existing Pages workflow and checked-in
  dashboard configuration; source status records under `specs/` are generated
  by shared hooks.

## Packaging and publication

`pyproject.toml` declares the `agent_connector_sdk.connector` entry point
`gitlab-mcp = "gitlab_api:connector"` and packages `skills/**`, `ontology/**`,
`connectors/**`, prompts, and `mcp_config.json`. When packaged content changes,
use `uv version --bump patch` and let the lockfile update with the project; add
the release note to `CHANGELOG.md`. Inspect `uv build` output for
`gitlab_api/skills/gitlab-api-development/SKILL.md`.

The canonical release caller delegates publication and connector rendering to
the shared pipelines. Do not commit generated Docker artifacts or claim
package, container, or Pages publication from a local build; require exact
source hosted evidence and the public artifact.

## Delivery discipline

Work in a real Git worktree based on `origin/main`. Inspect the complete diff,
stage only reviewed paths, and verify `git status --short` after every gate. Do
not use `git stash`, `git add -A`, or `git add .`; preserve unrelated working
tree changes. Keep runtime, ontology, status, and generated artifacts outside
this bounded skill slice unless the owning requirement explicitly requires
them.
