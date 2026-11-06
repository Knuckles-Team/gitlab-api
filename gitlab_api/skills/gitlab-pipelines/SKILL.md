---
name: gitlab-pipelines
skill_type: skill
description: >-
  CI/CD pipeline review on GitLab via the gitlab-api MCP server — review pipeline results for a project, a group, or the whole instance, drill into the CI jobs of a pipeline, and read a job's log; also trigger a pipeline on a ref. Use when the agent must review CI results across a project/group/organization, check whether a branch is green, inspect a pipeline's jobs, or read job logs. Do NOT use for merge-request review/merge (gitlab-merge-request-review), issues (gitlab-issues), or repo/branch reads (gitlab-repositories); prefer those.
license: MIT
tags: []
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Gitlab Pipelines

Typed gitlab_* tools take project_id (id or URL-encoded path) explicitly; resolve it before acting.

## Rules

- Resolve project_id (and the merge request or issue iid) before any call.
- Read first, then change, then read the object back.
- Delete, erase and merge-class tools need an explicit request; ask first.

## Task workflows

### review-ci-results

Read pipelines, jobs and job logs for a project. Contract steps, in order:

1. `gitlab_get_commit_statuses`(; optional project_id, commit_hash, branch, dry_run, message, state)
2. `gitlab_get_pipeline`(; optional project_id, total_pages, max_pages, per_page, page, status)
3. `gitlab_get_pipeline_jobs`(; optional project_id, pipeline_id, job_id, scope, total_pages, max_pages)
4. `gitlab_get_pipelines`(; optional project_id, total_pages, max_pages, per_page, page, status)
5. `gitlab_get_project_job`(; optional project_id, pipeline_id, job_id, scope, total_pages, max_pages)
6. `gitlab_get_project_job_log`(; optional project_id, pipeline_id, job_id, scope, total_pages, max_pages)
7. `gitlab_get_project_jobs`(; optional project_id, pipeline_id, job_id, scope, total_pages, max_pages)
8. `gitlab_graphql_ops_get_job`(project_id, job_id)
9. `gitlab_ingest_pipelines`(project_id; optional status, ref, per_page, include_jobs)

### run-ci

Run, retry, cancel and erase pipelines and jobs and post build status. Contract steps, in order:

1. `gitlab_cancel_project_job`(; optional project_id, pipeline_id, job_id, scope, total_pages, max_pages)
2. `gitlab_erase_project_job`(; optional project_id, pipeline_id, job_id, scope, total_pages, max_pages)
3. `gitlab_graphql_ops_cancel_pipeline`(project_id, pipeline_id)
4. `gitlab_graphql_ops_create_pipeline`(project_id, ref; optional variables)
5. `gitlab_graphql_ops_retry_pipeline`(project_id, pipeline_id)
6. `gitlab_post_build_status_to_commit`(; optional project_id, commit_hash, branch, dry_run, message, state)
7. `gitlab_retry_project_job`(; optional project_id, pipeline_id, job_id, scope, total_pages, max_pages)
8. `gitlab_run_pipeline`(; optional project_id, total_pages, max_pages, per_page, page, status)
9. `gitlab_run_project_job`(; optional project_id, pipeline_id, job_id, scope, total_pages, max_pages)

### manage-pipeline-schedules

Create, run, change and delete pipeline schedules and their variables. Contract steps, in order:

1. `gitlab_create_pipeline_schedule`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
2. `gitlab_create_pipeline_schedule_variable`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
3. `gitlab_delete_pipeline_schedule`(; optional project_id, max_pages, page, per_page, pipeline_schedule_id, confirm) (destructive: pass confirm=true only after the person agrees)
4. `gitlab_delete_pipeline_schedule_variable`(; optional project_id, max_pages, page, per_page, pipeline_schedule_id, key) (destructive: pass confirm=true only after the person agrees)
5. `gitlab_edit_pipeline_schedule`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
6. `gitlab_get_pipeline_schedule`(; optional project_id, max_pages, page, per_page, pipeline_schedule_id)
7. `gitlab_get_pipeline_schedules`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
8. `gitlab_get_pipelines_triggered_from_schedule`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
9. `gitlab_run_pipeline_schedule`(; optional project_id, max_pages, page, per_page, pipeline_schedule_id)
10. `gitlab_take_pipeline_schedule_ownership`(; optional project_id, max_pages, page, per_page, pipeline_schedule_id)
