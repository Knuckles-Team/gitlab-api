---
name: gitlab-api-operations
skill_type: skill
description: >-
  Operate gitlab-api through its governed MCP and Arbora capabilities, including gitlab issues, gitlab merge request create, gitlab merge request review, gitlab pipelines, gitlab vulnerabilities. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
license: MIT
tags: []
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Gitlab Api Operations

Typed gitlab_* tools take project_id (id or URL-encoded path) explicitly; resolve it before acting.

## Rules

- Resolve project_id (and the merge request or issue iid) before any call.
- Read first, then change, then read the object back.
- Delete, erase and merge-class tools need an explicit request; ask first.

## Task workflows

### find-projects-and-groups

Find projects and groups and read their details, members and statistics. Contract steps, in order:

1. `gitlab_api_request`(method, endpoint; optional data, json)
2. `gitlab_discover_graphql_schema`(; optional type_name)
3. `gitlab_get_group`(; optional group_id, name, path, auto_devops_enabled, avatar, default_branch)
4. `gitlab_get_group_descendant_groups`(; optional group_id, name, path, auto_devops_enabled, avatar, default_branch)
5. `gitlab_get_group_members`(; optional group_id, project_id, per_page, page)
6. `gitlab_get_group_projects`(; optional group_id, name, path, auto_devops_enabled, avatar, default_branch)
7. `gitlab_get_group_subgroups`(; optional group_id, name, path, auto_devops_enabled, avatar, default_branch)
8. `gitlab_get_groups`(; optional group_id, name, path, auto_devops_enabled, avatar, default_branch)
9. `gitlab_get_namespace`(; optional namespace_id, search, owned_only, top_level_only, max_pages, data)
10. `gitlab_get_namespaces`(; optional namespace_id, search, owned_only, top_level_only, max_pages, data)
11. `gitlab_get_nested_projects_by_group`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
12. `gitlab_get_project`(; optional project_id, max_pages, page, per_page)
13. `gitlab_get_project_contributors`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
14. `gitlab_get_project_dependencies`(; optional project_id, group_id, vulnerability_id, package_manager, max_pages, per_page)
15. `gitlab_get_project_groups`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
16. `gitlab_get_project_members`(; optional group_id, project_id, per_page, page)
17. `gitlab_get_project_statistics`(; optional project_id, max_pages, page, per_page)
18. `gitlab_get_projects`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
19. `gitlab_graphql`(query; optional variables, operation_name)
20. `gitlab_instances_get`(name)
21. `gitlab_instances_list`(no arguments)

### provision-a-project

Create or change a project or group and share it. Contract steps, in order:

1. `gitlab_archive_project`(; optional project_id, max_pages, page, per_page)
2. `gitlab_create_project`(; optional name, path, namespace_id, visibility, description, initialize_with_readme)
3. `gitlab_delete_shared_project_link`(; optional project_id, group_id, max_pages, page, per_page, confirm) (destructive: pass confirm=true only after the person agrees)
4. `gitlab_edit_group`(; optional group_id, name, path, auto_devops_enabled, avatar, default_branch)
5. `gitlab_edit_project`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
6. `gitlab_share_project`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
7. `gitlab_unarchive_project`(; optional project_id, max_pages, page, per_page)

### manage-environments

Create, protect, stop and delete environments. Contract steps, in order:

1. `gitlab_create_environment`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
2. `gitlab_delete_environment`(; optional project_id, max_pages, page, per_page, environment_id, confirm) (destructive: pass confirm=true only after the person agrees)
3. `gitlab_delete_stopped_environments`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge) (destructive: pass confirm=true only after the person agrees)
4. `gitlab_get_environment`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
5. `gitlab_get_environments`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
6. `gitlab_get_protected_environment`(; optional project_id, max_pages, page, per_page, name)
7. `gitlab_get_protected_environments`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
8. `gitlab_protect_environment`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
9. `gitlab_stop_environment`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
10. `gitlab_stop_stale_environments`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
11. `gitlab_unprotect_environment`(; optional project_id, max_pages, page, per_page, name, confirm) (destructive: pass confirm=true only after the person agrees)
12. `gitlab_update_environment`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
13. `gitlab_update_protected_environment`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)

