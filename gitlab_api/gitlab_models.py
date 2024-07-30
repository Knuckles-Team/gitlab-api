#!/usr/bin/python
# coding: utf-8
import logging
import re

from typing import Union, List, Dict, Optional, Any
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

from gitlab_api.gitlab_db_models import (
    DeployTokenDBModel,
    RuleDBModel,
    AccessControlDBModel,
    SourcesDBModel,
    LinkDBModel,
    AssetsDBModel,
    EvidenceDBModel,
    ReleaseLinksDBModel,
    TokenDBModel,
    ToDoDBModel,
    WikiPageDBModel,
    WikiAttachmentLinkDBModel,
    WikiAttachmentDBModel,
    AgentDBModel,
    AgentsDBModel,
    ReleaseDBModel,
    BranchDBModel,
    ApprovalRuleDBModel,
    MergeRequestDBModel,
    GroupAccessDBModel,
    DefaultBranchProtectionDefaultsDBModel,
    GroupDBModel,
    WebhookDBModel,
    AccessLevelDBModel,
    ApprovedByDBModel,
    ProjectDBModel,
    RunnerDBModel,
    EpicDBModel,
    IssueDBModel,
    JobDBModel,
    PipelineDBModel,
    PipelineVariableDBModel,
    PackageLinkDBModel,
    PackageVersionDBModel,
    ProjectConfigDBModel,
    PackageDBModel,
    ContributorDBModel,
    CommitStatsDBModel,
    CommitSignatureDBModel,
    CommentDBModel,
    CommitDBModel,
    MembershipDBModel,
    TestCaseDBModel,
    TestSuiteDBModel,
    TestReportDBModel,
    TestReportTotalDBModel,
    MergeApprovalsDBModel,
    IssueStatsDBModel,
    MilestoneDBModel,
    TimeStatsDBModel,
    TaskCompletionStatusDBModel,
    ReferencesDBModel,
    ArtifactDBModel,
    ArtifactsFileDBModel,
    RunnerManagerDBModel,
    ConfigurationDBModel,
    IterationDBModel,
    IdentityDBModel,
    GroupSamlIdentityDBModel,
    CreatedByDBModel,
    UserDBModel,
    UsersDBModel,
    NamespaceDBModel,
    ContainerExpirationPolicyDBModel,
    PermissionsDBModel,
    StatisticsDBModel,
    LinksDBModel,
    DiffDBModel,
    DetailedStatusDBModel,
)


logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

