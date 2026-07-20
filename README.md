# Gitlab Api
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/gitlab-api)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/gitlab-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/gitlab-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/gitlab-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/gitlab-api)
![PyPI - License](https://img.shields.io/pypi/l/gitlab-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/gitlab-api)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/gitlab-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/gitlab-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/gitlab-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/gitlab-api)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/gitlab-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/gitlab-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/gitlab-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/gitlab-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/gitlab-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/gitlab-api)

*Version: 26.4.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, the integrated A2A agent server, and guidance for provisioning the
> backing GitLab instance are maintained in the
> [official documentation](https://knuckles-team.github.io/gitlab-api/).

---

## Overview

**Gitlab Api** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with GitLab API + MCP Server + A2A Server.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the GitLab API + MCP Server + A2A Server API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Tool surface — `MCP_TOOL_MODE`

Set `MCP_TOOL_MODE` (in the shared `~/.config/agent-utilities/config.json` or env):
`condensed` (default — the action-routed tools below), `verbose` (one named 1:1 tool
per API method, e.g. `gitlab_get_branches(...)`, tagged `verbose`), or `both`. Filter
the verbose set with `--tools tag:verbose` / `MCP_ENABLED_TAGS=verbose`. See the
agent-utilities *MCP Tool Modes* guide.

### Available MCP Tools

_Auto-generated from the live MCP server — do not edit by hand._

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `api_request` | `CUSTOM_APITOOL` | Execute arbitrary GitLab REST API requests directly. |
| `gitlab_branches` | `BRANCHESTOOL` | Manage gitlab branches operations. |
| `gitlab_commits` | `COMMITSTOOL` | Manage gitlab commits operations. |
| `gitlab_deploy_tokens` | `DEPLOY_TOKENSTOOL` | Manage gitlab deploy tokens operations. |
| `gitlab_discover_graphql_schema` | `GRAPHQLTOOL` | Discover the dynamic GitLab GraphQL schema including types, fields, and custom attributes in real-time. |
| `gitlab_environments` | `ENVIRONMENTSTOOL` | Manage gitlab environments operations. |
| `gitlab_epics` | `EPICSTOOL` | Manage GitLab epics. |
| `gitlab_graphql` | `GRAPHQLTOOL` | Execute raw GraphQL queries and mutations natively on GitLab. |
| `gitlab_graphql_ops` | `GRAPHQL_OPSTOOL` | Run a typed GitLab GraphQL operation by name. |
| `gitlab_groups` | `GROUPSTOOL` | Manage gitlab groups operations. |
| `gitlab_ingest_pipelines` | `MISCTOOL` | Natively ingest GitLab CI pipeline runs (+ jobs) into epistemic-graph. |
| `gitlab_ingest_projects` | `MISCTOOL` | Natively ingest GitLab projects into epistemic-graph as typed :Project nodes. |
| `gitlab_instances` | `MISCTOOL` | List the configured GitLab tenants (CONCEPT:AU-KG.backend.declared-columns-so-schema). |
| `gitlab_issues` | `ISSUESTOOL` | Manage GitLab issues. |
| `gitlab_jobs` | `JOBSTOOL` | Manage gitlab jobs operations. |
| `gitlab_labels` | `LABELSTOOL` | Manage GitLab labels. |
| `gitlab_members` | `MEMBERSTOOL` | Manage gitlab members operations. |
| `gitlab_merge_requests` | `MERGE_REQUESTSTOOL` | Manage gitlab merge requests operations. |
| `gitlab_merge_rules` | `MERGE_RULESTOOL` | Manage gitlab merge rules operations. |
| `gitlab_milestones` | `MILESTONESTOOL` | Manage GitLab milestones. |
| `gitlab_namespaces` | `NAMESPACESTOOL` | Manage gitlab namespaces operations. |
| `gitlab_notes` | `NOTESTOOL` | Manage GitLab notes/comments on issues, merge requests, commits, and epics. |
| `gitlab_packages` | `PACKAGESTOOL` | Manage gitlab packages operations. |
| `gitlab_pipeline_schedules` | `PIPELINE_SCHEDULESTOOL` | Manage gitlab pipeline schedules operations. |
| `gitlab_pipelines` | `PIPELINESTOOL` | Manage gitlab pipelines operations. |
| `gitlab_projects` | `PROJECTSTOOL` | Manage gitlab projects operations. |
| `gitlab_protected_branches` | `PROTECTED_BRANCHESTOOL` | Manage gitlab protected branches operations. |
| `gitlab_releases` | `RELEASESTOOL` | Manage gitlab releases operations. |
| `gitlab_runners` | `RUNNERSTOOL` | Manage gitlab runners operations. |
| `gitlab_snippets` | `SNIPPETSTOOL` | Manage GitLab snippets. |
| `gitlab_tags` | `TAGSTOOL` | Manage gitlab tags operations. |
| `gitlab_users` | `USERSTOOL` | Manage gitlab users operations. |
| `gitlab_vulnerabilities` | `VULNERABILITIESTOOL` | Review a project's dependency list and security vulnerabilities (the GitLab counterpart to GitHub Dependabot). |
| `gitlab_wiki` | `WIKITOOL` | Manage gitlab wiki operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>196 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `gitlab_accept_merge_request` | `MERGE_REQUESTSTOOL` | Accept (merge) a merge request. |
| `gitlab_api_request` | `SYSTEMTOOL` | Make a custom API request to the GitLab server. |
| `gitlab_approve_merge_request` | `MERGE_REQUESTSTOOL` | Approve a specific merge request. |
| `gitlab_archive_project` | `PROJECTSTOOL` | Archive a specific project. |
| `gitlab_cancel_merge_when_pipeline_succeeds` | `MERGE_REQUESTSTOOL` | Cancel a merge request's queued "merge when pipeline succeeds" (auto-merge). |
| `gitlab_cancel_project_job` | `PROJECTSTOOL` | Cancel a specific job within a project. |
| `gitlab_cherry_pick_commit` | `REPOSITORIESTOOL` | Cherry-pick a commit into a new branch. |
| `gitlab_create_branch` | `REPOSITORIESTOOL` | Create a new branch in a project. |
| `gitlab_create_commit` | `REPOSITORIESTOOL` | Create a new commit. |
| `gitlab_create_commit_comment` | `REPOSITORIESTOOL` | Create a comment on a commit. |
| `gitlab_create_environment` | `ENVIRONMENTSTOOL` | Create a new environment for a project. |
| `gitlab_create_epic` | `ISSUESTOOL` | Create a new group epic. |
| `gitlab_create_group_deploy_token` | `USERS_GROUPSTOOL` | Create a deploy token for a group. |
| `gitlab_create_issue` | `ISSUESTOOL` | Create a new issue. |
| `gitlab_create_label` | `ISSUESTOOL` | Create a new label. |
| `gitlab_create_merge_request` | `MERGE_REQUESTSTOOL` | Create a new merge request. |
| `gitlab_create_milestone` | `ISSUESTOOL` | Create a project milestone. |
| `gitlab_create_note` | `OTHERTOOL` | Create a new note/comment on an issue. |
| `gitlab_create_pipeline_schedule` | `PIPELINESTOOL` | Create a pipeline schedule for a specific project. |
| `gitlab_create_pipeline_schedule_variable` | `PIPELINESTOOL` | Create a variable for a pipeline schedule. |
| `gitlab_create_project` | `PROJECTSTOOL` | Create a new project. |
| `gitlab_create_project_deploy_token` | `PROJECTSTOOL` | Create a deploy token for a project. |
| `gitlab_create_project_level_rule` | `PROJECTSTOOL` | Create a new project-level merge request approval rule. |
| `gitlab_create_release` | `ENVIRONMENTSTOOL` | Create a new release in a project. |
| `gitlab_create_release_evidence` | `ENVIRONMENTSTOOL` | Create evidence for a release in a project. |
| `gitlab_create_snippet` | `OTHERTOOL` | Create a project snippet or personal snippet. |
| `gitlab_create_tag` | `REPOSITORIESTOOL` | Create a tag in a project. |
| `gitlab_create_user` | `USERS_GROUPSTOOL` | Create a new user. |
| `gitlab_create_wiki_page` | `OTHERTOOL` | Create a new wiki page for a project. |
| `gitlab_delete_branch` | `REPOSITORIESTOOL` | Delete a branch in a project. |
| `gitlab_delete_environment` | `ENVIRONMENTSTOOL` | Delete an environment for a project. |
| `gitlab_delete_epic` | `ISSUESTOOL` | Delete a group epic. |
| `gitlab_delete_group_deploy_token` | `USERS_GROUPSTOOL` | Delete a deploy token for a group. |
| `gitlab_delete_issue` | `ISSUESTOOL` | Delete an issue. |
| `gitlab_delete_label` | `ISSUESTOOL` | Delete a label. |
| `gitlab_delete_merged_branches` | `REPOSITORIESTOOL` | Delete all merged branches in a project. |
| `gitlab_delete_milestone` | `ISSUESTOOL` | Delete a project milestone. |
| `gitlab_delete_note` | `OTHERTOOL` | Delete a note. |
| `gitlab_delete_pipeline_schedule` | `PIPELINESTOOL` | Delete a pipeline schedule for a specific project. |
| `gitlab_delete_pipeline_schedule_variable` | `PIPELINESTOOL` | Delete a variable from a pipeline schedule. |
| `gitlab_delete_project` | `PROJECTSTOOL` | Delete a specific project. |
| `gitlab_delete_project_deploy_token` | `PROJECTSTOOL` | Delete a deploy token for a project. |
| `gitlab_delete_project_level_rule` | `PROJECTSTOOL` | Delete a project-level merge request approval rule. |
| `gitlab_delete_project_runner` | `PROJECTSTOOL` | Delete a runner from a project. |
| `gitlab_delete_release` | `ENVIRONMENTSTOOL` | Delete a release in a project. |
| `gitlab_delete_runner` | `PIPELINESTOOL` | Delete a runner. |
| `gitlab_delete_shared_project_link` | `PROJECTSTOOL` | Unshare a specific project from a group. |
| `gitlab_delete_snippet` | `OTHERTOOL` | Delete a snippet. |
| `gitlab_delete_stopped_environments` | `ENVIRONMENTSTOOL` | Delete stopped environments (review apps) for a project. |
| `gitlab_delete_tag` | `REPOSITORIESTOOL` | Delete a tag in a project. |
| `gitlab_delete_user` | `USERS_GROUPSTOOL` | Delete a user. |
| `gitlab_delete_wiki_page` | `OTHERTOOL` | Delete a wiki page for a project. |
| `gitlab_download_release_asset` | `ENVIRONMENTSTOOL` | Download a release asset from a group's release. |
| `gitlab_download_repository_package` | `OTHERTOOL` | Download a repository package for a specific project. |
| `gitlab_edit_group` | `USERS_GROUPSTOOL` | Edit a specific group. |
| `gitlab_edit_group_level_rule` | `USERS_GROUPSTOOL` | Edit a group-level merge request approval setting. |
| `gitlab_edit_pipeline_schedule` | `PIPELINESTOOL` | Edit a pipeline schedule for a specific project. |
| `gitlab_edit_project` | `PROJECTSTOOL` | Edit a specific project. |
| `gitlab_edit_project_level_rule` | `PROJECTSTOOL` | Edit a project-level merge request approval setting. |
| `gitlab_enable_project_runner` | `PROJECTSTOOL` | Enable a runner in a project. |
| `gitlab_erase_project_job` | `PROJECTSTOOL` | Erase a specific job within a project. |
| `gitlab_get_approval_state_merge_requests` | `MERGE_REQUESTSTOOL` | Get the approval state of merge requests for a specific project. |
| `gitlab_get_branch` | `REPOSITORIESTOOL` | Retrieve information about a specific branch in a project. |
| `gitlab_get_branches` | `REPOSITORIESTOOL` | Retrieve information about branches in a project. |
| `gitlab_get_commit` | `REPOSITORIESTOOL` | Get a specific commit. |
| `gitlab_get_commit_comments` | `REPOSITORIESTOOL` | Get comments on a commit. |
| `gitlab_get_commit_diff` | `REPOSITORIESTOOL` | Get the diff of a commit. |
| `gitlab_get_commit_discussions` | `REPOSITORIESTOOL` | Get discussions on a commit. |
| `gitlab_get_commit_gpg_signature` | `REPOSITORIESTOOL` | Get GPG signature of a commit. |
| `gitlab_get_commit_merge_requests` | `REPOSITORIESTOOL` | Get merge requests associated with a commit. |
| `gitlab_get_commit_references` | `REPOSITORIESTOOL` | Get references of a commit. |
| `gitlab_get_commit_statuses` | `REPOSITORIESTOOL` | Get statuses of a commit. |
| `gitlab_get_commits` | `REPOSITORIESTOOL` | Get commits. |
| `gitlab_get_deploy_tokens` | `ENVIRONMENTSTOOL` | Get all deploy tokens. |
| `gitlab_get_environment` | `ENVIRONMENTSTOOL` | Get details of a specific environment. |
| `gitlab_get_environments` | `ENVIRONMENTSTOOL` | Get a list of environments for a project. |
| `gitlab_get_epic` | `ISSUESTOOL` | Get a specific group epic. |
| `gitlab_get_epics` | `ISSUESTOOL` | Get all epics for a group. |
| `gitlab_get_group` | `USERS_GROUPSTOOL` | Get details of a specific group. |
| `gitlab_get_group_deploy_token` | `USERS_GROUPSTOOL` | Get a specific deploy token for a group. |
| `gitlab_get_group_deploy_tokens` | `USERS_GROUPSTOOL` | Get deploy tokens for a specific group. |
| `gitlab_get_group_descendant_groups` | `USERS_GROUPSTOOL` | Get descendant groups of a specific group. |
| `gitlab_get_group_issues` | `ISSUESTOOL` | Get the list of issues for a group (and, by default, its subgroups). |
| `gitlab_get_group_level_rule` | `USERS_GROUPSTOOL` | Get details of a group-level merge request approval setting. |
| `gitlab_get_group_members` | `USERS_GROUPSTOOL` | Get members of a specific group. |
| `gitlab_get_group_merge_requests` | `MERGE_REQUESTSTOOL` | Get merge requests associated with a specific group. |
| `gitlab_get_group_projects` | `PROJECTSTOOL` | Get projects associated with a specific group. |
| `gitlab_get_group_releases` | `USERS_GROUPSTOOL` | Get information about releases in a group. |
| `gitlab_get_group_runners` | `PIPELINESTOOL` | Get information about runners in a group. |
| `gitlab_get_group_subgroups` | `USERS_GROUPSTOOL` | Get subgroups of a specific group. |
| `gitlab_get_group_vulnerabilities` | `VULNERABILITIESTOOL` | Get a group's security vulnerability findings (Ultimate). |
| `gitlab_get_groups` | `USERS_GROUPSTOOL` | Get a list of groups. |
| `gitlab_get_issue` | `ISSUESTOOL` | Get a single issue. |
| `gitlab_get_issues` | `ISSUESTOOL` | Get list of issues. Can filter by project_id. |
| `gitlab_get_label` | `ISSUESTOOL` | Get a specific label by name. |
| `gitlab_get_labels` | `ISSUESTOOL` | Get all labels for a project. |
| `gitlab_get_latest_release` | `ENVIRONMENTSTOOL` | Get information about the latest release in a project. |
| `gitlab_get_latest_release_asset` | `ENVIRONMENTSTOOL` | Get the asset for the latest release in a project. |
| `gitlab_get_latest_release_evidence` | `ENVIRONMENTSTOOL` | Get evidence for the latest release in a project. |
| `gitlab_get_merge_request_level_rules` | `MERGE_REQUESTSTOOL` | Get merge request-level approval rules for a specific project and merge request. |
| `gitlab_get_merge_requests` | `MERGE_REQUESTSTOOL` | Get a list of merge requests. |
| `gitlab_get_milestone` | `ISSUESTOOL` | Get a specific project milestone. |
| `gitlab_get_milestones` | `ISSUESTOOL` | Get all milestones for a project. |
| `gitlab_get_namespace` | `USERS_GROUPSTOOL` | Get information about a specific namespace. |
| `gitlab_get_namespaces` | `USERS_GROUPSTOOL` | Get information about namespaces. |
| `gitlab_get_nested_projects_by_group` | `PROJECTSTOOL` | Get information about nested projects within a group. |
| `gitlab_get_note` | `OTHERTOOL` | Get a specific note. |
| `gitlab_get_notes` | `OTHERTOOL` | Get all notes for a specific issue. |
| `gitlab_get_pipeline` | `PIPELINESTOOL` | Get information about a specific pipeline in a project. |
| `gitlab_get_pipeline_jobs` | `PIPELINESTOOL` | Get jobs associated with a specific pipeline within a project. |
| `gitlab_get_pipeline_schedule` | `PIPELINESTOOL` | Get information about a specific pipeline schedule in a project. |
| `gitlab_get_pipeline_schedules` | `PIPELINESTOOL` | Get pipeline schedules for a specific project. |
| `gitlab_get_pipelines` | `PIPELINESTOOL` | Get information about pipelines for a specific project. |
| `gitlab_get_pipelines_triggered_from_schedule` | `PIPELINESTOOL` | Get pipelines triggered from a specific pipeline schedule. |
| `gitlab_get_project` | `PROJECTSTOOL` | Get information about a specific project. |
| `gitlab_get_project_contributors` | `PROJECTSTOOL` | Get information about contributors to a project. |
| `gitlab_get_project_dependencies` | `VULNERABILITIESTOOL` | Get a project's Dependency List (all detected dependencies). |
| `gitlab_get_project_deploy_token` | `PROJECTSTOOL` | Get a specific deploy token for a project. |
| `gitlab_get_project_deploy_tokens` | `PROJECTSTOOL` | Get deploy tokens for a specific project. |
| `gitlab_get_project_groups` | `PROJECTSTOOL` | Get groups associated with a specific project. |
| `gitlab_get_project_job` | `PROJECTSTOOL` | Get details of a specific job within a project. |
| `gitlab_get_project_job_log` | `PROJECTSTOOL` | Get the log of a specific job within a project. |
| `gitlab_get_project_jobs` | `PROJECTSTOOL` | Get jobs associated with a specific project. |
| `gitlab_get_project_level_merge_request_rule` | `PROJECTSTOOL` | Get details of a specific project-level merge request approval rule. |
| `gitlab_get_project_level_merge_request_rules` | `PROJECTSTOOL` | Get project-level merge request approval rules. |
| `gitlab_get_project_level_rule` | `PROJECTSTOOL` | Get details of a project-level merge request approval setting. |
| `gitlab_get_project_members` | `PROJECTSTOOL` | Get members of a specific project. |
| `gitlab_get_project_merge_request` | `PROJECTSTOOL` | Get details of a specific merge request in a project. |
| `gitlab_get_project_merge_requests` | `PROJECTSTOOL` | Get merge requests for a specific project. |
| `gitlab_get_project_runners` | `PROJECTSTOOL` | Get information about runners in a project. |
| `gitlab_get_project_statistics` | `PROJECTSTOOL` | Get statistics for a specific project. |
| `gitlab_get_project_vulnerabilities` | `VULNERABILITIESTOOL` | Get a project's security vulnerabilities (Ultimate). |
| `gitlab_get_projects` | `PROJECTSTOOL` | Get information about projects. |
| `gitlab_get_protected_branch` | `REPOSITORIESTOOL` | Get information about a specific protected branch in a project. |
| `gitlab_get_protected_branches` | `REPOSITORIESTOOL` | Get information about protected branches in a project. |
| `gitlab_get_protected_environment` | `ENVIRONMENTSTOOL` | Get details of a specific protected environment. |
| `gitlab_get_protected_environments` | `ENVIRONMENTSTOOL` | Get a list of protected environments for a project. |
| `gitlab_get_protected_tag` | `REPOSITORIESTOOL` | Get information about a specific protected tag in a project. |
| `gitlab_get_protected_tags` | `REPOSITORIESTOOL` | Get information about protected tags in a project. |
| `gitlab_get_release_by_tag` | `REPOSITORIESTOOL` | Get information about a release by its tag in a project. |
| `gitlab_get_releases` | `ENVIRONMENTSTOOL` | Get information about releases in a project. |
| `gitlab_get_repository_packages` | `OTHERTOOL` | Get information about repository packages for a specific project. |
| `gitlab_get_runner` | `PIPELINESTOOL` | Get information about a specific runner. |
| `gitlab_get_runner_jobs` | `PIPELINESTOOL` | Get jobs for a specific runner. |
| `gitlab_get_runners` | `PIPELINESTOOL` | Get information about runners. |
| `gitlab_get_snippet` | `OTHERTOOL` | Get a specific snippet. |
| `gitlab_get_snippets` | `OTHERTOOL` | Get list of snippets. Can filter by project_id. |
| `gitlab_get_tag` | `REPOSITORIESTOOL` | Get information about a specific tag in a project. |
| `gitlab_get_tags` | `REPOSITORIESTOOL` | Get information about tags in a project. |
| `gitlab_get_user` | `USERS_GROUPSTOOL` | Get information about a specific user. |
| `gitlab_get_users` | `USERS_GROUPSTOOL` | Get information about users. |
| `gitlab_get_vulnerability` | `VULNERABILITIESTOOL` | Get a single vulnerability by its global ID (Ultimate). |
| `gitlab_get_wiki_list` | `OTHERTOOL` | Get a list of wiki pages for a project. |
| `gitlab_get_wiki_page` | `OTHERTOOL` | Get information about a specific wiki page. |
| `gitlab_merge_request_level_approvals` | `MERGE_REQUESTSTOOL` | Get approvals for a specific merge request. |
| `gitlab_pause_runner` | `PIPELINESTOOL` | Pause or unpause a specific runner. |
| `gitlab_post_build_status_to_commit` | `REPOSITORIESTOOL` | Post build status to a commit. |
| `gitlab_protect_branch` | `REPOSITORIESTOOL` | Protect a specific branch in a project. |
| `gitlab_protect_environment` | `ENVIRONMENTSTOOL` | Protect an environment for a project. |
| `gitlab_protect_tag` | `REPOSITORIESTOOL` | Protect a tag in a project. |
| `gitlab_publish_repository_package` | `OTHERTOOL` | Publish a repository package for a specific project. |
| `gitlab_register_new_runner` | `PIPELINESTOOL` | Register a new runner. |
| `gitlab_require_code_owner_approvals_single_branch` | `REPOSITORIESTOOL` | Require code owner approvals for a specific branch in a project. |
| `gitlab_reset_gitlab_runner_token` | `PIPELINESTOOL` | Reset GitLab runner registration token. |
| `gitlab_reset_group_runner_token` | `PIPELINESTOOL` | Reset registration token for a group's runner. |
| `gitlab_reset_project_runner_token` | `PROJECTSTOOL` | Reset registration token for a project's runner. |
| `gitlab_reset_token` | `OTHERTOOL` | Reset authentication token for a runner. |
| `gitlab_retry_project_job` | `PROJECTSTOOL` | Retry a specific job within a project. |
| `gitlab_revert_commit` | `REPOSITORIESTOOL` | Revert a commit. |
| `gitlab_run_pipeline` | `PIPELINESTOOL` | Run a pipeline for a specific project. |
| `gitlab_run_pipeline_schedule` | `PIPELINESTOOL` | Run a pipeline schedule for a specific project. |
| `gitlab_run_project_job` | `PROJECTSTOOL` | Run a specific job within a project. |
| `gitlab_share_project` | `PROJECTSTOOL` | Share a specific project with a group. |
| `gitlab_stop_environment` | `ENVIRONMENTSTOOL` | Stop an environment for a project. |
| `gitlab_stop_stale_environments` | `ENVIRONMENTSTOOL` | Stop stale environments for a project. |
| `gitlab_take_pipeline_schedule_ownership` | `PIPELINESTOOL` | Take ownership of a pipeline schedule for a specific project. |
| `gitlab_unapprove_merge_request` | `MERGE_REQUESTSTOOL` | Unapprove a specific merge request. |
| `gitlab_unarchive_project` | `PROJECTSTOOL` | Unarchive a specific project. |
| `gitlab_unprotect_branch` | `REPOSITORIESTOOL` | Unprotect a specific branch in a project. |
| `gitlab_unprotect_environment` | `ENVIRONMENTSTOOL` | Unprotect an environment for a project. |
| `gitlab_unprotect_tag` | `REPOSITORIESTOOL` | Unprotect a tag in a project. |
| `gitlab_update_environment` | `ENVIRONMENTSTOOL` | Update an existing environment for a project. |
| `gitlab_update_epic` | `ISSUESTOOL` | Update a group epic. |
| `gitlab_update_issue` | `ISSUESTOOL` | Update an issue. |
| `gitlab_update_label` | `ISSUESTOOL` | Update an existing label. |
| `gitlab_update_milestone` | `ISSUESTOOL` | Update a project milestone. |
| `gitlab_update_note` | `OTHERTOOL` | Update a note. |
| `gitlab_update_project_level_rule` | `PROJECTSTOOL` | Update an existing project-level merge request approval rule. |
| `gitlab_update_protected_environment` | `ENVIRONMENTSTOOL` | Update a protected environment for a project. |
| `gitlab_update_release` | `ENVIRONMENTSTOOL` | Update information about a release in a project. |
| `gitlab_update_runner_details` | `PIPELINESTOOL` | Update details for a specific runner. |
| `gitlab_update_snippet` | `OTHERTOOL` | Update a snippet. |
| `gitlab_update_user` | `USERS_GROUPSTOOL` | Update an existing user. |
| `gitlab_update_wiki_page` | `OTHERTOOL` | Update an existing wiki page for a project. |
| `gitlab_upload_wiki_page_attachment` | `OTHERTOOL` | Upload an attachment to a wiki page for a project. |
| `gitlab_verify_runner_authentication` | `PIPELINESTOOL` | Verify runner authentication. |

</details>

_34 action-routed tool(s) (default) · 196 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/usage.md](docs/usage.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `gitlab-api[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "gitlab-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "gitlab-api[mcp]",
        "gitlab-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "intent",
        "BRANCHESTOOL": "True",
        "COMMITSTOOL": "True",
        "CUSTOM_APITOOL": "True",
        "DEPLOY_TOKENSTOOL": "True",
        "ENVIRONMENTSTOOL": "True",
        "EPICSTOOL": "True",
        "GITLAB_TOKEN": "your_gitlab_token_here",
        "GITLAB_URL": "https://gitlab.example.com",
        "GRAPHQLTOOL": "True",
        "GRAPHQL_OPSTOOL": "True",
        "GROUPSTOOL": "True",
        "ISSUESTOOL": "True",
        "JOBSTOOL": "True",
        "LABELSTOOL": "True",
        "MEMBERSTOOL": "True",
        "MERGE_REQUESTSTOOL": "True",
        "MERGE_RULESTOOL": "True",
        "MILESTONESTOOL": "True",
        "MISCTOOL": "True",
        "NAMESPACESTOOL": "True",
        "NOTESTOOL": "True",
        "PACKAGESTOOL": "True",
        "PIPELINESTOOL": "True",
        "PIPELINE_SCHEDULESTOOL": "True",
        "PROJECTSTOOL": "True",
        "PROTECTED_BRANCHESTOOL": "True",
        "RELEASESTOOL": "True",
        "RUNNERSTOOL": "True",
        "SNIPPETSTOOL": "True",
        "TAGSTOOL": "True",
        "USERSTOOL": "True",
        "VULNERABILITIESTOOL": "True",
        "WIKITOOL": "True"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as GraphOS. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "gitlab-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "gitlab-api[mcp]",
        "gitlab-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "BRANCHESTOOL": "True",
        "COMMITSTOOL": "True",
        "CUSTOM_APITOOL": "True",
        "DEPLOY_TOKENSTOOL": "True",
        "ENVIRONMENTSTOOL": "True",
        "EPICSTOOL": "True",
        "GITLAB_TOKEN": "your_gitlab_token_here",
        "GITLAB_URL": "https://gitlab.example.com",
        "GRAPHQLTOOL": "True",
        "GRAPHQL_OPSTOOL": "True",
        "GROUPSTOOL": "True",
        "ISSUESTOOL": "True",
        "JOBSTOOL": "True",
        "LABELSTOOL": "True",
        "MEMBERSTOOL": "True",
        "MERGE_REQUESTSTOOL": "True",
        "MERGE_RULESTOOL": "True",
        "MILESTONESTOOL": "True",
        "MISCTOOL": "True",
        "NAMESPACESTOOL": "True",
        "NOTESTOOL": "True",
        "PACKAGESTOOL": "True",
        "PIPELINESTOOL": "True",
        "PIPELINE_SCHEDULESTOOL": "True",
        "PROJECTSTOOL": "True",
        "PROTECTED_BRANCHESTOOL": "True",
        "RELEASESTOOL": "True",
        "RUNNERSTOOL": "True",
        "SNIPPETSTOOL": "True",
        "TAGSTOOL": "True",
        "USERSTOOL": "True",
        "VULNERABILITIESTOOL": "True",
        "WIKITOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "gitlab-mcp": {
      "url": "http://localhost:8000/gitlab-mcp/mcp"
    }
  }
}
```

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e BRANCHESTOOL=True \
  -e COMMITSTOOL=True \
  -e CUSTOM_APITOOL=True \
  -e DEPLOY_TOKENSTOOL=True \
  -e ENVIRONMENTSTOOL=True \
  -e EPICSTOOL=True \
  -e GITLAB_TOKEN=your_gitlab_token_here \
  -e GITLAB_URL=https://gitlab.example.com \
  -e GRAPHQLTOOL=True \
  -e GRAPHQL_OPSTOOL=True \
  -e GROUPSTOOL=True \
  -e ISSUESTOOL=True \
  -e JOBSTOOL=True \
  -e LABELSTOOL=True \
  -e MEMBERSTOOL=True \
  -e MERGE_REQUESTSTOOL=True \
  -e MERGE_RULESTOOL=True \
  -e MILESTONESTOOL=True \
  -e MISCTOOL=True \
  -e NAMESPACESTOOL=True \
  -e NOTESTOOL=True \
  -e PACKAGESTOOL=True \
  -e PIPELINESTOOL=True \
  -e PIPELINE_SCHEDULESTOOL=True \
  -e PROJECTSTOOL=True \
  -e PROTECTED_BRANCHESTOOL=True \
  -e RELEASESTOOL=True \
  -e RUNNERSTOOL=True \
  -e SNIPPETSTOOL=True \
  -e TAGSTOOL=True \
  -e USERSTOOL=True \
  -e VULNERABILITIESTOOL=True \
  -e WIKITOOL=True \
  registry.example.invalid/gitlab-api@sha256:<digest> gitlab-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`gitlab-api` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/gitlab-api/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
<!-- END GENERATED: additional-deployment-options -->

---

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `GITLAB_URL` | `https://gitlab.example.com` |  |
| `GITLAB_TOKEN` | `your_gitlab_token_here` |  |
| `GITLAB_TLS_PROFILE` | _(unset)_ | Optional runtime TLS profile selector; verification is mandatory |
| `MISCTOOL` | `True` |  |
| `BRANCHESTOOL` | `True` |  |
| `PROTECTED_BRANCHESTOOL` | `True` |  |
| `COMMITSTOOL` | `True` |  |
| `DEPLOY_TOKENSTOOL` | `True` |  |
| `ENVIRONMENTSTOOL` | `True` |  |
| `EPICSTOOL` | `True` |  |
| `GROUPSTOOL` | `True` |  |
| `ISSUESTOOL` | `True` |  |
| `JOBSTOOL` | `True` |  |
| `LABELSTOOL` | `True` |  |
| `MEMBERSTOOL` | `True` |  |
| `MERGE_REQUESTSTOOL` | `True` |  |
| `MERGE_RULESTOOL` | `True` |  |
| `MILESTONESTOOL` | `True` |  |
| `NAMESPACESTOOL` | `True` |  |
| `NOTESTOOL` | `True` |  |
| `PACKAGESTOOL` | `True` |  |
| `PIPELINESTOOL` | `True` |  |
| `PIPELINE_SCHEDULESTOOL` | `True` |  |
| `PROJECTSTOOL` | `True` |  |
| `RELEASESTOOL` | `True` |  |
| `RUNNERSTOOL` | `True` |  |
| `SNIPPETSTOOL` | `True` |  |
| `TAGSTOOL` | `True` |  |
| `USERSTOOL` | `True` |  |
| `VULNERABILITIESTOOL` | `True` |  |
| `WIKITOOL` | `True` |  |
| `CUSTOM_APITOOL` | `True` |  |
| `GRAPHQLTOOL` | `True` |  |
| `GRAPHQL_OPSTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_45 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


Every variable the server reads.

### Connection & Credentials
The connector is single-host by default and **multi-tenant** when `gitlab_instances` is
configured (see [Multi-Tenancy](#multi-tenancy-multiple-gitlab-instances)). When no
instances are configured, it falls back to the single-host `GITLAB_*` values below.

| Variable | Description | Default |
|----------|-------------|---------|
| `GITLAB_URL` | Base GitLab instance URL | `https://gitlab.example.com` |
| `GITLAB_TOKEN` | GitLab personal/project access token (`glpat-…`) | — |
| `GITLAB_TLS_PROFILE` | Optional runtime TLS profile selector | _(unset)_ |

> Multiple instances are declared once under `gitlab_instances` in the shared
> agent-utilities XDG config (`~/.config/agent-utilities/config.json`) — each entry has
> `name`, `url`, `token`, and optional `tls_profile`. Target a tenant by **name** from the client
> factory; an unset instance resolves to the first configured one (else `GITLAB_URL` /
> `GITLAB_TOKEN`).

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |
| `DEBUG` | Verbose logging | `False` |
| `PYTHONUNBUFFERED` | Unbuffered stdout (recommended in containers) | `1` |

### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`).
The full list is in the [Available MCP Tools](#available-mcp-tools) table above
(e.g. `PROJECTSTOOL`, `MERGE_REQUESTSTOOL`, `PIPELINESTOOL`, `GRAPHQLTOOL`, `CUSTOM_APITOOL`).

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Agent CLI (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |

See [`.env.example`](.env.example) for a copy-paste starting point.

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export GITLAB_URL="your_value"
export GITLAB_TOKEN="your_value"

# Run the agent server
gitlab-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  gitlab-api-mcp:
    image: example/gitlab-api:mcp
    container_name: gitlab-api-mcp
    hostname: gitlab-api-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  gitlab-api-agent:
    image: example/gitlab-api@sha256:<digest>
    container_name: gitlab-api-agent
    hostname: gitlab-api-agent
    restart: always
    depends_on:
      - gitlab-api-mcp
    env_file:
      - ../.env
    command: [ "gitlab-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9017
      - MCP_URL=http://gitlab-api-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9017:9017"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9017/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/deployment.md](docs/deployment.md).

---

## Multi-Tenancy (multiple GitLab instances)

The client is natively multi-tenant. The set of instances is declared once in the
shared **agent-utilities XDG config** (`~/.config/agent-utilities/config.json`) under
`gitlab_instances` — the **same** list the Knowledge-Graph GitLab indexer reads, so one
config drives both code/metadata indexing and every API/MCP call:

```json
{
  "gitlab_instances": [
    {"name": "internal", "url": "https://gitlab.example.invalid", "token": "<GITLAB_TOKEN>", "tls_profile": "private-pki"},
    {"name": "public",   "url": "https://gitlab.com",  "token": "<GITLAB_TOKEN>"}
  ]
}
```

Target a tenant by **name** from the client factory; a bare URL still works, and an
unset instance resolves to the first configured one (else `GITLAB_URL`/`GITLAB_TOKEN`):

```python
from gitlab_api.auth import get_client
from gitlab_api.instances import list_configured_instances

internal = get_client(instance="internal")   # resolves URL, token, and TLS profile
public   = get_client(instance="public")
default  = get_client()                        # first configured / GITLAB_URL fallback
names    = [i.name for i in list_configured_instances()]
```

The MCP server exposes a `gitlab_instances` tool (`action=list|get`) to discover the
configured tenants (tokens are never returned). When no instances are configured, the
connector falls back to the single-host `GITLAB_URL`/`GITLAB_TOKEN` it has always used.

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `gitlab-api[mcp]` | Connector-focused MCP server (`agent-utilities[mcp]` — FastMCP/FastAPI + `epistemic-graph[full]`) | You only run the **MCP server** (smallest install / image) |
| `gitlab-api[agent]` | Agent runtime (`agent-utilities[agent-runtime,logfire]` — model orchestration + `epistemic-graph[full]`) | You run the **integrated agent** |
| `gitlab-api[all]` | Everything (`mcp` + `agent` + `gql` + `logfire`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "gitlab-api[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "gitlab-api[agent]"

# Everything (development)
uv pip install "gitlab-api[all]"      # or: python -m pip install "gitlab-api[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/gitlab-api:mcp` | `--target mcp` | `gitlab-api[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `gitlab-mcp` |
| `example/gitlab-api@sha256:<digest>` | `--target agent` (default) | `gitlab-api[agent]` — **agent runtime**, model orchestration + `epistemic-graph[full]` | `gitlab-agent` |

```bash
docker build --target mcp   -t example/gitlab-api:mcp    docker/   # connector-focused MCP server
docker build --target agent -t example/gitlab-api:agent-local docker/   # agent runtime
```

`docker/mcp.compose.yml` runs the connector-focused `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Both `[mcp]` and `[agent]` carry the **epistemic-graph** engine through the required
Agent Utilities core dependency (`epistemic-graph[full]`). The `[mcp]` extra keeps
the server connector-focused; `[agent]` additionally enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/gitlab-api/) and is the
recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/gitlab-api/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/gitlab-api/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/gitlab-api/usage/) | the MCP tools, the `Api` client, the CLI |
| [Backing Platform](https://knuckles-team.github.io/gitlab-api/platform/) | deploy GitLab with Docker |
| [Overview](https://knuckles-team.github.io/gitlab-api/overview/) | the action-routed tool surface and architecture |
| [Concepts](https://knuckles-team.github.io/gitlab-api/concepts/) | concept registry (`CONCEPT:GL-*`) |

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `gitlab-api` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "gitlab-api[mcp]"`, then run `gitlab-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `gitlab-mcp` |
| Immutable container | deploy `registry.example.invalid/gitlab-api@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, GraphOS delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
