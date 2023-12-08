from typing import Union, List
from pydantic import BaseModel, field_validator

try:
    from gitlab_api.decorators import require_auth
except ModuleNotFoundError:
    from decorators import require_auth
try:
    from gitlab_api.exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)
except ModuleNotFoundError:
    from exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)


class BranchModel(BaseModel):
    project_id: Union[int, str]
    branch: str = None
    reference: str = None

    @field_validator('branch', 'reference')
    def validate_required_parameters(cls, v, values):
        if 'project_id' in values and values['project_id'] is not None and v is not None:
            return v
        else:
            raise ValueError("Missing project_id field, it is required")


class CommitModel(BaseModel):
    project_id: Union[int, str]
    commit_hash: str = None
    branch: str = None
    dry_run: bool = None
    message: str = None
    state: str = None
    reference: str = None
    name: str = None
    context: str = None
    target_url: str = None
    description: str = None
    coverage: Union[float, str] = None
    pipeline_id: Union[int, str] = None
    actions: list = None
    start_branch: str = None
    start_sha: str = None
    start_project: Union[int, str] = None
    author_email: str = None
    author_name: str = None
    stats: bool = None
    force: bool = None
    line: int = None
    line_type: str = None
    note: str = None
    path: str = None
    group_ids: list = None
    protected_branch_ids: list = None
    report_type: str = None
    rule_type: str = None
    user_ids: list = None

    @field_validator('dry_run', 'stats', 'force')
    def validate_bool_fields(cls, v, values):
        if v is not None and not isinstance(v, bool):
            raise ParameterError
        return v

    @field_validator('project_id', 'commit_hash', 'branch', 'start_branch', 'start_sha', 'start_project',
                     'pipeline_id', 'line')
    def validate_optional_parameters(cls, v, values):
        if 'project_id' in values and values['project_id'] is not None and v is not None:
            return v
        else:
            raise MissingParameterError

    @field_validator('commit_hash', 'branch', 'reference', 'name', 'context', 'note', 'path', 'line_type')
    def validate_string_parameters(cls, v, values):
        if v is not None and not isinstance(v, str):
            raise ParameterError
        return v

    @field_validator('coverage')
    def validate_coverage(cls, v):
        if v is not None and not isinstance(v, (float, int)):
            raise ParameterError
        return v

    @field_validator('state')
    def validate_state(cls, v):
        if v is not None and v not in ['pending', 'running', 'success', 'failed', 'canceled']:
            raise ParameterError
        return v

    @field_validator('line_type')
    def validate_line_type(cls, v):
        if v is not None and v not in ['new', 'old']:
            raise ParameterError
        return v

    @field_validator('report_type')
    def validate_report_type(cls, v):
        if v is not None and v not in ['license_scanning', 'code_coverage']:
            raise ParameterError
        return v

    @field_validator('rule_type')
    def validate_rule_type(cls, v):
        if v is not None and v not in ['any_approver', 'regular']:
            raise ParameterError
        return v

    @field_validator('user_ids', 'group_ids', 'protected_branch_ids')
    def validate_list_parameters(cls, v):
        if v is not None and not isinstance(v, list):
            raise ParameterError
        return v

    @field_validator("data")
    def construct_data_dict(cls, values):
        data = {
            "branch": values.get("branch"),
            "commit_message": values.get("commit_message"),
            "start_branch": values.get("start_branch"),
            "start_sha": values.get("start_sha"),
            "start_project": values.get("start_project"),
            "actions": values.get("actions"),
            "author_email": values.get("author_email"),
            "author_name": values.get("author_name"),
            "stats": values.get("stats"),
            "force": values.get("force"),
            "note": values.get("note"),
            "path": values.get("path"),
            "line": values.get("line"),
            "line_type": values.get("line_type"),
            "state": values.get("state"),
            "ref": values.get("ref"),
            "name": values.get("name"),
            "context": values.get("context"),
            "target_url": values.get("target_url"),
            "description": values.get("description"),
            "coverage": values.get("coverage"),
            "pipeline_id": values.get("pipeline_id"),
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if not data:
            raise ValueError("At least one key is required in the data dictionary.")

        return data


class DeployTokenModel(BaseModel):
    project_id: Union[int, str] = None
    group_id: Union[int, str] = None
    token: str = None
    name: str = None
    expires_at: str = None
    username: str = None
    scopes: str = None

    @field_validator('expires_at')
    def validate_expires_at(cls, v):
        if v is not None and not isinstance(v, str):
            raise ParameterError
        return v

    @field_validator('project_id', 'group_id', 'token')
    def validate_optional_parameters(cls, v, values):
        if ('project_id' in values or 'group_id' in values) and v is not None:
            return v
        else:
            raise MissingParameterError

    @field_validator('name', 'username', 'scopes')
    def validate_string_parameters(cls, v):
        if v is not None and not isinstance(v, str):
            raise ParameterError
        return v

    @field_validator('scopes')
    def validate_scopes(cls, v):
        valid_scopes = ['read_repository', 'read_registry', 'write_registry', 'read_package_registry', 'write_package_registry']
        if v is not None and v not in valid_scopes:
            raise ParameterError
        return v


class GroupModel(BaseModel):
    group_id: Union[int, str] = None
    per_page: int = 100
    page: int = 1
    argument: str = 'state=opened'

    @field_validator('per_page', 'page')
    def validate_positive_integer(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ParameterError
        return v

    @field_validator('argument')
    def validate_argument(cls, v):
        if not isinstance(v, str):
            raise ParameterError
        return v

    @field_validator('group_id')
    def validate_group_id(cls, v):
        if v is None:
            raise MissingParameterError
        return v

    @field_validator("api_parameters")
    def build_api_parameters(cls, values):
        filters = []

        if values.get("page") is not None:
            filters.append(f'page={values["page"]}')

        if values.get("per_page") is not None:
            filters.append(f'per_page={values["per_page"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None


class ProjectModel(BaseModel):
    project_id: Union[int, str]
    allow_merge_on_skipped_pipeline: bool = None
    only_allow_merge_if_all_status_checks_passed: bool = None
    analytics_access_level: str = None
    approvals_before_merge: int = None
    auto_cancel_pending_pipelines: str = None
    auto_devops_deploy_strategy: str = None
    auto_devops_enabled: bool = None
    autoclose_referenced_issues: bool = None
    avatar: str = None
    build_git_strategy: str = None
    build_timeout: int = None
    builds_access_level: str = None
    ci_config_path: str = None
    ci_default_git_depth: int = None
    ci_forward_deployment_enabled: bool = None
    ci_allow_fork_pipelines_to_run_in_parent_project: bool = None
    ci_separated_caches: bool = None
    container_expiration_policy_attributes: str = None
    container_registry_access_level: str = None
    default_branch: str = None
    description: str = None
    emails_disabled: bool = None
    enforce_auth_checks_on_uploads: bool = None
    external_authorization_classification_label: str = None
    forking_access_level: str = None
    import_url: str = None
    issues_access_level: str = None
    issues_template: str = None
    keep_latest_artifact: bool = None
    lfs_enabled: bool = None
    merge_commit_template: str = None
    merge_method: str = None
    merge_pipelines_enabled: bool = None
    merge_requests_access_level: str = None
    merge_requests_template: str = None
    merge_trains_enabled: bool = None
    mirror_overwrites_diverged_branches: bool = None
    mirror_trigger_builds: bool = None
    mirror_user_id: int = None
    mirror: bool = None
    mr_default_target_self: bool = None
    name: str = None
    only_allow_merge_if_all_discussions_are_resolved: bool = None
    only_allow_merge_if_pipeline_succeeds: bool = None
    only_mirror_protected_branches: bool = None
    operations_access_level: str = None
    packages_enabled: bool = None
    pages_access_level: str = None
    path: str = None
    printing_merge_request_link_enabled: bool = None
    public_builds: bool = None
    releases_access_level: str = None
    remove_source_branch_after_merge: bool = None
    repository_access_level: str = None
    repository_storage: str = None
    request_access_enabled: bool = None
    requirements_access_level: str = None
    resolve_outdated_diff_discussions: bool = None
    restrict_user_defined_variables: bool = None
    security_and_compliance_access_level: str = None
    service_desk_enabled: bool = None
    shared_runners_enabled: bool = None
    snippets_access_level: str = None
    squash_commit_template: str = None
    squash_option: str = None
    suggestion_commit_message: str = None
    tag_list: List[str] = None
    topics: List[str] = None
    visibility: str = None
    wiki_access_level: str = None

    @field_validator("analytics_access_level", "builds_access_level", "container_registry_access_level",
                     "forking_access_level", "issues_access_level", "operations_access_level", "pages_access_level",
                     "releases_access_level", "repository_access_level", "requirements_access_level",
                     "security_and_compliance_access_level", "snippets_access_level", "wiki_access_level")
    def validate_access_level(cls, value):
        valid_access_levels = ['disabled', 'private', 'enabled']
        if value and value not in valid_access_levels:
            raise ValueError("Invalid access level value")
        return value

    @field_validator("auto_cancel_pending_pipelines", "auto_devops_deploy_strategy",
                     "mirror_overwrites_diverged_branches",
                     "mirror_trigger_builds", "mr_default_target_self",
                     "only_allow_merge_if_all_discussions_are_resolved",
                     "only_allow_merge_if_pipeline_succeeds", "only_mirror_protected_branches", "auto_devops_enabled",
                     "autoclose_referenced_issues", "emails_disabled", "enforce_auth_checks_on_uploads",
                     "ci_forward_deployment_enabled", "ci_allow_fork_pipelines_to_run_in_parent_project",
                     "ci_separated_caches", "keep_latest_artifact", "lfs_enabled", "merge_pipelines_enabled",
                     "merge_trains_enabled", "printing_merge_request_link_enabled", "public_builds",
                     "remove_source_branch_after_merge", "request_access_enabled", "resolve_outdated_diff_discussions",
                     "restrict_user_defined_variables", "service_desk_enabled", "shared_runners_enabled",
                     "packages_enabled")
    def validate_boolean(cls, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("Invalid boolean value")
        return value

    @field_validator("approvals_before_merge", "build_timeout", "ci_default_git_depth", "mirror_user_id")
    def validate_positive_integer(cls, value):
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError("Invalid positive integer value")
        return value

    @field_validator("tag_list", "topics")
    def validate_tag_topics(cls, value):
        if value is not None and not all(isinstance(tag, str) for tag in value):
            raise ValueError("Invalid tag or topic value")
        return value


class MergeRequestModel(BaseModel):
    approved_by_ids: List[int] = None
    approver_ids: List[int] = None
    assignee_id: int = None
    author_id: int = None
    author_username: str = None
    created_after: str = None
    created_before: str = None
    deployed_after: str = None
    deployed_before: str = None
    environment: str = None
    search_in: str = None
    labels: str = None
    milestone: str = None
    my_reaction_emoji: str = None
    search_exclude: str = None
    order_by: str = None
    reviewer_id: Union[int, str] = None
    reviewer_username: str = None
    scope: List[str] = None
    search: str = None
    sort: str = None
    source_branch: str = None
    state: str = None
    target_branch: str = None
    updated_after: str = None
    updated_before: str = None
    view: str = None
    with_labels_details: bool = None
    with_merge_status_recheck: bool = None
    wip: str = None
    max_pages: int = 0
    per_page: int = 100

    @field_validator("api_parameters")
    def build_api_parameters(cls, values):
        filters = []

        if values.get("approved_by_ids") is not None:
            filters.append(f'approved_by_ids={values["approved_by_ids"]}')

        if values.get("approver_ids") is not None:
            filters.append(f'approver_ids={values["approver_ids"]}')

        if values.get("assignee_id") is not None:
            filters.append(f'assignee_id={values["assignee_id"]}')

        if values.get("author_id") is not None:
            filters.append(f'author_id={values["author_id"]}')

        if values.get("author_username") is not None:
            filters.append(f'author_username={values["author_username"]}')

        if values.get("created_after") is not None:
            filters.append(f'created_after={values["created_after"]}')

        if values.get("deployed_after") is not None:
            filters.append(f'deployed_after={values["deployed_after"]}')

        if values.get("deployed_before") is not None:
            filters.append(f'deployed_before={values["deployed_before"]}')

        if values.get("environment") is not None:
            filters.append(f'environment={values["environment"]}')

        if values.get("search_in") is not None:
            filters.append(f'search_in={values["search_in"]}')

        if values.get("labels") is not None:
            filters.append(f'labels={values["labels"]}')

        if values.get("milestone") is not None:
            filters.append(f'milestone={values["milestone"]}')

        if values.get("my_reaction_emoji") is not None:
            filters.append(f'my_reaction_emoji={values["my_reaction_emoji"]}')

        if values.get("search_exclude") is not None:
            filters.append(f'search_exclude={values["search_exclude"]}')

        if values.get("order_by") is not None:
            filters.append(f'order_by={values["order_by"]}')

        if values.get("reviewer_id") is not None:
            filters.append(f'reviewer_id={values["reviewer_id"]}')

        if values.get("reviewer_username") is not None:
            filters.append(f'reviewer_username={values["reviewer_username"]}')

        if values.get("scope") is not None:
            filters.append(f'scope={values["scope"]}')

        if values.get("search") is not None:
            filters.append(f'search={values["search"]}')

        if values.get("sort") is not None:
            filters.append(f'sort={values["sort"]}')

        if values.get("source_branch") is not None:
            filters.append(f'source_branch={values["source_branch"]}')

        if values.get("state") is not None:
            filters.append(f'state={values["state"]}')

        if values.get("target_branch") is not None:
            filters.append(f'target_branch={values["target_branch"]}')

        if values.get("updated_after") is not None:
            filters.append(f'updated_after={values["updated_after"]}')

        if values.get("updated_before") is not None:
            filters.append(f'updated_before={values["updated_before"]}')

        if values.get("view") is not None:
            filters.append(f'view={values["view"]}')

        if values.get("with_labels_details") is not None:
            filters.append(f'with_labels_details={values["with_labels_details"]}')

        if values.get("with_merge_status_recheck") is not None:
            filters.append(f'with_merge_status_recheck={values["with_merge_status_recheck"]}')

        if values.get("wip") is not None:
            filters.append(f'wip={values["wip"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None

    @field_validator("scope")
    def validate_scope(cls, value):
        valid_scopes = ['created_by_me', 'assigned_to_me', 'all']
        if value and not all(scope in valid_scopes for scope in value):
            raise ValueError("Invalid scope values")
        return value

    @field_validator("search_in")
    def validate_search_in(cls, value):
        valid_search_in = ['title', 'description', 'title,description']
        if value and value not in valid_search_in:
            raise ValueError("Invalid search_in value")
        return value

    @field_validator("search_exclude")
    def validate_search_exclude(cls, value):
        valid_search_exclude = ['labels', 'milestone', 'author_id', 'assignee_id', 'author_username',
                                'reviewer_id', 'reviewer_username', 'my_reaction_emoji']
        if value and value not in valid_search_exclude:
            raise ValueError("Invalid search_exclude value")
        return value

    @field_validator("state")
    def validate_state(cls, value):
        valid_states = ['opened', 'closed', 'locked', 'merged']
        if value and value not in valid_states:
            raise ValueError("Invalid state value")
        return value

    @field_validator("sort")
    def validate_sort(cls, value):
        valid_sorts = ['asc', 'desc']
        if value and value not in valid_sorts:
            raise ValueError("Invalid sort value")
        return value

    @field_validator("wip")
    def validate_wip(cls, value):
        valid_wip_values = ['yes', 'no']
        if value and value not in valid_wip_values:
            raise ValueError("Invalid wip value")
        return value


class MergeRequestRuleModel(BaseModel):
    project_id: Union[int, str] = None
    approval_rule_id: Union[int, str] = None
    approvals_required: int = None
    name: str = None
    applies_to_all_protected_branches: bool = None
    group_ids: List[int] = None
    protected_branch_ids: List[int] = None
    report_type: str = None
    rule_type: str = None
    user_ids: List[int] = None

    @field_validator("project_id", "approvals_required", "name")
    def check_required_fields(cls, value):
        if value is None:
            raise ValueError("This field is required.")
        return value

    @field_validator("report_type")
    def validate_report_type(cls, value):
        if value not in ['license_scanning', 'code_coverage']:
            raise ValueError("Invalid report_type")
        return value

    @field_validator("rule_type")
    def validate_rule_type(cls, value):
        if value not in ['any_approver', 'regular']:
            raise ValueError("Invalid rule_type")
        return value

    @field_validator("approval_rule_id")
    def validate_approval_rule_id(cls, value, values):
        # Validate presence of approval_rule_id when creating rules
        if values.get("approvals_required") is not None and value is None:
            raise ValueError("approval_rule_id is required when creating rules.")
        return value

    @field_validator("data")
    def construct_data_dict(cls, values):
        data = {
            "approvals_required": values.get("approvals_required"),
            "name": values.get("name"),
            "applies_to_all_protected_branches": values.get("applies_to_all_protected_branches"),
            "group_ids": values.get("group_ids"),
            "protected_branch_ids": values.get("protected_branch_ids"),
            "report_type": values.get("report_type"),
            "rule_type": values.get("rule_type"),
            "user_ids": values.get("user_ids"),
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if not data:
            raise ValueError("At least one key is required in the data dictionary.")

        return data
