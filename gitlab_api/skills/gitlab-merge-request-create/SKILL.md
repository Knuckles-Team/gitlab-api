---
name: gitlab-merge-request-create
description: >-
  Open a new GitLab merge request against a project via the gitlab-api MCP server — from a
  source branch into a target branch, with title, description, assignees, reviewers, labels,
  and remove-source-branch/squash options. Use when the agent must create/open an MR for a
  project. Do NOT use to review, approve, or merge an existing MR (gitlab-merge-request-review),
  to triage issues (gitlab-issues), or to review pipelines (gitlab-pipelines).
license: MIT
tags: [gitlab, merge-requests, create, reviewers, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# GitLab Merge Request Create

Domain-typed creation of a GitLab **merge request** against a project via the gitlab-api MCP
server. This skill opens the MR; reviewing/approving/merging it is `gitlab-merge-request-review`.

## When to use
- Open an MR from a `source_branch` into a `target_branch` on a project.
- Set title/description, **assignees**, **reviewers**, labels, and merge options
  (`remove_source_branch`, `squash`) at creation time.

## When NOT to use
- Reviewing, approving, auto-merging, or merging an existing MR → `gitlab-merge-request-review`.
- Creating the source branch or committing files first → `gitlab-repositories`.
- Filing an issue → `gitlab-issues`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gitlab-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GITLAB_URL` | ✅ | GitLab instance base URL |
| `GITLAB_TOKEN` | ✅ | Access token with `api` scope (write) |
| `GITLAB_SSL_VERIFY` | optional | TLS verification toggle |

Full env/tag matrix: the mcp-client reference `agent-tools/mcp-client/references/gitlab-api.md`.
`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface (below).

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `gitlab_merge_requests` | `create` |

### Key parameters
- `project_id` — required (numeric id or `group/project` path).
- `data` — object of field→value: `source_branch`, `target_branch`, `title` (all required),
  plus optional `description`, `assignee_ids` (list), `reviewer_ids` (list), `labels`,
  `milestone_id`, `remove_source_branch` (bool), `squash` (bool),
  `target_project_id` (for cross-fork MRs).

## Recipes (`params_json`)
Open a merge request:
```json
{"project_id":"platform/agent-utilities","data":{"source_branch":"feat/fleet-enrichment","target_branch":"main","title":"Fleet enrichment: gitlab ontology + skills","description":"Adds ontology + specialist skills.","remove_source_branch":true}}
```
Open an MR with reviewers and assignees:
```json
{"project_id":"platform/agent-utilities","data":{"source_branch":"fix/runner-link","target_branch":"main","title":"Fix runner link","reviewer_ids":[12,34],"assignee_ids":[12],"labels":"bug","squash":true}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it, and note the MR fields
  go **inside** a nested `data` object.
- `assignee_ids`/`reviewer_ids` are numeric **user ids**, not usernames — resolve usernames to
  ids first (`gitlab_members get_project`).
- The source branch must exist and be ahead of the target, or GitLab rejects the MR.
- `labels` is a comma-separated string on write.

## Related
- **Next step:** review/approve/merge the MR with `gitlab-merge-request-review`.
- **KG mapping:** the new MR maps to a `:MergeRequest` node via `gitlab_api.kg_ingest`.
