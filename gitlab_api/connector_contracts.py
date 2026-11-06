"""Tool-use contracts, surface links, data locations and business roles of gitlab-mcp.

The SDK serves this declaration as the connector's surface ontology and checks it
against the served tools, prompts and skills (SCION-CONNECTOR-CONTROL-R916).
"""

# ruff: noqa: E501
from __future__ import annotations

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS: tuple[ToolUseContract, ...] = (
    ToolUseContract(
        "find-projects-and-groups",
        description="Find projects and groups and read their details, members and statistics",
        steps=(
            ToolStep(
                "gitlab_api_request",
                params=("method", "endpoint"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_discover_graphql_schema",
                params=("type_name",),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group",
                params=("group_id", "name", "path"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_descendant_groups",
                params=("group_id", "name", "path"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_members",
                params=("group_id", "project_id", "per_page"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_projects",
                params=("group_id", "name", "path"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_subgroups",
                params=("group_id", "name", "path"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_groups",
                params=("group_id", "name", "path"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_namespace",
                params=("namespace_id", "search", "owned_only"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_namespaces",
                params=("namespace_id", "search", "owned_only"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_nested_projects_by_group",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_contributors",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_dependencies",
                params=("project_id", "group_id", "vulnerability_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_groups",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_members",
                params=("group_id", "project_id", "per_page"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_statistics",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_projects",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_graphql", params=("query",), result=("result",), refusals=()
            ),
            ToolStep(
                "gitlab_instances_get",
                params=("name",),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_instances_list", params=(), result=("result",), refusals=()
            ),
        ),
    ),
    ToolUseContract(
        "provision-a-project",
        description="Create or change a project or group and share it",
        steps=(
            ToolStep(
                "gitlab_archive_project",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_create_project",
                params=("name", "path", "namespace_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_delete_shared_project_link",
                params=("project_id", "group_id", "max_pages"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_edit_group",
                params=("group_id", "name", "path"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_edit_project",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_share_project",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_unarchive_project",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "retire-a-project",
        description="Delete a project",
        steps=(
            ToolStep(
                "gitlab_delete_project",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "work-issues",
        description="Read, open, change and comment on issues, epics, labels and milestones",
        steps=(
            ToolStep(
                "gitlab_create_epic",
                params=("group_id", "epic_iid", "title"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_create_issue",
                params=("project_id", "group_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_create_label",
                params=("project_id", "name", "color"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_create_milestone",
                params=("project_id", "milestone_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_create_note",
                params=("project_id", "issue_iid", "note_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_delete_epic",
                params=("group_id", "epic_iid", "title"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_issue",
                params=("project_id", "group_id", "title"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_label",
                params=("project_id", "name", "color"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_milestone",
                params=("project_id", "milestone_id", "title"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_note",
                params=("project_id", "issue_iid", "note_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_epic",
                params=("group_id", "epic_iid", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_epics",
                params=("group_id", "epic_iid", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_issues",
                params=("project_id", "group_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_issue",
                params=("project_id", "group_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_issues",
                params=("project_id", "group_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_label",
                params=("project_id", "name", "color"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_labels",
                params=("project_id", "name", "color"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_milestone",
                params=("project_id", "milestone_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_milestones",
                params=("project_id", "milestone_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_note",
                params=("project_id", "issue_iid", "note_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_notes",
                params=("project_id", "issue_iid", "note_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_epic",
                params=("group_id", "epic_iid", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_issue",
                params=("project_id", "group_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_label",
                params=("project_id", "name", "color"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_milestone",
                params=("project_id", "milestone_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_note",
                params=("project_id", "issue_iid", "note_id"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "create-a-merge-request",
        description="Branch, commit and open a merge request",
        steps=(
            ToolStep(
                "gitlab_cherry_pick_commit",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_create_branch",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_create_commit",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_create_merge_request",
                params=("approved_by_ids", "approver_ids", "assignee_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_branch",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_branches",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_revert_commit",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "review-a-merge-request",
        description="Read a merge request, its approvals, commits and discussions",
        steps=(
            ToolStep(
                "gitlab_get_approval_state_merge_requests",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_commit",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_commit_comments",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_commit_diff",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_commit_discussions",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_commit_gpg_signature",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_commit_merge_requests",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_commit_references",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_commit_statuses",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_commits",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_merge_requests",
                params=("group_id", "name", "path"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_merge_request_level_rules",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_merge_requests",
                params=("approved_by_ids", "approver_ids", "assignee_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_level_merge_request_rule",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_level_merge_request_rules",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_merge_request",
                params=("approved_by_ids", "approver_ids", "assignee_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_merge_requests",
                params=("approved_by_ids", "approver_ids", "assignee_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_merge_request_level_approvals",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "land-a-merge-request",
        description="Approve, merge or auto-merge a merge request and clean up branches",
        steps=(
            ToolStep(
                "gitlab_accept_merge_request",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_approve_merge_request",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_cancel_merge_when_pipeline_succeeds",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_delete_branch",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_merged_branches",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_graphql_ops_delete_merge_request",
                params=("project_id", "merge_request_iid"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_graphql_ops_update_merge_request",
                params=("project_id", "merge_request_iid"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_unapprove_merge_request",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "manage-approval-rules",
        description="Create, change and delete approval rules and code-owner approval",
        steps=(
            ToolStep(
                "gitlab_create_project_level_rule",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_project_level_rule",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_edit_group_level_rule",
                params=("project_id", "group_id", "allow_author_approval"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_edit_project_level_rule",
                params=("project_id", "group_id", "allow_author_approval"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_level_rule",
                params=("project_id", "group_id", "allow_author_approval"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_level_rule",
                params=("project_id", "group_id", "allow_author_approval"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_require_code_owner_approvals_single_branch",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_project_level_rule",
                params=("project_id", "group_id", "approval_rule_id"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "review-ci-results",
        description="Read pipelines, jobs and job logs for a project",
        steps=(
            ToolStep(
                "gitlab_get_commit_statuses",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_pipeline",
                params=("project_id", "total_pages", "max_pages"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_pipeline_jobs",
                params=("project_id", "pipeline_id", "job_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_pipelines",
                params=("project_id", "total_pages", "max_pages"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_job",
                params=("project_id", "pipeline_id", "job_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_job_log",
                params=("project_id", "pipeline_id", "job_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_jobs",
                params=("project_id", "pipeline_id", "job_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_graphql_ops_get_job",
                params=("project_id", "job_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_ingest_pipelines",
                params=("project_id",),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "run-ci",
        description="Run, retry, cancel and erase pipelines and jobs and post build status",
        steps=(
            ToolStep(
                "gitlab_cancel_project_job",
                params=("project_id", "pipeline_id", "job_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_erase_project_job",
                params=("project_id", "pipeline_id", "job_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_graphql_ops_cancel_pipeline",
                params=("project_id", "pipeline_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_graphql_ops_create_pipeline",
                params=("project_id", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_graphql_ops_retry_pipeline",
                params=("project_id", "pipeline_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_post_build_status_to_commit",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_retry_project_job",
                params=("project_id", "pipeline_id", "job_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_run_pipeline",
                params=("project_id", "total_pages", "max_pages"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_run_project_job",
                params=("project_id", "pipeline_id", "job_id"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "manage-pipeline-schedules",
        description="Create, run, change and delete pipeline schedules and their variables",
        steps=(
            ToolStep(
                "gitlab_create_pipeline_schedule",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_create_pipeline_schedule_variable",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_delete_pipeline_schedule",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_pipeline_schedule_variable",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_edit_pipeline_schedule",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_pipeline_schedule",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_pipeline_schedules",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_pipelines_triggered_from_schedule",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_run_pipeline_schedule",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_take_pipeline_schedule_ownership",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "manage-environments",
        description="Create, protect, stop and delete environments",
        steps=(
            ToolStep(
                "gitlab_create_environment",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_environment",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_stopped_environments",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_environment",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_environments",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_protected_environment",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_protected_environments",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_protect_environment",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_stop_environment",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_stop_stale_environments",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_unprotect_environment",
                params=("project_id", "max_pages", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_update_environment",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_protected_environment",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "manage-runners",
        description="Register, enable, pause, reset and delete runners",
        steps=(
            ToolStep(
                "gitlab_delete_project_runner",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_runner",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_enable_project_runner",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_runners",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_runners",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_runner",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_runner_jobs",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_runners",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_pause_runner",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_register_new_runner",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_reset_gitlab_runner_token",
                params=(),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_reset_group_runner_token",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_reset_project_runner_token",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_reset_token",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_runner_details",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_verify_runner_authentication",
                params=("runner_id", "description", "active"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "manage-protection",
        description="Protect and unprotect branches and tags",
        steps=(
            ToolStep(
                "gitlab_create_tag",
                params=("project_id", "tag", "ref"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_tag",
                params=("project_id", "tag", "ref"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_protected_branch",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_protected_branches",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_protected_tag",
                params=("project_id", "tag", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_protected_tags",
                params=("project_id", "tag", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_tag",
                params=("project_id", "tag", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_tags",
                params=("project_id", "tag", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_protect_branch",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_protect_tag",
                params=("project_id", "tag", "ref"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_unprotect_branch",
                params=("project_id", "branch", "ref"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_unprotect_tag",
                params=("project_id", "tag", "ref"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "publish-a-release",
        description="Create, read, change and delete releases and their assets and packages",
        steps=(
            ToolStep(
                "gitlab_create_release",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_create_release_evidence",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_delete_release",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_download_release_asset",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_download_repository_package",
                params=("project_id", "group_id", "package_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_releases",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_latest_release",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_latest_release_asset",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_latest_release_evidence",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_release_by_tag",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_releases",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_repository_packages",
                params=("project_id", "group_id", "package_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_publish_repository_package",
                params=("project_id", "group_id", "package_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_release",
                params=("project_id", "group_id", "order_by"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "manage-deploy-tokens",
        description="Create, read and delete deploy tokens",
        steps=(
            ToolStep(
                "gitlab_create_group_deploy_token",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_create_project_deploy_token",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_delete_group_deploy_token",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_project_deploy_token",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_deploy_tokens",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_deploy_token",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_group_deploy_tokens",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_deploy_token",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_project_deploy_tokens",
                params=("project_id", "group_id", "token"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "triage-vulnerabilities",
        description="Read vulnerabilities of a project, group or one finding",
        steps=(
            ToolStep(
                "gitlab_get_group_vulnerabilities",
                params=("project_id", "group_id", "vulnerability_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_project_vulnerabilities",
                params=("project_id", "group_id", "vulnerability_id"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_vulnerability",
                params=("project_id", "group_id", "vulnerability_id"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "manage-wikis-and-snippets",
        description="Read and edit wiki pages and snippets",
        steps=(
            ToolStep(
                "gitlab_create_snippet",
                params=("project_id", "snippet_id", "title"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_create_wiki_page",
                params=("project_id", "slug", "content"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_delete_snippet",
                params=("project_id", "snippet_id", "title"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_wiki_page",
                params=("project_id", "slug", "content"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_snippet",
                params=("project_id", "snippet_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_snippets",
                params=("project_id", "snippet_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_wiki_list",
                params=("project_id", "slug", "content"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_wiki_page",
                params=("project_id", "slug", "content"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_snippet",
                params=("project_id", "snippet_id", "title"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_wiki_page",
                params=("project_id", "slug", "content"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_upload_wiki_page_attachment",
                params=("project_id", "slug", "content"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "administer-users",
        description="Create, change and delete users",
        steps=(
            ToolStep(
                "gitlab_create_user",
                params=("username", "active", "blocked"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_delete_user",
                params=("username", "active", "blocked"),
                result=("result",),
                refusals=(
                    Refusal(
                        "confirmation_required",
                        "the destructive call omits confirm=true",
                    ),
                ),
            ),
            ToolStep(
                "gitlab_get_user",
                params=("username", "active", "blocked"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_get_users",
                params=("username", "active", "blocked"),
                result=("result",),
                refusals=(),
            ),
            ToolStep(
                "gitlab_update_user",
                params=("username", "active", "blocked"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "ingest-projects",
        description="Mirror projects into the knowledge graph",
        steps=(
            ToolStep(
                "gitlab_get_projects",
                params=("project_id", "group_id", "allow_merge_on_skipped_pipeline"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
            ToolStep(
                "gitlab_ingest_projects",
                params=("membership", "owned", "search"),
                result=("result",),
                refusals=(),
            ),
        ),
    ),
    ToolUseContract(
        "other-operations",
        description="Operations not covered by a named workflow",
        steps=(
            ToolStep(
                "gitlab_create_commit_comment",
                params=("project_id", "commit_hash", "branch"),
                result=("result",),
                refusals=(
                    Refusal(
                        "access_denied", "the credential lacks access to the system"
                    ),
                ),
            ),
        ),
    ),
)

LINKS: tuple[SurfaceLink, ...] = (
    SurfaceLink(
        "find-projects-and-groups",
        tools=(
            "gitlab_api_request",
            "gitlab_discover_graphql_schema",
            "gitlab_get_group",
            "gitlab_get_group_descendant_groups",
            "gitlab_get_group_members",
            "gitlab_get_group_projects",
            "gitlab_get_group_subgroups",
            "gitlab_get_groups",
            "gitlab_get_namespace",
            "gitlab_get_namespaces",
            "gitlab_get_nested_projects_by_group",
            "gitlab_get_project",
            "gitlab_get_project_contributors",
            "gitlab_get_project_dependencies",
            "gitlab_get_project_groups",
            "gitlab_get_project_members",
            "gitlab_get_project_statistics",
            "gitlab_get_projects",
            "gitlab_graphql",
            "gitlab_instances_get",
            "gitlab_instances_list",
        ),
        prompts=(
            "gitlab-mcp-operator",
            "gitlab-mcp-project-administrator",
            "gitlab-mcp-triage-lead",
        ),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "provision-a-project",
        tools=(
            "gitlab_archive_project",
            "gitlab_create_project",
            "gitlab_delete_shared_project_link",
            "gitlab_edit_group",
            "gitlab_edit_project",
            "gitlab_share_project",
            "gitlab_unarchive_project",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-project-administrator"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "retire-a-project",
        tools=("gitlab_delete_project",),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-project-administrator"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "work-issues",
        tools=(
            "gitlab_create_epic",
            "gitlab_create_issue",
            "gitlab_create_label",
            "gitlab_create_milestone",
            "gitlab_create_note",
            "gitlab_delete_epic",
            "gitlab_delete_issue",
            "gitlab_delete_label",
            "gitlab_delete_milestone",
            "gitlab_delete_note",
            "gitlab_get_epic",
            "gitlab_get_epics",
            "gitlab_get_group_issues",
            "gitlab_get_issue",
            "gitlab_get_issues",
            "gitlab_get_label",
            "gitlab_get_labels",
            "gitlab_get_milestone",
            "gitlab_get_milestones",
            "gitlab_get_note",
            "gitlab_get_notes",
            "gitlab_update_epic",
            "gitlab_update_issue",
            "gitlab_update_label",
            "gitlab_update_milestone",
            "gitlab_update_note",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-triage-lead"),
        skills=("gitlab-issues",),
    ),
    SurfaceLink(
        "create-a-merge-request",
        tools=(
            "gitlab_cherry_pick_commit",
            "gitlab_create_branch",
            "gitlab_create_commit",
            "gitlab_create_merge_request",
            "gitlab_get_branch",
            "gitlab_get_branches",
            "gitlab_revert_commit",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-merge-request-create",),
    ),
    SurfaceLink(
        "review-a-merge-request",
        tools=(
            "gitlab_get_approval_state_merge_requests",
            "gitlab_get_commit",
            "gitlab_get_commit_comments",
            "gitlab_get_commit_diff",
            "gitlab_get_commit_discussions",
            "gitlab_get_commit_gpg_signature",
            "gitlab_get_commit_merge_requests",
            "gitlab_get_commit_references",
            "gitlab_get_commit_statuses",
            "gitlab_get_commits",
            "gitlab_get_group_merge_requests",
            "gitlab_get_merge_request_level_rules",
            "gitlab_get_merge_requests",
            "gitlab_get_project_level_merge_request_rule",
            "gitlab_get_project_level_merge_request_rules",
            "gitlab_get_project_merge_request",
            "gitlab_get_project_merge_requests",
            "gitlab_merge_request_level_approvals",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-merge-request-review",),
    ),
    SurfaceLink(
        "land-a-merge-request",
        tools=(
            "gitlab_accept_merge_request",
            "gitlab_approve_merge_request",
            "gitlab_cancel_merge_when_pipeline_succeeds",
            "gitlab_delete_branch",
            "gitlab_delete_merged_branches",
            "gitlab_graphql_ops_delete_merge_request",
            "gitlab_graphql_ops_update_merge_request",
            "gitlab_unapprove_merge_request",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-merge-request-review",),
    ),
    SurfaceLink(
        "manage-approval-rules",
        tools=(
            "gitlab_create_project_level_rule",
            "gitlab_delete_project_level_rule",
            "gitlab_edit_group_level_rule",
            "gitlab_edit_project_level_rule",
            "gitlab_get_group_level_rule",
            "gitlab_get_project_level_rule",
            "gitlab_require_code_owner_approvals_single_branch",
            "gitlab_update_project_level_rule",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-merge-request-review",),
    ),
    SurfaceLink(
        "review-ci-results",
        tools=(
            "gitlab_get_commit_statuses",
            "gitlab_get_pipeline",
            "gitlab_get_pipeline_jobs",
            "gitlab_get_pipelines",
            "gitlab_get_project_job",
            "gitlab_get_project_job_log",
            "gitlab_get_project_jobs",
            "gitlab_graphql_ops_get_job",
            "gitlab_ingest_pipelines",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-pipelines",),
    ),
    SurfaceLink(
        "run-ci",
        tools=(
            "gitlab_cancel_project_job",
            "gitlab_erase_project_job",
            "gitlab_graphql_ops_cancel_pipeline",
            "gitlab_graphql_ops_create_pipeline",
            "gitlab_graphql_ops_retry_pipeline",
            "gitlab_post_build_status_to_commit",
            "gitlab_retry_project_job",
            "gitlab_run_pipeline",
            "gitlab_run_project_job",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-pipelines",),
    ),
    SurfaceLink(
        "manage-pipeline-schedules",
        tools=(
            "gitlab_create_pipeline_schedule",
            "gitlab_create_pipeline_schedule_variable",
            "gitlab_delete_pipeline_schedule",
            "gitlab_delete_pipeline_schedule_variable",
            "gitlab_edit_pipeline_schedule",
            "gitlab_get_pipeline_schedule",
            "gitlab_get_pipeline_schedules",
            "gitlab_get_pipelines_triggered_from_schedule",
            "gitlab_run_pipeline_schedule",
            "gitlab_take_pipeline_schedule_ownership",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-pipelines",),
    ),
    SurfaceLink(
        "manage-environments",
        tools=(
            "gitlab_create_environment",
            "gitlab_delete_environment",
            "gitlab_delete_stopped_environments",
            "gitlab_get_environment",
            "gitlab_get_environments",
            "gitlab_get_protected_environment",
            "gitlab_get_protected_environments",
            "gitlab_protect_environment",
            "gitlab_stop_environment",
            "gitlab_stop_stale_environments",
            "gitlab_unprotect_environment",
            "gitlab_update_environment",
            "gitlab_update_protected_environment",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "manage-runners",
        tools=(
            "gitlab_delete_project_runner",
            "gitlab_delete_runner",
            "gitlab_enable_project_runner",
            "gitlab_get_group_runners",
            "gitlab_get_project_runners",
            "gitlab_get_runner",
            "gitlab_get_runner_jobs",
            "gitlab_get_runners",
            "gitlab_pause_runner",
            "gitlab_register_new_runner",
            "gitlab_reset_gitlab_runner_token",
            "gitlab_reset_group_runner_token",
            "gitlab_reset_project_runner_token",
            "gitlab_reset_token",
            "gitlab_update_runner_details",
            "gitlab_verify_runner_authentication",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-project-administrator"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "manage-protection",
        tools=(
            "gitlab_create_tag",
            "gitlab_delete_tag",
            "gitlab_get_protected_branch",
            "gitlab_get_protected_branches",
            "gitlab_get_protected_tag",
            "gitlab_get_protected_tags",
            "gitlab_get_tag",
            "gitlab_get_tags",
            "gitlab_protect_branch",
            "gitlab_protect_tag",
            "gitlab_unprotect_branch",
            "gitlab_unprotect_tag",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-project-administrator"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "publish-a-release",
        tools=(
            "gitlab_create_release",
            "gitlab_create_release_evidence",
            "gitlab_delete_release",
            "gitlab_download_release_asset",
            "gitlab_download_repository_package",
            "gitlab_get_group_releases",
            "gitlab_get_latest_release",
            "gitlab_get_latest_release_asset",
            "gitlab_get_latest_release_evidence",
            "gitlab_get_release_by_tag",
            "gitlab_get_releases",
            "gitlab_get_repository_packages",
            "gitlab_publish_repository_package",
            "gitlab_update_release",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-release-manager"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "manage-deploy-tokens",
        tools=(
            "gitlab_create_group_deploy_token",
            "gitlab_create_project_deploy_token",
            "gitlab_delete_group_deploy_token",
            "gitlab_delete_project_deploy_token",
            "gitlab_get_deploy_tokens",
            "gitlab_get_group_deploy_token",
            "gitlab_get_group_deploy_tokens",
            "gitlab_get_project_deploy_token",
            "gitlab_get_project_deploy_tokens",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-project-administrator"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "triage-vulnerabilities",
        tools=(
            "gitlab_get_group_vulnerabilities",
            "gitlab_get_project_vulnerabilities",
            "gitlab_get_vulnerability",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-triage-lead"),
        skills=("gitlab-vulnerabilities",),
    ),
    SurfaceLink(
        "manage-wikis-and-snippets",
        tools=(
            "gitlab_create_snippet",
            "gitlab_create_wiki_page",
            "gitlab_delete_snippet",
            "gitlab_delete_wiki_page",
            "gitlab_get_snippet",
            "gitlab_get_snippets",
            "gitlab_get_wiki_list",
            "gitlab_get_wiki_page",
            "gitlab_update_snippet",
            "gitlab_update_wiki_page",
            "gitlab_upload_wiki_page_attachment",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-project-administrator"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "administer-users",
        tools=(
            "gitlab_create_user",
            "gitlab_delete_user",
            "gitlab_get_user",
            "gitlab_get_users",
            "gitlab_update_user",
        ),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-project-administrator"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "ingest-projects",
        tools=("gitlab_get_projects", "gitlab_ingest_projects"),
        prompts=("gitlab-mcp-operator", "gitlab-mcp-project-administrator"),
        skills=("gitlab-api-operations",),
    ),
    SurfaceLink(
        "other-operations",
        tools=("gitlab_create_commit_comment",),
        prompts=("gitlab-mcp-operator",),
        skills=(),
    ),
)

LOCATIONS: tuple[DataLocation, ...] = (
    DataLocation(
        "gitlab-projects",
        ("SoftwareProject", "Repository"),
        "GITLAB_URL",
        "gitlab_get_projects",
        federation_key="project_id",
    ),
    DataLocation(
        "gitlab-merge-requests",
        ("MergeRequest",),
        "GITLAB_URL",
        "gitlab_get_merge_requests",
        federation_key="merge_request_iid",
    ),
    DataLocation(
        "gitlab-issues",
        ("Issue",),
        "GITLAB_URL",
        "gitlab_get_issues",
        federation_key="issue_iid",
    ),
    DataLocation(
        "gitlab-pipelines",
        ("Deployment",),
        "GITLAB_URL",
        "gitlab_get_pipelines",
        federation_key="pipeline_id",
    ),
    DataLocation(
        "gitlab-groups",
        ("Organization", "IdentityGroup", "IdentityUser"),
        "GITLAB_URL",
        "gitlab_get_groups",
        federation_key="group_id",
    ),
)

ROLES: tuple[BusinessRole, ...] = (
    BusinessRole(
        "release-manager",
        tasks=(
            "create-a-merge-request",
            "review-a-merge-request",
            "land-a-merge-request",
            "manage-approval-rules",
            "review-ci-results",
            "run-ci",
            "manage-pipeline-schedules",
            "manage-environments",
            "publish-a-release",
        ),
    ),
    BusinessRole(
        "project-administrator",
        tasks=(
            "find-projects-and-groups",
            "provision-a-project",
            "retire-a-project",
            "manage-protection",
            "manage-runners",
            "manage-deploy-tokens",
            "administer-users",
            "manage-wikis-and-snippets",
            "ingest-projects",
        ),
    ),
    BusinessRole(
        "triage-lead",
        tasks=("work-issues", "triage-vulnerabilities", "find-projects-and-groups"),
    ),
)
