---
name: gitlab-issues
description: >-
  Issue-tracking operations on GitLab via the gitlab-api MCP server — read, create,
  update, and close issues for a project with the domain-typed tool. Use when the
  agent must triage a project's issues, open a new issue, update labels/assignee/
  state, or delete one. Do NOT use for merge requests (gitlab-merge-requests),
  pipelines (gitlab-pipelines), or repo/branch reads (gitlab-repositories); prefer
  those.
license: MIT
tags: [gitlab, issues, tracking, devops, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# GitLab Issues

Domain-typed access to GitLab **Issues** for work-item tracking and triage.

## When to use
- Read / triage a project's issues (by state, label, milestone).
- Fetch a single issue by `issue_iid`.
- Create, update (labels/assignee/state), or delete an issue.

## When NOT to use
- Merge requests / reviews → `gitlab-merge-requests`.
- Pipeline/job status → `gitlab-pipelines`.
- Branch/commit/tag/project reads → `gitlab-repositories`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gitlab-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GITLAB_URL` | ✅ | GitLab instance base URL |
| `GITLAB_TOKEN` | ✅ | Access token with `api` scope for writes |
| `GITLAB_SSL_VERIFY` | optional | TLS verification toggle |

Full env/tag matrix: the mcp-client reference
`agent-tools/mcp-client/references/gitlab-api.md`. `MCP_TOOL_MODE`
(`condensed`|`verbose`|`both`) selects the condensed vs. one-to-one verbose tools.

## Tools & actions
| Condensed tool | Actions |
|----------------|---------|
| `gitlab_issues` | `get`, `create`, `update`, `delete` |

### Key parameters
- `project_id` — required (numeric id or `group/project` path).
- `issue_iid` — required for `get`/`update`/`delete` (project-scoped `#iid`).
- `data` — field→value for `create`/`update` (`title`, `description`, `labels`,
  `assignee_ids`, `milestone_id`, `state_event`: `close`|`reopen`).

## Recipes (`params_json`)
List open issues with a label, newest first:
```json
{"project_id":"platform/agent-utilities","state":"opened","labels":"bug","order_by":"created_at","sort":"desc","per_page":25}
```
Create an issue:
```json
{"data":{"title":"Fleet ontology: gitlab domain missing runners link","labels":"ontology,enhancement","assignee_ids":[]}}
```
Close an issue:
```json
{"project_id":"platform/agent-utilities","issue_iid":17,"data":{"state_event":"close"}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- Use `issue_iid` (project `#iid`), not the global issue id, for `get`/`update`/`delete`.
- `labels` is a comma-separated string on write, but returned as a list on read.

## Related
- Epics and milestones that aggregate issues are covered by their own tools in the
  gitlab-api surface (`gitlab_epics`, `gitlab_milestones`).
