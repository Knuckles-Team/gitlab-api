# CONN-GITLAB-API — GitLab ingestible sources

Owner: gitlab-api. Cross-repo IDs: SDK-SOURCE-INGEST-R004.19, SDK-SOURCE-INGEST-R004.21, ARBORA-OPS-R020.6.

## Purpose and user stories

An operator syncs GitLab records into the knowledge graph. The connector declares which records it can ingest and which read-only tool pages them.

## Requirements and acceptance

- FR-001: The connector declares the `projects` source in its ontology pack.
- SC-001: The packaged declaration validates, and its tool is a served read-only operation tool.

## Why a new spec

This repository had no local spec. The search `git grep -n ingest -- specs` found only the template. The SDK owns the declaration format and the runner. Arbora owns the served sync operations. This spec owns only the GitLab declaration.

## Scope and interfaces

The connector ships `gitlab_api/ontology/ingest_sources.json`. The SDK serves it as the read-only `gitlab_ingest_sources` tool. Non-goals: write operations, scheduling and storage.

## Traceability

| Requirement | Design section | Test ID | Evidence |
|---|---|---|---|
| FR-001 | [plan.md](plan.md) | `tests/test_ingest_sources.py` |  |

## Open questions

None.
