# Gitlab Issues

Issue review and tracking on GitLab via the gitlab-api MCP server — review a project's issues, review issues across a whole group/organization, and read, create, update, or close an issue with the domain-typed tool. Use when the agent must triage a project's issues, see every issue affecting a group, open a new issue, update labels/assignee/state, or delete one. Do NOT use for merge requests (gitlab-merge-request-review / gitlab-merge-request-create), pipelines (gitlab-pipelines), or repo/branch reads (gitlab-repositories); prefer those.

# GitLab Issues

Domain-typed access to GitLab **Issues** for work-item review and triage — at **project** scope
and across a whole **group / organization**.

## When to use
- Review / triage the issues for a **project** (by state, label, milestone, assignee).
- Review issues affecting a whole **group / organization** (spans its subgroups).
- Fetch a single issue by `issue_iid`.
- Create, update (labels/assignee/state), or delete an issue.

## When NOT to use
- Merge requests / reviews → `gitlab-merge-request-review`.
- Pipeline/job status → `gitlab-pipelines`.
- Branch/commit/tag/project reads → `gitlab-repositories`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gitlab-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GITLAB_URL` | ✅ | GitLab instance base URL |
| `GITLAB_TOKEN` | ✅ | Access token with `api` scope for writes |
| `GITLAB_TLS_PROFILE` | optional | Runtime TLS profile selector; verification is mandatory |

Full env/tag matrix: the mcp-client reference `agent-tools/mcp-client/references/gitlab-api.md`.
`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed vs. one-to-one verbose tools.

## Tools & actions
| Condensed tool | Actions |
|----------------|---------|
| `gitlab_issues` | `get`, `get_group`, `create`, `update`, `delete` |

### Key parameters
- `project_id` — for project-scoped `get` (and required for `create`/`update`/`delete`); numeric
  id or `group/project` path.
- `group_id` — required for `get_group` (issues across the group and its subgroups).
- `issue_iid` — required for single `get`/`update`/`delete` (project-scoped `#iid`).
- `data` — field→value for `create`/`update` (`title`, `description`, `labels`, `assignee_ids`,
  `milestone_id`, `state_event`: `close`|`reopen`). Read filters: `state`, `labels`,
  `assignee_username`, `milestone`, `order_by`, `sort`.

## Recipes (`params_json`)
Review open `bug` issues for a project, newest first:
```json
{"project_id":"platform/agent-utilities","state":"opened","labels":"bug","order_by":"created_at","sort":"desc","per_page":25}
```
Review every open issue across a group / organization:
```json
{"group_id":"platform","state":"opened","per_page":50}
```
Create an issue:
```json
{"project_id":"platform/agent-utilities","data":{"title":"Fleet ontology: gitlab domain missing runners link","labels":"ontology,enhancement"}}
```
Close an issue:
```json
{"project_id":"platform/agent-utilities","issue_iid":17,"data":{"state_event":"close"}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- `get_group` needs `group_id` (not `project_id`) and returns issues from the group **and its
  subgroups** — filter with `state`/`labels`/`assignee_username` to keep it focused.
- Use `issue_iid` (project `#iid`), not the global issue id, for `get`/`update`/`delete`.
- `labels` is a comma-separated string on write, but returned as a list on read.

## Related
- Epics and milestones that aggregate issues are covered by their own tools (`gitlab_epics`,
  `gitlab_milestones`).
- **Siblings:** `gitlab-merge-request-review`, `gitlab-pipelines`.
