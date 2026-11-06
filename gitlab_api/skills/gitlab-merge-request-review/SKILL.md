---
name: gitlab-merge-request-review
skill_type: skill
description: >-
  Review and merge GitLab merge requests via the gitlab-api MCP server — by default the MRs assigned to you or where you are a reviewer, optionally scoped to a project, group, or the whole instance. Read an MR, gate it on a green pipeline (pipeline → jobs → job log), then approve, accept/merge, or set merge-when-pipeline-succeeds (auto-merge) — writes are confirmed with the user and CI-gated. Use when the agent must review open MRs, verify CI, approve, merge, or set auto-merge. Do NOT use to open an MR (gitlab-merge-request-create), review issues (gitlab-issues), or review pipelines broadly (gitlab-pipelines).
license: MIT
tags: []
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Gitlab Merge Request Review

Typed gitlab_* tools take project_id (id or URL-encoded path) explicitly; resolve it before acting.

## Rules

- Resolve project_id (and the merge request or issue iid) before any call.
- Read first, then change, then read the object back.
- Delete, erase and merge-class tools need an explicit request; ask first.

## Task workflows

### review-a-merge-request

Read a merge request, its approvals, commits and discussions. Contract steps, in order:

1. `gitlab_get_approval_state_merge_requests`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
2. `gitlab_get_commit`(; optional project_id, commit_hash, branch, dry_run, message, state)
3. `gitlab_get_commit_comments`(; optional project_id, commit_hash, branch, dry_run, message, state)
4. `gitlab_get_commit_diff`(; optional project_id, commit_hash, branch, dry_run, message, state)
5. `gitlab_get_commit_discussions`(; optional project_id, commit_hash, branch, dry_run, message, state)
6. `gitlab_get_commit_gpg_signature`(; optional project_id, commit_hash, branch, dry_run, message, state)
7. `gitlab_get_commit_merge_requests`(; optional project_id, commit_hash, branch, dry_run, message, state)
8. `gitlab_get_commit_references`(; optional project_id, commit_hash, branch, dry_run, message, state)
9. `gitlab_get_commit_statuses`(; optional project_id, commit_hash, branch, dry_run, message, state)
10. `gitlab_get_commits`(; optional project_id, commit_hash, branch, dry_run, message, state)
11. `gitlab_get_group_merge_requests`(; optional group_id, name, path, auto_devops_enabled, avatar, default_branch)
12. `gitlab_get_merge_request_level_rules`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
13. `gitlab_get_merge_requests`(; optional approved_by_ids, approver_ids, assignee_id, author_id, author_username, created_after)
14. `gitlab_get_project_level_merge_request_rule`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
15. `gitlab_get_project_level_merge_request_rules`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
16. `gitlab_get_project_merge_request`(; optional approved_by_ids, approver_ids, assignee_id, author_id, author_username, created_after)
17. `gitlab_get_project_merge_requests`(; optional approved_by_ids, approver_ids, assignee_id, author_id, author_username, created_after)
18. `gitlab_merge_request_level_approvals`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)

### land-a-merge-request

Approve, merge or auto-merge a merge request and clean up branches. Contract steps, in order:

1. `gitlab_accept_merge_request`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
2. `gitlab_approve_merge_request`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
3. `gitlab_cancel_merge_when_pipeline_succeeds`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
4. `gitlab_delete_branch`(; optional project_id, branch, ref, max_pages, page, per_page) (destructive: pass confirm=true only after the person agrees)
5. `gitlab_delete_merged_branches`(; optional project_id, branch, ref, max_pages, page, per_page) (destructive: pass confirm=true only after the person agrees)
6. `gitlab_graphql_ops_delete_merge_request`(project_id, merge_request_iid; optional confirm) (destructive: pass confirm=true only after the person agrees)
7. `gitlab_graphql_ops_update_merge_request`(project_id, merge_request_iid; optional title, description, target_branch)
8. `gitlab_unapprove_merge_request`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)

### manage-approval-rules

Create, change and delete approval rules and code-owner approval. Contract steps, in order:

1. `gitlab_create_project_level_rule`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
2. `gitlab_delete_project_level_rule`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches) (destructive: pass confirm=true only after the person agrees)
3. `gitlab_edit_group_level_rule`(; optional project_id, group_id, allow_author_approval, allow_committer_approval, allow_overrides_to_approver_list_per_merge_request, retain_approvals_on_push)
4. `gitlab_edit_project_level_rule`(; optional project_id, group_id, allow_author_approval, allow_committer_approval, allow_overrides_to_approver_list_per_merge_request, retain_approvals_on_push)
5. `gitlab_get_group_level_rule`(; optional project_id, group_id, allow_author_approval, allow_committer_approval, allow_overrides_to_approver_list_per_merge_request, retain_approvals_on_push)
6. `gitlab_get_project_level_rule`(; optional project_id, group_id, allow_author_approval, allow_committer_approval, allow_overrides_to_approver_list_per_merge_request, retain_approvals_on_push)
7. `gitlab_require_code_owner_approvals_single_branch`(; optional project_id, branch, ref, max_pages, page, per_page)
8. `gitlab_update_project_level_rule`(; optional project_id, group_id, approval_rule_id, approvals_required, name, applies_to_all_protected_branches)
