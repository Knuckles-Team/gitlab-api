#!/usr/bin/python
# coding: utf-8

from typing import Union, List, Dict, Optional, Any, TypeVar, Generic

import requests
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
    HttpUrl,
    EmailStr,
)
from datetime import datetime


class IssueStats(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="IssueStats")
    total: Optional[int] = Field(default=None, description="Total number of issues")
    closed: Optional[int] = Field(default=None, description="Number of closed issues")
    opened: Optional[int] = Field(default=None, description="Number of opened issues")


class Milestone(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Milestone")
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the milestone"
    )
    iid: Optional[int] = Field(
        default=None, description="Internal ID for the milestone"
    )
    project_id: Optional[int] = Field(
        default=None, description="ID of the project the milestone belongs to"
    )
    title: Optional[str] = Field(default=None, description="Title of the milestone")
    description: Optional[str] = Field(
        default=None, description="Description of the milestone"
    )
    state: Optional[str] = Field(
        default=None, description="State of the milestone (e.g., active, closed)"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the milestone was created"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the milestone was last updated"
    )
    due_date: Optional[str] = Field(
        default=None, description="Due date for the milestone"
    )
    start_date: Optional[str] = Field(
        default=None, description="Start date for the milestone"
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL to the milestone in GitLab"
    )
    closed_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the milestone was closed."
    )
    issue_stats: Optional[IssueStats] = Field(
        default=None, description="Statistics of issues related to the milestone"
    )


class TimeStats(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="TimeStats")
    time_estimate: Optional[int] = Field(
        default=None,
        description="Estimated time to complete the merge request (in seconds)",
    )
    total_time_spent: Optional[int] = Field(
        default=None, description="Total time spent on the merge request (in seconds)"
    )
    human_time_estimate: Optional[str] = Field(
        default=None,
        description="Human-readable estimated time to complete the merge request",
    )
    human_total_time_spent: Optional[str] = Field(
        default=None, description="Human-readable total time spent on the merge request"
    )


class TaskCompletionStatus(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="TaskCompletionStatus")
    count: Optional[int] = Field(
        default=None, description="Total number of tasks in the merge request"
    )
    completed_count: Optional[int] = Field(
        default=None, description="Number of completed tasks in the merge request"
    )


class References(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="References")
    short: Optional[str] = Field(
        default=None, description="Short reference of the merge request"
    )
    relative: Optional[str] = Field(
        default=None, description="Relative reference of the merge request"
    )
    full: Optional[str] = Field(
        default=None, description="Full reference of the merge request"
    )


class Artifact(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Artifact")
    file_type: Optional[str] = Field(
        default=None, description="Type of the artifact file."
    )
    size: Optional[int] = Field(default=None, description="Size of the artifact file.")
    filename: Optional[str] = Field(
        default=None, description="Filename of the artifact file."
    )
    file_format: Optional[str] = Field(
        default=None, description="Format of the artifact file."
    )


class ArtifactsFile(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="ArtifactsFile")
    filename: Optional[str] = Field(
        default=None, description="Filename of the artifacts file."
    )
    size: Optional[int] = Field(default=None, description="Size of the artifacts file.")


class RunnerManager(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="RunnerManager")
    id: Optional[int] = Field(default=None, description="ID of the runner manager.")
    system_id: Optional[str] = Field(
        default=None, description="System ID of the runner manager."
    )
    version: Optional[str] = Field(
        default=None, description="Version of the runner manager."
    )
    revision: Optional[str] = Field(
        default=None, description="Revision of the runner manager."
    )
    platform: Optional[str] = Field(
        default=None, description="Platform of the runner manager."
    )
    architecture: Optional[str] = Field(
        default=None, description="Architecture of the runner manager."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the runner manager was created."
    )
    contacted_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the runner manager was last contacted.",
    )
    ip_address: Optional[str] = Field(
        default=None, description="IP address of the runner manager."
    )
    status: Optional[str] = Field(
        default=None, description="Status of the runner manager."
    )


