from typing import Union, List, Dict, Any, Optional
from typing_extensions import Self
from pydantic import BaseModel, ValidationInfo, field_validator, model_validator
import re

try:
    from gitlab_api.decorators import require_auth
except ModuleNotFoundError:
    from decorators import require_auth
try:
    from gitlab_api.exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)
except ModuleNotFoundError:
    from exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)


class BranchModel(BaseModel):
    """
    Pydantic model representing information about a branch.

    Attributes:
        project_id (Union[int, str]): The identifier of the project associated with the branch.
        branch (str, optional): The name of the branch.
        reference (str, optional): Reference information for the branch.
        api_parameters (str): Additional API parameters for the group.

    Notes:
        This model includes a validator `validate_required_parameters` to ensure that the `project_id` field is
        provided when either `branch` or `reference` is specified.
    """
    project_id: Union[int, str]
    branch: Optional[str] = None
    reference: Optional[str] = None
    api_parameters: Optional[str] = ""

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters for the job.

        Args:
        - values: Dictionary of all values.

        Returns:
        - str: The constructed API parameters.

        Note:
        Constructs API parameters based on provided values.
        """

        filters = []
        if 'branch' in values:
            filters.append(f'branch={values["branch"]}')
        if 'reference' in values:
            filters.append(f'ref={values["reference"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters
        return values


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
    target_url: Optional[str] = None
    description: Optional[str] = None
    coverage: Optional[Union[float, str]] = None
    pipeline_id: Optional[Union[int, str]] = None
    actions: Optional[list] = None
    start_branch: Optional[str] = None
    start_sha: Optional[str] = None
    start_project: Optional[Union[int, str]] = None
    author_email: Optional[str] = None
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

    @field_validator('dry_run', 'stats', 'force')
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

    @field_validator('commit_hash', 'branch', 'reference', 'name', 'context', 'note', 'path', 'line_type')
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

    @field_validator('coverage')
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

    @field_validator('state')
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
        if v is not None and v.lower() not in ['pending', 'running', 'success', 'failed', 'canceled']:
            raise ValueError("Invalid states")
        return v

    @field_validator('line_type')
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
        if v is not None and v.lower() not in ['new', 'old']:
            raise ValueError("Invalid line_type")
        return v

    @field_validator('report_type')
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
        if v is not None and v.lower() not in ['license_scanning', 'code_coverage']:
            raise ValueError("Invalid report_type")
        return v

    @field_validator('rule_type')
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
        if v is not None and v.lower() not in ['any_approver', 'regular']:
            raise ValueError("Invalid rule_type")
        return v

    @field_validator('user_ids', 'group_ids', 'protected_branch_ids')
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

    @field_validator("data")
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

        if 'branch' in values:
            data['branch'] = values.get("branch")
        if 'commit_message' in values:
            data['commit_message'] = values.get("commit_message")
        if 'start_branch' in values:
            data['start_branch'] = values.get("start_branch")
        if 'start_sha' in values:
            data['start_sha'] = values.get("start_sha")
        if 'start_project' in values:
            data['start_project'] = values.get("start_project")
        if 'actions' in values:
            data['actions'] = values.get("actions")
        if 'author_email' in values:
            data['author_email'] = values.get("author_email")
        if 'author_name' in values:
            data['author_name'] = values.get("author_name")
        if 'stats' in values:
            data['stats'] = values.get("stats")
        if 'force' in values:
            data['force'] = values.get("force")
        if 'note' in values:
            data['note'] = values.get("note")
        if 'path' in values:
            data['path'] = values.get("path")
        if 'line' in values:
            data['line'] = values.get("line")
        if 'line_type' in values:
            data['line_type'] = values.get("line_type")
        if 'state' in values:
            data['state'] = values.get("state")
        if 'reference' in values:
            data['ref'] = values.get("reference")
        if 'name' in values:
            data['name'] = values.get("name")
        if 'context' in values:
            data['context'] = values.get("context")
        if 'target_url' in values:
            data['target_url'] = values.get("target_url")
        if 'description' in values:
            data['description'] = values.get("description")
        if 'coverage' in values:
            data['coverage'] = values.get("coverage")
        if 'pipeline_id' in values:
            data['pipeline_id'] = values.get("pipeline_id")

        data = {k: v for k, v in data.items() if v is not None}

        values['data'] = data
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

    @field_validator('expires_at')
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

    @field_validator('project_id', 'group_id', 'token')
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
        if ('project_id' in values.lower() or 'group_id' in values.lower()) and v is not None:
            return v.lower()
        else:
            raise MissingParameterError

    @field_validator('name', 'username', 'scopes')
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

    @field_validator('scopes')
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
        valid_scopes = ['read_repository', 'read_registry', 'write_registry', 'read_package_registry',
                        'write_package_registry']
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
    argument: Optional[str] = 'state=opened'
    api_parameters: Optional[str] = ""

    @field_validator('per_page', 'page')
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
        if not isinstance(v, int) or v <= 0:
            raise ParameterError
        return v

    @field_validator('argument')
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

    @field_validator('group_id')
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

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters for the group.

        Args:
        - values: Dictionary of all values.

        Returns:
        - str: The constructed API parameters.

        Note:
        Constructs API parameters based on provided values.
        """
        filters = []
        if 'page' in values:
            filters.append(f'page={values["page"]}')
        if 'per_page' in values:
            filters.append(f'per_page={values["per_page"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters
        return values


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
    api_parameters: Optional[str] = ""

    @field_validator('per_page', 'page')
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
        if not isinstance(v, int) or v <= 0:
            raise ParameterError
        return v

    @field_validator('include_retried')
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

    @field_validator('scope')
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
        if v.lower() not in ['created', 'pending', 'running', 'failed', 'success', 'canceled', 'skipped',
                             'waiting_for_resource', 'manual']:
            raise ParameterError
        return v.lower()

    @field_validator('job_variable_attributes')
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
        if v is not None and (not isinstance(v, dict) or "job_variable_attributes" not in v.keys()):
            raise ParameterError
        return v

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters for the job.

        Args:
        - values: Dictionary of all values.

        Returns:
        - str: The constructed API parameters.

        Note:
        Constructs API parameters based on provided values.
        """
        filters = []
        if 'page' in values:
            filters.append(f'page={values["page"]}')
        if 'per_page' in values:
            filters.append(f'per_page={values["per_page"]}')
        if 'scope' in values:
            filters.append(f'scope[]={values["scope"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters
        return values


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
    api_parameters: Optional[str] = ""

    @field_validator('per_page', 'page')
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
        if not isinstance(v, int) or v <= 0:
            raise ParameterError
        return v

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters for members.

        Args:
        - values: Dictionary of all values.

        Returns:
        - str: The constructed API parameters.

        Note:
        Constructs API parameters based on provided values.
        """
        filters = []
        if 'page' in values:
            filters.append(f'page={values["page"]}')
        if 'per_page' in values:
            filters.append(f'per_page={values["per_page"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters
        return values


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
    api_parameters: Optional[str] = ""
    data: Optional[Dict] = None

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters for the merge request.

        Args:
        - values: Dictionary of all values.

        Returns:
        - str: The constructed API parameters.

        Note:
        Constructs API parameters based on provided values.
        """
        filters = []
        if 'approved_by_ids' in values:
            filters.append(f'approved_by_ids={values["approved_by_ids"]}')
        if 'approver_ids' in values:
            filters.append(f'approver_ids={values["approver_ids"]}')
        if 'assignee_id' in values:
            filters.append(f'assignee_id={values["assignee_id"]}')
        if 'author_id' in values:
            filters.append(f'author_id={values["author_id"]}')
        if 'author_username' in values:
            filters.append(f'author_username={values["author_username"]}')
        if 'created_after' in values:
            filters.append(f'created_after={values["created_after"]}')
        if 'deployed_after' in values:
            filters.append(f'deployed_after={values["deployed_after"]}')
        if 'deployed_before' in values:
            filters.append(f'deployed_before={values["deployed_before"]}')
        if 'environment' in values:
            filters.append(f'environment={values["environment"]}')
        if 'search_in' in values:
            filters.append(f'search_in={values["search_in"]}')
        if 'labels' in values:
            filters.append(f'labels={values["labels"]}')
        if 'milestone' in values:
            filters.append(f'milestone={values["milestone"]}')
        if 'my_reaction_emoji' in values:
            filters.append(f'my_reaction_emoji={values["my_reaction_emoji"]}')
        if 'search_exclude' in values:
            filters.append(f'search_exclude={values["search_exclude"]}')
        if 'order_by' in values:
            filters.append(f'order_by={values["order_by"]}')
        if 'reviewer_id' in values:
            filters.append(f'reviewer_id={values["reviewer_id"]}')
        if 'reviewer_username' in values:
            filters.append(f'reviewer_username={values["reviewer_username"]}')
        if 'scope' in values:
            filters.append(f'scope={values["scope"]}')
        if 'search' in values:
            filters.append(f'search={values["search"]}')
        if 'source_branch' in values:
            filters.append(f'source_branch={values["source_branch"]}')
        if 'state' in values:
            filters.append(f'state={values["state"]}')
        if 'target_branch' in values:
            filters.append(f'target_branch={values["target_branch"]}')
        if 'updated_after' in values:
            filters.append(f'updated_after={values["updated_after"]}')
        if 'updated_before' in values:
            filters.append(f'updated_before={values["updated_before"]}')
        if 'view' in values:
            filters.append(f'view={values["view"]}')
        if 'with_labels_details' in values:
            filters.append(f'with_labels_details={values["with_labels_details"]}')
        if 'with_merge_status_recheck' in values:
            filters.append(f'with_merge_status_recheck={values["with_merge_status_recheck"]}')
        if 'wip' in values:
            filters.append(f'wip={values["wip"]}')
        if 'with_merge_status_recheck' in values:
            filters.append(f'with_merge_status_recheck={values["with_merge_status_recheck"]}')
        if 'with_merge_status_recheck' in values:
            filters.append(f'with_merge_status_recheck={values["with_merge_status_recheck"]}')
        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters

        data = {}

        if 'source_branch' in values:
            data['source_branch'] = values.get("source_branch")
        if 'target_branch' in values:
            data['target_branch'] = values.get("target_branch")
        if 'title' in values:
            data['title'] = values.get("title")
        if 'allow_collaboration' in values:
            data['allow_collaboration'] = values.get("allow_collaboration")
        if 'allow_maintainer_to_push' in values:
            data['allow_maintainer_to_push'] = values.get("allow_maintainer_to_push")
        if 'approvals_before_merge' in values:
            data['approvals_before_merge'] = values.get("approvals_before_merge")
        if 'assignee_id' in values:
            data['assignee_id'] = values.get("assignee_id")
        if 'description' in values:
            data['description'] = values.get("description")
        if 'labels' in values:
            data['labels'] = values.get("labels")
        if 'milestone_id' in values:
            data['milestone_id'] = values.get("milestone_id")
        if 'remove_source_branch' in values:
            data['remove_source_branch'] = values.get("remove_source_branch")
        if 'reviewer_ids' in values:
            data['reviewer_ids'] = values.get("reviewer_ids")
        if 'squash' in values:
            data['squash'] = values.get("squash")
        if 'target_project_id' in values:
            data['target_project_id'] = values.get("target_project_id")

        data = {k: v for k, v in data.items() if v is not None}

        values['data'] = data
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
        valid_scopes = ['created_by_me', 'assigned_to_me', 'all']
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
        valid_search_in = ['title', 'description', 'title,description']
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
        valid_search_exclude = ['labels', 'milestone', 'author_id', 'assignee_id', 'author_username',
                                'reviewer_id', 'reviewer_username', 'my_reaction_emoji']
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

        valid_states = ['opened', 'closed', 'locked', 'merged']
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
        valid_sorts = ['asc', 'desc']
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
        valid_wip_values = ['yes', 'no']
        if value and value.lower() not in valid_wip_values:
            raise ValueError("Invalid wip value")
        return value.lower()

    @field_validator('source_branch', 'target_branch', 'title')
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

    @field_validator('allow_collaboration', 'allow_maintainer_to_push', 'squash')
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

    @field_validator('approvals_before_merge', 'assignee_id', 'milestone_id', 'target_project_id')
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
        if not isinstance(v, int) or v <= 0:
            raise ParameterError
        return v

    @field_validator('assignee_ids', 'reviewer_ids')
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
        if value not in ['license_scanning', 'code_coverage']:
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

        if value not in ['any_approver', 'regular']:
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

        if 'approvals_required' in values:
            data['approvals_required'] = values.get("approvals_required")
        if 'name' in values:
            data['name'] = values.get("name")
        if 'applies_to_all_protected_branches' in values:
            data['applies_to_all_protected_branches'] = values.get("applies_to_all_protected_branches")
        if 'group_ids' in values:
            data['group_ids'] = values.get("group_ids")
        if 'protected_branch_ids' in values:
            data['protected_branch_ids'] = values.get("protected_branch_ids")
        if 'report_type' in values:
            data['report_type'] = values.get("report_type")
        if 'rule_type' in values:
            data['rule_type'] = values.get("rule_type")
        if 'user_ids' in values:
            data['user_ids'] = values.get("user_ids")
        if 'usernames' in values:
            data['usernames'] = values.get("usernames")

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        values['data'] = data
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
    - build_api_parameters(values): Build API parameters.
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
    api_parameters: Optional[str] = ""

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        filters = []
        if 'status' in values:
            filters.append(f'status={values["status"]}')
        if 'per_page' in values:
            filters.append(f'per_page={values["per_page"]}')
        if 'reference' in values:
            filters.append(f'ref={values["reference"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters
        return values

    @field_validator('file_name', 'package_name')
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
        pattern = r'^[a-zA-Z0-9._-]+$'
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
        if value not in ['default', 'hidden']:
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
        if value not in ['package_file', 'package_file']:
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

    Methods:
    - build_api_parameters(values): Build API parameters.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """
    project_id: Union[int, str] = None
    per_page: Optional[int] = 100
    page: Optional[int] = 1
    pipeline_id: Optional[Union[int, str]] = None
    reference: Optional[str] = None
    variables: Optional[Dict] = None
    api_parameters: Optional[str] = ""

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        filters = []
        if 'page' in values:
            filters.append(f'page={values["page"]}')
        if 'per_page' in values:
            filters.append(f'per_page={values["per_page"]}')
        if 'reference' in values:
            filters.append(f'ref={values["reference"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters
        return values


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
    - ... (other attributes)

    Methods:
    - build_api_parameters(values): Build API parameters.
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
    import_url: Optional[str] = None
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
    api_parameters: Optional[str] = None
    data: Optional[Dict] = None

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        filters = []

        if 'group_id' in values:
            filters.append(f'group_id={values["group_id"]}')
        if 'group_access' in values:
            filters.append(f'group_access={values["group_access"]}')
        if 'expires_at' in values:
            filters.append(f'expires_at={values["expires_at"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters

        data = {}

        if 'allow_merge_on_skipped_pipeline' in values:
            data['allow_merge_on_skipped_pipeline'] = values.get("allow_merge_on_skipped_pipeline")
        if 'allow_pipeline_trigger_approve_deployment' in values:
            data['allow_pipeline_trigger_approve_deployment'] = values.get("allow_pipeline_trigger_approve_deployment")
        if 'only_allow_merge_if_all_status_checks_passed' in values:
            data['only_allow_merge_if_all_status_checks_passed'] = (
                values.get("only_allow_merge_if_all_status_checks_passed"))
        if 'analytics_access_level' in values:
            data['analytics_access_level'] = values.get("analytics_access_level")
        if 'approvals_before_merge' in values:
            data['approvals_before_merge'] = values.get("approvals_before_merge")
        if 'auto_cancel_pending_pipelines' in values:
            data['auto_cancel_pending_pipelines'] = values.get("auto_cancel_pending_pipelines")
        if 'auto_devops_deploy_strategy' in values:
            data['auto_devops_deploy_strategy'] = values.get("auto_devops_deploy_strategy")
        if 'auto_devops_enabled' in values:
            data['auto_devops_enabled'] = values.get("auto_devops_enabled")
        if 'autoclose_referenced_issues' in values:
            data['autoclose_referenced_issues'] = values.get("autoclose_referenced_issues")
        if 'avatar' in values:
            data['avatar'] = values.get("avatar")
        if 'build_git_strategy' in values:
            data['build_git_strategy'] = values.get("build_git_strategy")
        if 'build_timeout' in values:
            data['build_timeout'] = values.get("build_timeout")
        if 'builds_access_level' in values:
            data['builds_access_level'] = values.get("builds_access_level")
        if 'ci_config_path' in values:
            data['ci_config_path'] = values.get("ci_config_path")
        if 'container_registry_access_level' in values:
            data['container_registry_access_level'] = values.get("container_registry_access_level")
        if 'container_registry_enabled' in values:
            data['container_registry_enabled'] = values.get("container_registry_enabled")
        if 'default_branch' in values:
            data['default_branch'] = values.get("default_branch")
        if 'description' in values:
            data['description'] = values.get("description")
        if 'emails_disabled' in values:
            data['emails_disabled'] = values.get("emails_disabled")
        if 'emails_enabled' in values:
            data['emails_enabled'] = values.get("emails_enabled")
        if 'enforce_auth_checks_on_uploads' in values:
            data['enforce_auth_checks_on_uploads'] = values.get("enforce_auth_checks_on_uploads")
        if 'environments_access_level' in values:
            data['environments_access_level'] = values.get("environments_access_level")
        if 'external_authorization_classification_label' in values:
            data['external_authorization_classification_label'] = (
                values.get("external_authorization_classification_label"))
        if 'feature_flags_access_level' in values:
            data['feature_flags_access_level'] = values.get("feature_flags_access_level")
        if 'forking_access_level' in values:
            data['forking_access_level'] = values.get("forking_access_level")
        if 'group_runners_enabled' in values:
            data['group_runners_enabled'] = values.get("group_runners_enabled")
        if 'group_with_project_templates_id' in values:
            data['group_with_project_templates_id'] = values.get("group_with_project_templates_id")
        if 'import_url' in values:
            data['import_url'] = values.get("import_url")
        if 'infrastructure_access_level' in values:
            data['infrastructure_access_level'] = values.get("infrastructure_access_level")
        if 'initialize_with_readme' in values:
            data['initialize_with_readme'] = values.get("initialize_with_readme")
        if 'issue_branch_template' in values:
            data['issue_branch_template'] = values.get("issue_branch_template")
        if 'issues_access_level' in values:
            data['issues_access_level'] = values.get("issues_access_level")
        if 'issues_enabled' in values:
            data['issues_enabled'] = values.get("issues_enabled")
        if 'jobs_enabled' in values:
            data['jobs_enabled'] = values.get("jobs_enabled")
        if 'lfs_enabled' in values:
            data['lfs_enabled'] = values.get("lfs_enabled")
        if 'merge_commit_template' in values:
            data['merge_commit_template'] = values.get("merge_commit_template")
        if 'merge_method' in values:
            data['merge_method'] = values.get("merge_method")
        if 'merge_requests_access_level' in values:
            data['merge_requests_access_level'] = values.get("merge_requests_access_level")
        if 'merge_requests_enabled' in values:
            data['merge_requests_enabled'] = values.get("merge_requests_enabled")
        if 'mirror_trigger_builds' in values:
            data['mirror_trigger_builds'] = values.get("mirror_trigger_builds")
        if 'mirror' in values:
            data['mirror'] = values.get("mirror")
        if 'model_experiments_access_level' in values:
            data['model_experiments_access_level'] = values.get("model_experiments_access_level")
        if 'model_registry_access_level' in values:
            data['model_registry_access_level'] = values.get("model_registry_access_level")
        if 'monitor_access_level' in values:
            data['monitor_access_level'] = values.get("monitor_access_level")
        if 'namespace_id' in values:
            data['namespace_id'] = values.get("namespace_id")
        if 'only_allow_merge_if_all_discussions_are_resolved' in values:
            data['only_allow_merge_if_all_discussions_are_resolved'] = (
                values.get("only_allow_merge_if_all_discussions_are_resolved"))
        if 'only_allow_merge_if_all_status_checks_passed' in values:
            data['only_allow_merge_if_all_status_checks_passed'] = (
                values.get("only_allow_merge_if_all_status_checks_passed"))
        if 'only_allow_merge_if_pipeline_succeeds' in values:
            data['only_allow_merge_if_pipeline_succeeds'] = values.get("only_allow_merge_if_pipeline_succeeds")
        if 'packages_enabled' in values:
            data['packages_enabled'] = values.get("packages_enabled")
        if 'pages_access_level' in values:
            data['pages_access_level'] = values.get("pages_access_level")
        if 'path' in values:
            data['path'] = values.get("path")
        if 'printing_merge_request_link_enabled' in values:
            data['printing_merge_request_link_enabled'] = values.get("printing_merge_request_link_enabled")
        if 'public_builds' in values:
            data['public_builds'] = values.get("public_builds")
        if 'public_jobs' in values:
            data['public_jobs'] = values.get("public_jobs")
        if 'releases_access_level' in values:
            data['releases_access_level'] = values.get("releases_access_level")
        if 'repository_object_format' in values:
            data['repository_object_format'] = values.get("repository_object_format")
        if 'remove_source_branch_after_merge' in values:
            data['remove_source_branch_after_merge'] = values.get("remove_source_branch_after_merge")
        if 'repository_access_level' in values:
            data['repository_access_level'] = values.get("repository_access_level")
        if 'repository_storage' in values:
            data['repository_storage'] = values.get("repository_storage")
        if 'request_access_enabled' in values:
            data['request_access_enabled'] = values.get("request_access_enabled")
        if 'requirements_access_level' in values:
            data['requirements_access_level'] = values.get("requirements_access_level")
        if 'resolve_outdated_diff_discussions' in values:
            data['resolve_outdated_diff_discussions'] = values.get("resolve_outdated_diff_discussions")
        if 'security_and_compliance_access_level' in values:
            data['security_and_compliance_access_level'] = values.get("security_and_compliance_access_level")
        if 'shared_runners_enabled' in values:
            data['shared_runners_enabled'] = values.get("shared_runners_enabled")
        if 'show_default_award_emojis' in values:
            data['show_default_award_emojis'] = values.get("show_default_award_emojis")
        if 'snippets_access_level' in values:
            data['snippets_access_level'] = values.get("snippets_access_level")
        if 'snippets_enabled' in values:
            data['snippets_enabled'] = values.get("snippets_enabled")
        if 'squash_commit_template' in values:
            data['squash_commit_template'] = values.get("squash_commit_template")
        if 'squash_option' in values:
            data['squash_option'] = values.get("squash_option")
        if 'suggestion_commit_message' in values:
            data['suggestion_commit_message'] = values.get("suggestion_commit_message")
        if 'tag_list' in values:
            data['tag_list'] = values.get("tag_list")
        if 'template_name' in values:
            data['template_name'] = values.get("template_name")
        if 'topics' in values:
            data['topics'] = values.get("topics")
        if 'use_custom_template' in values:
            data['use_custom_template'] = values.get("use_custom_template")
        if 'visibility' in values:
            data['visibility'] = values.get("visibility")
        if 'warn_about_potentially_unwanted_characters' in values:
            data['warn_about_potentially_unwanted_characters'] = (
                values.get("warn_about_potentially_unwanted_characters"))
        if 'wiki_access_level' in values:
            data['wiki_access_level'] = values.get("wiki_access_level")
        if 'wiki_enabled' in values:
            data['wiki_enabled'] = values.get("wiki_enabled")

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        values['data'] = data

        return values

    @field_validator("analytics_access_level", "builds_access_level", "container_registry_access_level",
                     "forking_access_level", "issues_access_level", "operations_access_level", "pages_access_level",
                     "releases_access_level", "repository_access_level", "requirements_access_level",
                     "security_and_compliance_access_level", "snippets_access_level", "wiki_access_level")
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

        valid_access_levels = ['disabled', 'private', 'enabled']
        if value and value.lower() not in valid_access_levels:
            raise ValueError("Invalid access level value")
        return value.lower()

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

    @field_validator("approvals_before_merge", "build_timeout", "ci_default_git_depth", "mirror_user_id")
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
        if value.lower() not in ['id', 'name', 'username', 'created_at', 'updated_at']:
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
    - build_api_parameters(values): Build API parameters.
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
    api_parameters: Optional[str] = ""
    data: Optional[Dict] = None

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """

        filters = []
        if 'branch' in values:
            filters.append(f'name={values["branch"]}')
        if 'push_access_level' in values:
            filters.append(f'push_access_level={values["push_access_level"]}')
        if 'merge_access_level' in values:
            filters.append(f'merge_access_level={values["merge_access_level"]}')
        if 'unprotect_access_level' in values:
            filters.append(f'unprotect_access_level={values["unprotect_access_level"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters

        data = {}

        if 'allow_force_push' in values:
            data['allow_force_push'] = values.get("allow_force_push")
        if 'allowed_to_push' in values:
            data['allowed_to_push'] = values.get("allowed_to_push")
        if 'allowed_to_merge' in values:
            data['allowed_to_merge'] = values.get("allowed_to_merge")
        if 'allowed_to_unprotect' in values:
            data['allowed_to_unprotect'] = values.get("allowed_to_unprotect")
        if 'code_owner_approval_required' in values:
            data['code_owner_approval_required'] = values.get("code_owner_approval_required")

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        values['data'] = data
        return values

    @field_validator('allow_force_push', 'code_owner_approval_required')
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

    @field_validator('project_id')
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
            raise ValueError('Project ID cannot be None')
        return value

    @field_validator('project_id')
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
            raise ValueError('Project ID must be an integer or a string')
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
    - build_api_parameters(values): Build API parameters.
    - validate_order_by(value): Validate order_by attribute.
    - validate_sort(value): Validate sort attribute.
    - validate_project_id(value): Validate project ID for non-None.
    - validate_project_id_type(value): Validate project ID for type (int or str).
    - construct_data_dict(values): Construct data dictionary.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """

    project_id: Union[int, str]
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
    api_parameters: Optional[str] = None
    data: Optional[Dict] = None

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        filters = []

        if 'simple' in values:
            filters.append(f'simple={values["simple"]}'.lower())

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters

        data = {}

        if 'description' in values:
            data['name'] = values.get("description")
        if 'tag_name' in values:
            data['tag_name'] = values.get("tag_name")
        if 'tag_message' in values:
            data['tag_message'] = values.get("tag_message")
        if 'description' in values:
            data['description'] = values.get("description")
        if 'ref' in values:
            data['ref'] = values.get("reference")
        if 'milestones' in values:
            data['milestones'] = values.get("milestones")
        if 'assets:links' in values:
            data['assets:links'] = values.get("assets:links")
        if 'assets:links:name' in values:
            data['assets:links:name'] = values.get("assets:links:name")
        if 'assets:links:url' in values:
            data['assets:links:url'] = values.get("assets:links:url")
        if 'assets:links:direct_asset_path' in values:
            data['assets:links:direct_asset_path'] = values.get("assets:links:direct_asset_path")
        if 'released_at' in values:
            data['released_at'] = values.get("released_at")

        data = {k: v for k, v in data.items() if v is not None}

        values['data'] = data

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
        if value not in ['id', 'name', 'username', 'created_at', 'updated_at']:
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
        valid_sorts = ['asc', 'desc']
        if value and value not in valid_sorts:
            raise ValueError("Invalid sort value")
        return value

    @field_validator('project_id')
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
            raise ValueError('Project ID cannot be None')
        return value

    @field_validator('project_id')
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
            raise ValueError('Project ID must be an integer or a string')
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
    - build_api_parameters(values): Build API parameters.
    - validate_runner_type(value): Validate runner_type attribute.
    - validate_status(value): Validate status attribute.
    - construct_data_dict(values): Construct data dictionary.

    Examples:
    - Example 1: How to use this Pydantic model.
    - Example 2: Another example of usage.
    """
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
    api_parameters: Optional[str] = ""
    data: Optional[Dict] = None

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        filters = []
        if 'tag_list' in values:
            filters.append(f'tag_list={values["tag_list"].lower()}')
        if 'runner_type' in values:
            filters.append(f'runner_type={values["runner_type"].lower()}')
        if 'status' in values:
            filters.append(f'status={values["status"].lower()}')
        if 'paused' in values:
            filters.append(f'paused={values["paused"].lower()}')
        if 'all_runners' in values:
            filters = ['/all']

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters

        data = {}

        if 'description' in values:
            data['name'] = values.get("description")
        if 'active' in values:
            data['active'] = values.get("active")
        if 'paused' in values:
            data['paused'] = values.get("paused")
        if 'tag_list' in values:
            data['tag_list'] = values.get("tag_list")
        if 'run_untagged' in values:
            data['run_untagged'] = values.get("run_untagged")
        if 'locked' in values:
            data['locked'] = values.get("locked")
        if 'access_level' in values:
            data['access_level'] = values.get("access_level")
        if 'maximum_timeout' in values:
            data['maximum_timeout'] = values.get("maximum_timeout")
        if 'info' in values:
            data['info'] = values.get("info")
        if 'maintenance_note' in values:
            data['maintenance_note'] = values.get("maintenance_note")
        if 'token' in values:
            data['token'] = values.get("token")

        data = {k: v for k, v in data.items() if v is not None}

        values['data'] = data

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
        if value.lower() not in ['instance_type', 'group_type', 'project_type']:
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
        if value.lower() not in ['online', 'offline', 'stale', 'never_contacted', 'active', 'paused']:
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
    - build_api_parameters(values): Build API parameters.
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
    api_parameters: Optional[str] = ""

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """

        filters = []

        if 'username' in values:
            filters.append(f'username={values["username"]}'.lower())
        if 'active' in values:
            filters.append(f'active={values["active"]}'.lower())
        if 'blocked' in values:
            filters.append(f'blocked={values["blocked"]}'.lower())
        if 'external' in values:
            filters.append(f'external={values["external"]}'.lower())
        if 'exclude_internal' in values:
            filters.append(f'exclude_internal={values["exclude_internal"]}'.lower())
        if 'exclude_external' in values:
            filters.append(f'exclude_external={values["exclude_external"]}'.lower())
        if 'without_project_bots' in values:
            filters.append(f'without_project_bots={values["without_project_bots"]}'.lower())
        if 'order_by' in values:
            filters.append(f'order_by={values["order_by"]}'.lower())
        if 'sort' in values:
            filters.append(f'sort={values["sort"]}'.lower())
        if 'two_factor' in values:
            filters.append(f'two_factor={values["two_factor"]}'.lower())
        if 'without_projects' in values:
            filters.append(f'without_projects={values["without_projects"]}'.lower())
        if 'admins' in values:
            filters.append(f'admins={values["admins"]}'.lower())
        if 'saml_provider_id' in values:
            filters.append(f'saml_provider_id={values["saml_provider_id"]}'.lower())
        if 'extern_uid' in values:
            filters.append(f'extern_uid={values["extern_uid"]}'.lower())
        if 'provider' in values:
            filters.append(f'provider={values["provider"]}'.lower())
        if 'created_before' in values:
            filters.append(f'created_before={values["created_before"]}'.lower())
        if 'created_after' in values:
            filters.append(f'created_after={values["created_after"]}'.lower())
        if 'with_custom_attributes' in values:
            filters.append(f'with_custom_attributes={values["with_custom_attributes"]}'.lower())
        if 'sudo' in values:
            filters.append(f'sudo={values["user_id"]}'.lower())
        if 'user_id' in values:
            filters.append(f'user_id={values["user_id"]}'.lower())
        if 'page' in values:
            filters.append(f'page={values["page"]}'.lower())
        if 'per_page' in values:
            filters.append(f'per_page={values["per_page"]}'.lower())

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters

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
        if value.lower() not in ['id', 'name', 'username', 'created_at', 'updated_at']:
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
        valid_sorts = ['asc', 'desc']
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
        valid_two_factor = ['enabled', 'disabled']
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
    - build_api_parameters(values): Build API parameters.
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
    file: Optional[str] = None
    branch: Optional[str] = None
    api_parameters: Optional[str] = ""
    data: Optional[Dict] = None

    @model_validator(mode="before")
    def build_api_parameters(cls, values):
        """
        Build API parameters.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed API parameters string.

        Raises:
        - None.
        """
        filters = []

        if 'with_content' in values:
            filters.append(f'with_content={values["with_content"]}'.lower())

        if 'render_html' in values:
            filters.append(f'render_html={values["render_html"]}'.lower())

        if 'version' in values:
            filters.append(f'version={values["version"]}'.lower())

        if filters:
            api_parameters = "?" + "&".join(filters)
            values['api_parameters'] = api_parameters

        data = {}

        if 'content' in values:
            data['content'] = values.get("content")
        if 'title' in values:
            data['title'] = values.get("title")
        if 'format' in values:
            data['format'] = values.get("format")

        data = {k: v for k, v in data.items() if v is not None}

        values['data'] = data

        return values

    @field_validator('project_id')
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
            raise ValueError('Project ID cannot be None')
        return value

    @field_validator('project_id')
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
            raise ValueError('Project ID must be an integer or a string')
        return value