########################################################################################################################
#                                               Input Models                                                           #
########################################################################################################################


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
    data: Optional[Dict] = None

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

    group_id: Union[int, str] = None
    per_page: Optional[int] = 100
    page: Optional[int] = 1
    argument: Optional[str] = "state=opened"
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
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page


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
    job_id: Union[int, str] = None
    scope: Optional[List[str]] = None
    per_page: Optional[int] = 100
    page: Optional[int] = 1
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
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page
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
    per_page: Optional[int] = 100
    page: Optional[int] = 1
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
    max_pages: Optional[int] = 0
    per_page: Optional[int] = 100
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = None

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

        if "source_branch" in values:
            data["source_branch"] = values.get("source_branch")
        if "target_branch" in values:
            data["target_branch"] = values.get("target_branch")
        if "title" in values:
            data["title"] = values.get("title")
        if "allow_collaboration" in values:
            data["allow_collaboration"] = values.get("allow_collaboration")
        if "allow_maintainer_to_push" in values:
            data["allow_maintainer_to_push"] = values.get("allow_maintainer_to_push")
        if "approvals_before_merge" in values:
            data["approvals_before_merge"] = values.get("approvals_before_merge")
        if "assignee_id" in values:
            data["assignee_id"] = values.get("assignee_id")
        if "description" in values:
            data["description"] = values.get("description")
        if "labels" in values:
            data["labels"] = values.get("labels")
        if "milestone_id" in values:
            data["milestone_id"] = values.get("milestone_id")
        if "remove_source_branch" in values:
            data["remove_source_branch"] = values.get("remove_source_branch")
        if "reviewer_ids" in values:
            data["reviewer_ids"] = values.get("reviewer_ids")
        if "squash" in values:
            data["squash"] = values.get("squash")
        if "target_project_id" in values:
            data["target_project_id"] = values.get("target_project_id")

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

    @field_validator(
        "approvals_before_merge", "assignee_id", "milestone_id", "target_project_id"
    )
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
    data: Optional[Dict] = None

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
    per_page: Optional[int] = 100
    page: Optional[int] = 1
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
        if self.status:
            self.api_parameters["status"] = self.status
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page
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
    max_pages: Optional[int] = 0
    per_page: Optional[int] = 100
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
    wiki_access_level: Optional[str] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)
    data: Optional[Dict] = None

    def model_post_init(self, __context):
        """
        Build the API parameters
        """
        self.api_parameters = {}
        if self.group_id:
            self.api_parameters["group_id"] = self.group_id
        if self.group_access:
            self.api_parameters["group_access"] = self.group_access
        if self.expires_at:
            self.api_parameters["expires_at"] = self.expires_at

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

        if "allow_merge_on_skipped_pipeline" in values:
            data["allow_merge_on_skipped_pipeline"] = values.get(
                "allow_merge_on_skipped_pipeline"
            )
        if "allow_pipeline_trigger_approve_deployment" in values:
            data["allow_pipeline_trigger_approve_deployment"] = values.get(
                "allow_pipeline_trigger_approve_deployment"
            )
        if "only_allow_merge_if_all_status_checks_passed" in values:
            data["only_allow_merge_if_all_status_checks_passed"] = values.get(
                "only_allow_merge_if_all_status_checks_passed"
            )
        if "analytics_access_level" in values:
            data["analytics_access_level"] = values.get("analytics_access_level")
        if "approvals_before_merge" in values:
            data["approvals_before_merge"] = values.get("approvals_before_merge")
        if "auto_cancel_pending_pipelines" in values:
            data["auto_cancel_pending_pipelines"] = values.get(
                "auto_cancel_pending_pipelines"
            )
        if "auto_devops_deploy_strategy" in values:
            data["auto_devops_deploy_strategy"] = values.get(
                "auto_devops_deploy_strategy"
            )
        if "auto_devops_enabled" in values:
            data["auto_devops_enabled"] = values.get("auto_devops_enabled")
        if "autoclose_referenced_issues" in values:
            data["autoclose_referenced_issues"] = values.get(
                "autoclose_referenced_issues"
            )
        if "avatar" in values:
            data["avatar"] = values.get("avatar")
        if "build_git_strategy" in values:
            data["build_git_strategy"] = values.get("build_git_strategy")
        if "build_timeout" in values:
            data["build_timeout"] = values.get("build_timeout")
        if "builds_access_level" in values:
            data["builds_access_level"] = values.get("builds_access_level")
        if "ci_config_path" in values:
            data["ci_config_path"] = values.get("ci_config_path")
        if "container_registry_access_level" in values:
            data["container_registry_access_level"] = values.get(
                "container_registry_access_level"
            )
        if "container_registry_enabled" in values:
            data["container_registry_enabled"] = values.get(
                "container_registry_enabled"
            )
        if "default_branch" in values:
            data["default_branch"] = values.get("default_branch")
        if "description" in values:
            data["description"] = values.get("description")
        if "emails_disabled" in values:
            data["emails_disabled"] = values.get("emails_disabled")
        if "emails_enabled" in values:
            data["emails_enabled"] = values.get("emails_enabled")
        if "enforce_auth_checks_on_uploads" in values:
            data["enforce_auth_checks_on_uploads"] = values.get(
                "enforce_auth_checks_on_uploads"
            )
        if "environments_access_level" in values:
            data["environments_access_level"] = values.get("environments_access_level")
        if "external_authorization_classification_label" in values:
            data["external_authorization_classification_label"] = values.get(
                "external_authorization_classification_label"
            )
        if "feature_flags_access_level" in values:
            data["feature_flags_access_level"] = values.get(
                "feature_flags_access_level"
            )
        if "forking_access_level" in values:
            data["forking_access_level"] = values.get("forking_access_level")
        if "group_runners_enabled" in values:
            data["group_runners_enabled"] = values.get("group_runners_enabled")
        if "group_with_project_templates_id" in values:
            data["group_with_project_templates_id"] = values.get(
                "group_with_project_templates_id"
            )
        if "import_url" in values:
            data["import_url"] = values.get("import_url")
        if "infrastructure_access_level" in values:
            data["infrastructure_access_level"] = values.get(
                "infrastructure_access_level"
            )
        if "initialize_with_readme" in values:
            data["initialize_with_readme"] = values.get("initialize_with_readme")
        if "issue_branch_template" in values:
            data["issue_branch_template"] = values.get("issue_branch_template")
        if "issues_access_level" in values:
            data["issues_access_level"] = values.get("issues_access_level")
        if "issues_enabled" in values:
            data["issues_enabled"] = values.get("issues_enabled")
        if "jobs_enabled" in values:
            data["jobs_enabled"] = values.get("jobs_enabled")
        if "lfs_enabled" in values:
            data["lfs_enabled"] = values.get("lfs_enabled")
        if "merge_commit_template" in values:
            data["merge_commit_template"] = values.get("merge_commit_template")
        if "merge_method" in values:
            data["merge_method"] = values.get("merge_method")
        if "merge_requests_access_level" in values:
            data["merge_requests_access_level"] = values.get(
                "merge_requests_access_level"
            )
        if "merge_requests_enabled" in values:
            data["merge_requests_enabled"] = values.get("merge_requests_enabled")
        if "mirror_trigger_builds" in values:
            data["mirror_trigger_builds"] = values.get("mirror_trigger_builds")
        if "mirror" in values:
            data["mirror"] = values.get("mirror")
        if "model_experiments_access_level" in values:
            data["model_experiments_access_level"] = values.get(
                "model_experiments_access_level"
            )
        if "model_registry_access_level" in values:
            data["model_registry_access_level"] = values.get(
                "model_registry_access_level"
            )
        if "monitor_access_level" in values:
            data["monitor_access_level"] = values.get("monitor_access_level")
        if "namespace_id" in values:
            data["namespace_id"] = values.get("namespace_id")
        if "only_allow_merge_if_all_discussions_are_resolved" in values:
            data["only_allow_merge_if_all_discussions_are_resolved"] = values.get(
                "only_allow_merge_if_all_discussions_are_resolved"
            )
        if "only_allow_merge_if_all_status_checks_passed" in values:
            data["only_allow_merge_if_all_status_checks_passed"] = values.get(
                "only_allow_merge_if_all_status_checks_passed"
            )
        if "only_allow_merge_if_pipeline_succeeds" in values:
            data["only_allow_merge_if_pipeline_succeeds"] = values.get(
                "only_allow_merge_if_pipeline_succeeds"
            )
        if "packages_enabled" in values:
            data["packages_enabled"] = values.get("packages_enabled")
        if "pages_access_level" in values:
            data["pages_access_level"] = values.get("pages_access_level")
        if "path" in values:
            data["path"] = values.get("path")
        if "printing_merge_request_link_enabled" in values:
            data["printing_merge_request_link_enabled"] = values.get(
                "printing_merge_request_link_enabled"
            )
        if "public_builds" in values:
            data["public_builds"] = values.get("public_builds")
        if "public_jobs" in values:
            data["public_jobs"] = values.get("public_jobs")
        if "releases_access_level" in values:
            data["releases_access_level"] = values.get("releases_access_level")
        if "repository_object_format" in values:
            data["repository_object_format"] = values.get("repository_object_format")
        if "remove_source_branch_after_merge" in values:
            data["remove_source_branch_after_merge"] = values.get(
                "remove_source_branch_after_merge"
            )
        if "repository_access_level" in values:
            data["repository_access_level"] = values.get("repository_access_level")
        if "repository_storage" in values:
            data["repository_storage"] = values.get("repository_storage")
        if "request_access_enabled" in values:
            data["request_access_enabled"] = values.get("request_access_enabled")
        if "requirements_access_level" in values:
            data["requirements_access_level"] = values.get("requirements_access_level")
        if "resolve_outdated_diff_discussions" in values:
            data["resolve_outdated_diff_discussions"] = values.get(
                "resolve_outdated_diff_discussions"
            )
        if "security_and_compliance_access_level" in values:
            data["security_and_compliance_access_level"] = values.get(
                "security_and_compliance_access_level"
            )
        if "shared_runners_enabled" in values:
            data["shared_runners_enabled"] = values.get("shared_runners_enabled")
        if "show_default_award_emojis" in values:
            data["show_default_award_emojis"] = values.get("show_default_award_emojis")
        if "snippets_access_level" in values:
            data["snippets_access_level"] = values.get("snippets_access_level")
        if "snippets_enabled" in values:
            data["snippets_enabled"] = values.get("snippets_enabled")
        if "squash_commit_template" in values:
            data["squash_commit_template"] = values.get("squash_commit_template")
        if "squash_option" in values:
            data["squash_option"] = values.get("squash_option")
        if "suggestion_commit_message" in values:
            data["suggestion_commit_message"] = values.get("suggestion_commit_message")
        if "tag_list" in values:
            data["tag_list"] = values.get("tag_list")
        if "template_name" in values:
            data["template_name"] = values.get("template_name")
        if "topics" in values:
            data["topics"] = values.get("topics")
        if "use_custom_template" in values:
            data["use_custom_template"] = values.get("use_custom_template")
        if "visibility" in values:
            data["visibility"] = values.get("visibility")
        if "warn_about_potentially_unwanted_characters" in values:
            data["warn_about_potentially_unwanted_characters"] = values.get(
                "warn_about_potentially_unwanted_characters"
            )
        if "wiki_access_level" in values:
            data["wiki_access_level"] = values.get("wiki_access_level")
        if "wiki_enabled" in values:
            data["wiki_enabled"] = values.get("wiki_enabled")

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
        "approvals_before_merge",
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
    data: Optional[Dict] = None

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

        if "allow_force_push" in values:
            data["allow_force_push"] = values.get("allow_force_push")
        if "allowed_to_push" in values:
            data["allowed_to_push"] = values.get("allowed_to_push")
        if "allowed_to_merge" in values:
            data["allowed_to_merge"] = values.get("allowed_to_merge")
        if "allowed_to_unprotect" in values:
            data["allowed_to_unprotect"] = values.get("allowed_to_unprotect")
        if "code_owner_approval_required" in values:
            data["code_owner_approval_required"] = values.get(
                "code_owner_approval_required"
            )

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
    data: Optional[Dict] = None

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

        if "description" in values:
            data["name"] = values.get("description")
        if "tag_name" in values:
            data["tag_name"] = values.get("tag_name")
        if "tag_message" in values:
            data["tag_message"] = values.get("tag_message")
        if "description" in values:
            data["description"] = values.get("description")
        if "ref" in values:
            data["ref"] = values.get("reference")
        if "milestones" in values:
            data["milestones"] = values.get("milestones")
        if "assets:links" in values:
            data["assets:links"] = values.get("assets:links")
        if "assets:links:name" in values:
            data["assets:links:name"] = values.get("assets:links:name")
        if "assets:links:url" in values:
            data["assets:links:url"] = values.get("assets:links:url")
        if "assets:links:direct_asset_path" in values:
            data["assets:links:direct_asset_path"] = values.get(
                "assets:links:direct_asset_path"
            )
        if "released_at" in values:
            data["released_at"] = values.get("released_at")

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
    data: Optional[Dict] = None

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

        if "description" in values:
            data["name"] = values.get("description")
        if "active" in values:
            data["active"] = values.get("active")
        if "paused" in values:
            data["paused"] = values.get("paused")
        if "tag_list" in values:
            data["tag_list"] = values.get("tag_list")
        if "run_untagged" in values:
            data["run_untagged"] = values.get("run_untagged")
        if "locked" in values:
            data["locked"] = values.get("locked")
        if "access_level" in values:
            data["access_level"] = values.get("access_level")
        if "maximum_timeout" in values:
            data["maximum_timeout"] = values.get("maximum_timeout")
        if "info" in values:
            data["info"] = values.get("info")
        if "maintenance_note" in values:
            data["maintenance_note"] = values.get("maintenance_note")
        if "token" in values:
            data["token"] = values.get("token")

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
    max_pages: Optional[int] = 0
    page: Optional[int] = 1
    per_page: Optional[int] = 100
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
        if self.page:
            self.api_parameters["page"] = self.page
        if self.per_page:
            self.api_parameters["per_page"] = self.per_page

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
    data: Optional[Dict] = None

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

        if "content" in values:
            data["content"] = values.get("content")
        if "title" in values:
            data["title"] = values.get("title")
        if "format" in values:
            data["format"] = values.get("format")
        if "file" in values:
            data["file"] = f'@{values.get("file")}'

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