class Configuration(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Configuration")
    approvals_before_merge: Optional[int] = Field(
        default=None, description="Number of approvals required before merge"
    )
    reset_approvals_on_push: Optional[bool] = Field(
        default=None, description="Whether approvals reset on new push"
    )
    selective_code_owner_removals: Optional[bool] = Field(
        default=None, description="Whether selective code owner removals are allowed"
    )
    disable_overriding_approvers_per_merge_request: Optional[bool] = Field(
        default=None,
        description="Whether overriding approvers per merge request is disabled",
    )
    merge_requests_author_approval: Optional[bool] = Field(
        default=None, description="Whether authors can approve their own merge requests"
    )
    merge_requests_disable_committers_approval: Optional[bool] = Field(
        default=None, description="Whether committers are disabled from approving"
    )
    require_password_to_approve: Optional[bool] = Field(
        default=None, description="Whether a password is required to approve"
    )
    require_reauthentication_to_approve: Optional[bool] = Field(
        default=None,
        description="Require reauthentication to approve (replacement for require_password_to_approve).",
    )


class Iteration(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Iteration")
    id: Optional[int] = Field(default=None)
    iid: Optional[int] = Field(default=None)
    sequence: Optional[int] = Field(default=None)
    group_id: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    state: Optional[int] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    due_date: Optional[str] = Field(default=None)
    web_url: Optional[Union[HttpUrl, str]] = Field(default=None)


class Identity(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Identity")
    provider: Optional[str] = Field(default=None, description="The external provider.")
    extern_uid: Optional[str] = Field(
        default=None, description="The external authentication provider UID."
    )


class GroupSamlIdentity(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="GroupSamlIdentity")
    extern_uid: Optional[str] = Field(
        default=None, description="External UID of the SAML identity"
    )
    provider: Optional[str] = Field(
        default=None, description="Provider of the SAML identity"
    )
    saml_provider_id: Optional[int] = Field(
        default=None, description="ID of the SAML provider"
    )


class User(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="User")
    id: Optional[int] = Field(default=None, description="The unique ID of the user.")
    username: Optional[str] = Field(
        default=None, description="The username of the user."
    )
    user: Optional[str] = Field(default=None, description="The user.")
    email: Optional[Union[EmailStr, str]] = Field(
        default=None, description="The email of the user."
    )
    name: Optional[str] = Field(default=None, description="The name of the user.")
    state: Optional[str] = Field(
        default=None, description="The state of the user (e.g., active, blocked)."
    )
    locked: Optional[bool] = Field(
        default=None, description="Indicates if the user is locked."
    )
    avatar_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The URL of the user's avatar."
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The URL of the user's web profile."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="The creation date of the user."
    )
    is_admin: Optional[bool] = Field(
        default=None, description="Indicates if the user is an administrator."
    )
    bio: Optional[str] = Field(default=None, description="The bio of the user.")
    location: Optional[str] = Field(
        default=None, description="The location of the user."
    )
    skype: Optional[str] = Field(default=None, description="The Skype ID of the user.")
    linkedin: Optional[str] = Field(
        default=None, description="The LinkedIn ID of the user."
    )
    twitter: Optional[str] = Field(
        default=None, description="The Twitter handle of the user."
    )
    discord: Optional[str] = Field(
        default=None, description="The Discord ID of the user."
    )
    website_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The website URL of the user."
    )
    organization: Optional[str] = Field(
        default=None, description="The organization the user belongs to."
    )
    job_title: Optional[str] = Field(
        default=None, description="The job title of the user."
    )
    last_sign_in_at: Optional[datetime] = Field(
        default=None, description="The last sign-in date of the user."
    )
    confirmed_at: Optional[datetime] = Field(
        default=None, description="The date the user was confirmed."
    )
    theme_id: Optional[int] = Field(
        default=None, description="The theme ID of the user's profile."
    )
    last_activity_on: Optional[datetime] = Field(
        default=None, description="The last activity date of the user."
    )
    color_scheme_id: Optional[int] = Field(
        default=None, description="The color scheme ID of the user's profile."
    )
    projects_limit: Optional[int] = Field(
        default=None, description="The project limit for the user."
    )
    current_sign_in_at: Optional[datetime] = Field(
        default=None, description="The current sign-in date of the user."
    )
    note: Optional[str] = Field(default=None, description="A note about the user.")
    identities: Optional[List[Identity]] = Field(
        default=None,
        description="List of external identities associated with the user.",
    )
    can_create_group: Optional[bool] = Field(
        default=None, description="Indicates if the user can create groups."
    )
    can_create_project: Optional[bool] = Field(
        default=None, description="Indicates if the user can create projects."
    )
    two_factor_enabled: Optional[bool] = Field(
        default=None, description="Indicates if two-factor authentication is enabled."
    )
    external: Optional[bool] = Field(
        default=None, description="Indicates if the user is external."
    )
    private_profile: Optional[bool] = Field(
        default=None, description="Indicates if the user's profile is private."
    )
    current_sign_in_ip: Optional[str] = Field(
        default=None, description="The current sign-in IP of the user."
    )
    last_sign_in_ip: Optional[str] = Field(
        default=None, description="The last sign-in IP of the user."
    )
    namespace_id: Optional[int] = Field(
        default=None, description="The namespace ID of the user."
    )
    created_by: Optional[Union[int, "User"]] = Field(
        default=None, description="The ID of the user who created this user."
    )
    email_reset_offered_at: Optional[datetime] = Field(
        default=None, description="The date when an email reset was offered."
    )
    expires_at: Optional[datetime] = Field(
        default=None, description="Timestamp of when the member's access expires"
    )
    access_level: Optional[int] = Field(
        default=None, description="Access level of the member"
    )
    group_saml_identity: Optional[GroupSamlIdentity] = Field(
        default=None, description="SAML identity details of the member"
    )
    approved: Optional[bool] = Field(
        default=None, description="Approval status of the pending member"
    )
    invited: Optional[bool] = Field(
        default=None, description="Invitation status of the pending member"
    )
    public_email: Optional[str] = Field(
        None, description="Public email address of the user"
    )
    pronouns: Optional[str] = Field(None, description="Pronouns of the user")
    bot: Optional[bool] = Field(
        default=None, description="Indicates if the user is a bot"
    )
    work_information: Optional[str] = Field(
        None, description="Work information of the user"
    )
    followers: Optional[int] = Field(
        default=None, description="Number of followers the user has"
    )
    following: Optional[int] = Field(
        default=None, description="Number of people the user is following"
    )
    local_time: Optional[str] = Field(None, description="Local time of the user")
    commit_email: Optional[str] = Field(
        default=None, description="Commit email address of the user"
    )
    shared_runners_minutes_limit: Optional[int] = Field(
        None, description="Shared runners minutes limit for the user"
    )
    extra_shared_runners_minutes_limit: Optional[int] = Field(
        None, description="Extra shared runners minutes limit"
    )
    membership_type: Optional[str] = Field(None, description="Membership type")
    removable: Optional[bool] = Field(
        default=None, description="Whether or not the members are removable"
    )
    last_login_at: Optional[datetime] = Field(
        default=None, description="The last login-in date of the user."
    )

    @field_validator("identities", mode="before")
    def validate_tags(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            identities = []
            for item in v:
                identities.append(Identity(**item))
            return identities
        return v


class Namespace(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Namespace")
    id: Optional[int] = Field(default=None, description="The ID of the namespace.")
    name: Optional[str] = Field(default=None, description="The name of the namespace.")
    path: Optional[str] = Field(default=None, description="The path of the namespace.")
    kind: Optional[str] = Field(default=None, description="The kind of the namespace.")
    full_path: Optional[str] = Field(
        default=None, description="The full path of the namespace."
    )
    parent_id: Optional[int] = Field(
        default=None, description="The parent ID of the namespace, if any."
    )
    root_repository_size: Optional[int] = Field(
        default=None, description="The root repository size."
    )
    projects_count: Optional[int] = Field(
        default=None, description="The project count."
    )
    avatar_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The avatar URL of the namespace."
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The web URL of the namespace."
    )
    members_count_with_descendants: Optional[int] = Field(
        default=None, description="Number of descendant members"
    )
    billable_members_count: Optional[int] = Field(
        default=None, description="The Billable members count of the namespace, if any."
    )
    plan: Optional[str] = Field(default=None, description="Plan of the Namespace")
    trial_ends_on: Optional[datetime] = Field(
        default=None, description="The date the Trial ends"
    )
    trial: Optional[bool] = Field(
        default=None, description="Indicates if the namespace is a trial"
    )


class ContainerExpirationPolicy(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="ContainerExpirationPolicy")
    cadence: Optional[str] = Field(
        default=None, description="The cadence of the expiration policy."
    )
    enabled: Optional[bool] = Field(
        default=None, description="Whether the expiration policy is enabled."
    )
    keep_n: Optional[int] = Field(default=None, description="Number of items to keep.")
    older_than: Optional[str] = Field(
        default=None, description="Items older than this will be removed."
    )
    name_regex: Optional[str] = Field(default=None, description="Regex to match names.")
    name_regex_keep: Optional[str] = Field(
        default=None, description="Regex to match names to keep."
    )
    next_run_at: Optional[datetime] = Field(
        default=None, description="The next run time of the policy."
    )


class Permissions(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Permissions")
    project_access: Optional[Dict] = Field(
        default=None, description="Project access level and notification settings."
    )
    group_access: Optional[Dict] = Field(
        default=None, description="Group access level and notification settings."
    )


class Statistics(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Statistics")
    commit_count: Optional[int] = Field(
        default=None, description="The number of commits in the project."
    )
    storage_size: Optional[int] = Field(
        default=None, description="The total storage size of the project."
    )
    repository_size: Optional[int] = Field(
        default=None, description="The size of the repository."
    )
    wiki_size: Optional[int] = Field(default=None, description="The size of the wiki.")
    lfs_objects_size: Optional[int] = Field(
        default=None, description="The size of LFS objects."
    )
    job_artifacts_size: Optional[int] = Field(
        default=None, description="The size of job artifacts."
    )
    pipeline_artifacts_size: Optional[int] = Field(
        default=None, description="The size of pipeline artifacts."
    )
    packages_size: Optional[int] = Field(
        default=None, description="The size of packages."
    )
    snippets_size: Optional[int] = Field(
        default=None, description="The size of snippets."
    )
    uploads_size: Optional[int] = Field(
        default=None, description="The size of uploads."
    )


class Diff(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Diff")
    id: Optional[int] = Field(default=None, description="The ID of the Diff")
    merge_request_id: Optional[int] = Field(
        default=None, description="The merge request ID"
    )
    head_commit_sha: Optional[str] = Field(
        default=None, description="The head commit sha"
    )
    base_commit_sha: Optional[str] = Field(
        default=None, description="The base commit sha"
    )
    start_commit_sha: Optional[str] = Field(
        default=None, description="The start commit sha"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Creation date of the note"
    )
    state: Optional[str] = Field(default=None, description="The state of the Diff")
    real_size: Optional[str] = Field(
        default=None, description="The real size of the Diff"
    )
    patch_id_sha: Optional[str] = Field(
        default=None, description="The patch ID of the sha"
    )
    diff: Optional[str] = Field(default=None, description="The diff of the commit")
    new_path: Optional[str] = Field(
        default=None, description="The new path of the file"
    )
    old_path: Optional[str] = Field(
        default=None, description="The old path of the file"
    )
    a_mode: Optional[str] = Field(
        default=None, description="The file mode for the old file"
    )
    b_mode: Optional[str] = Field(
        default=None, description="The file mode for the new file"
    )
    new_file: Optional[bool] = Field(
        default=None, description="Whether this is a new file"
    )
    renamed_file: Optional[bool] = Field(
        default=None, description="Whether this file was renamed"
    )
    deleted_file: Optional[bool] = Field(
        default=None, description="Whether this file was deleted"
    )
    generated_file: Optional[bool] = Field(
        default=None, description="Whether this file was generated"
    )


class DetailedStatus(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="DetailedStatus")
    icon: Optional[str] = Field(
        default=None, description="The icon representing the status."
    )
    text: Optional[str] = Field(
        default=None, description="The text describing the status."
    )
    label: Optional[str] = Field(default=None, description="The label of the status.")
    group: Optional[str] = Field(
        default=None, description="The group to which this status belongs."
    )
    tooltip: Optional[str] = Field(
        default=None, description="The tooltip text for the status."
    )
    has_details: Optional[bool] = Field(
        default=None, description="Indicates if the status has details."
    )
    details_path: Optional[str] = Field(
        default=None, description="The path to the details of the status."
    )
    illustration: Optional[Any] = Field(
        default=None, description="The illustration object related to the status."
    )
    favicon: Optional[str] = Field(
        default=None, description="The URL to the favicon representing the status."
    )


class PipelineSchedule(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="PipelineSchedule")
    id: Optional[int] = Field(default=None, description="ID of the pipeline schedule")
    description: Optional[str] = Field(
        default=None, description="Description of the schedule"
    )
    ref: Optional[str] = Field(
        default=None, description="Git reference (e.g., refs/heads/main)"
    )
    cron: Optional[str] = Field(
        default=None, description="Cron expression for scheduling"
    )
    cron_timezone: Optional[str] = Field(
        default=None, description="Timezone for the cron schedule"
    )
    next_run_at: Optional[datetime] = Field(
        default=None, description="Next scheduled run time"
    )
    active: bool = Field(default=True, description="Whether the schedule is active")
    created_at: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update timestamp"
    )
    owner: Optional[User] = Field(
        default=None, description="Owner of the pipeline schedule"
    )
    last_pipeline: Optional["Pipeline"] = Field(
        default=None, description="Last pipeline triggered by this schedule"
    )
    variables: Optional[List["PipelineVariable"]] = Field(
        default=None, description="List of variables for the schedule"
    )


class Pipeline(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Pipeline")
    id: Optional[int] = Field(default=None, description="ID of the pipeline")
    iid: Optional[int] = Field(
        default=None, description="The internal ID of the pipeline."
    )
    ref: Optional[str] = Field(
        default=None, description="Reference name of the pipeline"
    )
    sha: Optional[str] = Field(default=None, description="SHA of the pipeline")
    status: Optional[str] = Field(default=None, description="Status of the pipeline")
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL for the pipeline"
    )
    project_id: Optional[int] = Field(
        default=None, description="The ID of the project associated with the pipeline."
    )
    before_sha: Optional[str] = Field(
        default=None, description="The commit SHA before the current one."
    )
    tag: Optional[bool] = Field(
        default=None, description="Indicates if the pipeline is for a tag."
    )
    yaml_errors: Optional[str] = Field(
        default=None,
        description="Errors encountered in the pipeline YAML configuration.",
    )
    user: Optional[User] = Field(
        default=None, description="The user who triggered the pipeline."
    )
    created_at: Optional[str] = Field(
        default=None, description="Timestamp when the pipeline was created."
    )
    updated_at: Optional[str] = Field(
        default=None, description="Timestamp when the pipeline was last updated."
    )
    started_at: Optional[str] = Field(
        default=None, description="Timestamp when the pipeline started."
    )
    finished_at: Optional[str] = Field(
        default=None, description="Timestamp when the pipeline finished."
    )
    committed_at: Optional[str] = Field(
        default=None, description="Timestamp when the pipeline was committed."
    )
    duration: Optional[float] = Field(
        default=None, description="The duration of the pipeline in seconds."
    )
    queued_duration: Optional[float] = Field(
        default=None, description="The duration the pipeline spent in the queue."
    )
    coverage: Optional[str] = Field(
        default=None, description="The code coverage percentage."
    )
    name: Optional[str] = Field(default=None, description="The name of the pipeline.")
    source: Optional[str] = Field(
        default=None, description="The source of the pipeline (e.g., push, web)."
    )
    detailed_status: Optional[DetailedStatus] = Field(
        default=None, description="The detailed status of the pipeline."
    )


class PackageLink(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="PackageLink")
    web_path: Optional[str] = Field(
        default=None, description="Web path to access the package"
    )
    delete_api_path: Optional[str] = Field(
        default=None, description="API path to delete the package"
    )


class PackageVersion(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="PackageVersion")
    id: Optional[int] = Field(default=None, description="Version ID of the package")
    version: Optional[str] = Field(default=None, description="Version of the package")
    created_at: Optional[datetime] = Field(
        default=None, description="Creation date and time of the package version"
    )
    pipelines: Optional[List[Pipeline]] = Field(
        default=None,
        description="List of pipelines associated with the package version",
    )

    @field_validator("pipelines", mode="before")
    def validate_pipelines(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            pipelines = []
            for item in v:
                pipelines.append(Pipeline(**item))
            return pipelines
        return v


class Package(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Package")
    id: Optional[int] = Field(default=None, description="Package ID")
    name: Optional[str] = Field(default=None, description="Name of the package")
    version: Optional[str] = Field(default=None, description="Version of the package")
    package_type: Optional[str] = Field(
        default=None, description="Type of the package (e.g., maven, npm, conan)"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Creation date and time of the package"
    )
    last_downloaded_at: Optional[datetime] = Field(
        default=None, description="Last downloaded date and time of the package"
    )
    conan_package_name: Optional[str] = Field(
        default=None, description="Conan package name if applicable"
    )
    links: Optional[PackageLink] = Field(
        default=None, alias="_links", description="Links related to the package"
    )
    pipelines: Optional[List[Pipeline]] = Field(
        default=None, description="List of pipelines associated with the package"
    )
    tags: Optional[List["Tag"]] = Field(
        default=None, description="List of tags associated with the package"
    )
    versions: Optional[List[PackageVersion]] = Field(
        default=None, description="List of different versions of the package"
    )
    package_id: Optional[int] = Field(
        default=None, description="ID of the package this file belongs to"
    )
    file_name: Optional[str] = Field(
        default=None, description="Name of the package file"
    )
    size: Optional[int] = Field(
        default=None, description="Size of the package file in bytes"
    )
    file_md5: Optional[str] = Field(
        default=None, description="MD5 checksum of the package file"
    )
    file_sha1: Optional[str] = Field(
        default=None, description="SHA-1 checksum of the package file"
    )
    file_sha256: Optional[str] = Field(
        default=None, description="SHA-256 checksum of the package file"
    )

    @field_validator("pipelines", mode="before")
    def validate_pipelines(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            pipelines = []
            for item in v:
                pipelines.append(Pipeline(**item))
            return pipelines
        return v

    @field_validator("tags", mode="before")
    def validate_tags(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            tags = []
            for item in v:
                tags.append(Tag(tag=item))
            return tags
        if isinstance(v, str):
            tags = [Tag(tag=v)]
            return tags
        return v


class Contributor(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Contributor")
    name: str = Field(default=None, description="The name of the contributor.")
    email: Union[EmailStr, str] = Field(
        default=None, description="The email of the contributor."
    )
    commits: int = Field(default=None, description="Number of commits from contributor")
    additions: int = Field(
        default=None, description="Number of additions from contributor"
    )
    deletions: int = Field(
        default=None, description="Number of deletions from contributor"
    )


class CommitStats(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="CommitStats")
    additions: Optional[int] = Field(
        default=None, description="Number of additions in the commit"
    )
    deletions: Optional[int] = Field(
        default=None, description="Number of deletions in the commit"
    )
    total: Optional[int] = Field(
        default=None, description="Total number of changes in the commit"
    )


class CommitSignature(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="CommitSignature")
    signature_type: Optional[str] = Field(
        default=None, description="Type of the signature"
    )
    verification_status: Optional[str] = Field(
        default=None, description="Verification status of the signature"
    )
    commit_source: Optional[str] = Field(
        default=None, description="Source of the commit"
    )
    gpg_key_id: Optional[int] = Field(default=None, description="ID of the GPG key")
    gpg_key_primary_keyid: Optional[str] = Field(
        default=None, description="Primary key ID of the GPG key"
    )
    gpg_key_user_name: Optional[str] = Field(
        default=None, description="User name of the GPG key owner"
    )
    gpg_key_user_email: Optional[str] = Field(
        default=None, description="User email of the GPG key owner"
    )
    gpg_key_subkey_id: Optional[str] = Field(
        default=None, description="Subkey ID of the GPG key"
    )
    key: Optional[Dict[str, Any]] = Field(default=None, description="SSH key details")
    x509_certificate: Optional[Dict[str, Any]] = Field(
        default=None, description="X509 certificate details"
    )
    message: Optional[str] = Field(
        default=None, description="The message from the signature response."
    )


class Comment(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Comment")
    id: Optional[int] = Field(default=None, description="ID of the note")
    type: Optional[str] = Field(default=None, description="Type of the note")
    body: Optional[str] = Field(default=None, description="Body content of the note")
    note: Optional[str] = Field(default=None, description="Content of the note")
    attachment: Optional[Any] = Field(
        default=None, description="Attachment associated with the note"
    )
    author: Optional[User] = Field(default=None, description="Author of the note")
    created_at: Optional[datetime] = Field(
        default=None, description="Creation date of the note"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update date of the note"
    )
    system: Optional[bool] = Field(
        default=None, description="Whether the note is a system note"
    )
    notable_id: Optional[int] = Field(
        default=None, description="ID of the notable entity", alias="noteable_id"
    )
    notable_type: Optional[str] = Field(
        default=None, description="Type of the notable entity", alias="noteable_type"
    )
    resolvable: Optional[bool] = Field(
        default=None, description="Whether the note is resolvable"
    )
    confidential: Optional[bool] = Field(
        default=None, description="Whether the note is confidential"
    )
    notable_iid: Optional[int] = Field(
        default=None, description="IID of the notable entity", alias="noteable_iid"
    )
    commands_changes: Optional[Dict[str, Any]] = Field(
        default=None, description="Command changes associated with the note"
    )
    line_type: Optional[str] = Field(default=None, description="Line type")
    path: Optional[str] = Field(default=None, description="Path")
    line: Optional[int] = Field(default=None, description="Line in note")


class ParentID(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="ParentID")
    parent_id: str = Field(default=None, description="Parent ID")


class Commit(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Commit")
    id: Optional[Union[str, int]] = Field(default=None, description="The commit ID.")
    short_id: Optional[str] = Field(
        default=None, description="A shortened version of the commit ID."
    )
    started_at: Optional[datetime] = Field(
        default=None, description="The start date of the commit."
    )
    finished_at: Optional[datetime] = Field(
        default=None, description="The finished date of the commit."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="The creation date of the commit."
    )
    parent_ids: Optional[List[ParentID]] = Field(
        default=None, description="A list of parent commit IDs."
    )
    title: Optional[str] = Field(default=None, description="The title of the commit.")
    description: Optional[str] = Field(
        default=None, description="The commit description."
    )
    message: Optional[str] = Field(
        default=None, description="The name of the commit author."
    )
    author: Optional[User] = Field(
        default=None, description="The author of the commit."
    )
    author_name: Optional[str] = Field(
        default=None, description="The name of the commit author."
    )
    author_email: Optional[str] = Field(
        default=None, description="The email of the commit author."
    )
    authored_date: Optional[datetime] = Field(
        default=None, description="The date the commit was authored."
    )
    committer_name: Optional[str] = Field(
        default=None, description="The name of the committer."
    )
    committer_email: Optional[Union[EmailStr, str]] = Field(
        default=None, description="The email of the committer."
    )
    committed_date: Optional[datetime] = Field(
        default=None, description="The date the commit was committed."
    )
    name: Optional[str] = Field(default=None, description="The name of the commit.")
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The web URL for the commit."
    )
    trailers: Optional[Dict[str, Any]] = Field(
        default=None, description="Trailers of the commit"
    )
    extended_trailers: Optional[Dict[str, list[str]]] = Field(
        default=None, description="Extended trailers of the commit"
    )
    stats: Optional[CommitStats] = Field(
        default=None, description="Statistics of the commit"
    )
    status: Optional[str] = Field(default=None, description="Status of the commit")
    last_pipeline: Optional[Pipeline] = Field(
        default=None, description="Last pipeline associated with the commit"
    )
    signature: Optional[CommitSignature] = Field(
        default=None, description="Signature associated with the commit"
    )
    sha: Optional[str] = Field(default=None, description="SHA signature")
    count: Optional[int] = Field(default=None, description="Commit count")
    dry_run: Optional[str] = Field(default=None, description="Dry run status")
    individual_note: Optional[bool] = Field(
        default=None, description="Flag that this was a discussion"
    )
    notes: Optional[List[Comment]] = Field(
        default=None, description="Discussion on commit"
    )
    allow_failure: Optional[bool] = Field(
        default=None, description="Flag allows for failure"
    )
    target_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The target url for the commit."
    )
    ref: Optional[str] = Field(default=None, description="The ref of the commit.")
    error_code: Optional[str] = Field(default=None, description="Error codes")
    coverage: Optional[float] = Field(default=None, description="Coverage of commit")

    @field_validator("parent_ids", mode="before")
    def validate_parent_ids(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            parent_ids = []
            for item in v:
                parent_ids.append(ParentID(parent_id=item))
            return parent_ids
        return v

    @field_validator("notes", mode="before")
    def validate_notes(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            notes = []
            for item in v:
                notes.append(Comment(**item))
            return notes
        return v

    @field_validator("trailers", "extended_trailers", mode="before")
    def validate_trailers(cls, v):
        if isinstance(v, dict) and not v:
            return None
        return v


class Membership(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Membership")
    id: Optional[int] = Field(default=None, description="ID of the membership")
    source_id: Optional[int] = Field(
        default=None, description="Source ID of the membership"
    )
    source_full_name: Optional[str] = Field(
        default=None, description="Full name of the source"
    )
    source_members_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL of the source members"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp of when the membership was created"
    )
    expires_at: Optional[datetime] = Field(
        default=None, description="Timestamp of when the membership expires"
    )
    access_level: Optional[dict] = Field(
        default=None, description="Access level details of the membership"
    )


class Deployable(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the deployable"
    )
    status: Optional[str] = Field(
        default=None, description="Status of the deployable (e.g., success)"
    )
    stage: Optional[str] = Field(
        default=None, description="Stage of the deployable in the pipeline"
    )
    name: Optional[str] = Field(default=None, description="Name of the deployable")
    ref: Optional[str] = Field(
        default=None, description="Reference (branch or tag) of the deployable"
    )
    tag: Optional[bool] = Field(
        default=None, description="Whether the deployable is a tag"
    )
    coverage: Optional[float] = Field(
        default=None, description="Code coverage percentage"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the deployable was created"
    )
    started_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the deployable started"
    )
    finished_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the deployable finished"
    )
    duration: Optional[float] = Field(
        default=None, description="Duration of the deployable in seconds"
    )
    project: Optional["Project"] = Field(
        default=None, description="Project associated with the deployable"
    )
    user: Optional["User"] = Field(
        default=None, description="User who triggered the deployable"
    )
    commit: Optional["Commit"] = Field(
        default=None, description="Commit associated with the deployable"
    )
    pipeline: Optional["Pipeline"] = Field(
        default=None, description="Pipeline associated with the deployable"
    )
    web_url: Optional[str] = Field(
        default=None, description="URL to the deployable in the web interface"
    )
    artifacts: Optional[List["Artifact"]] = Field(
        default=None, description="List of artifacts generated by the deployable"
    )
    runner: Optional[dict] = Field(
        default=None, description="Runner information (null in this case)"
    )
    artifacts_expire_at: Optional[datetime] = Field(
        default=None, description="Timestamp when artifacts expire"
    )
    paused: Optional[bool] = Field(
        default=None,
        description="Indicates if the runner is paused (replacement for active).",
    )


class LastDeployment(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the last deployment"
    )
    iid: Optional[int] = Field(
        default=None, description="Internal ID of the deployment"
    )
    ref: Optional[str] = Field(
        default=None, description="Reference (branch or tag) of the deployment"
    )
    sha: Optional[str] = Field(default=None, description="SHA of the commit deployed")
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the deployment was created"
    )
    status: Optional[str] = Field(
        default=None, description="Status of the deployment (e.g., success)"
    )
    user: Optional[User] = Field(
        default=None, description="User who performed the deployment"
    )
    deployable: Optional[Deployable] = Field(
        default=None, description="Deployable associated with the deployment"
    )


class Environment(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Environment")
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the environment"
    )
    name: Optional[str] = Field(default=None, description="Name of the environment")
    slug: Optional[str] = Field(
        default=None, description="Slugified name of the environment"
    )
    description: Optional[str] = Field(
        default=None, description="Description of the environment"
    )
    external_url: Optional[str] = Field(
        default=None, description="External URL for the environment"
    )
    state: Optional[str] = Field(
        default=None, description="State of the environment (e.g., available)"
    )
    tier: Optional[str] = Field(
        default=None, description="Tier of the environment (e.g., development)"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Last updated timestamp"
    )
    enable_advanced_logs_querying: Optional[bool] = Field(
        default=None, description="Enable advanced logs querying"
    )
    logs_api_path: Optional[str] = Field(default=None, description="Path to logs API")
    auto_stop_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the environment auto-stops"
    )
    kubernetes_namespace: Optional[str] = Field(
        default=None, description="Kubernetes namespace for the environment"
    )
    flux_resource_path: Optional[str] = Field(
        default=None, description="Flux resource path (e.g., HelmRelease)"
    )
    auto_stop_setting: Optional[str] = Field(
        default=None, description="Auto-stop setting (e.g., always)"
    )
    deploy_access_levels: Optional[List["AccessLevel"]] = Field(
        default=None, description="List of access levels for deployment"
    )
    required_approval_count: Optional[int] = Field(
        default=None, description="Number of required approvals"
    )
    last_deployment: Optional["LastDeployment"] = Field(
        default=None, description="Details of the last deployment"
    )
    cluster_agent: Optional["ClusterAgent"] = Field(
        default=None, description="Cluster agent associated with the environment"
    )


class Label(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Label")
    name: str = Field(default=None)


class Tag(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Tag")
    tag: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    create_access_levels: Optional[List["AccessLevel"]] = Field(default=None)


class Topic(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Topic")
    name: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    total_projects_count: int = Field(default=None)
    organization_id: int = Field(default=None)
    avatar_url: str = Field(default=None)


class ComplianceFrameworks(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="ComplianceFrameworks")
    name: str = Field(default=None)


class CIIDTokenComponents(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="CIIDTokenComponents")
    name: str = Field(default=None)


class Link(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Links")
    self_link: Optional[str] = Field(
        default=None, alias="self", description="URL to the project itself."
    )
    issues: Optional[str] = Field(
        default=None, description="URL to the project's issues."
    )
    merge_requests: Optional[str] = Field(
        default=None, description="URL to the project's merge requests."
    )
    repo_branches: Optional[str] = Field(
        default=None, description="URL to the project's repository branches."
    )
    labels: Optional[str] = Field(
        default=None, description="URL to the project's labels."
    )
    events: Optional[str] = Field(
        default=None, description="URL to the project's events."
    )
    members: Optional[str] = Field(
        default=None, description="URL to the project's members."
    )
    cluster_agents: Optional[str] = Field(
        default=None, description="URL to the project's cluster agents."
    )
    notes: Optional[str] = Field(
        default=None, description="API URL to the notes of the issue."
    )
    award_emoji: Optional[str] = Field(
        default=None, description="API URL to the award emojis of the issue."
    )
    project: Optional[str] = Field(
        default=None, description="API URL to the project of the issue."
    )
    closed_as_duplicate_of: Optional[str] = Field(
        default=None,
        description="API URL to the issue this one was closed as duplicate of.",
    )
    id: Optional[int] = Field(default=None, description="Link ID")
    name: Optional[str] = Field(default=None, description="Name of the link")
    url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL of the link"
    )
    direct_asset_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="Direct URL of the asset"
    )
    link_type: Optional[str] = Field(
        default=None, description="Type of the link (e.g., other)"
    )


class License(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="License")
    key: Optional[str] = Field(
        default=None, description="License key (e.g., 'lgpl-3.0')."
    )
    name: Optional[str] = Field(
        default=None,
        description="License name (e.g., 'GNU Lesser General Public License v3.0').",
    )
    nickname: Optional[str] = Field(
        default=None, description="License nickname (e.g., 'GNU LGPLv3')."
    )
    html_url: Optional[str] = Field(default=None, description="URL to license details.")
    source_url: Optional[str] = Field(
        default=None, description="URL to license source text."
    )


class Project(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Project")
    id: Optional[int] = Field(default=None, description="The ID of the project.")
    description: Optional[str] = Field(
        default=None, description="The description of the project."
    )
    description_html: Optional[str] = Field(
        default=None, description="The HTML description of the project."
    )
    default_branch: Optional[str] = Field(
        default=None, description="The default branch of the project."
    )
    visibility: Optional[str] = Field(
        default=None,
        description="The visibility of the project (private, internal, public).",
    )
    ssh_url_to_repo: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The SSH URL to the repository."
    )
    http_url_to_repo: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The HTTP URL to the repository."
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The web URL to the project."
    )
    readme_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The URL to the README file."
    )
    tag_list: Optional[List["Tag"]] = Field(
        default=None, description="Deprecated. Use `topics` instead."
    )
    topics: Optional[List["Topic"]] = Field(
        default=None, description="The topics of the project."
    )
    name: Optional[str] = Field(default=None, description="The name of the project.")
    name_with_namespace: Optional[str] = Field(
        default=None, description="The name with namespace of the project."
    )
    path: Optional[str] = Field(default=None, description="The path of the project.")
    path_with_namespace: Optional[str] = Field(
        default=None, description="The path with namespace of the project."
    )
    issues_enabled: Optional[bool] = Field(
        default=None, description="Deprecated. Use `issues_access_level` instead."
    )
    open_issues_count: Optional[int] = Field(
        default=None, description="Number of open issues in the project."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="The creation time of the project."
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="The last update time of the project."
    )
    avatar_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The avatar URL of the project."
    )
    forks_count: Optional[int] = Field(default=None, description="The number of forks.")
    star_count: Optional[int] = Field(default=None, description="The number of stars.")
    last_activity_at: Optional[datetime] = Field(
        default=None, description="The time of the last activity."
    )
    namespace: Optional[Namespace] = Field(
        default=None, description="The namespace of the project."
    )
    container_registry_image_prefix: Optional[str] = Field(
        default=None, description="The container registry image prefix."
    )
    additional_links: Optional["Link"] = Field(
        default=None, alias="_links", description="Related links."
    )
    packages_enabled: Optional[bool] = Field(
        default=None,
        description="Deprecated in GitLab 17.10. Use `package_registry_access_level` instead.",
    )
    empty_repo: Optional[bool] = Field(
        default=None, description="Whether the repository is empty."
    )
    archived: Optional[bool] = Field(
        default=None, description="Whether the project is archived."
    )
    resolve_outdated_diff_discussions: Optional[bool] = Field(
        default=None, description="Whether outdated diff discussions are resolved."
    )
    pre_receive_secret_detection_enabled: Optional[bool] = Field(
        default=None, description="Whether secret detection is enabled."
    )
    container_expiration_policy: Optional[ContainerExpirationPolicy] = Field(
        default=None, description="The container expiration policy."
    )
    releases_access_level: Optional[str] = Field(
        default=None, description="Release access level."
    )
    environments_access_level: Optional[str] = Field(
        default=None, description="Environments access level."
    )
    feature_flags_access_level: Optional[str] = Field(
        default=None, description="Feature flags access level."
    )
    infrastructure_access_level: Optional[str] = Field(
        default=None, description="Infrastructure access level."
    )
    monitor_access_level: Optional[str] = Field(
        default=None, description="Monitor access level."
    )
    machine_learning_model_experiments_access_level: Optional[str] = Field(
        default=None,
        alias="model_experiments_access_level",
        description="Model experiments access level.",
    )
    machine_learning_model_registry_access_level: Optional[str] = Field(
        default=None,
        alias="model_registry_access_level",
        description="Model registry access level.",
    )
    merge_requests_enabled: Optional[bool] = Field(
        default=None,
        description="Deprecated. Use `merge_requests_access_level` instead.",
    )
    wiki_enabled: Optional[bool] = Field(
        default=None, description="Deprecated. Use `wiki_access_level` instead."
    )
    jobs_enabled: Optional[bool] = Field(
        default=None, description="Deprecated. Use `builds_access_level` instead."
    )
    snippets_enabled: Optional[bool] = Field(
        default=None, description="Deprecated. Use `snippets_access_level` instead."
    )
    container_registry_enabled: Optional[bool] = Field(
        default=None,
        description="Deprecated. Use `container_registry_access_level` instead.",
    )
    container_registry_access_level: Optional[str] = Field(
        default=None, description="The access level for the container registry."
    )
    security_and_compliance_access_level: Optional[str] = Field(
        default=None, description="The access level for security and compliance."
    )
    creator_id: Optional[int] = Field(
        default=None, description="The ID of the creator."
    )
    import_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The import URL."
    )
    import_type: Optional[str] = Field(default=None, description="The import type.")
    import_status: Optional[str] = Field(default=None, description="The import status.")
    import_error: Optional[str] = Field(default=None, description="The import error.")
    shared_runners_enabled: Optional[bool] = Field(
        default=None, description="Whether shared runners are enabled."
    )
    group_runners_enabled: Optional[bool] = Field(
        default=None, description="Whether group runners are enabled."
    )
    lfs_enabled: Optional[bool] = Field(
        default=None, description="Whether LFS is enabled."
    )
    ci_default_git_depth: Optional[int] = Field(
        default=None, description="The default git depth for CI."
    )
    ci_forward_deployment_enabled: Optional[bool] = Field(
        default=None, description="Whether forward deployment is enabled for CI."
    )
    ci_forward_deployment_rollback_allowed: Optional[bool] = Field(
        default=None,
        description="Whether rollback is allowed for CI forward deployment.",
    )
    ci_allow_fork_pipelines_to_run_in_parent_project: Optional[bool] = Field(
        default=None,
        description="Whether fork pipelines can run in the parent project.",
    )
    ci_separated_caches: Optional[bool] = Field(
        default=None, description="Whether CI caches are separated."
    )
    ci_restrict_pipeline_cancellation_role: Optional[str] = Field(
        default=None, description="The role that can cancel pipelines."
    )
    forked_from_project: Optional["Project"] = Field(
        default=None, description="The project from where this project was forked from."
    )
    mr_default_target_self: Optional[bool] = Field(
        default=None, description="Merge Request default target self."
    )
    public_jobs: Optional[bool] = Field(
        default=None, description="Whether jobs are public."
    )
    shared_with_groups: Optional[List["Group"]] = Field(
        default=None, description="Groups the project is shared with."
    )
    only_allow_merge_if_pipeline_succeeds: Optional[bool] = Field(
        default=None,
        description="Whether merging is only allowed if the pipeline succeeds.",
    )
    allow_merge_on_skipped_pipeline: Optional[Union[bool, str]] = Field(
        default=None, description="Whether merging is allowed on skipped pipelines."
    )
    restrict_user_defined_variables: Optional[bool] = Field(
        default=None,
        description="Deprecated in GitLab 17.7. Use `ci_pipeline_variables_minimum_override_role` instead.",
    )
    code_suggestions: Optional[bool] = Field(
        default=None, description="Enable code suggestions."
    )
    only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = Field(
        default=None,
        description="Whether merging is only allowed if all discussions are resolved.",
    )
    remove_source_branch_after_merge: Optional[bool] = Field(
        default=None, description="Whether the source branch is removed after merging."
    )
    request_access_enabled: Optional[bool] = Field(
        default=None, description="Whether requesting access is enabled."
    )
    merge_pipelines_enabled: Optional[bool] = Field(
        default=None, description="Whether merge pipelines are enabled."
    )
    merge_trains_skip_train_allowed: Optional[bool] = Field(
        default=None, description="Whether merge trains can skip pipelines."
    )
    allow_pipeline_trigger_approve_deployment: Optional[bool] = Field(
        default=None, description="Whether pipeline can trigger deployment approval."
    )
    repository_object_format: Optional[str] = Field(
        default=None, description="Repository object format (e.g., 'sha1')."
    )
    merge_method: Optional[str] = Field(
        default=None,
        description="The method used for merging (merge, rebase_merge, ff).",
    )
    squash_option: Optional[str] = Field(
        default=None,
        description="The squash option (never, always, default_on, default_off).",
    )
    enforce_auth_checks_on_uploads: Optional[bool] = Field(
        default=None, description="Whether auth checks are enforced on uploads."
    )
    suggestion_commit_message: Optional[str] = Field(
        default=None, description="The suggestion commit message."
    )
    compliance_frameworks: Optional[List["ComplianceFrameworks"]] = Field(
        default=None, description="The compliance frameworks."
    )
    issues_template: Optional[str] = Field(
        default=None, description="The issues template (Premium and Ultimate only)."
    )
    merge_requests_template: Optional[str] = Field(
        default=None,
        description="The merge requests template (Premium and Ultimate only).",
    )
    packages_relocation_enabled: Optional[bool] = Field(
        default=None, description="Whether package relocation is enabled."
    )
    requirements_enabled: Optional[bool] = Field(
        default=None, description="Whether the requirements feature is enabled."
    )
    build_git_strategy: Optional[str] = Field(
        default=None, description="The build git strategy (e.g., 'fetch')."
    )
    build_timeout: Optional[int] = Field(
        default=None, description="The build timeout in seconds."
    )
    auto_cancel_pending_pipelines: Optional[str] = Field(
        default=None,
        description="The auto-cancel pending pipelines setting (enabled, disabled).",
    )
    build_coverage_regex: Optional[str] = Field(
        default=None, description="The build coverage regex."
    )
    ci_config_path: Optional[str] = Field(
        default=None, description="The CI config path."
    )
    shared_runners_minutes_limit: Optional[int] = Field(
        default=None, description="The shared runners minutes limit."
    )
    extra_shared_runners_minutes_limit: Optional[int] = Field(
        default=None, description="The extra shared runners minutes limit."
    )
    printing_merge_request_link_enabled: Optional[bool] = Field(
        default=None, description="Whether printing the merge request link is enabled."
    )
    merge_trains_enabled: Optional[bool] = Field(
        default=None, description="Whether merge trains are enabled."
    )
    has_open_issues: Optional[bool] = Field(
        default=None,
        description="Whether the project has open issues (potentially redundant with open_issues_count).",
    )
    approvals_before_merge: Optional[int] = Field(
        default=None,
        description="Deprecated in GitLab 16.0. Use Merge Request Approvals API instead.",
    )
    mirror: Optional[bool] = Field(
        default=None, description="Whether the project is a mirror."
    )
    mirror_user_id: Optional[int] = Field(
        default=None, description="The ID of the mirror user."
    )
    mirror_trigger_builds: Optional[bool] = Field(
        default=None, description="Whether mirror builds are triggered."
    )
    only_mirror_protected_branches: Optional[bool] = Field(
        default=None, description="Whether only protected branches are mirrored."
    )
    mirror_overwrites_diverged_branches: Optional[bool] = Field(
        default=None, description="Whether diverged branches are overwritten."
    )
    permissions: Optional[Permissions] = Field(
        default=None, description="The permissions settings."
    )
    statistics: Optional[Statistics] = Field(
        default=None, description="The project statistics."
    )
    links: Optional[Link] = Field(default=None, description="Related links.")
    service_desk_enabled: Optional[bool] = Field(
        default=None, description="Whether Service Desk is enabled."
    )
    can_create_merge_request_in: Optional[bool] = Field(
        default=None,
        description="Whether merge requests can be created in the project.",
    )
    repository_access_level: Optional[str] = Field(
        default=None,
        description="Repository access level (disabled, private, enabled).",
    )
    merge_requests_access_level: Optional[str] = Field(
        default=None,
        description="Merge request access level (disabled, private, enabled).",
    )
    issues_access_level: Optional[str] = Field(
        default=None, description="Issue access level (disabled, private, enabled)."
    )
    forking_access_level: Optional[str] = Field(
        default=None, description="Forking access level (disabled, private, enabled)."
    )
    wiki_access_level: Optional[str] = Field(
        default=None, description="Wiki access level (disabled, private, enabled)."
    )
    builds_access_level: Optional[str] = Field(
        default=None, description="Build access level (disabled, private, enabled)."
    )
    snippets_access_level: Optional[str] = Field(
        default=None, description="Snippet access level (disabled, private, enabled)."
    )
    pages_access_level: Optional[str] = Field(
        default=None,
        description="Page access level (disabled, private, enabled, public).",
    )
    analytics_access_level: Optional[str] = Field(
        default=None, description="Analytics access level (disabled, private, enabled)."
    )
    emails_disabled: Optional[bool] = Field(
        default=None, description="Deprecated. Use `emails_enabled` instead."
    )
    emails_enabled: Optional[bool] = Field(
        default=None, description="Whether email notifications are enabled."
    )
    ci_job_token_scope_enabled: Optional[bool] = Field(
        default=None, description="Whether CI Job Token scope is enabled."
    )
    merge_commit_template: Optional[str] = Field(
        default=None, description="Template for merge commit messages."
    )
    squash_commit_template: Optional[str] = Field(
        default=None, description="Template for squash commit messages."
    )
    issue_branch_template: Optional[str] = Field(
        default=None, description="Template for branch names created from issues."
    )
    auto_devops_enabled: Optional[bool] = Field(
        default=None, description="Whether Auto DevOps is enabled."
    )
    auto_devops_deploy_strategy: Optional[str] = Field(
        default=None,
        description="Auto DevOps deploy strategy (continuous, manual, timed_incremental).",
    )
    autoclose_referenced_issues: Optional[bool] = Field(
        default=None, description="Whether referenced issues are auto-closed."
    )
    keep_latest_artifact: Optional[bool] = Field(
        default=None, description="Whether to keep the latest artifact."
    )
    runner_token_expiration_interval: Optional[bool] = Field(
        default=None, description="Runner token expiration interval."
    )
    external_authorization_classification_label: Optional[str] = Field(
        default=None, description="External authorization classification label."
    )
    requirements_access_level: Optional[str] = Field(
        default=None,
        description="Requirements access level (disabled, private, enabled).",
    )
    security_and_compliance_enabled: Optional[bool] = Field(
        default=None,
        description="Whether security and compliance features are enabled.",
    )
    warn_about_potentially_unwanted_characters: Optional[bool] = Field(
        default=None,
        description="Whether warnings for potentially unwanted characters are enabled.",
    )
    owner: Optional[User] = Field(default=None, description="Owner user.")
    runners_token: Optional[str] = Field(default=None, description="Runners token.")
    secret_push_protection_enabled: Optional[bool] = Field(
        default=None,
        description="Whether secret push protection is enabled (Ultimate only).",
    )
    repository_storage: Optional[str] = Field(
        default=None, description="Repository storage shard."
    )
    service_desk_address: Optional[str] = Field(
        default=None, description="Service desk email address."
    )
    marked_for_deletion_at: Optional[str] = Field(
        default=None, description="Deprecated. Use `marked_for_deletion_on` instead."
    )
    marked_for_deletion_on: Optional[str] = Field(
        default=None, description="Date when project was marked for deletion."
    )
    operations_access_level: Optional[str] = Field(
        default=None,
        description="Access level of operations (non-standard, verify usage).",
    )
    ci_dockerfile: Optional[str] = Field(
        default=None, description="Dockerfile for CI (non-standard, verify usage)."
    )
    groups: Optional[List["Group"]] = Field(
        default=None, description="List of groups (non-standard, verify usage)."
    )
    public: Optional[bool] = Field(
        default=None,
        description="Whether project is allowed to be public (non-standard, verify usage).",
    )
    ci_id_token_sub_claim_components: Optional[List["CIIDTokenComponents"]] = Field(
        default=None, description="CI ID Token Sub Claim Components"
    )
    ci_pipeline_variables_minimum_override_role: Optional[str] = Field(
        default=None,
        description="The minimum role required to override CI pipeline variables (owner, maintainer, developer, no_one_allowed) (introduced in GitLab 17.1, replaces restrict_user_defined_variables).",
    )
    ci_push_repository_for_job_token_allowed: Optional[bool] = Field(
        default=None,
        description="Whether pushing to the repository using a job token is allowed (introduced in GitLab 17.2).",
    )
    default_branch_protection_defaults: Optional["DefaultBranchProtectionDefaults"] = (
        Field(
            default=None,
            description="Defaults for default branch protection (replacement for default_branch_protection).",
        )
    )
    only_allow_merge_if_all_status_checks_passed: Optional[bool] = Field(
        default=None,
        description="Whether merges are blocked unless all status checks have passed (introduced in GitLab 15.5, Ultimate only).",
    )
    spp_repository_pipeline_access: Optional[bool] = Field(
        default=None,
        description="Whether read-only access is allowed to fetch security policy configurations (Ultimate only).",
    )
    # New fields added based on documentation
    license: Optional[License] = Field(
        default=None, description="License details for the project."
    )
    ci_delete_pipelines_in_seconds: Optional[int] = Field(
        default=None, description="Time in seconds after which pipelines are deleted."
    )
    max_artifacts_size: Optional[int] = Field(
        default=None,
        description="Maximum file size in megabytes for individual job artifacts.",
    )
    prevent_merge_without_jira_issue: Optional[bool] = Field(
        default=None,
        description="Whether merge requests require an associated Jira issue (Ultimate only).",
    )
    auto_duo_code_review_enabled: Optional[bool] = Field(
        default=None,
        description="Whether automatic reviews by GitLab Duo are enabled on merge requests (Ultimate only).",
    )
    duo_remote_flows_enabled: Optional[bool] = Field(
        default=None, description="Whether Duo remote flows can run in the project."
    )
    web_based_commit_signing_enabled: Optional[bool] = Field(
        default=None,
        description="Whether web-based commit signing is enabled for commits created from the GitLab UI (GitLab SaaS only, experimental).",
    )

    @field_validator("tag_list", mode="before")
    def validate_tags(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            tags = []
            for item in v:
                tags.append(Tag(tag=item))
            return tags
        return v

    @field_validator("topics", mode="before")
    def validate_topics(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            topics = []
            for item in v:
                topics.append(Topic(name=item))
            return topics
        return v

    @field_validator("ci_id_token_sub_claim_components", mode="before")
    def validate_ci_id_token_sub_claim_components(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            ci_id_token_sub_claim_components = []
            for item in v:
                ci_id_token_sub_claim_components.append(CIIDTokenComponents(name=item))
            return ci_id_token_sub_claim_components
        return v

    @field_validator("compliance_frameworks", mode="before")
    def validate_compliance_frameworks(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            compliance_frameworks = []
            for item in v:
                compliance_frameworks.append(ComplianceFrameworks(name=item))
            return compliance_frameworks
        return v

    @field_validator("groups", "shared_with_groups", mode="before")
    def validate_groups(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            groups = []
            for item in v:
                groups.append(Group(**item))
            return groups
        return v


class Runner(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Runner")
    id: Optional[int] = Field(default=None, description="ID of the runner.")
    description: Optional[str] = Field(
        default=None, description="Description of the runner."
    )
    ip_address: Optional[str] = Field(
        default=None, description="IP address of the runner."
    )
    active: Optional[bool] = Field(
        default=None, description="Indicates if the runner is active."
    )
    paused: Optional[bool] = Field(
        default=None, description="Indicates if the runner is paused."
    )
    is_shared: Optional[bool] = Field(
        default=None, description="Indicates if the runner is shared."
    )
    runner_type: Optional[str] = Field(default=None, description="Type of the runner.")
    name: Optional[str] = Field(default=None, description="Name of the runner.")
    online: Optional[bool] = Field(
        default=None, description="Indicates if the runner is online."
    )
    status: Optional[str] = Field(default=None, description="Status of the runner.")
    contacted_at: Optional[datetime] = Field(
        None, description="Last contacted date and time"
    )
    architecture: Optional[str] = Field(None, description="Architecture of the runner")
    platform: Optional[str] = Field(None, description="Platform of the runner")
    revision: Optional[str] = Field(None, description="Revision of the runner")
    version: Optional[str] = Field(None, description="Version of the runner")
    access_level: Optional[str] = Field(None, description="Access level of the runner")
    maximum_timeout: Optional[int] = Field(
        None, description="Maximum timeout for the runner"
    )
    maintenance_note: Optional[str] = Field(
        None, description="Maintenance note for the runner"
    )
    projects: Optional[List[Project]] = Field(
        None, description="List of projects associated with the runner"
    )
    tag_list: Optional[List[Tag]] = Field(
        None, description="List of tags associated with the runner"
    )

    @field_validator("tag_list", mode="before")
    def validate_tags(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            tags = []
            for item in v:
                tags.append(Tag(tag=item))
            return tags
        return v

    @field_validator("projects", mode="before")
    def validate_projects(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            projects = []
            for item in v:
                projects.append(Project(**item))
            return projects
        return v


class ProjectConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="ProjectConfig")
    id: int = Field(default=None, description="Project identifier")
    description: Optional[str] = Field(None, description="Description of the project")
    name: str = Field(default=None, description="Name of the project")
    name_with_namespace: str = Field(
        default=None, description="Full project name with namespace"
    )
    path: str = Field(default=None, description="Path of the project")
    path_with_namespace: str = Field(
        default=None, description="Full path of the project including namespace"
    )
    created_at: datetime = Field(
        default=None, description="Creation timestamp of the project"
    )
    ci_job_token_scope_enabled: Optional[bool] = Field(
        None, description="CI Job Token Scope Enabled for Project"
    )


class ClusterAgent(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the cluster agent"
    )
    name: Optional[str] = Field(default=None, description="Name of the cluster agent")
    config_project: Optional["ProjectConfig"] = Field(
        default=None, description="Project configuring the agent"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the cluster agent was created"
    )
    created_by_user_id: Optional[int] = Field(
        default=None, description="ID of the user who created the agent"
    )


class Job(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Job", description="Type of the model")
    id: Optional[int] = Field(default=None, description="ID of the job")
    name: Optional[str] = Field(default=None, description="Name of the job")
    commit: Optional[Commit] = Field(
        default=None, description="Details of the commit associated with the job"
    )
    coverage: Optional[float] = Field(
        default=None, description="Code coverage percentage"
    )
    archived: Optional[bool] = Field(
        default=None, description="Indicates if the job is archived"
    )
    source: Optional[str] = Field(
        default=None, description="Source of the job (e.g., push, web, schedule)"
    )  # Added missing field
    allow_failure: Optional[bool] = Field(
        default=None, description="Indicates if the job is allowed to fail"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the job was created"
    )
    started_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the job was started"
    )
    finished_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the job was finished"
    )
    erased_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the job was erased"
    )
    duration: Optional[float] = Field(
        default=None, description="Duration of the job in seconds"
    )
    queued_duration: Optional[float] = Field(
        default=None, description="Time the job spent queued before starting"
    )
    artifacts_file: Optional[ArtifactsFile] = Field(
        default=None, description="Details of the artifacts file produced by the job"
    )
    artifacts: Optional[List[Artifact]] = Field(
        default=None, description="List of artifacts produced by the job"
    )
    artifacts_expire_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the artifacts expire"
    )
    tags: Optional[List[Tag]] = Field(
        default=None,
        description="List of tags associated with the job",
        alias="tag_list",
    )  # Renamed from tag_list
    pipeline: Optional[Pipeline] = Field(
        default=None, description="Details of the pipeline associated with the job"
    )
    ref: Optional[str] = Field(default=None, description="Reference of the job")
    download_url: Optional[str] = Field(
        default=None, description="URL to download job artifacts, if available"
    )  # Added missing field
    runner: Optional[Runner] = Field(
        default=None, description="Details of the runner that executed the job"
    )
    runner_manager: Optional[RunnerManager] = Field(
        default=None, description="Details of the runner manager"
    )
    stage: Optional[str] = Field(default=None, description="Stage of the job")
    status: Optional[str] = Field(
        default=None, description="Status of the job (e.g., pending, running, failed)"
    )
    failure_reason: Optional[str] = Field(
        default=None, description="Reason for the job failure, if applicable"
    )
    tag: Optional[bool] = Field(
        default=None, description="Indicates if the job is tagged (purpose unclear)"
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL to view the job on the web"
    )
    project: Optional[ProjectConfig] = Field(
        default=None, description="Details of the project associated with the job"
    )
    user: Optional[User] = Field(
        default=None, description="Details of the user who created the job"
    )
    downstream_pipeline: Optional[Pipeline] = Field(
        default=None, description="Details of the downstream pipeline, if applicable"
    )

    @field_validator("tags", mode="before")
    def validate_tags(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            tags = []
            for item in v:
                tags.append(Tag(tag=item))
            return tags
        return v

    @field_validator("artifacts", mode="before")
    def validate_artifacts(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            artifacts = []
            for item in v:
                artifacts.append(Artifact(**item))
            return artifacts
        return v


class GroupAccess(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="GroupAccess")
    access_level: Optional[int] = Field(
        default=None, description="Access level for a group"
    )


class DefaultBranchProtectionDefaults(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="DefaultBranchProtectionDefaults")
    allowed_to_push: Optional[List[GroupAccess]] = Field(
        default=None, description="List of groups allowed to push"
    )
    allow_force_push: Optional[bool] = Field(
        default=None, description="Whether force push is allowed"
    )
    allowed_to_merge: Optional[List[GroupAccess]] = Field(
        default=None, description="List of groups allowed to merge"
    )

    @field_validator("allowed_to_push", "allowed_to_merge", mode="before")
    def validate_group_accesses(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            group_accesses = []
            for item in v:
                group = GroupAccess(**item)
                group_accesses.append(group)
            return group_accesses
        return v


class RootStorageStatistics(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="RootStorageStatistics")
    build_artifacts_size: Optional[int] = Field(
        default=None, description="Build artifacts storage size in bytes."
    )
    container_registry_size: Optional[int] = Field(
        default=None, description="Container registry storage size in bytes."
    )
    container_registry_size_is_estimated: Optional[bool] = Field(
        default=None, description="Whether container registry size is estimated."
    )
    dependency_proxy_size: Optional[int] = Field(
        default=None, description="Dependency proxy storage size in bytes."
    )
    lfs_objects_size: Optional[int] = Field(
        default=None, description="LFS objects storage size in bytes."
    )
    packages_size: Optional[int] = Field(
        default=None, description="Packages storage size in bytes."
    )
    pipeline_artifacts_size: Optional[int] = Field(
        default=None, description="Pipeline artifacts storage size in bytes."
    )
    repository_size: Optional[int] = Field(
        default=None, description="Repository storage size in bytes."
    )
    snippets_size: Optional[int] = Field(
        default=None, description="Snippets storage size in bytes."
    )
    storage_size: Optional[int] = Field(
        default=None, description="Total storage size in bytes."
    )
    uploads_size: Optional[int] = Field(
        default=None, description="Uploads storage size in bytes."
    )
    wiki_size: Optional[int] = Field(
        default=None, description="Wiki storage size in bytes."
    )


class Group(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Group")
    id: Optional[int] = Field(default=None, description="The ID of the group.")
    group_id: Optional[int] = Field(
        default=None,
        description="The ID of the group (used in shared_with_groups context, maps to id).",
    )
    group_name: Optional[str] = Field(
        default=None,
        description="Full name of the group (used in shared_with_groups context, maps to name).",
    )
    group_full_path: Optional[str] = Field(
        default=None,
        description="Full path of the group (used in shared_with_groups context, maps to full_path).",
    )
    group_access_level: Optional[int] = Field(
        default=None,
        description="Group access level (used in shared_with_groups context).",
    )
    expires_at: Optional[datetime] = Field(
        default=None, description="Expiration date of the group invitation (ISO 8601)."
    )
    organization_id: Optional[int] = Field(
        default=None, description="The Organization ID of the group."
    )
    name: Optional[str] = Field(default=None, description="The name of the group.")
    path: Optional[str] = Field(default=None, description="The path of the group.")
    description: Optional[str] = Field(
        default=None, description="The description of the group."
    )
    visibility: Optional[str] = Field(
        default=None,
        description="The visibility level of the group (private, internal, public).",
    )
    shared_runners_setting: Optional[str] = Field(
        default=None,
        description="Shared runner setting (enabled, disabled_and_overridable, disabled_and_unoverridable).",
    )
    share_with_group_lock: Optional[bool] = Field(
        default=None, description="Prevent sharing with other groups within this group."
    )
    require_two_factor_authentication: Optional[bool] = Field(
        default=None, description="Whether two-factor authentication is required."
    )
    two_factor_grace_period: Optional[int] = Field(
        default=None,
        description="Grace period for two-factor authentication enforcement (in hours).",
    )
    project_creation_level: Optional[str] = Field(
        default=None,
        description="Level required to create projects ('noone', 'maintainer', 'developer').",
    )
    auto_devops_enabled: Optional[bool] = Field(
        default=None,
        description="Whether Auto DevOps is enabled for projects in this group.",
    )
    subgroup_creation_level: Optional[str] = Field(
        default=None,
        description="Level required to create subgroups (owner, maintainer).",
    )
    emails_disabled: Optional[bool] = Field(
        default=None,
        description="Deprecated in GitLab 16.5. Use emails_enabled instead.",
    )
    emails_enabled: Optional[bool] = Field(
        default=None, description="Whether email notifications are enabled."
    )
    mentions_disabled: Optional[bool] = Field(
        default=None, description="Whether mentions are disabled."
    )
    lfs_enabled: Optional[bool] = Field(
        default=None,
        description="Whether Git LFS is enabled for projects in this group.",
    )
    default_branch: Optional[str] = Field(
        default=None, description="The default branch name for group's projects."
    )
    default_branch_protection: Optional[int] = Field(
        default=None,
        description="Deprecated in GitLab 17.0. Use default_branch_protection_defaults instead.",
    )
    default_branch_protection_defaults: Optional[DefaultBranchProtectionDefaults] = (
        Field(default=None, description="Default branch protection settings.")
    )
    avatar_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL of the group's avatar."
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="Web URL of the group."
    )
    request_access_enabled: Optional[bool] = Field(
        default=None, description="Whether request access is enabled."
    )
    repository_storage: Optional[str] = Field(
        default=None, description="Repository storage type (e.g., 'default')."
    )
    full_name: Optional[str] = Field(
        default=None, description="Full name of the group."
    )
    full_path: Optional[str] = Field(
        default=None, description="Full path of the group."
    )
    file_template_project_id: Optional[int] = Field(
        default=None, description="ID of the file template project."
    )
    parent_id: Optional[int] = Field(
        default=None, description="Parent ID of the group."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Creation timestamp of the group (ISO 8601)."
    )
    statistics: Optional[Statistics] = Field(
        default=None, description="Statistics of the group (admin only)."
    )
    root_storage_statistics: Optional[RootStorageStatistics] = Field(
        default=None,
        description="Root storage statistics for top-level groups (admin only).",
    )
    wiki_access_level: Optional[str] = Field(
        default=None,
        description="Wiki access level (disabled, private, enabled; Premium/Ultimate only).",
    )
    duo_features_enabled: Optional[bool] = Field(
        default=None,
        description="Whether GitLab Duo features are enabled (Premium/Ultimate only).",
    )
    lock_duo_features_enabled: Optional[bool] = Field(
        default=None,
        description="Whether GitLab Duo features are locked for subgroups (Premium/Ultimate only).",
    )
    duo_availability: Optional[str] = Field(
        default=None,
        description="Duo availability setting (default_on, default_off, never_on; Premium/Ultimate only).",
    )
    experiment_features_enabled: Optional[bool] = Field(
        default=None,
        description="Whether experiment features are enabled (Premium/Ultimate only).",
    )
    runners_token: Optional[str] = Field(
        default=None, description="Runners token for the group (admin/owner only)."
    )
    enabled_git_access_protocol: Optional[str] = Field(
        default=None, description="Enabled Git access protocol (ssh, http, all)."
    )
    shared_with_groups: Optional[List["Group"]] = Field(
        default=None, description="Groups shared with this group."
    )
    prevent_sharing_groups_outside_hierarchy: Optional[bool] = Field(
        default=None,
        description="Prevent sharing groups outside hierarchy (top-level groups only).",
    )
    projects: Optional[List[Project]] = Field(
        default=None,
        description="Projects within the group (deprecated in API v5, use GET /groups/:id/projects).",
    )
    shared_projects: Optional[List[Project]] = Field(
        default=None,
        description="Projects shared to the group (deprecated in API v5, use GET /groups/:id/projects/shared).",
    )
    ip_restriction_ranges: Optional[str] = Field(
        default=None,
        description="Comma-separated list of IP addresses or subnet masks to restrict group access (Premium/Ultimate only).",
    )
    math_rendering_limits_enabled: Optional[bool] = Field(
        default=None, description="Whether math rendering limits are enabled."
    )
    lock_math_rendering_limits_enabled: Optional[bool] = Field(
        default=None,
        description="Whether math rendering limits are locked for subgroups.",
    )
    shared_runners_minutes_limit: Optional[int] = Field(
        default=None,
        description="Shared runners limit in minutes (Premium/Ultimate only).",
    )
    extra_shared_runners_minutes_limit: Optional[int] = Field(
        default=None,
        description="Extra shared runners limit in minutes (Premium/Ultimate only).",
    )
    marked_for_deletion_on: Optional[str] = Field(
        default=None,
        description="Date when group was marked for deletion (Premium/Ultimate only).",
    )
    membership_lock: Optional[bool] = Field(
        default=None,
        description="Whether membership is locked (Premium/Ultimate only).",
    )
    ldap_cn: Optional[str] = Field(default=None, description="LDAP CN information.")
    ldap_access: Optional[str] = Field(default=None, description="LDAP access level.")
    prevent_forking_outside_group: Optional[bool] = Field(
        default=None,
        description="Prevent forking projects outside the group (Premium/Ultimate only).",
    )
    allowed_email_domains_list: Optional[str] = Field(
        default=None,
        description="Comma-separated list of email address domains to allow group access (introduced in GitLab 17.4, Premium/Ultimate only).",
    )
    unique_project_download_limit: Optional[int] = Field(
        default=None,
        description="Maximum number of unique projects a user can download before being banned (Ultimate only, top-level groups, default: 0, max: 10000).",
    )
    unique_project_download_limit_interval_in_seconds: Optional[int] = Field(
        default=None,
        description="Time period in seconds for unique project download limit (Ultimate only, top-level groups, default: 0, max: 864000).",
    )
    unique_project_download_limit_allowlist: Optional[List[str]] = Field(
        default=None,
        description="Usernames excluded from unique project download limit (Ultimate only, top-level groups, max: 100 usernames).",
    )
    unique_project_download_limit_alertlist: Optional[List[int]] = Field(
        default=None,
        description="User IDs emailed when unique project download limit is exceeded (Ultimate only, top-level groups, max: 100 user IDs).",
    )
    auto_ban_user_on_excessive_projects_download: Optional[bool] = Field(
        default=None,
        description="Automatically ban users who exceed unique project download limit (Ultimate only, top-level groups).",
    )
    web_based_commit_signing_enabled: Optional[bool] = Field(
        default=None,
        description="Enables web-based commit signing for commits created from the GitLab UI (GitLab SaaS, top-level groups only, experimental).",
    )
    step_up_auth_required_oauth_provider: Optional[str] = Field(
        default=None,
        description="OAuth provider required for step-up authentication (introduced in GitLab 18.4, feature flag omniauth_step_up_auth_for_namespace).",
    )
    archived: Optional[bool] = Field(
        default=None,
        description="Whether the group is archived (experimental, introduced in GitLab 18.2).",
    )
    max_artifacts_size: Optional[int] = Field(
        default=None,
        description="Maximum file size in megabytes for individual job artifacts.",
    )

    @model_validator(mode="before")
    def populate_id(cls, values):
        if "group_id" in values and "id" not in values:
            values["id"] = values["group_id"]
        if "group_name" in values and "name" not in values:
            values["name"] = values["group_name"]
        if "group_full_path" in values and "full_path" not in values:
            values["full_path"] = values["group_full_path"]
        return values

    @field_validator("projects", "shared_projects", mode="before")
    def validate_projects(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            return [Project(**item) for item in v]
        return v

    @field_validator("shared_with_groups", mode="before")
    def validate_groups(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            return [Group(**item) for item in v]
        return v


class Webhook(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Webhook")
    id: int = Field(default=None, description="Unique identifier for the webhook")
    url: Union[HttpUrl, str] = Field(
        default=None, description="The URL the webhook should target"
    )
    name: str = Field(default=None, description="Name of the webhook")
    description: str = Field(default=None, description="Description of the webhook")
    group_id: int = Field(
        default=None, description="Group ID to which the webhook belongs"
    )
    push_events: bool = Field(
        default=None, description="Whether push events trigger the webhook"
    )
    push_events_branch_filter: str = Field(
        default="", description="Branch filter for push events"
    )
    issues_events: bool = Field(
        default=None, description="Whether issues events trigger the webhook"
    )
    confidential_issues_events: bool = Field(
        default=None,
        description="Whether confidential issues events trigger the webhook",
    )
    merge_requests_events: bool = Field(
        default=None, description="Whether merge requests events trigger the webhook"
    )
    tag_push_events: bool = Field(
        default=None, description="Whether tag push events trigger the webhook"
    )
    note_events: bool = Field(
        default=None, description="Whether note events trigger the webhook"
    )
    confidential_note_events: bool = Field(
        default=None, description="Whether confidential note events trigger the webhook"
    )
    job_events: bool = Field(
        default=None, description="Whether job events trigger the webhook"
    )
    pipeline_events: bool = Field(
        default=None, description="Whether pipeline events trigger the webhook"
    )
    wiki_page_events: bool = Field(
        default=None, description="Whether wiki page events trigger the webhook"
    )
    deployment_events: bool = Field(
        default=None, description="Whether deployment events trigger the webhook"
    )
    releases_events: bool = Field(
        default=None, description="Whether releases events trigger the webhook"
    )
    subgroup_events: bool = Field(
        default=None, description="Whether subgroup events trigger the webhook"
    )
    member_events: bool = Field(
        default=None, description="Whether member events trigger the webhook"
    )
    enable_ssl_verification: bool = Field(
        default=None, description="Whether SSL verification is enabled for the webhook"
    )
    repository_update_events: bool = Field(
        default=None,
        description="Whether repository update events trigger the webhook",
    )
    alert_status: Optional[str] = Field(
        default=None, description="Status of the webhook, e.g., 'executable'"
    )
    disabled_until: Optional[datetime] = Field(
        default=None, description="Timestamp until which the webhook is disabled"
    )
    url_variables: list[str] = Field(
        default_factory=list, description="List of URL variables for the webhook"
    )
    created_at: datetime = Field(
        default=None, description="Creation timestamp of the webhook"
    )
    resource_access_token_events: bool = Field(
        default=None,
        description="Whether resource access token events trigger the webhook",
    )
    custom_webhook_template: str = Field(
        default=None, description="Custom webhook template JSON"
    )


class AccessLevel(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="AccessLevel")
    id: Optional[int] = Field(default=None, description="Access level ID")
    access_level: Optional[int] = Field(
        default=None, description="Numeric access level"
    )
    access_level_description: Optional[str] = Field(
        default=None, description="Description of the access level"
    )
    deploy_key_id: Optional[int] = Field(default=None, description="Deploy key ID")
    user_id: Optional[int] = Field(default=None, description="User ID")
    group_id: Optional[int] = Field(default=None, description="Group ID")
    group_inheritence_type: Optional[int] = Field(
        default=None, description="Group inheritance type"
    )


class Branch(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Branch")
    name: Optional[str] = Field(default=None, description="The name of the branch.")
    merged: Optional[bool] = Field(
        default=None, description="Whether the branch is merged."
    )
    protected: Optional[bool] = Field(
        default=None, description="Whether the branch is protected."
    )
    default: Optional[bool] = Field(
        default=None, description="Whether the branch is the default branch."
    )
    developers_can_push: Optional[bool] = Field(
        default=None, description="Whether developers can push to the branch."
    )
    developers_can_merge: Optional[bool] = Field(
        default=None, description="Whether developers can merge the branch."
    )
    can_push: Optional[bool] = Field(
        default=None, description="Whether the user can push to the branch."
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The web URL for the branch."
    )
    commit: Optional[Commit] = Field(
        default=None, description="The commit associated with the branch."
    )
    id: Optional[int] = Field(default=None, description="Branch ID")
    push_access_levels: Optional[List[AccessLevel]] = Field(
        default=None, description="Push access levels for the branch"
    )
    merge_access_levels: Optional[List[AccessLevel]] = Field(
        default=None, description="Merge access levels for the branch"
    )
    unprotect_access_levels: Optional[List[AccessLevel]] = Field(
        default=None, description="Unprotect access levels for the branch"
    )
    allow_force_push: Optional[bool] = Field(
        default=None, description="Whether force pushing is allowed"
    )
    code_owner_approval_required: Optional[bool] = Field(
        default=None, description="Whether code owner approval is required"
    )
    inherited: Optional[bool] = Field(
        default=None, description="Whether the branch is inherited"
    )

    @field_validator(
        "push_access_levels",
        "merge_access_levels",
        "unprotect_access_levels",
        mode="before",
    )
    def validate_access_levels(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            access_levels = []
            for item in v:
                access_levels.append(AccessLevel(**item))
            return access_levels
        return v


class ApprovalRule(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="ApprovalRule")
    id: Optional[int] = Field(default=None, description="Approval rule ID")
    name: Optional[str] = Field(default=None, description="Approval rule name")
    rule_type: Optional[str] = Field(
        default=None, description="Type of the approval rule"
    )
    eligible_approvers: Optional[List[User]] = Field(
        default=None, description="List of eligible approvers"
    )
    approvals_required: Optional[int] = Field(
        default=None, description="Number of required approvals"
    )
    users: Optional[List[User]] = Field(
        default=None, description="List of associated users"
    )
    groups: Optional[List[Group]] = Field(
        default=None, description="List of associated groups"
    )
    contains_hidden_groups: Optional[bool] = Field(
        default=None, description="Whether the rule contains hidden groups"
    )
    protected_branches: Optional[List[Branch]] = Field(
        default=None, description="List of protected branches the rule applies to"
    )
    applies_to_all_protected_branches: Optional[bool] = Field(
        default=None, description="Whether the rule applies to all protected branches"
    )
    source_rule: Optional[str] = Field(
        default=None, description="Source rule for merge request rules"
    )
    approved: Optional[bool] = Field(
        default=None, description="Whether the rule is approved"
    )
    overridden: Optional[bool] = Field(
        default=None, description="Whether the rule is overridden"
    )
    approved_by: Optional[List[User]] = Field(
        default=None, description="List of users who approved"
    )
    report_type: Optional[str] = Field(default=None, description="The type of report")

    @field_validator("eligible_approvers", "approved_by", "users", mode="before")
    def validate_users(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            users = []
            for item in v:
                if "user" in item:
                    users.append(User(**item["user"]))
                else:
                    users.append(User(**item))
            return users
        return v

    @field_validator("protected_branches", mode="before")
    def validate_protected_branches(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            protected_branches = []
            for item in v:
                protected_branches.append(Branch(**item))
            return protected_branches
        return v

    @field_validator("groups", mode="before")
    def validate_groups(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            groups = []
            for item in v:
                groups.append(Group(**item))
            return groups
        return v


class DiffRefs(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="DiffRefs", description="Type of the model")
    base_sha: str = Field(description="Base SHA of the diff")
    head_sha: str = Field(description="Head SHA of the diff")
    start_sha: str = Field(description="Start SHA of the diff")


class MergeRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="MergeRequest", description="Type of the model")
    id: Optional[int] = Field(default=None, description="ID of the merge request")
    iid: Optional[int] = Field(
        default=None, description="Internal ID of the merge request"
    )
    project_id: Optional[int] = Field(
        default=None, description="ID of the project the merge request belongs to"
    )
    title: Optional[str] = Field(default=None, description="Title of the merge request")
    description: Optional[str] = Field(
        default=None, description="Description of the merge request"
    )
    state: Optional[str] = Field(
        default=None,
        description="State of the merge request (e.g., opened, closed, merged)",
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Creation date of the merge request"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update date of the merge request"
    )
    target_branch: Optional[str] = Field(
        default=None, description="Target branch of the merge request"
    )
    source_branch: Optional[str] = Field(
        default=None, description="Source branch of the merge request"
    )
    upvotes: Optional[int] = Field(
        default=None, description="Number of upvotes the merge request has received"
    )
    downvotes: Optional[int] = Field(
        default=None, description="Number of downvotes the merge request has received"
    )
    author: Optional[User] = Field(
        default=None, description="Author of the merge request"
    )
    assignees: Optional[List[User]] = Field(
        default=None, description="List of users assigned to the merge request"
    )  # Replaced assignee
    assignee: Optional[User] = Field(
        default=None,
        description="Assignee of the merge request (deprecated: use assignees)",
    )  # Deprecated
    source_project_id: Optional[int] = Field(
        default=None, description="ID of the source project"
    )
    target_project_id: Optional[int] = Field(
        default=None, description="ID of the target project"
    )
    labels: Optional[List[Label]] = Field(
        default=None, description="List of labels assigned to the merge request"
    )  # Replaced tag_list
    tag_list: Optional[List[Tag]] = Field(
        default=None,
        description="List of tags associated with the merge request (deprecated: use labels)",
    )  # Deprecated
    draft: Optional[bool] = Field(
        default=None, description="Draft state of the merge request"
    )  # Replaced work_in_progress
    work_in_progress: Optional[bool] = Field(
        default=None,
        description="Whether the merge request is a work in progress (deprecated: use draft)",
    )  # Deprecated
    milestone: Optional[Milestone] = Field(
        default=None, description="Milestone associated with the merge request"
    )
    auto_merge: Optional[bool] = Field(
        default=None,
        description="Whether to merge automatically when conditions are met",
    )  # Replaced merge_when_pipeline_succeeds
    merge_when_pipeline_succeeds: Optional[bool] = Field(
        default=None,
        description="Whether to merge when the pipeline succeeds (deprecated: use auto_merge)",
    )  # Deprecated
    merge_status: Optional[str] = Field(
        default=None,
        description="Merge status of the merge request (deprecated: use detailed_merge_status)",
    )  # Deprecated
    detailed_merge_status: Optional[str] = Field(
        default=None, description="Detailed status of the merge request mergeability"
    )
    sha: Optional[str] = Field(default=None, description="SHA of the merge request")
    merge_commit_sha: Optional[str] = Field(
        default=None, description="Merge commit SHA of the merge request"
    )
    squash_commit_sha: Optional[str] = Field(
        default=None, description="Squash commit SHA of the merge request"
    )
    squash: Optional[bool] = Field(
        default=None, description="Whether the merge request should be squashed"
    )
    user_notes_count: Optional[int] = Field(
        default=None, description="Number of user notes on the merge request"
    )
    discussion_locked: Optional[bool] = Field(
        default=None, description="Whether the discussion is locked"
    )
    should_remove_source_branch: Optional[bool] = Field(
        default=None, description="Whether the source branch should be removed"
    )
    force_remove_source_branch: Optional[bool] = Field(
        default=None, description="Whether to force remove the source branch"
    )
    allow_collaboration: Optional[bool] = Field(
        default=None, description="Whether collaboration is allowed"
    )
    allow_maintainer_to_push: Optional[bool] = Field(
        default=None,
        description="Whether the maintainer can push (deprecated: alias for allow_collaboration)",
    )  # Deprecated
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="Web URL of the merge request"
    )
    references: Optional[References] = Field(
        default=None, description="References associated with the merge request"
    )  # Replaced reference
    reference: Optional[str] = Field(
        default=None,
        description="Reference associated with the merge request (deprecated: use references)",
    )  # Deprecated
    time_stats: Optional[TimeStats] = Field(
        default=None, description="Time statistics for the merge request"
    )
    task_completion_status: Optional[TaskCompletionStatus] = Field(
        default=None, description="Task completion status for the merge request"
    )
    has_conflicts: Optional[bool] = Field(
        default=None, description="Whether the merge request has conflicts"
    )
    blocking_discussions_resolved: Optional[bool] = Field(
        default=None, description="Whether blocking discussions are resolved"
    )
    changes: Optional[List[Diff]] = Field(
        default=None,
        description="List of changes (diffs) in the merge request (deprecated: use /diffs endpoint)",
    )  # Deprecated
    merge_user: Optional[User] = Field(
        default=None, description="User who merged the merge request"
    )  # Replaced merged_by
    merged_by: Optional[User] = Field(
        default=None,
        description="Merger of the merge request (deprecated: use merge_user)",
    )  # Deprecated
    merged_at: Optional[datetime] = Field(
        default=None, description="Date when the merge request was merged"
    )
    merge_after: Optional[datetime] = Field(
        default=None, description="Date when the merge request is set to be merged"
    )
    closed_by: Optional[User] = Field(
        default=None, description="User who closed the merge request"
    )
    closed_at: Optional[datetime] = Field(
        default=None, description="Date when the merge request was closed"
    )
    latest_build_started_at: Optional[datetime] = Field(
        default=None, description="Start date of the latest build"
    )
    latest_build_finished_at: Optional[datetime] = Field(
        default=None, description="Finish date of the latest build"
    )
    first_deployed_to_production_at: Optional[datetime] = Field(
        default=None, description="Date when first deployed to production"
    )
    head_pipeline: Optional[Pipeline] = Field(
        default=None, description="Head pipeline associated with the merge request"
    )  # Replaced pipeline
    pipeline: Optional[Pipeline] = Field(
        default=None,
        description="Pipeline associated with the merge request (deprecated: use head_pipeline)",
    )  # Deprecated
    diff_refs: Optional[DiffRefs] = Field(
        default=None, description="Diff references associated with the merge request"
    )  # Typed submodel
    user: Optional[User] = Field(
        default=None, description="User-specific information"
    )  # Typed submodel
    changes_count: Optional[str] = Field(
        default=None, description="Count of changes in the merge request"
    )
    rebase_in_progress: Optional[bool] = Field(
        default=None, description="Whether a rebase is in progress"
    )
    approvals_before_merge: Optional[int] = Field(
        default=None,
        description="Number of approvals required before merging (deprecated: use Approvals API)",
    )  # Deprecated
    imported: Optional[bool] = Field(
        default=None, description="Indicates if the merge request was imported"
    )
    imported_from: Optional[str] = Field(
        default=None, description="Source from where the merge request was imported"
    )
    prepared_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the merge request was prepared"
    )
    reviewers: Optional[List[User]] = Field(
        default=None, description="List of users reviewing the merge request"
    )  # Replaced reviewer
    reviewer: Optional[List[User]] = Field(
        default=None,
        description="List of reviewers for the merge request (deprecated: use reviewers)",
    )  # Deprecated
    review: Optional[Dict[str, Any]] = Field(
        default=None, description="Review information associated with the merge request"
    )
    subscribed: Optional[bool] = Field(
        default=None, description="Whether the user is subscribed to the merge request"
    )
    overflow: Optional[bool] = Field(
        default=None, description="Indicates if overflow is enabled"
    )
    diverged_commits_count: Optional[int] = Field(
        default=None, description="Number of diverged commits"
    )
    merge_error: Optional[Union[str, Any]] = Field(
        default=None, description="Merge errors, if any"
    )
    approvals_required: Optional[int] = Field(
        default=None, description="Number of approvals required"
    )
    approvals_left: Optional[int] = Field(
        default=None, description="Number of approvals still needed"
    )
    approved_by: Optional[List[User]] = Field(
        default=None, description="List of users who approved the merge request"
    )
    approval_rules_overwritten: Optional[bool] = Field(
        default=None, description="Whether approval rules are overwritten"
    )
    rules: Optional[List[ApprovalRule]] = Field(
        default=None, description="List of merge request approval rules"
    )
    first_contribution: Optional[bool] = Field(
        default=None, description="Indicates if this is the user's first contribution"
    )

    @field_validator("assignees", "reviewers", "approved_by", mode="before")
    def validate_users(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            users = []
            for item in v:
                if "user" in item:
                    users.append(User(**item["user"]))
                else:
                    users.append(User(**item))
            return users
        return v

    @field_validator("changes", mode="before")
    def validate_changes(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            diffs = []
            for item in v:
                diffs.append(Diff(**item))
            return diffs
        return v

    @field_validator("labels", mode="before")
    def validate_labels(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            labels = []
            for item in v:
                labels.append(Label(name=item))
            return labels
        return v

    @field_validator("tag_list", mode="before")
    def validate_tags(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            tags = []
            for item in v:
                tags.append(Tag(tag=item))
            return tags
        return v

    @field_validator("rules", mode="before")
    def validate_approval_rules(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            rules = []
            for item in v:
                rules.append(ApprovalRule(**item))
            return rules
        return v


class Epic(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Epic")
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the epic."
    )
    iid: Optional[int] = Field(
        default=None, description="Internal ID of the epic within the project."
    )
    title: Optional[str] = Field(default=None, description="Title of the epic.")
    url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL to the epic."
    )
    group_id: Optional[int] = Field(
        default=None, description="Group ID to which the epic belongs."
    )


class Issue(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Issue")
    state: Optional[str] = Field(
        default=None, description="State of the issue, e.g., opened or closed."
    )
    description: Optional[str] = Field(
        default=None, description="Description of the issue."
    )
    author: Optional[User] = Field(default=None, description="Author of the issue.")
    milestone: Optional[Milestone] = Field(
        default=None, description="Milestone associated with the issue."
    )
    project_id: Optional[int] = Field(
        default=None, description="Unique identifier for the project."
    )
    assignees: Optional[List[User]] = Field(
        default=None, description="List of assignees for the issue."
    )
    assignee: Optional[User] = Field(default=None, description="Assignee of the issue.")
    type: Optional[str] = Field(default=None, description="Type of the issue.")
    updated_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the issue was last updated."
    )
    closed_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the issue was closed."
    )
    closed_by: Optional[User] = Field(
        default=None, description="User who closed the issue."
    )
    changes_count: Optional[str] = Field(
        default=None, description="Count of changes in the issue"
    )
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the issue."
    )
    title: Optional[str] = Field(default=None, description="Title of the issue.")
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the issue was created."
    )
    moved_to_id: Optional[int] = Field(
        default=None, description="ID of the issue to which this issue was moved."
    )
    iid: Optional[int] = Field(
        default=None, description="Internal ID of the issue within the project."
    )
    labels: Optional[List[Label]] = Field(
        default=None, description="Labels associated with the issue."
    )
    upvotes: Optional[int] = Field(
        default=None, description="Number of upvotes the issue has received."
    )
    downvotes: Optional[int] = Field(
        default=None, description="Number of downvotes the issue has received."
    )
    merge_requests_count: Optional[int] = Field(
        default=None, description="Number of merge requests related to the issue."
    )
    user_notes_count: Optional[int] = Field(
        default=None, description="Number of user notes on the issue."
    )
    iteration: Optional[Iteration] = Field(
        default=None, description="Iteration of issue."
    )
    due_date: Optional[str] = Field(default=None, description="Due date for the issue.")
    imported: Optional[bool] = Field(
        default=None,
        description="Indicates if the issue was imported from another system.",
    )
    imported_from: Optional[str] = Field(
        default=None, description="Source from which the issue was imported."
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="Web URL to view the issue."
    )
    references: Optional[References] = Field(
        default=None, description="References of the issue."
    )
    time_stats: Optional[TimeStats] = Field(
        default=None, description="Time statistics for the issue."
    )
    has_tasks: Optional[bool] = Field(
        default=None, description="Indicates if the issue has tasks."
    )
    task_status: Optional[str] = Field(
        default=None, description="Status of the tasks in the issue."
    )
    confidential: Optional[bool] = Field(
        default=None, description="Indicates if the issue is confidential."
    )
    discussion_locked: Optional[bool] = Field(
        default=None, description="Indicates if discussion on the issue is locked."
    )
    issue_type: Optional[str] = Field(default=None, description="Type of the issue.")
    severity: Optional[str] = Field(
        default=None, description="Severity level of the issue."
    )
    links: Optional[Link] = Field(
        default=None, alias="_links", description="Links related to the issue."
    )
    task_completion_status: Optional[TaskCompletionStatus] = Field(
        default=None, description="Completion status of tasks in the issue."
    )
    weight: Optional[int] = Field(default=None, description="Weight of the issue.")
    epic_iid: Optional[int] = Field(
        default=None, description="Deprecated, use `iid` of the `epic` attribute."
    )
    epic: Optional[Epic] = Field(
        default=None, description="Epic to which the issue belongs."
    )
    health_status: Optional[str] = Field(
        default=None,
        description="Health status of the issue, e.g., on track or at risk.",
    )
    subscribed: Optional[bool] = Field(
        default=None, description="Indicates if the user is subscribed to the issue."
    )
    service_desk_reply_to: Optional[str] = Field(
        default=None, description="Service desk email for replies related to the issue."
    )
    blocking_issues_count: Optional[int] = Field(
        default=None, description="Blocking issue count."
    )

    @field_validator("assignees", mode="before")
    def empty_list_to_none(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            return v
        return v

    @field_validator("labels", mode="before")
    def validate_labels(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            labels = []
            for item in v:
                labels.append(Label(name=item))
            return labels
        return v


class PipelineVariable(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="PipelineVariable")
    key: Optional[str] = Field(default=None, description="The key of the variable.")
    variable_type: Optional[str] = Field(
        default=None, description="The type of the variable (e.g., env_var)."
    )
    value: Optional[str] = Field(default=None, description="The value of the variable.")


class TestCase(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="TestCase")
    status: Optional[str] = Field(
        default=None, description="The status of the test case (e.g., success, failed)."
    )
    name: Optional[str] = Field(default=None, description="The name of the test case.")
    classname: Optional[str] = Field(
        default=None, description="The class name of the test case."
    )
    execution_time: Optional[float] = Field(
        default=None, description="The execution time of the test case in seconds."
    )
    system_output: Optional[str] = Field(
        default=None, description="The system output of the test case."
    )
    stack_trace: Optional[str] = Field(
        default=None, description="The stack trace of the test case if it failed."
    )


class TestSuite(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="TestSuite")
    name: Optional[str] = Field(default=None, description="The name of the test suite.")
    total_time: Optional[float] = Field(
        default=None, description="The total time of the test suite in seconds."
    )
    total_count: Optional[int] = Field(
        default=None, description="The total number of test cases in the suite."
    )
    success_count: Optional[int] = Field(
        default=None, description="The number of successful test cases."
    )
    failed_count: Optional[int] = Field(
        default=None, description="The number of failed test cases."
    )
    skipped_count: Optional[int] = Field(
        default=None, description="The number of skipped test cases."
    )
    error_count: Optional[int] = Field(
        default=None, description="The number of test cases with errors."
    )
    test_cases: Optional[List[TestCase]] = Field(
        default=None, description="A list of test cases in the suite."
    )
    build_ids: Optional[List[int]] = Field(
        default=None, description="A list of build IDs related to the test suite."
    )
    suite_error: Optional[str] = Field(
        default=None, description="Errors encountered in the test suite."
    )

    @field_validator("test_cases", mode="before")
    def validate_test_cases(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            test_cases = []
            for item in v:
                test_cases.append(TestCase(**item))
            return test_cases
        return v


class TestReportTotal(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="TestReportTotal")
    time: Optional[int] = Field(
        default=None, description="The total time for all test cases in seconds."
    )
    count: Optional[int] = Field(
        default=None, description="The total number of test cases."
    )
    success: Optional[int] = Field(
        default=None, description="The total number of successful test cases."
    )
    failed: Optional[int] = Field(
        default=None, description="The total number of failed test cases."
    )
    skipped: Optional[int] = Field(
        default=None, description="The total number of skipped test cases."
    )
    error: Optional[int] = Field(
        default=None, description="The total number of test cases with errors."
    )
    suite_error: Optional[str] = Field(
        default=None, description="Errors encountered in the test suite."
    )


class TestReport(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="TestReport")
    total: Optional[TestReportTotal] = Field(
        default=None, description="Total count in test report."
    )
    test_suites: Optional[List[TestSuite]] = Field(
        default=None, description="A list of test suites in the report."
    )
    total_time: Optional[int] = Field(
        default=None, description="Total time of test report"
    )
    total_count: Optional[int] = Field(
        default=None, description="Total count of test report"
    )
    success_count: Optional[int] = Field(
        default=None, description="Success count of test report"
    )
    failed_count: Optional[int] = Field(
        default=None, description="Failed count of test report"
    )
    skipped_count: Optional[int] = Field(
        default=None, description="Skipped count of test report"
    )
    error_count: Optional[int] = Field(
        default=None, description="Error count of test report"
    )

    @field_validator("test_suites", mode="before")
    def validate_test_suites(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            test_suites = []
            for item in v:
                test_suites.append(TestSuite(**item))
            return test_suites
        return v


class MergeApprovals(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="MergeApprovals")
    approvers: Optional[List[User]] = Field(
        default=None, description="List of approvers"
    )
    approver_groups: Optional[List[Group]] = Field(
        default=None, description="List of approver groups"
    )
    approvals_before_merge: Optional[int] = Field(
        default=None, description="Number of approvals required before merge"
    )
    reset_approvals_on_push: Optional[bool] = Field(
        default=None, description="Whether approvals reset on new push"
    )
    selective_code_owner_removals: Optional[bool] = Field(
        default=None, description="Whether selective code owner removals are allowed"
    )
    disable_overriding_approvers_per_merge_request: Optional[bool] = Field(
        default=None,
        description="Whether overriding approvers per merge request is disabled",
    )
    merge_requests_author_approval: Optional[bool] = Field(
        default=None, description="Whether authors can approve their own merge requests"
    )
    merge_requests_disable_committers_approval: Optional[bool] = Field(
        default=None, description="Whether committers are disabled from approving"
    )
    require_password_to_approve: Optional[bool] = Field(
        default=None, description="Whether a password is required to approve"
    )

    @field_validator("approvers", mode="before")
    def empty_list_to_none(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            return v
        return v

    @field_validator("approver_groups", mode="before")
    def validate_groups(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            groups = []
            for item in v:
                groups.append(Group(**item))
            return groups
        return v


class DeployToken(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="DeployToken")
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the deploy token"
    )
    user_id: Optional[int] = Field(default=None, description="User ID.")
    name: Optional[str] = Field(default=None, description="Name of the deploy token")
    username: Optional[str] = Field(
        default=None, description="Username associated with the deploy token"
    )
    expires_at: Optional[datetime] = Field(
        default=None, description="Expiration date of the deploy token"
    )
    token: Optional[str] = Field(
        default=None, description="The actual deploy token string"
    )
    revoked: Optional[bool] = Field(
        default=None, description="Indicates whether the token has been revoked"
    )
    expired: Optional[bool] = Field(
        default=None, description="Indicates whether the token has expired"
    )
    scopes: Optional[List[str]] = Field(
        default=None, description="List of scopes assigned to the deploy token"
    )
    active: Optional[bool] = Field(default=None, description="Active token")
    last_used_at: Optional[Any] = Field(default=None, description="Last used at")
    created_at: Optional[datetime] = Field(
        default=None, description="Creation date and time of the token"
    )


class Rule(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Rule")
    id: int = Field(default=None, description="Unique identifier for the rule")
    created_at: datetime = Field(
        default=None, description="Timestamp when the rule was created"
    )
    commit_committer_check: bool = Field(
        default=None, description="Check for committer compliance"
    )
    commit_committer_name_check: bool = Field(
        default=None, description="Check for committer's name compliance"
    )
    reject_unsigned_commits: bool = Field(
        default=None, description="Flag to reject unsigned commits"
    )
    commit_message_regex: Optional[str] = Field(
        default=None, description="Regex for validating commit messages"
    )
    commit_message_negative_regex: Optional[str] = Field(
        default=None, description="Negative regex for commit messages"
    )
    branch_name_regex: Optional[str] = Field(
        default=None, description="Regex for validating branch names"
    )
    deny_delete_tag: bool = Field(
        default=None, description="Flag to deny deletion of tags"
    )
    member_check: bool = Field(default=None, description="Check for valid membership")
    prevent_secrets: bool = Field(
        default=None, description="Flag to prevent secrets in commits"
    )
    author_email_regex: Optional[str] = Field(
        default=None, description="Regex for author's email validation"
    )
    file_name_regex: Optional[str] = Field(
        default=None, description="Regex for file name validation"
    )
    max_file_size: Optional[int] = Field(
        default=None, description="Maximum file size allowed in MB"
    )


class Setting(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Setting")
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the setting"
    )
    value: bool = Field(default=None, description="Setting value.")
    locked: bool = Field(default=None, description="Locked State of setting.")
    inherited_from: str = Field(
        default=None, description="Project inherited rules from"
    )


class MergeRequestRuleSettings(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="MergeRequestRuleSettings")
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the rule"
    )
    allow_author_approval: Optional[Setting] = Field(
        default=None,
        description="Allow or prevent authors from self approving merge requests; true means authors can self approve.",
    )
    allow_committer_approval: Optional[Setting] = Field(
        default=None,
        description="Allow or prevent committers from self approving merge requests.",
    )
    allow_overrides_to_approver_list_per_merge_request: Optional[Setting] = Field(
        default=None,
        description="Allow or prevent overriding approvers per merge request.",
    )
    retain_approvals_on_push: Optional[Setting] = Field(
        default=None, description="Retain approval count on a new push."
    )
    selective_code_owner_removals: Optional[Setting] = Field(
        default=None,
        description="Reset approvals from Code Owners if their files changed. You must disable the retain_approvals_on_push field to use this field.",
    )
    require_password_to_approve: Optional[Setting] = Field(
        default=None, description="Negative regex for commit messages"
    )
    require_reauthentication_to_approve: Optional[Setting] = Field(
        default=None,
        description="Require approver to authenticate before adding the approval.",
    )


class AccessControl(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="AccessControl")
    name: str = Field(default=None, description="Name of the access group")
    access_level: Optional[int] = Field(
        default=None, description="Access level as an integer"
    )
    member_role_id: Optional[int] = Field(
        default=None, description="Role ID for the member in the group"
    )


class Source(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Source")
    format: Optional[str] = Field(
        default=None, description="Format of the source file (e.g., zip, tar.gz)"
    )
    url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL to download the source file"
    )


class Assets(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Assets")
    count: Optional[int] = Field(default=None, description="Total count of assets")
    sources: Optional[List[Source]] = Field(
        default=None, description="List of source files"
    )
    links: Optional[List[Link]] = Field(
        default=None, description="List of additional links"
    )
    evidence_file_path: Optional[str] = Field(
        default=None, description="URL to the evidence file"
    )

    @field_validator("sources", mode="before")
    def validate_sources(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            sources = []
            for item in v:
                sources.append(Source(**item))
            return sources
        return v

    @field_validator("links", mode="before")
    def validate_links(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            links = []
            for item in v:
                links.append(Link(**item))
            return links
        return v


class Evidence(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Evidence")
    sha: Optional[str] = Field(
        default=None, description="SHA checksum of the evidence file"
    )
    filepath: Optional[str] = Field(
        default=None, description="Filepath of the evidence file"
    )
    collected_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the evidence was collected"
    )


class ReleaseLinks(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="ReleaseLinks")
    closed_issues_url: Optional[Union[HttpUrl, str]] = Field(
        None, description="URL to the list of closed issues"
    )
    closed_merge_requests_url: Optional[Union[HttpUrl, str]] = Field(
        None, description="URL to the list of closed merge requests"
    )
    edit_url: Optional[Union[HttpUrl, str]] = Field(
        None, description="URL to edit the release"
    )
    merged_merge_requests_url: Optional[Union[HttpUrl, str]] = Field(
        None, description="URL to the list of merged merge requests"
    )
    opened_issues_url: Optional[Union[HttpUrl, str]] = Field(
        None, description="URL to the list of opened issues"
    )
    opened_merge_requests_url: Optional[Union[HttpUrl, str]] = Field(
        None, description="URL to the list of opened merge requests"
    )
    self_link: Optional[str] = Field(
        None, alias="self", description="Self-referencing URL"
    )


class Release(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Release")
    tag_name: Optional[str] = Field(default=None, description="Tag name of the release")
    description: Optional[str] = Field(
        default=None, description="Description of the release"
    )
    name: Optional[str] = Field(default=None, description="Name of the release")
    upcoming_release: Optional[bool] = Field(
        default=None, description="If this is an upcoming release"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Creation date and time of the release"
    )
    released_at: Optional[datetime] = Field(
        default=None, description="Release date and time"
    )
    author: Optional[User] = Field(default=None, description="Author of the release")
    commit: Optional[Commit] = Field(
        default=None, description="Commit associated with the release"
    )
    milestones: Optional[List[Milestone]] = Field(
        default=None, description="List of milestones related to the release"
    )
    commit_path: Optional[str] = Field(
        default=None, description="Path to the commit associated with the release"
    )
    tag_path: Optional[str] = Field(
        default=None, description="Path to the tag associated with the release"
    )
    assets: Optional[Assets] = Field(
        default=None, description="Assets related to the release"
    )
    evidences: Optional[List[Evidence]] = Field(
        default=None, description="List of evidences related to the release"
    )
    links: Optional[ReleaseLinks] = Field(
        default=None, alias="_links", description="Links related to the release"
    )
    evidence_sha: Optional[str] = Field(default=None, description="Evidence hash")

    @field_validator("milestones", mode="before")
    def validate_milestones(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            milestones = []
            for item in v:
                milestones.append(Milestone(**item))
            return milestones
        return v

    @field_validator("evidences", mode="before")
    def validate_evidences(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            evidences = []
            for item in v:
                evidences.append(Evidence(**item))
            return evidences
        return v


class Token(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Token")
    id: Optional[int] = Field(None, description="Token ID")
    token: Optional[str] = Field(None, description="Authentication token")
    token_expires_at: Optional[datetime] = Field(
        None, description="Expiration date and time of the token"
    )


class ToDo(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="ToDo")
    id: int = Field(default=None, description="To-do identifier")
    project: Project = Field(
        default=None, description="Project associated with the to-do"
    )
    author: User = Field(default=None, description="Author of the to-do")
    action_name: str = Field(default=None, description="Action taken in the to-do")
    target_type: str = Field(
        default=None, description="Type of target referenced in the to-do"
    )
    target: Issue = Field(default=None, description="Target issue for the to-do")
    target_url: Union[HttpUrl, str] = Field(
        default=None, description="URL pointing to the target of the to-do"
    )
    body: str = Field(default=None, description="Body text of the to-do")
    state: str = Field(default=None, description="State of the to-do")
    created_at: datetime = Field(
        default=None, description="Timestamp when the to-do was created"
    )


class WikiPage(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="WikiPage")
    content: Optional[str] = Field(None, description="Content of the wiki page")
    format: Optional[str] = Field(
        None, description="Format of the wiki page content (e.g., markdown, rdoc)"
    )
    slug: Optional[str] = Field(
        None, description="Slug (URL-friendly identifier) of the wiki page"
    )
    title: Optional[str] = Field(None, description="Title of the wiki page")
    encoding: Optional[str] = Field(
        None, description="Encoding of the wiki page content (e.g., UTF-8)"
    )


class WikiAttachmentLink(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="WikiAttachmentLink")
    url: Optional[Union[HttpUrl, str]] = Field(
        None, description="URL of the uploaded attachment"
    )
    markdown: Optional[str] = Field(
        None, description="Markdown to embed the uploaded attachment"
    )


class WikiAttachment(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="WikiAttachment")
    file_name: Optional[str] = Field(None, description="Name of the uploaded file")
    file_path: Optional[str] = Field(None, description="Path where the file is stored")
    branch: Optional[str] = Field(
        None, description="Branch where the attachment is uploaded"
    )
    link: Optional[WikiAttachmentLink] = Field(
        None, description="Link information for the uploaded attachment"
    )


class Agent(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Agent")
    id: int = Field(default=None, description="Agent identifier")
    config_project: ProjectConfig = Field(
        default=None, description="Configuration project associated with the agent"
    )


class Agents(BaseModel):
    model_config = ConfigDict(extra="allow")
    __hash__ = object.__hash__
    base_type: str = Field(default="Agents")
    allowed_agents: list[Agent] = Field(
        default=None, description="List of allowed agents"
    )
    job: Job = Field(default=None, description="Job associated with the agents")
    pipeline: Pipeline = Field(
        default=None, description="Pipeline associated with the agents"
    )
    project: Project = Field(
        default=None, description="Project associated with the agents"
    )
    user: User = Field(default=None, description="User associated with the agents")


T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """
    A wrapper class to hold the original requests.Response along with the parsed Pydantic data.
    This allows access to response metadata (e.g., status_code, headers) while providing
    the parsed data in Pydantic models.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)
    base_type: str = Field(default="Response")
    response: requests.Response = Field(
        default=None, description="The original requests.Response object", exclude=True
    )
    data: Optional[Union[T, List[T]]] = Field(
        default=None, description="The Pydantic models converted from the response"
    )
