---
name: gitlab-merge-request-review
skill_type: skill
description: >-
  Review and merge GitLab merge requests via the gitlab-api MCP server — by default the MRs
  assigned to you or where you are a reviewer, optionally scoped to a project, group, or the
  whole instance. Read an MR, gate it on a green pipeline (pipeline → jobs → job log), then
  approve, accept/merge, or set merge-when-pipeline-succeeds (auto-merge) — writes are confirmed
  with the user and CI-gated. Use when the agent must review open MRs, verify CI, approve, merge,
  or set auto-merge. Do NOT use to open an MR (gitlab-merge-request-create), review issues
  (gitlab-issues), or review pipelines broadly (gitlab-pipelines).
license: MIT
tags: [gitlab, merge-requests, code-review, approve, merge, auto-merge, ci, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# GitLab Merge Request Review

Domain-typed review-to-merge for GitLab **Merge Requests** via the gitlab-api MCP server.
Default focus: the MRs that are *yours to act on* (assigned to you or awaiting your review);
widen to a project, group, or the whole instance on request.

## When to use
- Review the MRs assigned to you or where you are a reviewer (the default).
- Scope MR review to a **project**, a **group**, or the **instance**.
- Read an MR and gate a merge on a green pipeline — pipeline → jobs → job log.
- **Approve**, **accept (merge)**, or set **merge-when-pipeline-succeeds** (auto-merge); cancel
  a queued auto-merge.

## When NOT to use
- Opening a new MR → `gitlab-merge-request-create`.
- Issue triage → `gitlab-issues`.
- Broad pipeline/CI review across a group/instance → `gitlab-pipelines`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gitlab-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GITLAB_URL` | ✅ | GitLab instance base URL |
| `GITLAB_TOKEN` | ✅ | Access token with `api` scope (approve/merge need write) |
| `GITLAB_SSL_VERIFY` | optional | TLS verification toggle |

Full env/tag matrix: the mcp-client reference `agent-tools/mcp-client/references/gitlab-api.md`.
`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface (below).

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `gitlab_merge_requests` | `get`, `get_project`, `accept`, `cancel_auto_merge` |
| `gitlab_merge_rules` | `get_mr_approvals`, `get_mr_approval_state`, `approve_mr`, `unapprove_mr` |
| `gitlab_groups` | `get_merge_requests` (group-scoped MRs) |
| `gitlab_pipelines` | `get` |
| `gitlab_jobs` | `get_pipeline_jobs`, `get_log` |

### Key parameters
- Default scope — instance-wide `gitlab_merge_requests get` with either `scope=assigned_to_me`
  or `reviewer_username=<me>` (run both and union). Project scope → `get_project` with
  `project_id`; group scope → `gitlab_groups get_merge_requests` with `group_id`.
- Single MR → `gitlab_merge_requests get` with `project_id` + `merge_request_iid`.
- CI gate — the MR object carries `pipeline`/`head_pipeline`; feed its id to `gitlab_pipelines
  get` (`pipeline_id`), then `gitlab_jobs get_pipeline_jobs` (`pipeline_id`), then `get_log`
  (`job_id`).
- Approve/merge — `gitlab_merge_rules approve_mr` (project_id + merge_request_iid);
  `gitlab_merge_requests accept` merges now, or pass `merge_when_pipeline_succeeds=true` to set
  auto-merge; `cancel_auto_merge` cancels a queued auto-merge.

## Recipes (`params_json`)
Default — MRs assigned to you, newest first:
```json
{"scope":"assigned_to_me","state":"opened","order_by":"updated_at","sort":"desc","per_page":25}
```
MRs where you are the reviewer:
```json
{"reviewer_username":"me","state":"opened"}
```
Open MRs for a group:
```json
{"group_id":"platform","state":"opened"}
```
One MR by iid:
```json
{"project_id":"platform/agent-utilities","merge_request_iid":42}
```
Gate on CI — jobs of the MR's pipeline, then a failing job's log:
```json
{"project_id":"platform/agent-utilities","pipeline_id":998877}
```
```json
{"project_id":"platform/agent-utilities","job_id":554433}
```
Approve the MR:
```json
{"project_id":"platform/agent-utilities","merge_request_iid":42}
```
Set auto-merge (merge when the pipeline succeeds):
```json
{"project_id":"platform/agent-utilities","merge_request_iid":42,"merge_when_pipeline_succeeds":true,"squash":true}
```
Merge now:
```json
{"project_id":"platform/agent-utilities","merge_request_iid":42,"should_remove_source_branch":true}
```

## Guarded write actions
`approve_mr`, `accept`, and `cancel_auto_merge` mutate the MR. Before calling any of them:
1. **Confirm CI is green** — the MR's pipeline `status=success` and no required job log shows a
   failure. Recommend `accept` (immediate merge) only when the pipeline has passed; otherwise
   prefer `merge_when_pipeline_succeeds=true`.
2. **Present the exact action to the user** — project, MR `!iid`/title, and the operation
   (approve / auto-merge / immediate merge) — and get explicit confirmation.
3. Only then call the tool.

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- Use `merge_request_iid` (the project `!iid`), not the global MR id.
- `project_id` accepts the URL-encoded `group/project` path or the numeric id.
- A pipeline `status=success` doesn't mean every job ran — check for `manual`/`skipped` stages
  before merging on a release branch.
- `accept` fails if the MR isn't mergeable (conflicts, unmet approvals, or a running pipeline
  when the project requires green CI) — read `merge_status`/approval state first.

## Related
- **Open an MR:** `gitlab-merge-request-create`.
- **KG mapping:** MRs map to `:MergeRequest` nodes via `gitlab_api.kg_ingest`.