### manage-runners

Register, enable, pause, reset and delete runners. Contract steps, in order:

1. `gitlab_delete_project_runner`(; optional runner_id, description, active, paused, tag_list, run_untagged) (destructive: pass confirm=true only after the person agrees)
2. `gitlab_delete_runner`(; optional runner_id, description, active, paused, tag_list, run_untagged) (destructive: pass confirm=true only after the person agrees)
3. `gitlab_enable_project_runner`(; optional runner_id, description, active, paused, tag_list, run_untagged)
4. `gitlab_get_group_runners`(; optional runner_id, description, active, paused, tag_list, run_untagged)
5. `gitlab_get_project_runners`(; optional runner_id, description, active, paused, tag_list, run_untagged)
6. `gitlab_get_runner`(; optional runner_id, description, active, paused, tag_list, run_untagged)
7. `gitlab_get_runner_jobs`(; optional runner_id, description, active, paused, tag_list, run_untagged)
8. `gitlab_get_runners`(; optional runner_id, description, active, paused, tag_list, run_untagged)
9. `gitlab_pause_runner`(; optional runner_id, description, active, paused, tag_list, run_untagged)
10. `gitlab_register_new_runner`(; optional runner_id, description, active, paused, tag_list, run_untagged)
11. `gitlab_reset_gitlab_runner_token`(no arguments)
12. `gitlab_reset_group_runner_token`(; optional runner_id, description, active, paused, tag_list, run_untagged)
13. `gitlab_reset_project_runner_token`(; optional runner_id, description, active, paused, tag_list, run_untagged)
14. `gitlab_reset_token`(; optional runner_id, description, active, paused, tag_list, run_untagged)
15. `gitlab_update_runner_details`(; optional runner_id, description, active, paused, tag_list, run_untagged)
16. `gitlab_verify_runner_authentication`(; optional runner_id, description, active, paused, tag_list, run_untagged)

### manage-protection

Protect and unprotect branches and tags. Contract steps, in order:

1. `gitlab_create_tag`(; optional project_id, tag, ref, message, max_pages, page)
2. `gitlab_delete_tag`(; optional project_id, tag, ref, message, max_pages, page) (destructive: pass confirm=true only after the person agrees)
3. `gitlab_get_protected_branch`(; optional project_id, branch, ref, max_pages, page, per_page)
4. `gitlab_get_protected_branches`(; optional project_id, branch, ref, max_pages, page, per_page)
5. `gitlab_get_protected_tag`(; optional project_id, tag, ref, message, max_pages, page)
6. `gitlab_get_protected_tags`(; optional project_id, tag, ref, message, max_pages, page)
7. `gitlab_get_tag`(; optional project_id, tag, ref, message, max_pages, page)
8. `gitlab_get_tags`(; optional project_id, tag, ref, message, max_pages, page)
9. `gitlab_protect_branch`(; optional project_id, branch, ref, max_pages, page, per_page)
10. `gitlab_protect_tag`(; optional project_id, tag, ref, message, max_pages, page)
11. `gitlab_unprotect_branch`(; optional project_id, branch, ref, max_pages, page, per_page) (destructive: pass confirm=true only after the person agrees)
12. `gitlab_unprotect_tag`(; optional project_id, tag, ref, message, max_pages, page) (destructive: pass confirm=true only after the person agrees)

### publish-a-release

Create, read, change and delete releases and their assets and packages. Contract steps, in order:

1. `gitlab_create_release`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
2. `gitlab_create_release_evidence`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
3. `gitlab_delete_release`(; optional project_id, group_id, order_by, sort, simple, include_html_description) (destructive: pass confirm=true only after the person agrees)
4. `gitlab_download_release_asset`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
5. `gitlab_download_repository_package`(; optional project_id, group_id, package_id, package_type, package_name, package_version)
6. `gitlab_get_group_releases`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
7. `gitlab_get_latest_release`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
8. `gitlab_get_latest_release_asset`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
9. `gitlab_get_latest_release_evidence`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
10. `gitlab_get_release_by_tag`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
11. `gitlab_get_releases`(; optional project_id, group_id, order_by, sort, simple, include_html_description)
12. `gitlab_get_repository_packages`(; optional project_id, group_id, package_id, package_type, package_name, package_version)
13. `gitlab_publish_repository_package`(; optional project_id, group_id, package_id, package_type, package_name, package_version)
14. `gitlab_update_release`(; optional project_id, group_id, order_by, sort, simple, include_html_description)

