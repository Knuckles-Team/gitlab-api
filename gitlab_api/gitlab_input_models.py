#!/usr/bin/python
# coding: utf-8
import re

from typing import Union, List, Dict, Optional
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    HttpUrl,
    EmailStr,
)

try:
    from gitlab_api.decorators import require_auth
except ModuleNotFoundError:
    pass
try:
    from gitlab_api.exceptions import (
        AuthError,
        UnauthorizedError,
        ParameterError,
        MissingParameterError,
    )
except ModuleNotFoundError:
    from exceptions import (
        ParameterError,
        MissingParameterError,
    )


class BranchModel(BaseModel):
    """
    Pydantic model representing information about a branch.

    Attributes:
        project_id (Union[int, str]): The identifier of the project associated with the branch.
        branch (str, optional): The name of the branch.
        reference (str, optional): Reference information for the branch.
        api_parameters (str): Additional API parameters for the group.

    Comments:
        This model includes a validator `validate_required_parameters` to ensure that the `project_id` field is
        provided when either `branch` or `reference` is specified.
    """

    project_id: Union[int, str]
    branch: Optional[str] = None
    reference: Optional[str] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.branch:
            self.api_parameters["branch"] = self.branch
        if self.reference:
            self.api_parameters["ref"] = self.reference


class CommitModel(BaseModel):
    """
    Pydantic model representing a commit.

    Attributes:
    - project_id (Union[int, str]): Identifier for the project.
    - commit_hash (str): Hash of the commit.
    - branch (str): Name of the branch.
    - dry_run (bool): Flag indicating a dry run.
    - message (str): Commit message.
    - state (str): State of the commit.
    - reference (str): Reference identifier.
    - name (str): Name of the commit.
    - context (str): Context of the commit.
    - target_url (str): Target URL for the commit.
    - description (str): Description of the commit.
    - coverage (Union[float, str]): Code coverage value.
    - pipeline_id (Union[int, str]): Identifier for the pipeline.
    - actions (list): List of actions.
    - start_branch (str): Starting branch for the commit.
    - start_sha (str): Starting SHA for the commit.
    - start_project (Union[int, str]): Identifier for the starting project.
    - author_email (str): Email of the author.
    - author_name (str): Name of the author.
    - stats (bool): Flag indicating whether to include stats.
    - force (bool): Flag indicating a forced commit.
    - line (int): Line number for the commit.
    - line_type (str): Type of line.
    - note (str): Note for the commit.
    - path (str): Path for the commit.
    - group_ids (list): List of group identifiers.
    - protected_branch_ids (list): List of protected branch identifiers.
    - report_type (str): Type of report.
    - rule_type (str): Type of rule.
    - user_ids (list): List of user identifiers.
    - data (Dict): Dictionary containing additional data.

    Note:
    The class includes field_validator functions for specific attribute validations.
    """

    project_id: Union[int, str]
    commit_hash: Optional[str] = None
    branch: Optional[str] = None
    dry_run: Optional[bool] = None
    message: Optional[str] = None
    state: Optional[str] = None
    reference: Optional[str] = None
    name: Optional[str] = None
    context: Optional[str] = None
    target_url: Optional[Union[HttpUrl, str]] = None
    description: Optional[str] = None
    coverage: Optional[Union[float, str]] = None
    pipeline_id: Optional[Union[int, str]] = None
    actions: Optional[list] = None
    start_branch: Optional[str] = None
    start_sha: Optional[str] = None
    start_project: Optional[Union[int, str]] = None
    author_email: Optional[EmailStr] = None
    author_name: Optional[str] = None
    stats: Optional[bool] = None
    force: Optional[bool] = None
    line: Optional[int] = None
    line_type: Optional[str] = None
    note: Optional[str] = None
    path: Optional[str] = None
    group_ids: Optional[list] = None
    protected_branch_ids: Optional[list] = None
    report_type: Optional[str] = None
    rule_type: Optional[str] = None
    user_ids: Optional[list] = None
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    @field_validator("dry_run", "stats", "force")
    def validate_bool_fields(cls, v):
        """
        Validate boolean fields to ensure they are valid boolean values.

        Args:
        - v: The value of the field.

        Returns:
        - bool: The validated field value.

        Raises:
        - ValueError: If the field is provided and not a boolean.
        """
        if v is not None and not isinstance(v, bool):
            raise ValueError("Invalid states")
        return v

    @field_validator(
        "commit_hash",
        "branch",
        "reference",
        "name",
        "context",
        "note",
        "path",
        "line_type",
    )
    def validate_string_parameters(cls, v):
        """
        Validate string parameters to ensure they are valid strings.

        Args:
        - v: The value of the parameter.

        Returns:
        - str: The validated parameter value.

        Raises:
        - ValueError: If the parameter is provided and not a string.
        """
        if v is not None and not isinstance(v, str):
            raise ValueError("Invalid optional params")
        return v

    @field_validator("coverage")
    def validate_coverage(cls, v):
        """
        Validate the 'coverage' parameter to ensure it is a valid float or int.

        Args:
        - v: The value of 'coverage'.

        Returns:
        - Union[float, str]: The validated 'coverage' value.

        Raises:
        - ValueError: If 'coverage' is provided and not a float or int.
        """
        if v is not None and not isinstance(v, (float, int)):
            raise ValueError("Invalid states")
        return v

    @field_validator("state")
    def validate_state(cls, v):
        """
        Validate the 'state' parameter to ensure it is a valid state.

        Args:
        - v: The value of 'state'.

        Returns:
        - str: The validated 'state'.

        Raises:
        - ValueError: If 'state' is provided and not a valid state.
        """
        if v is not None and v.lower() not in [
            "pending",
            "running",
            "success",
            "failed",
            "canceled",
        ]:
            raise ValueError("Invalid states")
        return v

    @field_validator("line_type")
    def validate_line_type(cls, v):
        """
        Validate the 'line_type' parameter to ensure it is a valid line type.

        Args:
        - v: The value of 'line_type'.

        Returns:
        - str: The validated 'line_type'.

        Raises:
        - ValueError: If 'line_type' is provided and not a valid line type.
        """
        if v is not None and v.lower() not in ["new", "old"]:
            raise ValueError("Invalid line_type")
        return v

    @field_validator("report_type")
    def validate_report_type(cls, v):
        """
        Validate the 'report_type' parameter to ensure it is a valid report type.

        Args:
        - v: The value of 'report_type'.

        Returns:
        - str: The validated 'report_type'.

        Raises:
        - ValueError: If 'report_type' is provided and not a valid report type.
        """
        if v is not None and v.lower() not in ["license_scanning", "code_coverage"]:
            raise ValueError("Invalid report_type")
        return v

    @field_validator("rule_type")
    def validate_rule_type(cls, v):
        """
        Validate the 'rule_type' parameter to ensure it is a valid rule type.

        Args:
        - v: The value of 'rule_type'.

        Returns:
        - str: The validated 'rule_type'.

        Raises:
        - ValueError: If 'rule_type' is provided and not a valid rule type.
        """
        if v is not None and v.lower() not in ["any_approver", "regular"]:
            raise ValueError("Invalid rule_type")
        return v

    @field_validator("user_ids", "group_ids", "protected_branch_ids")
    def validate_list_parameters(cls, v):
        """
        Validate list parameters to ensure they are valid lists.

        Args:
        - v: The value of the parameter.

        Returns:
        - list: The validated parameter value.

        Raises:
        - ValueError: If the parameter is provided and not a list.
        """
        if v is not None and not isinstance(v, list):
            raise ValueError("Invalid user_ids, group_ids, protected_branch_ids")
        return v

    @model_validator(mode="before")
    def construct_data_dict(cls, values):
        """
        Construct a data dictionary from specific values.

        Args:
        - values: The values of specific parameters.

        Returns:
        - Dict: The constructed data dictionary.

        Raises:
        - ValueError: If no key is present in the data dictionary.
        """
        data = {}

        if "branch" in values:
            data["branch"] = values.get("branch")
        if "commit_message" in values:
            data["commit_message"] = values.get("commit_message")
        if "start_branch" in values:
            data["start_branch"] = values.get("start_branch")
        if "start_sha" in values:
            data["start_sha"] = values.get("start_sha")
        if "start_project" in values:
            data["start_project"] = values.get("start_project")
        if "actions" in values:
            data["actions"] = values.get("actions")
        if "author_email" in values:
            data["author_email"] = values.get("author_email")
        if "author_name" in values:
            data["author_name"] = values.get("author_name")
        if "stats" in values:
            data["stats"] = values.get("stats")
        if "force" in values:
            data["force"] = values.get("force")
        if "note" in values:
            data["note"] = values.get("note")
        if "path" in values:
            data["path"] = values.get("path")
        if "line" in values:
            data["line"] = values.get("line")
        if "line_type" in values:
            data["line_type"] = values.get("line_type")
        if "state" in values:
            data["state"] = values.get("state")
        if "reference" in values:
            data["ref"] = values.get("reference")
        if "name" in values:
            data["name"] = values.get("name")
        if "context" in values:
            data["context"] = values.get("context")
        if "target_url" in values:
            data["target_url"] = values.get("target_url")
        if "description" in values:
            data["description"] = values.get("description")
        if "coverage" in values:
            data["coverage"] = values.get("coverage")
        if "pipeline_id" in values:
            data["pipeline_id"] = values.get("pipeline_id")

        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data
        return values


