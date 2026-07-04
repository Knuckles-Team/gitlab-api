---
name: gitlab-pipelines
description: >-
  CI/CD pipeline operations on GitLab via the gitlab-api MCP server — list/read a
  project's pipelines and trigger a new pipeline run for a ref with the
  domain-typed tool. Use when the agent must check CI status for a branch/commit,
  fetch one pipeline by id, or kick off a pipeline on a ref. Do NOT use for merge
  requests (gitlab-merge-requests), issues (gitlab-issues), or repo/branch reads
  (gitlab-repositories); prefer those.
license: MIT
tags: [gitlab, pipelines, ci-cd, devops, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# GitLab Pipelines

Domain-typed access to GitLab **CI/CD Pipelines** for delivery status and triggering.

## When to use
- Check pipeline status for a project / ref (is `main` green?).
- Fetch a single pipeline by `pipeline_id` (status, duration, ref, sha).
- Trigger (`run`) a new pipeline on a branch or tag.

## When NOT to use
- Merge requests / reviews → `gitlab-merge-requests`.
- Issues, epics, milestones → `gitlab-issues`.
- Branch/commit/tag/project reads → `gitlab-repositories`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gitlab-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GITLAB_URL` | ✅ | GitLab instance base URL |
| `GITLAB_TOKEN` | ✅ | Access token with `api` scope (needed to `run`) |
| `GITLAB_SSL_VERIFY` | optional | TLS verification toggle |

Full env/tag matrix: the mcp-client reference
`agent-tools/mcp-client/references/gitlab-api.md`. `MCP_TOOL_MODE`
(`condensed`|`verbose`|`both`) selects the condensed vs. one-to-one verbose tools.

## Tools & actions
| Condensed tool | Actions |
|----------------|---------|
| `gitlab_pipelines` | `get`, `run` |

### Key parameters
- `project_id` — required (numeric id or `group/project` path).
- `pipeline_id` — required for `get` of a single pipeline.
- `ref` — branch/tag for `run`; `variables` — optional CI variables object.

## Recipes (`params_json`)
List recent pipelines for a ref, newest first:
```json
{"project_id":"platform/agent-utilities","ref":"main","order_by":"id","sort":"desc","per_page":10}
```
Get one pipeline by id:
```json
{"project_id":"platform/agent-utilities","pipeline_id":123456}
```
Trigger a pipeline on a branch with a variable:
```json
{"project_id":"platform/agent-utilities","ref":"main","variables":{"DEPLOY":"true"}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- `run` needs a token with `api` scope and pipeline-trigger permission on the project.
- A pipeline `status` of `success` doesn't imply all jobs ran — check the jobs surface
  for `manual`/`skipped` stages when gating a release.

## Related
- **Composed by:** the same review workflow as `gitlab-merge-requests`, to gate a
  merge on a green pipeline for the MR's head sha.
