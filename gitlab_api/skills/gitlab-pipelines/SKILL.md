---
name: gitlab-pipelines
skill_type: skill
description: >-
  CI/CD pipeline review on GitLab via the gitlab-api MCP server — review pipeline results for a
  project, a group, or the whole instance, drill into the CI jobs of a pipeline, and read a
  job's log; also trigger a pipeline on a ref. Use when the agent must review CI results across
  a project/group/organization, check whether a branch is green, inspect a pipeline's jobs, or
  read job logs. Do NOT use for merge-request review/merge (gitlab-merge-request-review), issues
  (gitlab-issues), or repo/branch reads (gitlab-repositories); prefer those.
license: MIT
tags: [gitlab, pipelines, ci-cd, jobs, logs, group, mcp]
metadata:
  author: Genius
  version: '0.2.0'
---
# GitLab Pipelines

Domain-typed review of GitLab **CI/CD Pipelines** — pipeline results at **project**, **group**,
or **instance** scope, the **jobs** within a pipeline, and per-job **logs**. Also triggers a
pipeline on a ref.

## When to use
- Review pipeline results for a **project** / ref (is `main` green?).
- Review CI results across a **group / organization** (enumerate projects, then their pipelines).
- Fetch a single pipeline by `pipeline_id`, list its **jobs**, and read a **job log**.
- Trigger (`run`) a new pipeline on a branch or tag.

## When NOT to use
- Gating one MR's merge on its pipeline → `gitlab-merge-request-review` (it reads the MR's
  pipeline/jobs/logs directly).
- Issues, epics, milestones → `gitlab-issues`.
- Branch/commit/tag/project reads → `gitlab-repositories`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gitlab-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GITLAB_URL` | ✅ | GitLab instance base URL |
| `GITLAB_TOKEN` | ✅ | Access token with `api` scope (needed to `run`) |
| `GITLAB_SSL_VERIFY` | optional | TLS verification toggle |

Full env/tag matrix: the mcp-client reference `agent-tools/mcp-client/references/gitlab-api.md`.
`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed vs. one-to-one verbose tools.

## Tools & actions
| Condensed tool | Actions |
|----------------|---------|
| `gitlab_groups` | `get_projects` (enumerate a group's projects) |
| `gitlab_pipelines` | `get`, `run` |
| `gitlab_jobs` | `get_pipeline_jobs`, `get_project_jobs`, `get_log`, `retry`, `cancel` |

### Key parameters
- Scope — **project**: `gitlab_pipelines get` with `project_id`. **group/org**: `gitlab_groups
  get_projects` (`group_id`) then `gitlab_pipelines get` per project. **instance**: iterate the
  projects you care about.
- `gitlab_pipelines get`: `project_id` (required); `pipeline_id` for a single pipeline; filters
  `ref`, `status`, `order_by`, `sort`, `per_page`.
- `gitlab_jobs get_pipeline_jobs`: `project_id` + `pipeline_id` — the jobs of one pipeline.
- `gitlab_jobs get_log`: `project_id` + `job_id` — the job trace/log.
- `gitlab_pipelines run`: `project_id` + `ref`; optional `variables` object.

## Recipes (`params_json`)
Review recent pipelines for a ref, newest first:
```json
{"project_id":"platform/agent-utilities","ref":"main","order_by":"id","sort":"desc","per_page":10}
```
Enumerate a group's projects to sweep CI across the org:
```json
{"group_id":"platform","per_page":100}
```
Failed pipelines for a project:
```json
{"project_id":"platform/agent-utilities","status":"failed","per_page":20}
```
Jobs of a pipeline:
```json
{"project_id":"platform/agent-utilities","pipeline_id":123456}
```
Read a job's log:
```json
{"project_id":"platform/agent-utilities","job_id":554433}
```
Trigger a pipeline on a branch with a variable:
```json
{"project_id":"platform/agent-utilities","ref":"main","variables":{"DEPLOY":"true"}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- A group/instance sweep fans out one `gitlab_pipelines get` per project — there is no single
  group-wide pipelines endpoint; cap `per_page` and filter by `status=failed`.
- A pipeline `status=success` doesn't imply all jobs ran — check the jobs for `manual`/`skipped`
  stages when gating a release.
- `run` needs a token with `api` scope and pipeline-trigger permission on the project.
- `get_log` returns the full job trace — pull one failing job at a time.

## Related
- **Per-MR CI gating:** `gitlab-merge-request-review`.
- **KG mapping:** pipelines relate to `:Project` nodes via `gitlab_api.kg_ingest`.