class DeployTokenModel(BaseModel):
    """
    Pydantic model representing a deploy token.

    Attributes:
    - project_id (Union[int, str]): Identifier for the project.
    - group_id (Union[int, str]): Identifier for the group.
    - token (str): Deploy token.
    - name (str): Name associated with the token.
    - expires_at (str): Expiration date and time of the token.
    - username (str): Username associated with the token.
    - scopes (str): Scopes assigned to the token.

    Note:
    The class includes field_validator functions for specific attribute validations.
    """

    project_id: Union[int, str] = None
    group_id: Optional[Union[int, str]] = None
    token: Optional[str] = None
    name: Optional[str] = None
    expires_at: Optional[str] = None
    username: Optional[str] = None
    scopes: Optional[str] = None

    @field_validator("expires_at")
    def validate_expires_at(cls, v):
        """
        Validate the 'expires_at' parameter to ensure it is a valid string.

        Args:
        - v: The value of 'expires_at'.

        Returns:
        - str: The validated 'expires_at' value.

        Raises:
        - ParameterError: If 'expires_at' is provided and not a string.
        """
        if v is not None and not isinstance(v, str):
            raise ParameterError
        return v

    @field_validator("project_id", "group_id", "token")
    def validate_optional_parameters(cls, v, values):
        """
        Validate optional parameters to ensure they are provided only when 'project_id' or 'group_id' is provided.

        Args:
        - v: The value of the parameter.
        - values: Dictionary of all values.

        Returns:
        - Any: The validated parameter value.

        Raises:
        - MissingParameterError: If the parameter is provided and 'project_id' and 'group_id' are None.
        """
        if (
            "project_id" in values.lower() or "group_id" in values.lower()
        ) and v is not None:
            return v.lower()
        else:
            raise MissingParameterError

    @field_validator("name", "username", "scopes")
    def validate_string_parameters(cls, v):
        """
        Validate string parameters to ensure they are valid strings.

        Args:
        - v: The value of the parameter.

        Returns:
        - str: The validated parameter value.

        Raises:
        - ParameterError: If the parameter is provided and not a string.
        """
        if v is not None and not isinstance(v, str):
            raise ParameterError
        return v

    @field_validator("scopes")
    def validate_scopes(cls, v):
        """
        Validate the 'scopes' parameter to ensure it is a valid scope.

        Args:
        - v: The value of 'scopes'.

        Returns:
        - str: The validated 'scopes' value.

        Raises:
        - ParameterError: If 'scopes' is provided and not a valid scope.
        """
        valid_scopes = [
            "read_repository",
            "read_registry",
            "write_registry",
            "read_package_registry",
            "write_package_registry",
        ]
        if v is not None and v.lower() not in valid_scopes:
            raise ParameterError
        return v


class GroupModel(BaseModel):
    """
    Pydantic model representing a group.

    Attributes:
    - group_id (Union[int, str]): Identifier for the group.
    - per_page (int): Number of items to display per page (default is 100).
    - page (int): Page number for pagination (default is 1).
    - argument (str): Argument to filter groups (default is 'state=opened').
    - api_parameters (str): Additional API parameters for the group.

    Note:
    The class includes field_validator functions for specific attribute validations.
    """

    group_id: Union[int, str] = Field(description="The group ID.", default=None)
    name: Optional[str] = Field(description="The name of the group.", default=None)
    path: Optional[str] = Field(description="The path of the group.", default=None)
    auto_devops_enabled: Optional[bool] = Field(
        description="Enable Auto DevOps pipeline by default.", default=None
    )
    avatar: Optional[bytes] = Field(
        description="Image file for avatar of the group.", default=None
    )
    default_branch: Optional[str] = Field(
        description="The default branch name for the group's projects.", default=None
    )
    default_branch_protection: Optional[int] = Field(
        description="Deprecated: Use default_branch_protection_defaults instead.",
        default=None,
    )
    default_branch_protection_defaults: Optional[Dict] = Field(
        description="Options for default_branch_protection_defaults.", default=None
    )
    description: Optional[str] = Field(
        description="The description of the group.", default=None
    )
    enabled_git_access_protocol: Optional[str] = Field(
        description="Enabled protocols for Git access (ssh, http, or all).",
        default=None,
    )
    emails_enabled: Optional[bool] = Field(
        description="Enable email notifications.", default=None
    )
    lfs_enabled: Optional[bool] = Field(
        description="Enable or disable Large File Storage (LFS).", default=None
    )
    mentions_disabled: Optional[bool] = Field(
        description="Disable mentions for the group.", default=None
    )
    prevent_sharing_groups_outside_hierarchy: Optional[bool] = Field(
        description="Prevent sharing groups outside the hierarchy.", default=None
    )
    project_creation_level: Optional[str] = Field(
        description="Determine if developers can create projects (no-one, maintainer, or developer).",
        default=None,
    )
    request_access_enabled: Optional[bool] = Field(
        description="Allow users to request member access.", default=None
    )
    require_two_factor_authentication: Optional[bool] = Field(
        description="Require all users to set up two-factor authentication.",
        default=None,
    )
    shared_runners_setting: Optional[str] = Field(
        description="Options for shared runners (enabled or disabled).", default=None
    )
    share_with_group_lock: Optional[bool] = Field(
        description="Prevent sharing a project with another group.", default=None
    )
    subgroup_creation_level: Optional[str] = Field(
        description="Allowed to create subgroups (owner or maintainer).", default=None
    )
    two_factor_grace_period: Optional[int] = Field(
        description="Time before two-factor authentication is enforced (in hours).",
        default=None,
    )
    visibility: Optional[str] = Field(
        description="Visibility level of the group (private, internal, or public).",
        default=None,
    )
    extra_shared_runners_minutes_limit: Optional[int] = Field(
        description="Additional compute minutes for the group (admins only).",
        default=None,
    )
    file_template_project_id: Optional[int] = Field(
        description="ID of a project to load custom file templates from.", default=None
    )
    membership_lock: Optional[bool] = Field(
        description="Prevent adding users to projects in this group.", default=None
    )
    prevent_forking_outside_group: Optional[bool] = Field(
        description="Prevent forking projects to external namespaces.", default=None
    )
    shared_runners_minutes_limit: Optional[int] = Field(
        description="Maximum number of monthly compute minutes for this group.",
        default=None,
    )
    unique_project_download_limit: Optional[int] = Field(
        description="Max unique projects a user can download in a time period.",
        default=None,
    )
    unique_project_download_limit_interval_in_seconds: Optional[int] = Field(
        description="Time period for unique project download limit (in seconds).",
        default=None,
    )
    unique_project_download_limit_allowlist: Optional[List[str]] = Field(
        description="Usernames excluded from the unique project download limit.",
        default=None,
    )
    unique_project_download_limit_alertlist: Optional[List[int]] = Field(
        description="User IDs alerted when unique project download limit is exceeded.",
        default=None,
    )
    auto_ban_user_on_excessive_projects_download: Optional[bool] = Field(
        description="Automatically ban users exceeding project download limits.",
        default=None,
    )
    ip_restriction_ranges: Optional[str] = Field(
        description="Comma-separated IP addresses or subnets to restrict access.",
        default=None,
    )
    allowed_email_domains_list: Optional[str] = Field(
        description="Comma-separated list of allowed email domains.", default=None
    )
    wiki_access_level: Optional[str] = Field(
        description="Wiki access level (disabled, private, or enabled).", default=None
    )
    math_rendering_limits_enabled: Optional[bool] = Field(
        description="Indicates if math rendering limits are used for this group.",
        default=None,
    )
    lock_math_rendering_limits_enabled: Optional[bool] = Field(
        description="Indicates if math rendering limits are locked for descendent groups.",
        default=None,
    )
    duo_features_enabled: Optional[bool] = Field(
        description="Indicates whether GitLab Duo features are enabled.", default=None
    )
    lock_duo_features_enabled: Optional[bool] = Field(
        description="Indicates whether GitLab Duo features setting is enforced for subgroups.",
        default=None,
    )
    total_pages: Optional[int] = Field(
        description="Total number of pages", default=None
    )
    max_pages: Optional[int] = Field(
        description="Max amount of pages to retrieve", default=None
    )
    per_page: Optional[int] = Field(description="Results per page", default=100)
    page: Optional[int] = Field(description="Pagination page", default=1)
    argument: Optional[str] = Field(
        description="Any additional parameter arguments.", default="state=opened"
    )
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    @model_validator(mode="before")
    def build_data(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        data = {}

        for field_name, value in values.items():
            if field_name in cls.__annotations__ and value is not None:
                data[field_name] = value

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data

        return values

    @field_validator("per_page", "page")
    def validate_positive_integer(cls, v):
        """
        Validate positive integer parameters.

        Args:
        - v: The value of the parameter.

        Returns:
        - int: The validated parameter value.

        Raises:
        - ParameterError: If the parameter is not a positive integer.
        """
        if not v:
            return None
        if isinstance(v, str):
            try:
                v = int(v)
            except Exception as e:
                raise e
        if not isinstance(v, int) or v < 0:
            raise ParameterError
        return v

    @field_validator("argument")
    def validate_argument(cls, v):
        """
        Validate the 'argument' parameter to ensure it is a valid string.

        Args:
        - v: The value of 'argument'.

        Returns:
        - str: The validated 'argument' value.

        Raises:
        - ParameterError: If 'argument' is provided and not a string.
        """
        if not isinstance(v, str):
            raise ParameterError
        return v

    @field_validator("visibility")
    def validate_visibility(cls, value):
        """
        Validate visibility value.

        Args:
        - value: visibility value to validate.

        Returns:
        - The validated visibility value.

        Raises:
        - ValueError: If the value is not a valid order_by.
        """
        if value.lower() not in ["internal", "private", "public"]:
            raise ValueError("Invalid visibility")
        return value.lower()

    @field_validator("group_id")
    def validate_group_id(cls, v):
        """
        Validate the 'group_id' parameter to ensure it is provided.

        Args:
        - v: The value of 'group_id'.

        Returns:
        - Union[int, str]: The validated 'group_id' value.

        Raises:
        - MissingParameterError: If 'group_id' is None.
        """
        if v is None:
            raise MissingParameterError
        return v

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.max_pages:
            self.api_parameters["max_pages"] = self.max_pages
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page
        if self.total_pages:
            self.api_parameters["total_pages"] = self.total_pages


class JobModel(BaseModel):
    """
    Pydantic model representing a job.

    Attributes:
    - project_id (Union[int, str]): Identifier for the project.
    - job_id (Union[int, str]): Identifier for the job.
    - scope (List[str]): List of job scopes.
    - per_page (int): Number of items to display per page (default is 100).
    - page (int): Page number for pagination (default is 1).
    - include_retried (bool): Flag indicating whether to include retried jobs.
    - job_variable_attributes (Dict): Dictionary of job variable attributes.
    - api_parameters (str): Additional API parameters for the job.

    Note:
    The class includes field_validator functions for specific attribute validations.
    """

    project_id: Union[int, str] = None
    pipeline_id: Union[int, str] = None
    job_id: Union[int, str] = None
    scope: Optional[List[str]] = None
    total_pages: Optional[int] = Field(
        description="Total number of pages", default=None
    )
    max_pages: Optional[int] = Field(
        description="Max amount of pages to retrieve", default=None
    )
    page: Optional[int] = Field(description="Page in multi-page response", default=None)
    per_page: Optional[int] = Field(
        description="Amount of items per page", default=None
    )
    include_retried: Optional[bool] = None
    job_variable_attributes: Optional[Dict] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)

    @field_validator("per_page", "page")
    def validate_positive_integer(cls, v):
        """
        Validate positive integer parameters.

        Args:
        - v: The value of the parameter.

        Returns:
        - int: The validated parameter value.

        Raises:
        - ParameterError: If the parameter is not a positive integer.
        """
        if not v:
            return None
        if isinstance(v, str):
            try:
                v = int(v)
            except Exception as e:
                raise e
        if not isinstance(v, int) or v < 0:
            raise ParameterError
        return v

    @field_validator("include_retried")
    def validate_include_retried(cls, v):
        """
        Validate the 'include_retried' parameter to ensure it is a valid boolean.

        Args:
        - v: The value of 'include_retried'.

        Returns:
        - bool: The validated 'include_retried' value.

        Raises:
        - ParameterError: If 'include_retried' is provided and not a boolean.
        """
        if v is not None and not isinstance(v, bool):
            raise ParameterError
        return v

    @field_validator("scope")
    def validate_scope(cls, v):
        """
        Validate the 'scope' parameter to ensure it is a valid list of job scopes.

        Args:
        - v: The value of 'scope'.

        Returns:
        - List[str]: The validated 'scope' value.

        Raises:
        - ParameterError: If 'scope' contains invalid values.
        """
        if v.lower() not in [
            "created",
            "pending",
            "running",
            "failed",
            "success",
            "canceled",
            "skipped",
            "waiting_for_resource",
            "manual",
        ]:
            raise ParameterError
        return v.lower()

    @field_validator("job_variable_attributes")
    def validate_job_variable_attributes(cls, v):
        """
        Validate the 'job_variable_attributes' parameter to ensure it is a valid dictionary.

        Args:
        - v: The value of 'job_variable_attributes'.

        Returns:
        - Dict: The validated 'job_variable_attributes' value.

        Raises:
        - ParameterError: If 'job_variable_attributes' is provided and not a dictionary or missing key.
        """
        if v is not None and (
            not isinstance(v, dict) or "job_variable_attributes" not in v.keys()
        ):
            raise ParameterError
        return v

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.max_pages:
            self.api_parameters["max_pages"] = self.max_pages
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page
        if self.total_pages:
            self.api_parameters["total_pages"] = self.total_pages
        if self.scope:
            self.api_parameters["scope[]"] = self.scope


