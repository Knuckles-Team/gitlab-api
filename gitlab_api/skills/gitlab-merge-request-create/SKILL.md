---
name: gitlab-merge-request-create
skill_type: skill
description: >-
  Open a new GitLab merge request against a project via the gitlab-api MCP server — from a source branch into a target branch, with title, description, assignees, reviewers, labels, and remove-source-branch/squash options. Use when the agent must create/open an MR for a project.
license: MIT
tags: []
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Gitlab Merge Request Create

Scope: Open a new GitLab merge request against a project via the gitlab-api MCP server — from a source branch into a target branch, with title, description, assignees, reviewers, labels, and remove-source-branch/squash options. Use when the agent must create/open an MR for a project. Do NOT use to review, approve, or merge an existing MR (gitlab-merge-request-review), to triage issues (gitlab-issues), or to review pipelines (gitlab-pipelines).

Typed gitlab_* tools take project_id (id or URL-encoded path) explicitly; resolve it before acting.

## Rules

- Resolve project_id (and the merge request or issue iid) before any call.
- Read first, then change, then read the object back.
- Delete, erase and merge-class tools need an explicit request; ask first.

## Steps

1. Resolve the project with `gitlab_get_project`(project_id). Verify the id matches the intended repository.
2. Confirm the source branch exists with `gitlab_get_branch`(project_id, branch), or create it with `gitlab_create_branch`(project_id, branch, ref). Verify the branch is returned.
3. Commit changes if needed with `gitlab_create_commit`(project_id, branch, message). Verify the commit hash is returned.
4. Open the request with `gitlab_create_merge_request`(project_id, source_branch, target_branch, title). Verify the response includes an iid and a web URL.
5. Read it back with `gitlab_get_project_merge_request`(project_id). Verify source, target, and title match.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Branch not found | Source branch was not pushed or the name is wrong | List names with `gitlab_get_branches`(project_id) and use the exact one |
| Merge request already exists | An open request for the same branches | Read it with `gitlab_get_project_merge_requests` and update it instead |
| No difference between branches | Nothing committed on the source branch | Create the commit with `gitlab_create_commit` before opening the request |

## Task workflows

### create-a-merge-request

Branch, commit and open a merge request. Contract steps, in order:

1. `gitlab_cherry_pick_commit`(; optional project_id, commit_hash, branch, dry_run, message, state)
2. `gitlab_create_branch`(; optional project_id, branch, ref, max_pages, page, per_page)
3. `gitlab_create_commit`(; optional project_id, commit_hash, branch, dry_run, message, state)
4. `gitlab_create_merge_request`(; optional approved_by_ids, approver_ids, assignee_id, author_id, author_username, created_after)
5. `gitlab_get_branch`(; optional project_id, branch, ref, max_pages, page, per_page)
6. `gitlab_get_branches`(; optional project_id, branch, ref, max_pages, page, per_page)
7. `gitlab_revert_commit`(; optional project_id, commit_hash, branch, dry_run, message, state)
