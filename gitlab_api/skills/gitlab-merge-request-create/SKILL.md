---
name: gitlab-merge-request-create
skill_type: skill
description: >-
  Open a new GitLab merge request against a project via the gitlab-api MCP server — from a source branch into a target branch, with title, description, assignees, reviewers, labels, and remove-source-branch/squash options. Use when the agent must create/open an MR for a project. Do NOT use to review, approve, or merge an existing MR (gitlab-merge-request-review), to triage issues (gitlab-issues), or to review pipelines (gitlab-pipelines).
license: MIT
tags: []
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Gitlab Merge Request Create

Typed gitlab_* tools take project_id (id or URL-encoded path) explicitly; resolve it before acting.

## Rules

- Resolve project_id (and the merge request or issue iid) before any call.
- Read first, then change, then read the object back.
- Delete, erase and merge-class tools need an explicit request; ask first.

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