class MembersModel(BaseModel):
    """
    Pydantic model representing members.

    Attributes:
    - group_id (Union[int, str]): Identifier for the group.
    - project_id (Union[int, str]): Identifier for the project.
    - per_page (int): Number of items to display per page (default is 100).
    - page (int): Page number for pagination (default is 1).
    - api_parameters (str): Additional API parameters for members.

    Note:
    The class includes field_validator functions for specific attribute validations.
    """

    group_id: Optional[Union[int, str]] = None
    project_id: Optional[Union[int, str]] = None
    per_page: Optional[int] = Field(description="Results per page", default=100)
    page: Optional[int] = Field(description="Pagination page", default=1)
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)

    @field_validator("per_page", "page")
    def validate_positive_integer(cls, v):
        """
        Validate positive integer parameters.

        Args:
        - v: The value of the parameter.

        Returns:
        - int: The validated parameter value.

        Raises:
        - ParameterError: If the parameter is not a positive integer.
        """
        if not v:
            return None
        if isinstance(v, str):
            try:
                v = int(v)
            except Exception as e:
                raise e
        if not isinstance(v, int) or v < 0:
            raise ParameterError
        return v

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page


class MergeRequestModel(BaseModel):
    """
    Pydantic model representing a merge request.

    Attributes:
    - approved_by_ids (List[int]): List of user IDs who approved the merge request.
    - approver_ids (List[int]): List of user IDs who can approve the merge request.
    - assignee_id (int): User ID assigned to the merge request.
    - author_id (int): User ID of the author of the merge request.
    - author_username (str): Username of the author of the merge request.
    - created_after (str): Date string for filtering merge requests created after a certain date.
    - created_before (str): Date string for filtering merge requests created before a certain date.
    - deployed_after (str): Date string for filtering merge requests deployed after a certain date.
    - deployed_before (str): Date string for filtering merge requests deployed before a certain date.
    - environment (str): Environment of the merge request.
    - search_in (str): Field to search within the merge request.
    - labels (str): Labels associated with the merge request.
    - milestone (str): Milestone of the merge request.
    - my_reaction_emoji (str): User's reaction emoji for the merge request.
    - project_id (Union[int, str]): Identifier for the project.
    - search_exclude (str): Field to exclude from search.
    - order_by (str): Field to order results by.
    - reviewer_id (Union[int, str]): User ID of the reviewer.
    - reviewer_username (str): Username of the reviewer.
    - scope (List[str]): List of scopes for the merge request.
    - search (str): Search term for filtering merge requests.
    - sort (str): Sort order for results.
    - source_branch (str): Source branch of the merge request.
    - state (str): State of the merge request.
    - target_branch (str): Target branch of the merge request.
    - updated_after (str): Date string for filtering merge requests updated after a certain date.
    - updated_before (str): Date string for filtering merge requests updated before a certain date.
    - view (str): View setting for the merge request.
    - with_labels_details (bool): Include label details in the merge request.
    - with_merge_status_recheck (bool): Include merge status recheck in the merge request.
    - wip (str): Work in progress status for the merge request.
    - title (str): Title of the merge request.
    - allow_collaboration (bool): Allow collaboration on the merge request.
    - allow_maintainer_to_push (bool): Allow maintainer to push to the merge request.
    - approvals_before_merge (int): Number of approvals required before merging.
    - assignee_ids (List[int]): List of user IDs assigned to the merge request.
    - description (str): Description of the merge request.
    - milestone_id (int): Milestone ID of the merge request.
    - remove_source_branch (str): Branch removal status for the merge request.
    - reviewer_ids (List[int]): List of user IDs who reviewed the merge request.
    - squash (bool): Squash commits on merge.
    - target_project_id (Union[int, str]): Identifier for the target project.
    - max_pages (int): Maximum number of pages to retrieve (default is 0).
    - per_page (int): Number of items to display per page (default is 100).
    - api_parameters (str): Additional API parameters for the merge request.
    - data (Dict): Additional data for the merge request.

    Note:
    The class includes field_validator functions for specific attribute validations.
    """

    approved_by_ids: Optional[List[int]] = None
    approver_ids: Optional[List[int]] = None
    assignee_id: Optional[int] = None
    author_id: Optional[int] = None
    author_username: Optional[str] = None
    created_after: Optional[str] = None
    created_before: Optional[str] = None
    deployed_after: Optional[str] = None
    deployed_before: Optional[str] = None
    environment: Optional[str] = None
    search_in: Optional[str] = None
    labels: Optional[str] = None
    milestone: Optional[str] = None
    my_reaction_emoji: Optional[str] = None
    project_id: Optional[Union[int, str]] = None
    search_exclude: Optional[str] = None
    order_by: Optional[str] = None
    reviewer_id: Optional[Union[int, str]] = None
    reviewer_username: Optional[str] = None
    scope: Optional[List[str]] = None
    search: Optional[str] = None
    sort: Optional[str] = None
    source_branch: Optional[str] = None
    state: Optional[str] = None
    target_branch: Optional[str] = None
    updated_after: Optional[str] = None
    updated_before: Optional[str] = None
    view: Optional[str] = None
    with_labels_details: Optional[bool] = None
    with_merge_status_recheck: Optional[bool] = None
    wip: Optional[str] = None
    title: Optional[str]
    allow_collaboration: Optional[bool] = None
    allow_maintainer_to_push: Optional[bool] = None
    approvals_before_merge: Optional[int] = None
    assignee_ids: Optional[List[int]] = None
    description: Optional[str] = None
    milestone_id: Optional[int] = None
    remove_source_branch: Optional[str] = None
    reviewer_ids: Optional[List[int]] = None
    squash: Optional[bool] = None
    target_project_id: Optional[Union[int, str]] = None
    max_pages: Optional[int] = Field(description="Maximum pages to return", default=0)
    per_page: Optional[int] = Field(description="Results per page", default=100)
    page: Optional[int] = Field(description="Pagination page", default=1)
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.approved_by_ids:
            self.api_parameters["approved_by_ids"] = self.approved_by_ids
        if self.approver_ids:
            self.api_parameters["approver_ids"] = self.approver_ids
        if self.assignee_id:
            self.api_parameters["assignee_id"] = self.assignee_id
        if self.author_id:
            self.api_parameters["author_id"] = self.author_id
        if self.author_username:
            self.api_parameters["author_username"] = self.author_username
        if self.created_after:
            self.api_parameters["created_after"] = self.created_after
        if self.deployed_after:
            self.api_parameters["deployed_after"] = self.deployed_after
        if self.deployed_before:
            self.api_parameters["deployed_before"] = self.deployed_before
        if self.environment:
            self.api_parameters["environment"] = self.environment
        if self.search_in:
            self.api_parameters["search_in"] = self.search_in
        if self.labels:
            self.api_parameters["labels"] = self.labels
        if self.milestone:
            self.api_parameters["milestone"] = self.milestone
        if self.my_reaction_emoji:
            self.api_parameters["my_reaction_emoji"] = self.my_reaction_emoji
        if self.search_exclude:
            self.api_parameters["search_exclude"] = self.search_exclude
        if self.order_by:
            self.api_parameters["order_by"] = self.order_by
        if self.reviewer_id:
            self.api_parameters["reviewer_id"] = self.reviewer_id
        if self.reviewer_username:
            self.api_parameters["reviewer_username"] = self.reviewer_username
        if self.scope:
            self.api_parameters["scope"] = self.scope
        if self.search:
            self.api_parameters["search"] = self.search
        if self.source_branch:
            self.api_parameters["source_branch"] = self.source_branch
        if self.state:
            self.api_parameters["state"] = self.state
        if self.target_branch:
            self.api_parameters["target_branch"] = self.target_branch
        if self.updated_after:
            self.api_parameters["updated_after"] = self.updated_after
        if self.updated_before:
            self.api_parameters["updated_before"] = self.updated_before
        if self.view:
            self.api_parameters["view"] = self.view
        if self.with_labels_details:
            self.api_parameters["with_labels_details"] = self.with_labels_details
        if self.with_merge_status_recheck:
            self.api_parameters["with_merge_status_recheck"] = (
                self.with_merge_status_recheck
            )
        if self.wip:
            self.api_parameters["wip"] = self.wip
        if self.with_merge_status_recheck:
            self.api_parameters["with_merge_status_recheck"] = (
                self.with_merge_status_recheck
            )
        if self.with_merge_status_recheck:
            self.api_parameters["with_merge_status_recheck"] = (
                self.with_merge_status_recheck
            )

    @model_validator(mode="before")
    def build_data(cls, values):
        """
        Build API parameters for the merge request.

        Args:
        - values: Dictionary of all values.

        Returns:
        - str: The constructed API parameters.

        Note:
        Constructs API parameters based on provided values.
        """
        data = {}

        for field_name, value in values.items():
            if field_name in cls.__annotations__ and value is not None:
                data[field_name] = value

        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data
        return values

    @field_validator("scope")
    def validate_scope(cls, value):
        """
        Validate the 'scope' field.

        Args:
        - value: The value of the 'scope' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid scope.
        """
        valid_scopes = ["created_by_me", "assigned_to_me", "all"]
        if value and not all(scope in valid_scopes for scope in value.lower()):
            raise ValueError("Invalid scope values")
        return value.lower()

    @field_validator("search_in")
    def validate_search_in(cls, value):
        """
        Validate the 'search_in' field.

        Args:
        - value: The value of the 'search_in' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid search_in value.
        """
        valid_search_in = ["title", "description", "title,description"]
        if value and value.lower() not in valid_search_in:
            raise ValueError("Invalid search_in value")
        return value.lower()

    @field_validator("search_exclude")
    def validate_search_exclude(cls, value):
        """
        Validate the 'search_exclude' field.

        Args:
        - value: The value of the 'search_exclude' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid search_exclude value.
        """
        valid_search_exclude = [
            "labels",
            "milestone",
            "author_id",
            "assignee_id",
            "author_username",
            "reviewer_id",
            "reviewer_username",
            "my_reaction_emoji",
        ]
        if value and value.lower() not in valid_search_exclude:
            raise ValueError("Invalid search_exclude value")
        return value.lower()

    @field_validator("state")
    def validate_state(cls, value):
        """
        Validate the 'state' field.

        Args:
        - value: The value of the 'state' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid state value.
        """

        valid_states = ["opened", "closed", "locked", "merged"]
        if value and value.lower() not in valid_states:
            raise ValueError("Invalid state value")
        return value.lower()

    @field_validator("sort")
    def validate_sort(cls, value):
        """
        Validate the 'sort' field.

        Args:
        - value: The value of the 'sort' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid sort value.
        """
        valid_sorts = ["asc", "desc"]
        if value and value.lower() not in valid_sorts:
            raise ValueError("Invalid sort value")
        return value.lower()

    @field_validator("wip")
    def validate_wip(cls, value):
        """
        Validate the 'wip' field.

        Args:
        - value: The value of the 'wip' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid wip value.
        """
        valid_wip_values = ["yes", "no"]
        if value and value.lower() not in valid_wip_values:
            raise ValueError("Invalid wip value")
        return value.lower()

    @field_validator("source_branch", "target_branch", "title")
    def validate_string(cls, v):
        """
        Validate string fields.

        Args:
        - v: The value of the string field.

        Returns:
        - The validated value if valid.

        Raises:
        - ParameterError: If 'v' is not a valid string.
        """
        if not isinstance(v, str):
            raise ParameterError
        return v

    @field_validator("allow_collaboration", "allow_maintainer_to_push", "squash")
    def validate_boolean(cls, v):
        """
        Validate boolean fields.

        Args:
        - v: The value of the boolean field.

        Returns:
        - The validated value if valid.

        Raises:
        - ParameterError: If 'v' is not a valid boolean.
        """
        if not isinstance(v, bool):
            raise ParameterError
        return v

    @field_validator("assignee_id", "milestone_id", "target_project_id")
    def validate_positive_integer(cls, v):
        """
        Validate positive integer fields.

        Args:
        - v: The value of the positive integer field.

        Returns:
        - The validated value if valid.

        Raises:
        - ParameterError: If 'v' is not a valid positive integer.
        """
        if isinstance(v, str):
            try:
                v = int(v)
            except Exception as e:
                raise e
        if not isinstance(v, int) or v < 0:
            raise ParameterError
        return v

    @field_validator("assignee_ids", "reviewer_ids")
    def validate_list_of_integers(cls, v):
        """
        Validate lists of integers.

        Args:
        - v: The value of the list of integers.

        Returns:
        - The validated value if valid.

        Raises:
        - ParameterError: If 'v' is not a valid list of integers.
        """
        if not isinstance(v, list) or not all(isinstance(i, int) for i in v):
            raise ParameterError
        return v