### manage-deploy-tokens

Create, read and delete deploy tokens. Contract steps, in order:

1. `gitlab_create_group_deploy_token`(; optional project_id, group_id, token, name, expires_at, username)
2. `gitlab_create_project_deploy_token`(; optional project_id, group_id, token, name, expires_at, username)
3. `gitlab_delete_group_deploy_token`(; optional project_id, group_id, token, name, expires_at, username) (destructive: pass confirm=true only after the person agrees)
4. `gitlab_delete_project_deploy_token`(; optional project_id, group_id, token, name, expires_at, username) (destructive: pass confirm=true only after the person agrees)
5. `gitlab_get_deploy_tokens`(; optional project_id, group_id, token, name, expires_at, username)
6. `gitlab_get_group_deploy_token`(; optional project_id, group_id, token, name, expires_at, username)
7. `gitlab_get_group_deploy_tokens`(; optional project_id, group_id, token, name, expires_at, username)
8. `gitlab_get_project_deploy_token`(; optional project_id, group_id, token, name, expires_at, username)
9. `gitlab_get_project_deploy_tokens`(; optional project_id, group_id, token, name, expires_at, username)

### manage-wikis-and-snippets

Read and edit wiki pages and snippets. Contract steps, in order:

1. `gitlab_create_snippet`(; optional project_id, snippet_id, title, file_name, content, visibility)
2. `gitlab_create_wiki_page`(; optional project_id, slug, content, title, format_type, with_content)
3. `gitlab_delete_snippet`(; optional project_id, snippet_id, title, file_name, content, visibility) (destructive: pass confirm=true only after the person agrees)
4. `gitlab_delete_wiki_page`(; optional project_id, slug, content, title, format_type, with_content) (destructive: pass confirm=true only after the person agrees)
5. `gitlab_get_snippet`(; optional project_id, snippet_id, title, file_name, content, visibility)
6. `gitlab_get_snippets`(; optional project_id, snippet_id, title, file_name, content, visibility)
7. `gitlab_get_wiki_list`(; optional project_id, slug, content, title, format_type, with_content)
8. `gitlab_get_wiki_page`(; optional project_id, slug, content, title, format_type, with_content)
9. `gitlab_update_snippet`(; optional project_id, snippet_id, title, file_name, content, visibility)
10. `gitlab_update_wiki_page`(; optional project_id, slug, content, title, format_type, with_content)
11. `gitlab_upload_wiki_page_attachment`(; optional project_id, slug, content, title, format_type, with_content)

### administer-users

Create, change and delete users. Contract steps, in order:

1. `gitlab_create_user`(; optional username, active, blocked, external, humans, exclude_internal)
2. `gitlab_delete_user`(; optional username, active, blocked, external, humans, exclude_internal) (destructive: pass confirm=true only after the person agrees)
3. `gitlab_get_user`(; optional username, active, blocked, external, humans, exclude_internal)
4. `gitlab_get_users`(; optional username, active, blocked, external, humans, exclude_internal)
5. `gitlab_update_user`(; optional username, active, blocked, external, humans, exclude_internal)

### ingest-projects

Mirror projects into the knowledge graph. Contract steps, in order:

1. `gitlab_get_projects`(; optional project_id, group_id, allow_merge_on_skipped_pipeline, only_allow_merge_if_all_status_checks_passed, analytics_access_level, approvals_before_merge)
2. `gitlab_ingest_projects`(; optional membership, owned, search, per_page, max_pages)

### retire-a-project

Delete a project. Contract steps, in order:

1. `gitlab_delete_project`(; optional project_id, max_pages, page, per_page, confirm) (destructive: pass confirm=true only after the person agrees)