########################################################################################################################
#                                              Output Models                                                           #
########################################################################################################################
class IssueStats(BaseModel):
    class Meta:
        orm_model = IssueStatsDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="IssueStats")
    total: Optional[int] = Field(default=None, description="Total number of issues")
    closed: Optional[int] = Field(default=None, description="Number of closed issues")
    opened: Optional[int] = Field(default=None, description="Number of opened issues")


class Milestone(BaseModel):
    class Meta:
        orm_model = MilestoneDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = TimeStatsDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = TaskCompletionStatusDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="TaskCompletionStatus")
    count: Optional[int] = Field(
        default=None, description="Total number of tasks in the merge request"
    )
    completed_count: Optional[int] = Field(
        default=None, description="Number of completed tasks in the merge request"
    )


class References(BaseModel):
    class Meta:
        orm_model = ReferencesDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = ArtifactDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = ArtifactsFileDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="ArtifactsFile")
    filename: Optional[str] = Field(
        default=None, description="Filename of the artifacts file."
    )
    size: Optional[int] = Field(default=None, description="Size of the artifacts file.")


class RunnerManager(BaseModel):
    class Meta:
        orm_model = RunnerManagerDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = ConfigurationDBModel

    model_config = ConfigDict(extra="forbid")
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


class Iteration(BaseModel):
    class Meta:
        orm_model = IterationDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = IdentityDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Identity")
    provider: Optional[str] = Field(default=None, description="The external provider.")
    extern_uid: Optional[str] = Field(
        default=None, description="The external authentication provider UID."
    )


class GroupSamlIdentity(BaseModel):
    class Meta:
        orm_model = GroupSamlIdentityDBModel

    model_config = ConfigDict(extra="forbid")
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


class CreatedBy(BaseModel):
    class Meta:
        orm_model = CreatedByDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="CreatedBy")
    id: Optional[int] = Field(
        default=None, description="ID of the user who created the member"
    )
    username: Optional[str] = Field(
        default=None, description="Username of the user who created the member"
    )
    name: Optional[str] = Field(
        default=None, description="Name of the user who created the member"
    )
    state: Optional[str] = Field(
        default=None, description="State of the user who created the member"
    )
    avatar_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="Avatar URL of the user who created the member"
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="Web URL of the user who created the member"
    )