class MergeRequestRuleModel(BaseModel):
    """
    Documentation for the MergeRequestRuleModel Pydantic model.

    This model represents a set of rules for merge requests.

    Attributes:
    - project_id (Union[int, str]): The ID of the project.
    - approval_rule_id (Union[int, str]): The ID of the approval rule.
    - approvals_required (int): The number of approvals required.
    - name (str): The name of the rule.
    - applies_to_all_protected_branches (bool): Indicates if the rule applies to all protected branches.
    - group_ids (List[int]): List of group IDs.
    - merge_request_iid (Union[int, str]): The IID of the merge request.
    - protected_branch_ids (List[int]): List of protected branch IDs.
    - report_type (str): The type of report associated with the rule.
    - rule_type (str): The type of rule.
    - user_ids (List[int]): List of user IDs.
    - data (Dict): Additional data dictionary.

    Methods:
    - check_required_fields(value): Validate required fields.
    - validate_report_type(value): Validate the 'report_type' field.
    - validate_rule_type(value): Validate the 'rule_type' field.
    - construct_data_dict(values): Construct a data dictionary.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    project_id: Optional[Union[int, str]] = None
    group_id: Optional[Union[int, str]] = None
    approval_rule_id: Optional[Union[int, str]] = None
    approvals_required: Optional[int] = None
    name: Optional[str] = None
    applies_to_all_protected_branches: Optional[bool] = None
    group_ids: Optional[List[int]] = None
    merge_request_iid: Optional[Union[int, str]] = None
    protected_branch_ids: Optional[List[int]] = None
    report_type: Optional[str] = None
    rule_type: Optional[str] = None
    user_ids: Optional[List[int]] = None
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    @field_validator("project_id", "approvals_required", "name")
    def check_required_fields(cls, value):
        """
        Check if required fields are provided.

        Args:
        - value: The value to check.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If the required fields are missing.
        """
        if value is None:
            raise ValueError("This field is required.")
        return value

    @field_validator("report_type")
    def validate_report_type(cls, value):
        """
        Validate the 'report_type' field.

        Args:
        - value: The value of the 'report_type' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid report_type.
        """
        if value not in ["license_scanning", "code_coverage"]:
            raise ValueError("Invalid report_type")
        return value

    @field_validator("rule_type")
    def validate_rule_type(cls, value):
        """
        Validate the 'rule_type' field.

        Args:
        - value: The value of the 'rule_type' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid rule_type.
        """

        if value not in ["any_approver", "regular"]:
            raise ValueError("Invalid rule_type")
        return value

    @model_validator(mode="before")
    def construct_data_dict(cls, values):
        """
        Construct a data dictionary.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed data dictionary.

        Raises:
        - ValueError: If the data dictionary is empty.
        """
        data = {}

        if "approvals_required" in values:
            data["approvals_required"] = values.get("approvals_required")
        if "name" in values:
            data["name"] = values.get("name")
        if "applies_to_all_protected_branches" in values:
            data["applies_to_all_protected_branches"] = values.get(
                "applies_to_all_protected_branches"
            )
        if "group_ids" in values:
            data["group_ids"] = values.get("group_ids")
        if "protected_branch_ids" in values:
            data["protected_branch_ids"] = values.get("protected_branch_ids")
        if "report_type" in values:
            data["report_type"] = values.get("report_type")
        if "rule_type" in values:
            data["rule_type"] = values.get("rule_type")
        if "user_ids" in values:
            data["user_ids"] = values.get("user_ids")
        if "usernames" in values:
            data["usernames"] = values.get("usernames")

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data
        return values


class NamespaceModel(BaseModel):
    """
    Documentation for the NamespaceModel Pydantic model.

    """

    namespace_id: Optional[Union[int, str]] = None
    search: Optional[str] = Field(description="Search parameters", default=None)
    owned_only: Optional[bool] = Field(
        description="Only show owned  namespace", default=None
    )
    top_level_only: Optional[bool] = Field(
        description="Only show top level namespaces", default=None
    )
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.search:
            self.api_parameters["search"] = self.search
        if self.owned_only:
            self.api_parameters["owned_only"] = self.owned_only
        if self.top_level_only:
            self.api_parameters["top_level_only"] = self.top_level_only


class PackageModel(BaseModel):
    """
    Documentation for the PackageModel Pydantic model.

    This model represents information about a package in a project.

    Attributes:
    - project_id (Union[int, str]): The ID of the project.
    - package_name (str): The name of the package.
    - package_version (str): The version of the package.
    - file_name (str): The name of the file associated with the package.
    - status (str): The status of the package.
    - select (str): Selection criteria for the package.
    - api_parameters (str): Additional API parameters.

    Methods:
    - validate_file_name(value): Validate the 'file_name' field.
    - validate_status(value): Validate the 'status' field.
    - validate_select(value): Validate the 'select' field.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    project_id: Union[int, str] = None
    package_name: Optional[str] = None
    package_version: Optional[str] = None
    file_name: Optional[str] = None
    status: Optional[str] = None
    select: Optional[str] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.status:
            self.api_parameters["status"] = self.status
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page
        if self.reference:
            self.api_parameters["ref"] = self.reference

    @field_validator("file_name", "package_name")
    def validate_file_name(cls, value):
        """
        Validate the 'file_name' field.

        Args:
        - value: The value of the 'file_name' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' contains invalid characters or exceeds the maximum length.
        """
        pattern = r"^[a-zA-Z0-9._-]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid characters in the filename")

        if len(value) > 255:
            raise ValueError("Filename is too long (maximum 255 characters)")

        return value

    @field_validator("status")
    def validate_rule_type(cls, value):
        """
        Validate the 'status' field.

        Args:
        - value: The value of the 'status' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid status.
        """
        if value not in ["default", "hidden"]:
            raise ValueError("Invalid rule_type")
        return value

    @field_validator("select")
    def validate_select(cls, value):
        """
        Validate the 'select' field.

        Args:
        - value: The value of the 'select' field.

        Returns:
        - The validated value if valid.

        Raises:
        - ValueError: If 'value' is not a valid selection criteria.
        """
        if value not in ["package_file", "package_file"]:
            raise ValueError("Invalid rule_type")
        return value


