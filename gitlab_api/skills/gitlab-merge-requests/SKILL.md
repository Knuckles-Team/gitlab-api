---
name: gitlab-merge-requests
description: >-
  Code-review operations on GitLab Merge Requests via the gitlab-api MCP server —
  list a project's MRs, read one by iid, and open a new merge request with the
  domain-typed tool. Use when the agent must review open MRs for a project, fetch
  one MR's state/approvals, or create an MR from a source to a target branch. Do
  NOT use for pipelines/jobs (gitlab-pipelines), issues/epics (gitlab-issues), or
  raw repo/branch/commit reads (gitlab-repositories); prefer those.
license: MIT
tags: [gitlab, merge-requests, code-review, devops, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# GitLab Merge Requests

Domain-typed access to GitLab **Merge Requests** for code review and change delivery.

## When to use
- List / review the open merge requests for a project.
- Fetch a single MR by its project `merge_request_iid` (state, approvals, pipeline).
- Create a new MR from a source branch into a target branch.

## When NOT to use
- Pipeline/job status for an MR → `gitlab-pipelines`.
- Issues, epics, or milestones → `gitlab-issues`.
- Branch/commit/tag/project reads → `gitlab-repositories`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gitlab-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GITLAB_URL` | ✅ | GitLab instance base URL |
| `GITLAB_TOKEN` | ✅ | Personal/project access token |
| `GITLAB_SSL_VERIFY` | optional | TLS verification toggle |

Full env/tag matrix (do not re-document here): the mcp-client reference
`agent-tools/mcp-client/references/gitlab-api.md`. `MCP_TOOL_MODE`
(`condensed`|`verbose`|`both`) selects the condensed surface (used below) vs. the
one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `gitlab_merge_requests` | `get_project`, `get`, `create` |

### Key parameters
- `project_id` — required for every action (numeric id or `group/project` path).
- `merge_request_iid` — required for `get` (the project-scoped `!iid`).
- `data` — object of field→value for `create` (`source_branch`, `target_branch`,
  `title`, `description`, `assignee_ids`, `reviewer_ids`, …).

## Recipes (`params_json`)
List a project's open merge requests:
```json
{"project_id":"platform/agent-utilities","state":"opened","order_by":"updated_at","per_page":25}
```
Get one merge request by iid:
```json
{"project_id":"platform/agent-utilities","merge_request_iid":42}
```
Open a merge request:
```json
{"data":{"source_branch":"feat/fleet-enrichment","target_branch":"main","title":"Fleet enrichment: gitlab ontology + skills","description":"Adds ontology + specialist skills.","remove_source_branch":true}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- Use `merge_request_iid` (the project `!iid`), not the global MR id.
- `project_id` accepts the URL-encoded `group/project` path or the numeric id.

## Related
- **Composed by:** a devops review workflow that pairs this with `gitlab-pipelines`
  to gate a merge on green CI.