class User(BaseModel):
    class Meta:
        orm_model = UserDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="User")
    id: Optional[int] = Field(default=None, description="The unique ID of the user.")
    username: Optional[str] = Field(
        default=None, description="The username of the user."
    )
    user: Optional[str] = Field(default=None, description="The user.")
    email: Optional[EmailStr] = Field(
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
    created_by: Optional[Union[int, CreatedBy]] = Field(
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


class Users(BaseModel):
    class Meta:
        orm_model = UsersDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Users")
    users: Optional[List[User]] = Field(default=None, description="All the users")


class Namespace(BaseModel):
    class Meta:
        orm_model = NamespaceDBModel

    model_config = ConfigDict(extra="forbid")
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
    avatar_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The avatar URL of the namespace."
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="The web URL of the namespace."
    )


class ContainerExpirationPolicy(BaseModel):
    class Meta:
        orm_model = ContainerExpirationPolicyDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = PermissionsDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Permissions")
    project_access: Optional[Dict] = Field(
        default=None, description="Project access level and notification settings."
    )
    group_access: Optional[Dict] = Field(
        default=None, description="Group access level and notification settings."
    )


class Statistics(BaseModel):
    class Meta:
        orm_model = StatisticsDBModel

    model_config = ConfigDict(extra="forbid")
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


class Links(BaseModel):
    class Meta:
        orm_model = LinksDBModel

    model_config = ConfigDict(extra="forbid")
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


class Diff(BaseModel):
    class Meta:
        orm_model = DiffDBModel

    model_config = ConfigDict(extra="forbid")
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


class Diffs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Diffs")
    diffs: List[Diff] = Field(default=None, description="List of diffs")


class DetailedStatus(BaseModel):
    class Meta:
        orm_model = DetailedStatusDBModel

    model_config = ConfigDict(extra="forbid")
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


class Pipeline(BaseModel):
    class Meta:
        orm_model = PipelineDBModel

    model_config = ConfigDict(extra="forbid")
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


class Pipelines(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Pipelines")
    pipelines: List[Pipeline] = Field(default=None, description="List of pipelines")


class PackageLink(BaseModel):
    class Meta:
        orm_model = PackageLinkDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="PackageLink")
    web_path: Optional[str] = Field(
        default=None, description="Web path to access the package"
    )
    delete_api_path: Optional[str] = Field(
        default=None, description="API path to delete the package"
    )


class PackageVersion(BaseModel):
    class Meta:
        orm_model = PackageVersionDBModel

    model_config = ConfigDict(extra="forbid")
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


class Package(BaseModel):
    class Meta:
        orm_model = PackageDBModel

    model_config = ConfigDict(extra="forbid")
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
    tags: Optional[List[str]] = Field(
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


class Packages(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Packages")
    packages: List[Package] = Field(default=None, description="List of packages")


class Contributor(BaseModel):
    class Meta:
        orm_model = ContributorDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="CommitStats")
    name: str = Field(default=None, description="The name of the contributor.")
    email: EmailStr = Field(default=None, description="The email of the contributor.")
    commits: int = Field(default=None, description="Number of commits from contributor")
    additions: int = Field(
        default=None, description="Number of additions from contributor"
    )
    deletions: int = Field(
        default=None, description="Number of deletions from contributor"
    )


class Contributors(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Contributors")
    contributors: List[Contributor] = Field(
        default=None, description="List of contributors"
    )


class CommitStats(BaseModel):
    class Meta:
        orm_model = CommitStatsDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = CommitSignatureDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = CommentDBModel

    model_config = ConfigDict(extra="forbid")
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
    noteable_id: Optional[int] = Field(
        default=None, description="ID of the noteable entity"
    )
    noteable_type: Optional[str] = Field(
        default=None, description="Type of the noteable entity"
    )
    resolvable: Optional[bool] = Field(
        default=None, description="Whether the note is resolvable"
    )
    confidential: Optional[bool] = Field(
        default=None, description="Whether the note is confidential"
    )
    noteable_iid: Optional[int] = Field(
        default=None, description="IID of the noteable entity"
    )
    commands_changes: Optional[Dict[str, Any]] = Field(
        default=None, description="Command changes associated with the note"
    )
    line_type: Optional[str] = Field(default=None, description="Line type")
    path: Optional[str] = Field(default=None, description="Path")
    line: Optional[int] = Field(default=None, description="Line in note")


class Comments(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Comments")
    comments: List[Comment] = Field(default=None, description="List of comments")


class Commit(BaseModel):
    class Meta:
        orm_model = CommitDBModel

    model_config = ConfigDict(extra="forbid")
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
    parent_ids: Optional[List[str]] = Field(
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
    committer_email: Optional[EmailStr] = Field(
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
    extended_trailers: Optional[Dict[str, List[str]]] = Field(
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


class Commits(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Commits")
    commits: List[Commit] = Field(default=None, description="List of commits")


class Membership(BaseModel):
    class Meta:
        orm_model = MembershipDBModel

    model_config = ConfigDict(extra="forbid")
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


class Memberships(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Memberships")
    memberships: List[Membership] = Field(
        default=None, description="List of memberships"
    )


class ApprovedBy(BaseModel):
    class Meta:
        orm_model = ApprovedByDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="ApprovedBy")
    user: User = Field(
        default=None, description="User who has approved the merge request"
    )


class Project(BaseModel):
    class Meta:
        orm_model = ProjectDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Project")
    id: Optional[int] = Field(default=None, description="The ID of the project.")
    description: Optional[str] = Field(
        default=None, description="The description of the project."
    )
    description_html: Optional[str] = Field(
        default=None, description="The HTML description of the project."
    )
    name: Optional[str] = Field(default=None, description="The name of the project.")
    name_with_namespace: Optional[str] = Field(
        default=None, description="The name with namespace of the project."
    )
    path: Optional[str] = Field(default=None, description="The path of the project.")
    path_with_namespace: Optional[str] = Field(
        default=None, description="The path with namespace of the project."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="The creation time of the project."
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="The last update time of the project."
    )
    default_branch: Optional[str] = Field(
        default=None, description="The default branch of the project."
    )
    tag_list: Optional[List[str]] = Field(
        default=None, description="Deprecated. Use `topics` instead."
    )
    topics: Optional[List[str]] = Field(
        default=None, description="The topics of the project."
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
    additional_links: Optional[Links] = Field(
        default=None, alias="_links", description="Related links."
    )
    packages_enabled: Optional[bool] = Field(
        default=None, description="Whether packages are enabled."
    )
    empty_repo: Optional[bool] = Field(
        default=None, description="Whether the repository is empty."
    )
    archived: Optional[bool] = Field(
        default=None, description="Whether the project is archived."
    )
    visibility: Optional[str] = Field(
        default=None, description="The visibility of the project."
    )
    resolve_outdated_diff_discussions: Optional[bool] = Field(
        default=None, description="Whether outdated diff discussions are resolved."
    )
    container_expiration_policy: Optional[ContainerExpirationPolicy] = Field(
        default=None, description="The container expiration policy."
    )
    releases_access_level: Optional[str] = Field(
        default=None, description="Release access level"
    )
    environments_access_level: Optional[str] = Field(
        default=None, description="Environments access level"
    )
    feature_flags_access_level: Optional[str] = Field(
        default=None, description="Feature flags access level"
    )
    infrastructure_access_level: Optional[str] = Field(
        default=None, description="Infrastructure access level"
    )
    monitor_access_level: Optional[str] = Field(
        default=None, description="Monitor access level"
    )
    machine_learning_model_experiments_access_level: Optional[str] = Field(
        default=None,
        alias="model_experiments_access_level",
        description="Model Experiments access level",
    )
    machine_learning_model_registry_access_level: Optional[str] = Field(
        default=None,
        alias="model_registry_access_level",
        description="Model registry access level",
    )
    issues_enabled: Optional[bool] = Field(
        default=None, description="Whether issues are enabled."
    )
    merge_requests_enabled: Optional[bool] = Field(
        default=None, description="Whether merge requests are enabled."
    )
    wiki_enabled: Optional[bool] = Field(
        default=None, description="Whether the wiki is enabled."
    )
    jobs_enabled: Optional[bool] = Field(
        default=None, description="Whether jobs are enabled."
    )
    snippets_enabled: Optional[bool] = Field(
        default=None, description="Whether snippets are enabled."
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
    forked_from_project: Optional[Dict] = Field(
        default=None, description="The project from where this project was forked from."
    )
    mr_default_target_self: Optional[bool] = Field(
        default=None,
        description="Merge Request default target self.",
    )
    public_jobs: Optional[bool] = Field(
        default=None, description="Whether jobs are public."
    )
    shared_with_groups: Optional[List] = Field(
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
        default=None, description="Whether user-defined variables are restricted."
    )
    code_suggestions: Optional[bool] = Field(
        default=None, description="Enable code suggestions"
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
        default=None, description="Merge pipelines enabled."
    )
    merge_trains_skip_train_allowed: Optional[bool] = Field(
        default=None, description="Merge trains skip trains enabled."
    )
    allow_pipeline_trigger_approve_deployment: Optional[bool] = Field(
        default=None, description="Allow pipeline to trigger deployment."
    )
    repository_object_format: Optional[str] = Field(
        default=None, description="Repository object format"
    )
    merge_method: Optional[str] = Field(
        default=None, description="The method used for merging."
    )
    squash_option: Optional[str] = Field(default=None, description="The squash option.")
    enforce_auth_checks_on_uploads: Optional[bool] = Field(
        default=None, description="Whether auth checks are enforced on uploads."
    )
    suggestion_commit_message: Optional[str] = Field(
        default=None, description="The suggestion commit message."
    )
    compliance_frameworks: Optional[List[str]] = Field(
        default=None, description="The compliance frameworks."
    )
    issues_template: Optional[str] = Field(
        default=None, description="The issues template."
    )
    merge_requests_template: Optional[str] = Field(
        default=None, description="The merge requests template."
    )
    packages_relocation_enabled: Optional[bool] = Field(
        default=None, description="Whether package relocation is enabled."
    )
    requirements_enabled: Optional[bool] = Field(
        default=None, description="The requirements feature enabled status."
    )
    build_git_strategy: Optional[str] = Field(
        default=None, description="The build git strategy."
    )
    build_timeout: Optional[int] = Field(default=None, description="The build timeout.")
    auto_cancel_pending_pipelines: Optional[str] = Field(
        default=None, description="The auto-cancel pending pipelines setting."
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
        default=None, description="Whether the project has open issues."
    )
    approvals_before_merge: Optional[int] = Field(
        default=None, description="Number of approvals required before merging."
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
    links: Optional[Links] = Field(default=None, description="Related links.")
    service_desk_enabled: Optional[bool] = Field(
        default=None, description="Service Desk Enabled"
    )
    can_create_merge_request_in: Optional[bool] = Field(
        default=None, description="Can create merge request in"
    )
    repository_access_level: Optional[str] = Field(
        default=None, description="Repository access level"
    )
    merge_requests_access_level: Optional[str] = Field(
        default=None, description="Merge request access level"
    )
    issues_access_level: Optional[str] = Field(
        default=None, description="Issue access level"
    )
    forking_access_level: Optional[str] = Field(
        default=None, description="Forking access level"
    )
    wiki_access_level: Optional[str] = Field(
        default=None, description="Wiki access level"
    )
    builds_access_level: Optional[str] = Field(
        default=None, description="Build access level"
    )
    snippets_access_level: Optional[str] = Field(
        default=None, description="Snippet access level"
    )
    pages_access_level: Optional[str] = Field(
        default=None, description="Page access level"
    )
    analytics_access_level: Optional[str] = Field(
        default=None, description="Analytics access level"
    )
    emails_disabled: Optional[bool] = Field(default=None, description="Emails disabled")
    emails_enabled: Optional[bool] = Field(default=None, description="Emails enabled")
    open_issues_count: Optional[int] = Field(
        default=None, description="Open issues in project"
    )
    ci_job_token_scope_enabled: Optional[bool] = Field(
        default=None, description="CI Job Token scope enabled"
    )
    merge_commit_template: Optional[str] = Field(
        default=None, description="Merge commit template"
    )
    squash_commit_template: Optional[str] = Field(
        default=None, description="Squash commit template"
    )
    issue_branch_template: Optional[str] = Field(
        default=None, description="Squash commit template"
    )
    auto_devops_enabled: Optional[bool] = Field(
        default=None, description="Autodevops enabled"
    )
    auto_devops_deploy_strategy: Optional[str] = Field(
        default=None, description="Autodevops deploy strategy"
    )
    autoclose_referenced_issues: Optional[bool] = Field(
        default=None, description="Autoclose referenced issues"
    )
    keep_latest_artifact: Optional[bool] = Field(
        default=None, description="Keep latest artifact"
    )
    runner_token_expiration_interval: Optional[bool] = Field(
        default=None, description="Runner token expiration interval"
    )
    external_authorization_classification_label: Optional[str] = Field(
        default=None, description="External authorization classification label"
    )
    requirements_access_level: Optional[str] = Field(
        default=None, description="Requirements access level"
    )
    security_and_compliance_enabled: Optional[bool] = Field(
        default=None, description="Security compliance enabled"
    )
    warn_about_potentially_unwanted_characters: Optional[bool] = Field(
        default=None, description="Warna bout potentially unwanted characters."
    )
    owner: Optional[User] = Field(default=None, description="Owner user")
    runners_token: Optional[str] = Field(default=None, description="Runners token")
    repository_storage: Optional[str] = Field(
        default=None, description="Repository storage enabled"
    )
    service_desk_address: Optional[str] = Field(
        default=None, description="Service desk address"
    )
    marked_for_deletion_at: Optional[str] = Field(
        default=None, description="Marked for deletion at"
    )
    marked_for_deletion_on: Optional[str] = Field(
        default=None, description="Marked for deletion on"
    )
    operations_access_level: Optional[str] = Field(
        default=None, description="Access level of operations"
    )
    ci_dockerfile: Optional[str] = Field(default=None, description="Dockerfile for CI")
    groups: Optional[List[Dict[str, int]]] = Field(
        default=None, description="List of groups"
    )
    public: Optional[bool] = Field(
        default=None, description="Whether project is allowed to be public."
    )


class Projects(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Projects")
    projects: List[Project] = Field(default=None, description="List of projects")


class Runner(BaseModel):
    class Meta:
        orm_model = RunnerDBModel

    model_config = ConfigDict(extra="forbid")
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
    tag_list: Optional[List[str]] = Field(
        None, description="List of tags associated with the runner"
    )


class Runners(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Runners")
    runners: List[Runner] = Field(default=None, description="List of runners")


class Job(BaseModel):
    class Meta:
        orm_model = JobDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Job")
    commit: Optional[Commit] = Field(
        default=None, description="Details of the commit associated with the job."
    )
    coverage: Optional[float] = Field(
        default=None, description="Code coverage percentage."
    )
    archived: Optional[bool] = Field(
        default=None, description="Indicates if the job is archived."
    )
    allow_failure: Optional[bool] = Field(
        default=None, description="Indicates if the job is allowed to fail."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the job was created."
    )
    started_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the job was started."
    )
    finished_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the job was finished."
    )
    erased_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the job was erased."
    )
    duration: Optional[float] = Field(
        default=None, description="Duration of the job in seconds."
    )
    queued_duration: Optional[float] = Field(
        default=None, description="Time the job spent queued before starting."
    )
    artifacts_file: Optional[ArtifactsFile] = Field(
        default=None, description="Details of the artifacts file produced by the job."
    )
    artifacts: Optional[List[Artifact]] = Field(
        default=None, description="List of artifacts produced by the job."
    )
    artifacts_expire_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the artifacts expire."
    )
    tag_list: Optional[List[str]] = Field(
        default=None, description="List of tags associated with the job."
    )
    id: Optional[int] = Field(default=None, description="ID of the job.")
    name: Optional[str] = Field(default=None, description="Name of the job.")
    pipeline: Optional[Pipeline] = Field(
        default=None, description="Details of the pipeline associated with the job."
    )
    ref: Optional[str] = Field(default=None, description="Reference of the job.")
    runner: Optional[Runner] = Field(
        default=None, description="Details of the runner that executed the job."
    )
    runner_manager: Optional[RunnerManager] = Field(
        default=None, description="Details of the runner manager."
    )
    stage: Optional[str] = Field(default=None, description="Stage of the job.")
    status: Optional[str] = Field(default=None, description="Status of the job.")
    failure_reason: Optional[str] = Field(
        default=None, description="Reason for the job failure."
    )
    tag: Optional[bool] = Field(
        default=None, description="Indicates if the job is tagged."
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL to view the job on the web."
    )
    project: Optional[Project] = Field(
        default=None, description="Details of the project associated with the job."
    )
    user: Optional[User] = Field(
        default=None, description="Details of the user who created the job."
    )
    downstream_pipeline: Optional[Pipeline] = Field(
        default=None, description="Downstream pipeline."
    )


class Jobs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Jobs")
    jobs: List[Job] = Field(default=None, description="List of jobs")


class GroupAccess(BaseModel):
    class Meta:
        orm_model = GroupAccessDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="GroupAccess")
    access_level: Optional[int] = Field(
        default=None, description="Access level for a group"
    )


class DefaultBranchProtectionDefaults(BaseModel):
    class Meta:
        orm_model = DefaultBranchProtectionDefaultsDBModel

    model_config = ConfigDict(extra="forbid")
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


class Group(BaseModel):
    class Meta:
        orm_model = GroupDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Group")
    id: Optional[int] = Field(default=None, description="The ID of the group")
    organization_id: Optional[int] = Field(
        default=None, description="The Organization ID of the group"
    )
    name: Optional[str] = Field(default=None, description="The name of the group")
    path: Optional[str] = Field(default=None, description="The path of the group")
    description: Optional[str] = Field(
        default=None, description="The description of the group"
    )
    visibility: Optional[str] = Field(
        default=None, description="The visibility level of the group"
    )
    shared_runners_setting: Optional[str] = Field(
        default=None, description="Share runner setting"
    )
    share_with_group_lock: Optional[bool] = Field(
        default=None, description="Lock sharing with other groups"
    )
    require_two_factor_authentication: Optional[bool] = Field(
        default=None, description="Whether 2FA is required"
    )
    two_factor_grace_period: Optional[int] = Field(
        default=None, description="Grace period for 2FA enforcement"
    )
    project_creation_level: Optional[str] = Field(
        default=None, description="Level required to create projects"
    )
    auto_devops_enabled: Optional[bool] = Field(
        default=None, description="Whether Auto DevOps is enabled"
    )
    subgroup_creation_level: Optional[str] = Field(
        default=None, description="Level required to create subgroups"
    )
    emails_disabled: Optional[bool] = Field(
        default=None, description="Whether emails are disabled"
    )
    emails_enabled: Optional[bool] = Field(
        default=None, description="Whether emails are enabled"
    )
    mentions_disabled: Optional[bool] = Field(
        default=None, description="Whether mentions are disabled"
    )
    lfs_enabled: Optional[bool] = Field(
        default=None, description="Whether Git LFS is enabled"
    )
    default_branch: Optional[str] = Field(
        default=None, description="The default branch of the group"
    )
    default_branch_protection: Optional[int] = Field(
        default=None, description="Protection level of the default branch"
    )
    default_branch_protection_defaults: Optional[DefaultBranchProtectionDefaults] = (
        Field(default=None, description="Default branch protection settings")
    )
    avatar_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL of the group's avatar"
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="Web URL of the group"
    )
    request_access_enabled: Optional[bool] = Field(
        default=None, description="Whether request access is enabled"
    )
    repository_storage: Optional[str] = Field(
        default=None, description="Repository storage type"
    )
    full_name: Optional[str] = Field(default=None, description="Full name of the group")
    full_path: Optional[str] = Field(default=None, description="Full path of the group")
    file_template_project_id: Optional[int] = Field(
        default=None, description="ID of the file template project"
    )
    parent_id: Optional[int] = Field(default=None, description="Parent ID of the group")
    created_at: Optional[str] = Field(
        default=None, description="Creation timestamp of the group"
    )
    statistics: Optional[Statistics] = Field(
        default=None, description="Statistics of the group"
    )
    wiki_access_level: Optional[str] = Field(
        default=None, description="Access level of the wiki"
    )
    duo_features_enabled: Optional[bool] = Field(
        default=None, description="Whether Duo features are enabled"
    )
    lock_duo_features_enabled: Optional[bool] = Field(
        default=None, description="Whether Duo features are locked"
    )
    runners_token: Optional[str] = Field(
        default=None, description="Runners token for the group"
    )
    enabled_git_access_protocol: Optional[str] = Field(
        default=None, description="Enabled Git access protocol"
    )
    shared_with_groups: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Groups shared with this group"
    )
    prevent_sharing_groups_outside_hierarchy: Optional[bool] = Field(
        default=None, description="Prevent sharing groups outside hierarchy"
    )
    projects: Optional[Union[List[Project]]] = Field(
        default=None, description="Projects within the group"
    )
    shared_projects: Optional[Union[List[Project]]] = Field(
        default=None, description="Projects within the group"
    )
    ip_restriction_ranges: Optional[Any] = Field(
        default=None, description="IP Restriction Ranges"
    )
    math_rendering_limits_enabled: Optional[bool] = Field(
        default=None, description="Math rendering limits enabled"
    )
    lock_math_rendering_limits_enabled: Optional[bool] = Field(
        default=None, description="Math rendering limits locked"
    )
    shared_runners_minutes_limit: Optional[int] = Field(
        default=None, description="Shared runners limit in minutes"
    )
    extra_shared_runners_minutes_limit: Optional[int] = Field(
        default=None, description="Extra shared runners limit in minutes"
    )
    marked_for_deletion_on: Optional[str] = Field(
        default=None, description="Marked for deletion on."
    )
    membership_lock: Optional[bool] = Field(
        default=None, description="Membership locked"
    )
    ldap_cn: Optional[Any] = Field(default=None, description="LDAP CN information")
    ldap_access: Optional[Any] = Field(default=None, description="LDAP Access")
    prevent_forking_outside_group: Optional[bool] = Field(
        default=None, description="Forking disabled outside group"
    )


class Groups(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Groups")
    groups: List[Group] = Field(default=None, description="List of groups")


class Webhook(BaseModel):
    class Meta:
        orm_model = WebhookDBModel

    model_config = ConfigDict(extra="forbid")
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
    url_variables: List[str] = Field(
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
    class Meta:
        orm_model = AccessLevelDBModel

    model_config = ConfigDict(extra="forbid")
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


class Branch(BaseModel):
    class Meta:
        orm_model = BranchDBModel

    model_config = ConfigDict(extra="forbid")
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


class Branches(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Branches")
    branches: List[Branch] = Field(default=None, description="List of branches")


class ApprovalRule(BaseModel):
    class Meta:
        orm_model = ApprovalRuleDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="ApprovalRule")
    id: Optional[int] = Field(default=None, description="Approval rule ID")
    name: Optional[str] = Field(default=None, description="Approval rule name")
    rule_type: Optional[str] = Field(
        default=None, description="Type of the approval rule"
    )
    eligible_approvers: Optional[Users] = Field(
        default=None, description="List of eligible approvers"
    )
    approvals_required: Optional[int] = Field(
        default=None, description="Number of required approvals"
    )
    users: Optional[Users] = Field(default=None, description="List of associated users")
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
    approved_by: Optional[Users] = Field(
        default=None, description="List of users who approved"
    )

    @field_validator("eligible_approvers", "users", "approved_by", mode="before")
    def empty_list_to_none(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            return Users(users=v)
        return v


class ApprovalRules(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="ApprovalRules")
    approval_rules: List[ApprovalRule] = Field(
        default=None, description="List of approval rules"
    )


class MergeRequest(BaseModel):
    class Meta:
        orm_model = MergeRequestDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="MergeRequest")
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
    state: Optional[str] = Field(default=None, description="State of the merge request")
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
    assignee: Optional[User] = Field(
        default=None, description="Assignee of the merge request"
    )
    source_project_id: Optional[int] = Field(
        default=None, description="ID of the source project"
    )
    target_project_id: Optional[int] = Field(
        default=None, description="ID of the target project"
    )
    labels: Optional[List[str]] = Field(
        default=None, description="List of labels assigned to the merge request"
    )
    work_in_progress: Optional[bool] = Field(
        default=None, description="Whether the merge request is a work in progress"
    )
    milestone: Optional[Milestone] = Field(
        default=None, description="Milestone associated with the merge request"
    )
    merge_when_pipeline_succeeds: Optional[bool] = Field(
        default=None, description="Whether to merge when the pipeline succeeds"
    )
    merge_status: Optional[str] = Field(
        default=None, description="Merge status of the merge request"
    )
    sha: Optional[str] = Field(default=None, description="SHA of the merge request")
    merge_commit_sha: Optional[str] = Field(
        default=None, description="Merge commit SHA of the merge request"
    )
    draft: Optional[bool] = Field(
        default=None, description="Draft state of merge request"
    )
    squash_commit_sha: Optional[str] = Field(
        default=None, description="Squash commit SHA of the merge request"
    )
    squash_on_merge: Optional[bool] = Field(
        default=None, description="Squash commits on merge"
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
        default=None, description="Whether the maintainer can push"
    )
    web_url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="Web URL of the merge request"
    )
    references: Optional[References] = Field(
        default=None, description="References associated with the merge request"
    )
    reference: Optional[str] = Field(
        default=None, description="Reference associated with the merge request"
    )
    time_stats: Optional[TimeStats] = Field(
        default=None, description="Time statistics for the merge request"
    )
    squash: Optional[bool] = Field(
        default=None, description="Whether the merge request should be squashed"
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
        default=None, description="List of changes (diffs) in the merge request"
    )
    merged_by: Optional[User] = Field(
        default=None, description="Merger of the merge request"
    )
    merged_at: Optional[datetime] = Field(
        default=None, description="Date when the merge request was merged"
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
    pipeline: Optional[Pipeline] = Field(
        default=None, description="Pipeline associated with the merge request"
    )
    head_pipeline: Optional[Pipeline] = Field(
        default=None, description="Head pipeline associated with the merge request"
    )
    diff_refs: Optional[Dict[str, Any]] = Field(
        default=None, description="Diff references associated with the merge request"
    )
    user: Optional[Dict[str, Any]] = Field(
        default=None, description="User-specific information"
    )
    changes_count: Optional[str] = Field(
        default=None, description="Count of changes in the merge request"
    )
    rebase_in_progress: Optional[bool] = Field(
        default=None, description="Whether a rebase is in progress"
    )
    approvals_before_merge: Optional[int] = Field(
        default=None, description="Number of approvals required before merging"
    )
    tag_list: Optional[List[str]] = Field(
        default=None, description="List of tags associated with the merge request"
    )
    imported: Optional[bool] = Field(
        default=None, description="Indicates if the merge request was imported"
    )
    imported_from: Optional[str] = Field(
        default=None, description="Source from where the merge request was imported"
    )
    merge_user: Optional[User] = Field(
        default=None,
        description="User who merged the merge request (use instead of merged_by)",
    )
    prepared_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the merge request was prepared"
    )
    assignees: Optional[Users] = Field(
        default=None, description="List of users assigned to the merge request"
    )
    reviewer: Optional[Users] = Field(
        default=None, description="List of reviewers for the merge request"
    )
    reviewers: Optional[Users] = Field(
        default=None, description="List of users reviewing the merge request"
    )
    review: Optional[Dict[str, Any]] = Field(
        default=None, description="Review information associated with the merge request"
    )
    detailed_merge_status: Optional[str] = Field(
        default=None, description="Detailed status of the merge request mergeability"
    )
    subscribed: Optional[bool] = Field(
        default=None, description="Subscribed to Merge Request"
    )
    overflow: Optional[bool] = Field(
        default=None, description="Indicates if overflow is enabled"
    )
    diverged_commits_count: Optional[int] = Field(
        default=None, description="Diverged commit count"
    )
    merge_error: Optional[Union[str, Any]] = Field(
        default=None, description="Merge errors"
    )
    approvals_required: Optional[int] = Field(
        default=None, description="Number of approvals required"
    )
    approvals_left: Optional[int] = Field(
        default=None, description="Number of approvals left"
    )
    approved_by: Optional[List[ApprovedBy]] = Field(
        default=None, description="List of users who approved"
    )
    approval_rules_overwritten: Optional[bool] = Field(
        default=None, description="Allow override of approval rules"
    )
    rules: Optional[List[ApprovalRule]] = Field(
        default=None, description="List of merge request rules"
    )

    @field_validator("assignees", "reviewers", "reviewer", mode="before")
    def empty_list_to_none(cls, v):
        if isinstance(v, list) and not v:
            return None
        if isinstance(v, list):
            return Users(users=v)
        return v


class MergeRequests(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="MergeRequests")
    merge_requests: List[MergeRequest] = Field(
        default=None, description="List of merge requests"
    )


class Epic(BaseModel):
    class Meta:
        orm_model = EpicDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = IssueDBModel

    model_config = ConfigDict(extra="forbid")
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
    assignees: Optional[Users] = Field(
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
    labels: Optional[List[str]] = Field(
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
    links: Optional[Links] = Field(
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
            return Users(users=v)
        return v


class Issues(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Issues")
    issues: List[Issue] = Field(default=None, description="List of issues")


class PipelineVariable(BaseModel):
    class Meta:
        orm_model = PipelineVariableDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="PipelineVariable")
    key: Optional[str] = Field(default=None, description="The key of the variable.")
    variable_type: Optional[str] = Field(
        default=None, description="The type of the variable (e.g., env_var)."
    )
    value: Optional[str] = Field(default=None, description="The value of the variable.")


class PipelineVariables(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="PipelineVariables")
    pipeline_variables: List[PipelineVariable] = Field(
        default=None, description="List of pipeline variables"
    )


class TestCase(BaseModel):
    class Meta:
        orm_model = TestCaseDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = TestSuiteDBModel

    model_config = ConfigDict(extra="forbid")
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


class TestReportTotal(BaseModel):
    class Meta:
        orm_model = TestReportTotalDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = TestReportDBModel

    model_config = ConfigDict(extra="forbid")
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


class MergeApprovals(BaseModel):
    class Meta:
        orm_model = MergeApprovalsDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="MergeApprovals")
    approvers: Optional[Users] = Field(default=None, description="List of approvers")
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
            return Users(users=v)
        return v


class DeployToken(BaseModel):
    class Meta:
        orm_model = DeployTokenDBModel

    model_config = ConfigDict(extra="forbid")
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


class DeployTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="DeployTokens")
    deploy_tokens: List[DeployToken] = Field(
        default=None, description="List of deploy tokens"
    )


class Rule(BaseModel):
    class Meta:
        orm_model = RuleDBModel

    model_config = ConfigDict(extra="forbid")
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


class AccessControl(BaseModel):
    class Meta:
        orm_model = AccessControlDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = SourcesDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Source")
    format: Optional[str] = Field(
        default=None, description="Format of the source file (e.g., zip, tar.gz)"
    )
    url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL to download the source file"
    )


class Link(BaseModel):
    class Meta:
        orm_model = LinkDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Link")
    id: Optional[int] = Field(default=None, description="Link ID")
    name: Optional[str] = Field(default=None, description="Name of the link")
    url: Optional[Union[HttpUrl, str]] = Field(
        default=None, description="URL of the link"
    )
    link_type: Optional[str] = Field(
        default=None, description="Type of the link (e.g., other)"
    )


class Assets(BaseModel):
    class Meta:
        orm_model = AssetsDBModel

    model_config = ConfigDict(extra="forbid")
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


class Evidence(BaseModel):
    class Meta:
        orm_model = EvidenceDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = ReleaseLinksDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = ReleaseDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Release")
    tag_name: Optional[str] = Field(default=None, description="Tag name of the release")
    description: Optional[str] = Field(
        default=None, description="Description of the release"
    )
    name: Optional[str] = Field(default=None, description="Name of the release")
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


class Releases(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Releases")
    releases: List[Release] = Field(default=None, description="List of releases")


class Token(BaseModel):
    class Meta:
        orm_model = TokenDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Token")
    id: Optional[int] = Field(None, description="Token ID")
    token: Optional[str] = Field(None, description="Authentication token")
    token_expires_at: Optional[datetime] = Field(
        None, description="Expiration date and time of the token"
    )


class ToDo(BaseModel):
    class Meta:
        orm_model = ToDoDBModel

    model_config = ConfigDict(extra="forbid")
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
    class Meta:
        orm_model = WikiPageDBModel

    model_config = ConfigDict(extra="forbid")
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


class WikiPages(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="WikiPages")
    wiki_pages: List[WikiPage] = Field(default=None, description="List of wiki pages")


class WikiAttachmentLink(BaseModel):
    class Meta:
        orm_model = WikiAttachmentLinkDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="WikiAttachmentLink")
    url: Optional[Union[HttpUrl, str]] = Field(
        None, description="URL of the uploaded attachment"
    )
    markdown: Optional[str] = Field(
        None, description="Markdown to embed the uploaded attachment"
    )


class WikiAttachment(BaseModel):
    class Meta:
        orm_model = WikiAttachmentDBModel

    model_config = ConfigDict(extra="forbid")
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


class ProjectConfig(BaseModel):
    class Meta:
        orm_model = ProjectConfigDBModel

    model_config = ConfigDict(extra="forbid")
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


class Agent(BaseModel):
    class Meta:
        orm_model = AgentDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Agent")
    id: int = Field(default=None, description="Agent identifier")
    config_project: ProjectConfig = Field(
        default=None, description="Configuration project associated with the agent"
    )


class Agents(BaseModel):
    class Meta:
        orm_model = AgentsDBModel

    model_config = ConfigDict(extra="forbid")
    __hash__ = object.__hash__
    base_type: str = Field(default="Agents")
    allowed_agents: List[Agent] = Field(
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


class Response(BaseModel):
    model_config = ConfigDict(extra="forbid")
    base_type: str = Field(default="Response")
    data: Optional[
        Union[
            List,
            Dict,
            Agents,
            Agent,
            Branches,
            Branch,
            Pipelines,
            Pipeline,
            Contributors,
            Contributor,
            Commits,
            Commit,
            PipelineVariable,
            PipelineVariables,
            CommitSignature,
            Diffs,
            Diff,
            Comments,
            Comment,
            Users,
            User,
            Memberships,
            Membership,
            Releases,
            Release,
            Issues,
            Issue,
            ToDo,
            TestReport,
            MergeRequests,
            MergeRequest,
            MergeApprovals,
            ApprovalRules,
            ApprovalRule,
            Runners,
            Runner,
            Jobs,
            Job,
            Packages,
            Package,
            DeployTokens,
            DeployToken,
            AccessLevel,
            AccessControl,
            Rule,
            Groups,
            Group,
            Projects,
            Project,
            TimeStats,
            Token,
            WikiPage,
            WikiPages,
            WikiAttachment,
            Webhook,
        ]
    ] = Field(default=None, description="Data")
    status_code: Union[str, int] = Field(
        default=None, description="Response status code"
    )
    headers: Dict = Field(default=None, description="Headers of payload")
    json_output: Optional[Union[List, Dict]] = Field(
        default=None, description="Response JSON data"
    )
    raw_output: Optional[bytes] = Field(default=None, description="Response Raw bytes")
    message: Optional[str] = Field(default=None, description="Any error messages")

    @field_validator("data")
    def determine_model_type(cls, value):
        single_models = {
            "Agents": Agents,
            "Branch": Branch,
            "Pipeline": Pipeline,
            "CommitSignature": CommitSignature,
            "Contributor": Contributor,
            "Commit": Commit,
            "PipelineVariable": PipelineVariable,
            "Diff": Diff,
            "Comment": Comment,
            "Issue": Issue,
            "ToDo": ToDo,
            "TestReport": TestReport,
            "MergeRequest": MergeRequest,
            "MergeApprovals": MergeApprovals,
            "Release": Release,
            "DeployToken": DeployToken,
            "User": User,
            "Membership": Membership,
            "Group": Group,
            "Job": Job,
            "Package": Package,
            "AccessLevel": AccessLevel,
            "AccessControl": AccessControl,
            "Rule": Rule,
            "Project": Project,
            "TimeStats": TimeStats,
            "Token": Token,
            "WikiPage": WikiPage,
            "WikiAttachment": WikiAttachment,
            "Webhook": Webhook,
            "ApprovalRule": ApprovalRule,
            "Runner": Runner,
        }
        temp_value = None
        if isinstance(value, list):
            if len(value) > 0:
                if all(isinstance(item, Dict) for item in value):
                    try:
                        branches = [Branch(**item) for item in value]
                        temp_value = Branches(branches=branches)
                        logging.info(f"Branches Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Branches Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        contributors = [Contributor(**item) for item in value]
                        temp_value = Contributors(contributors=contributors)
                        logging.info(f"Contributors Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Contributors Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        commits = [Commit(**item) for item in value]
                        temp_value = Commits(commits=commits)
                        logging.info(f"Commits Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Commits Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        pipelines = [Pipeline(**item) for item in value]
                        temp_value = Pipelines(pipelines=pipelines)
                        logging.info(f"Pipelines Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Pipelines Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        merge_requests = [MergeRequest(**item) for item in value]
                        temp_value = MergeRequests(merge_requests=merge_requests)
                        logging.info(f"Merge Requests Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Merge Requests Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        releases = [Release(**item) for item in value]
                        temp_value = Releases(releases=releases)
                        logging.info(f"Releases Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Releases Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        diffs = [Diff(**item) for item in value]
                        temp_value = Diffs(diffs=diffs)
                        logging.info(f"Diffs Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Diffs Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        comments = [Comment(**item) for item in value]
                        temp_value = Comments(comments=comments)
                        logging.info(f"Comments Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Comments Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        deploy_tokens = [DeployToken(**item) for item in value]
                        temp_value = DeployTokens(deploy_tokens=deploy_tokens)
                        logging.info(f"Deploy Tokens Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Deploy Tokens Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        users = [User(**item) for item in value]
                        temp_value = Users(users=users)
                        logging.info(f"Users Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Users Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        memberships = [Membership(**item) for item in value]
                        temp_value = Memberships(memberships=memberships)
                        logging.info(f"Memberships Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Memberships Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        groups = [Group(**item) for item in value]
                        temp_value = Groups(groups=groups)
                        logging.info(f"Groups Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Groups Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        pipeline_variables = [
                            PipelineVariable(**item) for item in value
                        ]
                        temp_value = PipelineVariables(
                            pipeline_variables=pipeline_variables
                        )
                        logging.info(f"PipelineVariable Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n PipelineVariable Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        projects = [Project(**item) for item in value]
                        temp_value = Projects(projects=projects)
                        logging.info(f"Projects Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Projects Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        issues = [Issue(**item) for item in value]
                        temp_value = Issues(issues=issues)
                        logging.info(f"Issues Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Issues Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        wiki_pages = [WikiPage(**item) for item in value]
                        temp_value = WikiPages(wiki_pages=wiki_pages)
                        logging.info(f"WikiPages Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n WikiPages Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        approval_rules = [ApprovalRule(**item) for item in value]
                        temp_value = ApprovalRules(approval_rules=approval_rules)
                        logging.info(f"ApprovalRules Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n ApprovalRules Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        jobs = [Job(**item) for item in value]
                        temp_value = Jobs(jobs=jobs)
                        logging.info(f"Jobs Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Jobs Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        packages = [Package(**item) for item in value]
                        temp_value = Packages(packages=packages)
                        logging.info(f"Packages Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Packages Validation Failed: {value}\nError: {e}"
                        )
                    try:
                        runners = [Runner(**item) for item in value]
                        temp_value = Runners(runners=runners)
                        logging.info(f"Runners Validation Success: {value}")
                    except Exception as e:
                        logging.warning(
                            f"\n\n\n Runners Validation Failed: {value}\nError: {e}"
                        )
            else:
                return value
            value = temp_value
        elif isinstance(value, dict):
            for model_name, model in single_models.items():
                try:
                    temp_value = model(**value)
                    logging.info(f"{model_name} Model Validation Success: {value}")
                    value = temp_value
                except Exception as e:
                    logging.warning(
                        f"\n\n\n {model_name} Dict Validation Failed for  - {value}\nError: {e}"
                    )
        return value