class PipelineModel(BaseModel):
    """
    Documentation for the PipelineModel Pydantic model.

    This model represents information about a pipeline in a project.

    Attributes:
    - project_id (Union[int, str]): The ID of the project.
    - per_page (int): Number of items per page.
    - page (int): Page number.
    - pipeline_id (Union[int, str]): The ID of the pipeline.
    - reference (str): Reference for the pipeline.
    - variables (Dict): Variables associated with the pipeline.
    - api_parameters (str): Additional API parameters.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    project_id: Union[int, str] = None
    total_pages: Optional[int] = Field(
        description="Total number of pages", default=None
    )
    max_pages: Optional[int] = Field(
        description="Max amount of pages to retrieve", default=None
    )
    per_page: Optional[int] = Field(description="Results per page", default=100)
    page: Optional[int] = Field(description="Pagination page", default=1)
    status: Optional[str] = Field(description="Status", default=None)
    pipeline_id: Optional[Union[int, str]] = None
    reference: Optional[str] = None
    variables: Optional[Dict] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.max_pages:
            self.api_parameters["max_pages"] = self.max_pages
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page
        if self.total_pages:
            self.api_parameters["total_pages"] = self.total_pages
        if self.status:
            self.api_parameters["status"] = self.status
        if self.reference:
            self.api_parameters["ref"] = self.reference


class ProjectModel(BaseModel):
    """
    Documentation for the ProjectModel Pydantic model.

    This model represents information about a project.

    Attributes:
    - project_id (Union[int, str]): The ID of the project.
    - group_id (Union[int, str]): The ID of the group associated with the project.
    - allow_merge_on_skipped_pipeline (bool): Allow merge on skipped pipeline.
    - only_allow_merge_if_all_status_checks_passed (bool): Allow merge only if all status checks passed.
    - analytics_access_level (str): Access level for analytics.
    - approvals_before_merge (int): Number of approvals required before merge.
    - auto_cancel_pending_pipelines (str): Auto-cancel pending pipelines.
    - default=None (other attributes)

    Methods:
    - validate_access_level(value): Validate access level values.
    - validate_boolean(value): Validate boolean values.
    - validate_positive_integer(value): Validate positive integer values.
    - validate_tag_topics(value): Validate tag or topic values.
    - validate_order_by(value): Validate order_by value.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    project_id: Optional[Union[int, str]] = None
    group_id: Optional[Union[int, str]] = None
    allow_merge_on_skipped_pipeline: Optional[bool] = None
    only_allow_merge_if_all_status_checks_passed: Optional[bool] = None
    analytics_access_level: Optional[str] = None
    approvals_before_merge: Optional[int] = None
    auto_cancel_pending_pipelines: Optional[str] = None
    auto_devops_deploy_strategy: Optional[str] = None
    auto_devops_enabled: Optional[bool] = None
    autoclose_referenced_issues: Optional[bool] = None
    avatar: Optional[str] = None
    build_git_strategy: Optional[str] = None
    build_timeout: Optional[int] = None
    builds_access_level: Optional[str] = None
    ci_config_path: Optional[str] = None
    ci_default_git_depth: Optional[int] = None
    ci_forward_deployment_enabled: Optional[bool] = None
    ci_allow_fork_pipelines_to_run_in_parent_project: Optional[bool] = None
    ci_separated_caches: Optional[bool] = None
    container_expiration_policy_attributes: Optional[str] = None
    container_registry_access_level: Optional[str] = None
    default_branch: Optional[str] = None
    description: Optional[str] = None
    emails_disabled: Optional[bool] = None
    enforce_auth_checks_on_uploads: Optional[bool] = None
    external_authorization_classification_label: Optional[str] = None
    expires_at: Optional[str] = None
    forking_access_level: Optional[str] = None
    group_access: Optional[int] = None
    import_url: Optional[Union[HttpUrl, str]] = None
    issues_access_level: Optional[str] = None
    issues_template: Optional[str] = None
    keep_latest_artifact: Optional[bool] = None
    lfs_enabled: Optional[bool] = None
    total_pages: Optional[int] = Field(
        description="Total number of pages", default=None
    )
    max_pages: Optional[int] = Field(
        description="Max amount of pages to retrieve", default=None
    )
    page: Optional[int] = Field(description="Page in multi-page response", default=None)
    per_page: Optional[int] = Field(
        description="Amount of items per page", default=None
    )
    merge_commit_template: Optional[str] = None
    merge_method: Optional[str] = None
    merge_pipelines_enabled: Optional[bool] = None
    merge_requests_access_level: Optional[str] = None
    merge_requests_template: Optional[str] = None
    merge_trains_enabled: Optional[bool] = None
    mirror_overwrites_diverged_branches: Optional[bool] = None
    mirror_trigger_builds: Optional[bool] = None
    mirror_user_id: Optional[int] = None
    mirror: Optional[bool] = None
    mr_default_target_self: Optional[bool] = None
    name: Optional[str] = None
    order_by: Optional[str] = None
    only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None
    only_allow_merge_if_pipeline_succeeds: Optional[bool] = None
    only_mirror_protected_branches: Optional[bool] = None
    operations_access_level: Optional[str] = None
    packages_enabled: Optional[bool] = None
    pages_access_level: Optional[str] = None
    path: Optional[str] = None
    printing_merge_request_link_enabled: Optional[bool] = None
    public_builds: Optional[bool] = None
    releases_access_level: Optional[str] = None
    remove_source_branch_after_merge: Optional[bool] = None
    repository_access_level: Optional[str] = None
    repository_storage: Optional[str] = None
    request_access_enabled: Optional[bool] = None
    requirements_access_level: Optional[str] = None
    resolve_outdated_diff_discussions: Optional[bool] = None
    restrict_user_defined_variables: Optional[bool] = None
    security_and_compliance_access_level: Optional[str] = None
    service_desk_enabled: Optional[bool] = None
    shared_runners_enabled: Optional[bool] = None
    snippets_access_level: Optional[str] = None
    squash_commit_template: Optional[str] = None
    squash_option: Optional[str] = None
    suggestion_commit_message: Optional[str] = None
    tag_list: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    visibility: Optional[str] = None
    archived: Optional[bool] = None
    id_after: Optional[int] = None
    id_before: Optional[int] = None
    imported: Optional[bool] = None
    include_hidden: Optional[bool] = None
    include_pending_delete: Optional[bool] = None
    membership: Optional[bool] = None
    search: Optional[str] = None
    sort: Optional[str] = None
    min_access_level: Optional[int] = None
    owned: Optional[bool] = None
    statistics: Optional[bool] = None
    simple: Optional[bool] = None
    starred: Optional[bool] = None
    topic: Optional[str] = None
    topic_id: Optional[int] = None
    repository_checksum_failed: Optional[bool] = None
    search_namespaces: Optional[bool] = None
    wiki_access_level: Optional[str] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.group_id:
            self.api_parameters["group_id"] = self.group_id
        if self.archived:
            self.api_parameters["archived"] = self.archived
        if self.group_access:
            self.api_parameters["group_access"] = self.group_access
        if self.expires_at:
            self.api_parameters["expires_at"] = self.expires_at
        if self.max_pages:
            self.api_parameters["max_pages"] = self.max_pages
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page
        if self.total_pages:
            self.api_parameters["total_pages"] = self.total_pages
        if self.id_after:
            self.api_parameters["id_after"] = self.id_after
        if self.id_before:
            self.api_parameters["id_before"] = self.id_before
        if self.imported:
            self.api_parameters["imported"] = self.imported
        if self.include_hidden:
            self.api_parameters["include_hidden"] = self.include_hidden
        if self.include_pending_delete:
            self.api_parameters["include_pending_delete"] = self.include_pending_delete
        if self.membership:
            self.api_parameters["membership"] = self.membership
        if self.min_access_level:
            self.api_parameters["min_access_level"] = self.min_access_level
        if self.order_by:
            self.api_parameters["order_by"] = self.order_by
        if self.owned:
            self.api_parameters["owned"] = self.owned
        if self.repository_checksum_failed:
            self.api_parameters["repository_checksum_failed"] = (
                self.repository_checksum_failed
            )
        if self.repository_storage:
            self.api_parameters["repository_storage"] = self.repository_storage
        if self.search_namespaces:
            self.api_parameters["search_namespaces"] = self.search_namespaces
        if self.search:
            self.api_parameters["search"] = self.search
        if self.simple:
            self.api_parameters["simple"] = self.simple
        if self.sort:
            self.api_parameters["sort"] = self.sort
        if self.starred:
            self.api_parameters["starred"] = self.starred
        if self.statistics:
            self.api_parameters["statistics"] = self.statistics
        if self.topic_id:
            self.api_parameters["topic_id"] = self.topic_id
        if self.topic:
            self.api_parameters["topic"] = self.topic
        if self.visibility:
            self.api_parameters["visibility"] = self.visibility

    @model_validator(mode="before")
    def build_data(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        data = {}

        for field_name, value in values.items():
            if field_name in cls.__annotations__ and value is not None:
                data[field_name] = value

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data

        return values

    @field_validator(
        "analytics_access_level",
        "builds_access_level",
        "container_registry_access_level",
        "forking_access_level",
        "issues_access_level",
        "operations_access_level",
        "pages_access_level",
        "releases_access_level",
        "repository_access_level",
        "requirements_access_level",
        "security_and_compliance_access_level",
        "snippets_access_level",
        "wiki_access_level",
    )
    def validate_access_level(cls, value):
        """
        Validate access level values.

        Args:
        - value: Access level value to validate.

        Returns:
        - The validated access level value.

        Raises:
        - ValueError: If the value is not a valid access level.
        """

        valid_access_levels = ["disabled", "private", "enabled"]
        if value and value.lower() not in valid_access_levels:
            raise ValueError("Invalid access level value")
        return value.lower()

    @field_validator(
        "auto_cancel_pending_pipelines",
        "auto_devops_deploy_strategy",
        "mirror_overwrites_diverged_branches",
        "mirror_trigger_builds",
        "mr_default_target_self",
        "only_allow_merge_if_all_discussions_are_resolved",
        "only_allow_merge_if_pipeline_succeeds",
        "only_mirror_protected_branches",
        "auto_devops_enabled",
        "autoclose_referenced_issues",
        "emails_disabled",
        "enforce_auth_checks_on_uploads",
        "ci_forward_deployment_enabled",
        "ci_allow_fork_pipelines_to_run_in_parent_project",
        "ci_separated_caches",
        "keep_latest_artifact",
        "lfs_enabled",
        "merge_pipelines_enabled",
        "merge_trains_enabled",
        "printing_merge_request_link_enabled",
        "public_builds",
        "remove_source_branch_after_merge",
        "request_access_enabled",
        "resolve_outdated_diff_discussions",
        "restrict_user_defined_variables",
        "service_desk_enabled",
        "shared_runners_enabled",
        "packages_enabled",
    )
    def validate_boolean(cls, value):
        """
        Validate boolean values.

        Args:
        - value: Boolean value to validate.

        Returns:
        - The validated boolean value.

        Raises:
        - ValueError: If the value is not a valid boolean.
        """
        if value is not None and not isinstance(value, bool):
            raise ValueError("Invalid boolean value")
        return value

    @field_validator(
        "build_timeout",
        "ci_default_git_depth",
        "mirror_user_id",
    )
    def validate_positive_integer(cls, value):
        """
        Validate positive integer values.

        Args:
        - value: Positive integer value to validate.

        Returns:
        - The validated positive integer value.

        Raises:
        - ValueError: If the value is not a valid positive integer.
        """
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError("Invalid positive integer value")
        return value

    @field_validator("tag_list", "topics")
    def validate_tag_topics(cls, value):
        """
        Validate tag or topic values.

        Args:
        - value: List of tags or topics to validate.

        Returns:
        - The validated list of tags or topics.

        Raises:
        - ValueError: If the value contains invalid elements.
        """
        if value is not None and not all(isinstance(tag, str) for tag in value):
            raise ValueError("Invalid tag or topic value")
        return value

    @field_validator("order_by")
    def validate_order_by(cls, value):
        """
        Validate order_by value.

        Args:
        - value: Order_by value to validate.

        Returns:
        - The validated order_by value.

        Raises:
        - ValueError: If the value is not a valid order_by.
        """
        if value.lower() not in ["id", "name", "username", "created_at", "updated_at"]:
            raise ValueError("Invalid order_by")
        return value.lower()

    @field_validator("visibility")
    def validate_visibility(cls, value):
        """
        Validate visibility value.

        Args:
        - value: visibility value to validate.

        Returns:
        - The validated visibility value.

        Raises:
        - ValueError: If the value is not a valid order_by.
        """
        if value.lower() not in ["internal", "private", "public"]:
            raise ValueError("Invalid visibility")
        return value.lower()


class ProtectedBranchModel(BaseModel):
    """
    Documentation for the ProtectedBranchModel Pydantic model.

    This model represents information about a protected branch.

    Attributes:
    - project_id (Union[int, str]): The ID of the project.
    - branch (str): The name of the protected branch.
    - push_access_level (int): Access level for push operations.
    - merge_access_level (int): Access level for merge operations.
    - unprotect_access_level (int): Access level for unprotecting the branch.
    - allow_force_push (List[str]): List of users/groups allowed to force push.
    - allowed_to_push (List[str]): List of users/groups allowed to push.
    - allowed_to_merge (List[str]): List of users/groups allowed to merge.
    - allowed_to_unprotect (List[str]): List of users/groups allowed to unprotect.
    - code_owner_approval_required (bool): Indicates if code owner approval is required.
    - api_parameters (str): Constructed API parameters string.
    - data (Dict): Dictionary containing additional data.

    Methods:
    - validate_project_id(value): Validate project ID for non-None.
    - validate_project_id_type(value): Validate project ID for type (int or str).
    - construct_data_dict(values): Construct data dictionary.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    project_id: Union[int, str]
    branch: str
    push_access_level: Optional[int] = None
    merge_access_level: Optional[int] = None
    unprotect_access_level: Optional[int] = None
    allow_force_push: Optional[bool] = None
    allowed_to_push: Optional[List[Dict]] = None
    allowed_to_merge: Optional[List[Dict]] = None
    allowed_to_unprotect: Optional[List[Dict]] = None
    code_owner_approval_required: Optional[bool] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.branch:
            self.api_parameters["name"] = self.branch
        if self.push_access_level:
            self.api_parameters["push_access_level"] = self.push_access_level
        if self.merge_access_level:
            self.api_parameters["merge_access_level"] = self.merge_access_level
        if self.unprotect_access_level:
            self.api_parameters["unprotect_access_level"] = self.unprotect_access_level

    @model_validator(mode="before")
    def build_data(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        data = {}

        for field_name, value in values.items():
            if field_name in cls.__annotations__ and value is not None:
                data[field_name] = value

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data
        return values

    @field_validator("allow_force_push", "code_owner_approval_required")
    def validate_bool_fields(cls, v):
        """
        Validate boolean fields to ensure they are valid boolean values.

        Args:
        - v: The value of the field.

        Returns:
        - bool: The validated field value.

        Raises:
        - ValueError: If the field is provided and not a boolean.
        """
        if v is not None and not isinstance(v, bool):
            raise ValueError("Invalid states")
        return v

    @field_validator("project_id")
    def validate_project_id(cls, value):
        """
        Validate project ID for non-None.

        Args:
        - value: Project ID to validate.

        Returns:
        - The validated project ID.

        Raises:
        - ValueError: If the project ID is None.
        """
        if value is None:
            raise ValueError("Project ID cannot be None")
        return value

    @field_validator("project_id")
    def validate_project_id_type(cls, value):
        """
        Validate project ID for type (int or str).

        Args:
        - value: Project ID to validate.

        Returns:
        - The validated project ID.

        Raises:
        - ValueError: If the project ID is not an integer or a string.
        """
        if not isinstance(value, (int, str)):
            raise ValueError("Project ID must be an integer or a string")
        return value


class ReleaseModel(BaseModel):
    """
    Documentation for the ReleaseModel Pydantic model.

    This model represents information about a release.

    Attributes:
    - project_id (Union[int, str]): The ID of the project.
    - order_by (str): Order releases by a specific attribute.
    - sort (str): Sort releases in ascending or descending order.
    - simple (bool): Flag indicating whether to include only basic information.
    - include_html_description (bool): Flag indicating whether to include HTML description.
    - tag_name (str): The name of the tag associated with the release.
    - description (str): Description of the release.
    - tag_message (str): Message associated with the tag of the release.
    - ref (str): Reference (branch or commit) associated with the release.
    - direct_asset_path (str): Direct path to the release assets.
    - name (List[str]): List of release names.
    - milestones (str): Milestones associated with the release.
    - released_at (str): Date and time when the release was made.
    - api_parameters (str): Constructed API parameters string.
    - data (Dict): Dictionary containing additional data.

    Methods:
    - validate_order_by(value): Validate order_by attribute.
    - validate_sort(value): Validate sort attribute.
    - validate_project_id(value): Validate project ID for non-None.
    - validate_project_id_type(value): Validate project ID for type (int or str).
    - construct_data_dict(values): Construct data dictionary.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    project_id: Union[int, str] = None
    group_id: Union[int, str] = None
    order_by: Optional[str] = None
    sort: Optional[str] = None
    simple: Optional[bool] = None
    include_html_description: Optional[bool] = None
    tag_name: Optional[str] = None
    description: Optional[str] = None
    tag_message: Optional[str] = None
    reference: Optional[str] = None
    direct_asset_path: Optional[str] = None
    name: Optional[List[str]] = None
    milestones: Optional[str] = None
    released_at: Optional[str] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.simple:
            self.api_parameters["simple"] = self.simple

    @model_validator(mode="before")
    def build_data(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        data = {}

        for field_name, value in values.items():
            if field_name in cls.__annotations__ and value is not None:
                data[field_name] = value

        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data

        return values

    @field_validator("order_by")
    def validate_order_by(cls, value):
        """
        Validate order_by attribute.

        Args:
        - value: Order_by attribute to validate.

        Returns:
        - The validated order_by attribute.

        Raises:
        - ValueError: If the order_by attribute is not valid.
        """
        if value not in ["id", "name", "username", "created_at", "updated_at"]:
            raise ValueError("Invalid order_by")
        return value

    @field_validator("sort")
    def validate_sort(cls, value):
        """
        Validate sort attribute.

        Args:
        - value: Sort attribute to validate.

        Returns:
        - The validated sort attribute.

        Raises:
        - ValueError: If the sort attribute is not valid.
        """
        valid_sorts = ["asc", "desc"]
        if value and value not in valid_sorts:
            raise ValueError("Invalid sort value")
        return value

    @field_validator("project_id")
    def validate_project_id(cls, value):
        """
        Validate project ID for non-None.

        Args:
        - value: Project ID to validate.

        Returns:
        - The validated project ID.

        Raises:
        - ValueError: If the project ID is None.
        """
        if value is None:
            raise ValueError("Project ID cannot be None")
        return value

    @field_validator("project_id")
    def validate_project_id_type(cls, value):
        """
        Validate project ID for type (int or str).

        Args:
        - value: Project ID to validate.

        Returns:
        - The validated project ID.

        Raises:
        - ValueError: If the project ID is not an integer or a string.
        """
        if not isinstance(value, (int, str)):
            raise ValueError("Project ID must be an integer or a string")
        return value


class RunnerModel(BaseModel):
    """
    Documentation for the RunnerModel Pydantic model.

    This model represents information about a runner.

    Attributes:
    - description (str): Description of the runner.
    - active (bool): Flag indicating whether the runner is active.
    - paused (bool): Flag indicating whether the runner is paused.
    - tag_list (List[str]): List of tags associated with the runner.
    - run_untagged (bool): Flag indicating whether the runner can run untagged jobs.
    - locked (bool): Flag indicating whether the runner is locked.
    - access_level (str): Access level of the runner.
    - maintenance_note (str): Maintenance note associated with the runner.
    - info (str): Additional information about the runner.
    - token (str): Token associated with the runner.
    - project_id (Union[int, str]): The ID of the project associated with the runner.
    - group_id (Union[int, str]): The ID of the group associated with the runner.
    - maximum_timeout (int): Maximum timeout allowed for the runner.
    - runner_type (str): Type of the runner (instance_type, group_type, project_type).
    - status (str): Status of the runner.
    - all_runners (bool): Flag indicating whether to include all runners.
    - api_parameters (str): Constructed API parameters string.
    - data (Dict): Dictionary containing additional data.

    Methods:
    - validate_runner_type(value): Validate runner_type attribute.
    - validate_status(value): Validate status attribute.
    - construct_data_dict(values): Construct data dictionary.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    runner_id: Optional[Union[str, int]] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    paused: Optional[bool] = None
    tag_list: Optional[List[str]] = None
    run_untagged: Optional[bool] = None
    locked: Optional[bool] = None
    access_level: Optional[str] = None
    maintenance_note: Optional[str] = None
    info: Optional[str] = None
    token: Optional[str] = None
    project_id: Optional[Union[int, str]] = None
    group_id: Optional[Union[int, str]] = None
    maximum_timeout: Optional[int] = None
    runner_type: Optional[str] = None
    status: Optional[str] = None
    all_runners: Optional[bool] = False
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.tag_list:
            self.api_parameters["tag_list"] = self.tag_list
        if self.runner_type:
            self.api_parameters["runner_type"] = self.runner_type
        if self.status:
            self.api_parameters["status"] = self.status
        if self.paused:
            self.api_parameters["paused"] = self.paused

    @model_validator(mode="before")
    def build_data(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        data = {}

        for field_name, value in values.items():
            if field_name in cls.__annotations__ and value is not None:
                data[field_name] = value

        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data

        return values

    @field_validator("runner_type")
    def validate_runner_type(cls, value):
        """
        Validate runner_type attribute.

        Args:
        - value: Runner_type attribute to validate.

        Returns:
        - The validated runner_type attribute.

        Raises:
        - ValueError: If the runner_type attribute is not valid.
        """
        if value.lower() not in ["instance_type", "group_type", "project_type"]:
            raise ValueError("Invalid runner_type")
        return value.lower()

    @field_validator("status")
    def validate_status(cls, value):
        """
        Validate status attribute.

        Args:
        - value: Status attribute to validate.

        Returns:
        - The validated status attribute.

        Raises:
        - ValueError: If the status attribute is not valid.
        """
        if value.lower() not in [
            "online",
            "offline",
            "stale",
            "never_contacted",
            "active",
            "paused",
        ]:
            raise ValueError("Invalid status")
        return value.lower()


class UserModel(BaseModel):
    """
    Documentation for the UserModel Pydantic model.

    This model represents information about a user.

    Attributes:
    - username (str): Username of the user.
    - active (bool): Flag indicating whether the user is active.
    - blocked (bool): Flag indicating whether the user is blocked.
    - external (bool): Flag indicating whether the user is external.
    - exclude_internal (bool): Flag indicating whether to exclude internal users.
    - exclude_external (bool): Flag indicating whether to exclude external users.
    - without_project_bots (bool): Flag indicating whether to exclude project bots.
    - extern_uid (str): External UID associated with the user.
    - provider (str): Provider associated with the user.
    - created_before (str): Filter users created before a specific date.
    - created_after (str): Filter users created after a specific date.
    - with_custom_attributes (str): Filter users with custom attributes.
    - sort (str): Sort order for the results.
    - order_by (str): Order results by a specific field.
    - two_factor (str): Filter users by two-factor authentication status.
    - without_projects (bool): Flag indicating whether to exclude users with projects.
    - admins (bool): Flag indicating whether to filter only admin users.
    - saml_provider_id (str): SAML provider ID associated with the user.
    - max_pages (int): Maximum number of pages.
    - page (int): Current page number.
    - per_page (int): Number of results per page.
    - sudo (bool): Flag indicating sudo user mode.
    - user_id (Union[str, int]): ID of the user.
    - api_parameters (str): Constructed API parameters string.

    Methods:
    - validate_order_by(value): Validate order_by attribute.
    - validate_sort(value): Validate sort attribute.
    - validate_two_factor(value): Validate two_factor attribute.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    username: Optional[str] = None
    active: Optional[bool] = None
    blocked: Optional[bool] = None
    external: Optional[bool] = None
    humans: Optional[bool] = None
    exclude_internal: Optional[bool] = None
    exclude_external: Optional[bool] = None
    without_project_bots: Optional[bool] = None
    extern_uid: Optional[str] = None
    provider: Optional[str] = None
    created_before: Optional[str] = None
    created_after: Optional[str] = None
    with_custom_attributes: Optional[str] = None
    sort: Optional[str] = None
    order_by: Optional[str] = None
    two_factor: Optional[str] = None
    without_projects: Optional[bool] = None
    admins: Optional[bool] = None
    saml_provider_id: Optional[str] = None
    total_pages: Optional[int] = Field(
        description="Total number of pages", default=None
    )
    max_pages: Optional[int] = Field(
        description="Max amount of pages to retrieve", default=None
    )
    page: Optional[int] = Field(description="Page in multi-page response", default=None)
    per_page: Optional[int] = Field(
        description="Amount of items per page", default=None
    )
    sudo: Optional[bool] = False
    user_id: Optional[Union[str, int]] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.username:
            self.api_parameters["username"] = self.username
        if self.username:
            self.api_parameters["username"] = self.username
        if self.blocked:
            self.api_parameters["blocked"] = self.blocked
        if self.external:
            self.api_parameters["external"] = self.external
        if self.humans:
            self.api_parameters["humans"] = self.humans
        if self.exclude_internal:
            self.api_parameters["exclude_internal"] = self.exclude_internal
        if self.exclude_external:
            self.api_parameters["exclude_external"] = self.exclude_external
        if self.without_project_bots:
            self.api_parameters["without_project_bots"] = self.without_project_bots
        if self.order_by:
            self.api_parameters["order_by"] = self.order_by
        if self.sort:
            self.api_parameters["sort"] = self.sort
        if self.two_factor:
            self.api_parameters["two_factor"] = self.two_factor
        if self.without_projects:
            self.api_parameters["without_projects"] = self.without_projects
        if self.admins:
            self.api_parameters["admins"] = self.admins
        if self.saml_provider_id:
            self.api_parameters["saml_provider_id"] = self.saml_provider_id
        if self.extern_uid:
            self.api_parameters["extern_uid"] = self.extern_uid
        if self.provider:
            self.api_parameters["provider"] = self.provider
        if self.created_before:
            self.api_parameters["created_before"] = self.created_before
        if self.created_after:
            self.api_parameters["created_after"] = self.created_after
        if self.with_custom_attributes:
            self.api_parameters["with_custom_attributes"] = self.with_custom_attributes
        if self.sudo:
            self.api_parameters["sudo"] = self.user_id
        if self.user_id:
            self.api_parameters["user_id"] = self.user_id
        if self.max_pages:
            self.api_parameters["max_pages"] = self.max_pages
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page
        if self.total_pages:
            self.api_parameters["total_pages"] = self.total_pages

    @field_validator("order_by")
    def validate_order_by(cls, value):
        """
        Validate order_by attribute.

        Args:
        - value: Order_by attribute to validate.

        Returns:
        - The validated order_by attribute.

        Raises:
        - ValueError: If the order_by attribute is not valid.
        """
        if value.lower() not in ["id", "name", "username", "created_at", "updated_at"]:
            raise ValueError("Invalid order_by")
        return value.lower()

    @field_validator("sort")
    def validate_sort(cls, value):
        """
        Validate sort attribute.

        Args:
        - value: Sort attribute to validate.

        Returns:
        - The validated sort attribute.

        Raises:
        - ValueError: If the sort attribute is not valid.
        """
        valid_sorts = ["asc", "desc"]
        if value and value.lower() not in valid_sorts:
            raise ValueError("Invalid sort value")
        return value.lower()

    @field_validator("two_factor")
    def validate_two_factor(cls, value):
        """
        Validate two_factor attribute.

        Args:
        - value: Two_factor attribute to validate.

        Returns:
        - The validated two_factor attribute.

        Raises:
        - ValueError: If the two_factor attribute is not valid.
        """
        valid_two_factor = ["enabled", "disabled"]
        if value and value.lower() not in valid_two_factor:
            raise ValueError("Invalid two_factor value")
        return value.lower()


class WikiModel(BaseModel):
    """
    Documentation for the WikiModel Pydantic model.

    This model represents information about a wiki.

    Attributes:
    - project_id (Union[int, str]): ID of the project associated with the wiki.
    - slug (str): Slug of the wiki.
    - content (str): Content of the wiki.
    - title (str): Title of the wiki.
    - format_type (str): Format type of the wiki.
    - with_content (bool): Flag indicating whether to include content.
    - file (str): File associated with the wiki.
    - branch (str): Branch of the wiki.
    - api_parameters (str): Constructed API parameters string.
    - data (Dict): Dictionary containing additional data.

    Methods:
    - validate_project_id(value): Validate project_id attribute.
    - validate_project_id_type(value): Validate project_id type.
    - construct_data_dict(values): Construct data dictionary.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    project_id: Union[int, str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    title: Optional[str] = None
    format_type: Optional[str] = None
    with_content: Optional[bool] = None
    render_html: Optional[bool] = None
    file: Optional[str] = None
    branch: Optional[str] = None
    version: Optional[str] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = Field(description="Data Payload", default=None)

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.with_content:
            self.api_parameters["with_content"] = self.with_content
        if self.render_html:
            self.api_parameters["render_html"] = self.render_html
        if self.version:
            self.api_parameters["version"] = self.version

    @model_validator(mode="before")
    def build_data(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        data = {}

        for field_name, value in values.items():
            if field_name in cls.__annotations__ and value is not None:
                data[field_name] = value

        data = {k: v for k, v in data.items() if v is not None}

        if "data" not in values or values["data"] is None:
            values["data"] = data

        return values

    @field_validator("project_id")
    def validate_project_id(cls, value):
        """
        Validate project_id attribute.

        Args:
        - value: Project_id attribute to validate.

        Returns:
        - The validated project_id attribute.

        Raises:
        - ValueError: If the project_id attribute is None.
        """
        if value is None:
            raise ValueError("Project ID cannot be None")
        return value

    @field_validator("project_id")
    def validate_project_id_type(cls, value):
        """
        Validate project_id type.

        Args:
        - value: Project_id attribute to validate.

        Returns:
        - The validated project_id attribute.

        Raises:
        - ValueError: If the project_id attribute is not an integer or a string.
        """
        if not isinstance(value, (int, str)):
            raise ValueError("Project ID must be an integer or a string")
        return value
