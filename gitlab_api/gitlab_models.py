from typing import Union, List, Dict
from pydantic import BaseModel, field_validator
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

    Notes:
        This model includes a validator `validate_required_parameters` to ensure that the `project_id` field is
        provided when either `branch` or `reference` is specified.
    """
    project_id: Union[int, str]
    branch: str = None
    reference: str = None

    @field_validator('branch', 'reference')
    def validate_required_parameters(cls, v, values):
        """
        Validator to ensure that `project_id` is provided when either `branch` or `reference` is specified.

        Args:
            v (str): The value of the current field being validated.
            values (dict): The values of all fields in the model.

        Raises:
            ValueError: If `project_id` is missing or `None` when either `branch` or `reference` is specified.
        """
        if 'project_id' in values and values['project_id'] is not None and v is not None:
            return v
        else:
            raise ValueError("Missing project_id field, it is required")


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
    data: Dict = None

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

    @field_validator('project_id', 'commit_hash', 'branch', 'start_branch', 'start_sha', 'start_project',
                     'pipeline_id', 'line')
    def validate_optional_parameters(cls, v, values):
        """
        Validate optional parameters to ensure they are provided only when 'project_id' is not None.

        Args:
        - v: The value of the parameter.
        - values: Dictionary of all values.

        Returns:
        - Any: The validated parameter value.

        Raises:
        - ValueError: If the parameter is provided and 'project_id' is None.
        """
        if 'project_id' in values and values['project_id'] is not None and v is not None:
            return v
        else:
            raise ValueError("Invalid optional params")

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
        if v is not None and v not in ['pending', 'running', 'success', 'failed', 'canceled']:
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
        if v is not None and v not in ['new', 'old']:
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
        if v is not None and v not in ['license_scanning', 'code_coverage']:
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
        if v is not None and v not in ['any_approver', 'regular']:
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
    group_id: Union[int, str] = None
    token: str = None
    name: str = None
    expires_at: str = None
    username: str = None
    scopes: str = None

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
        if ('project_id' in values or 'group_id' in values) and v is not None:
            return v
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
        if v is not None and v not in valid_scopes:
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
    per_page: int = 100
    page: int = 1
    argument: str = 'state=opened'
    api_parameters: str = None

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

    @field_validator("api_parameters")
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

        if values.get("page") is not None:
            filters.append(f'page={values["page"]}')

        if values.get("per_page") is not None:
            filters.append(f'per_page={values["per_page"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None


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
    scope: List[str] = None
    per_page: int = 100
    page: int = 1
    include_retried: bool = None
    job_variable_attributes: Dict = None
    api_parameters: str = None

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
        if v not in ['created', 'pending', 'running', 'failed', 'success', 'canceled', 'skipped',
                     'waiting_for_resource', 'manual']:
            raise ParameterError
        return v

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

    @field_validator("api_parameters")
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

        if values.get("page") is not None:
            filters.append(f'page={values["page"]}')

        if values.get("per_page") is not None:
            filters.append(f'per_page={values["per_page"]}')

        if values.get("scope") is not None:
            filters.append(f'scope[]={values["scope"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None


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
    group_id: Union[int, str] = None
    project_id: Union[int, str] = None
    per_page: int = 100
    page: int = 1
    api_parameters: str = None

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

    @field_validator("api_parameters")
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

        if values.get("page") is not None:
            filters.append(f'page={values["page"]}')

        if values.get("per_page") is not None:
            filters.append(f'per_page={values["per_page"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None


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
    project_id: Union[int, str] = None
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
    title: str
    allow_collaboration: bool = None
    allow_maintainer_to_push: bool = None
    approvals_before_merge: int = None
    assignee_ids: List[int] = None
    description: str = None
    milestone_id: int = None
    remove_source_branch: str = None
    reviewer_ids: List[int] = None
    squash: bool = None
    target_project_id: Union[int, str] = None
    max_pages: int = 0
    per_page: int = 100
    api_parameters: str = None
    data: Dict = None

    @field_validator("api_parameters")
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
        if value and not all(scope in valid_scopes for scope in value):
            raise ValueError("Invalid scope values")
        return value

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
        if value and value not in valid_search_in:
            raise ValueError("Invalid search_in value")
        return value

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
        if value and value not in valid_search_exclude:
            raise ValueError("Invalid search_exclude value")
        return value

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
        if value and value not in valid_states:
            raise ValueError("Invalid state value")
        return value

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
        if value and value not in valid_sorts:
            raise ValueError("Invalid sort value")
        return value

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
        if value and value not in valid_wip_values:
            raise ValueError("Invalid wip value")
        return value

    @field_validator('project_id', 'source_branch', 'target_branch', 'title')
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

    @field_validator("data")
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
        data = {
            "source_branch": values.get("source_branch"),
            "target_branch": values.get("target_branch"),
            "title": values.get("title"),
            "allow_collaboration": values.get("allow_collaboration"),
            "allow_maintainer_to_push": values.get("allow_maintainer_to_push"),
            "approvals_before_merge": values.get("approvals_before_merge"),
            "assignee_id": values.get("assignee_id"),
            "description": values.get("description"),
            "labels": values.get("labels"),
            "milestone_id": values.get("milestone_id"),
            "remove_source_branch": values.get("remove_source_branch"),
            "reviewer_ids": values.get("reviewer_ids"),
            "squash": values.get("squash"),
            "target_project_id": values.get("target_project_id"),
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if not data:
            raise ValueError("At least one key is required in the data dictionary.")

        return data


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
    project_id: Union[int, str] = None
    approval_rule_id: Union[int, str] = None
    approvals_required: int = None
    name: str = None
    applies_to_all_protected_branches: bool = None
    group_ids: List[int] = None
    merge_request_iid: Union[int, str] = None
    protected_branch_ids: List[int] = None
    report_type: str = None
    rule_type: str = None
    user_ids: List[int] = None
    data: Dict = None

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

    @field_validator("data")
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
    package_name: str = None
    package_version: str = None
    file_name: str = None
    status: str = None
    select: str = None
    api_parameters: str = None

    @field_validator("api_parameters")
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

        if values.get("status") is not None:
            filters.append(f'status={values["status"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None

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
    per_page: int = 100
    page: int = 1
    pipeline_id: Union[int, str] = None
    reference: str = None
    variables: Dict = None
    api_parameters: str = None

    @field_validator("api_parameters")
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

        if values.get("page") is not None:
            filters.append(f'page={values["page"]}')

        if values.get("per_page") is not None:
            filters.append(f'per_page={values["per_page"]}')

        if values.get("ref") is not None:
            filters.append(f'ref={values["reference"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None


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
    project_id: Union[int, str]
    group_id: Union[int, str] = None
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
    expires_at: str = None
    forking_access_level: str = None
    group_acces: int = None
    import_url: str = None
    issues_access_level: str = None
    issues_template: str = None
    keep_latest_artifact: bool = None
    lfs_enabled: bool = None
    max_pages: int = 0
    per_page: int = 100
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
    order_by: str = None
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
    api_parameters: str = None
    data: Dict = None

    @field_validator("api_parameters")
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

        if values.get("group_id") is not None:
            filters.append(f'group_id={values["group_id"]}')

        if values.get("group_access") is not None:
            filters.append(f'group_access={values["group_access"]}')

        if values.get("expires_at") is not None:
            filters.append(f'expires_at={values["expires_at"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None

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
        if value not in ['id', 'name', 'username', 'created_at', 'updated_at']:
            raise ValueError("Invalid order_by")
        return value


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
    push_access_level: int
    merge_access_level: int
    unprotect_access_level: int
    allow_force_push: List[str]
    allowed_to_push: List[str]
    allowed_to_merge: List[str]
    allowed_to_unprotect: List[str]
    code_owner_approval_required: bool
    api_parameters: str = None
    data: Dict = None

    @field_validator("api_parameters")
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

        if values.get("branch") is not None:
            filters.append(f'name={values["branch"]}')

        if values.get("push_access_level") is not None:
            filters.append(f'push_access_level={values["push_access_level"]}')

        if values.get("merge_access_level") is not None:
            filters.append(f'merge_access_level={values["merge_access_level"]}')

        if values.get("unprotect_access_level") is not None:
            filters.append(f'unprotect_access_level={values["unprotect_access_level"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None

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

    @field_validator("data")
    def construct_data_dict(cls, values):
        """
        Construct data dictionary.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed data dictionary.

        Raises:
        - ValueError: If no key is present in the data dictionary.
        """
        data = {
            "allow_force_push": values.get("allow_force_push"),
            "allowed_to_push": values.get("allowed_to_push"),
            "allowed_to_merge": values.get("allowed_to_merge"),
            "allowed_to_unprotect": values.get("allowed_to_unprotect"),
            "code_owner_approval_required": values.get("code_owner_approval_required"),
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if not data:
            raise ValueError("At least one key is required in the data dictionary.")

        return data


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
    order_by: str = None
    sort: str = None
    simple: bool = None
    include_html_description: bool = None
    tag_name: str = None
    description: str = None
    tag_message: str = None
    ref: str = None
    direct_asset_path: str = None
    name: List[str] = None
    milestones: str = None
    released_at: str = None
    api_parameters: str = None
    data: Dict = None

    @field_validator("api_parameters")
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

        if values.get("simple") is not None:
            filters.append(f'simple=true')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None

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

    @field_validator("data")
    def construct_data_dict(cls, values):
        """
        Construct data dictionary.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed data dictionary.

        Raises:
        - ValueError: If no key is present in the data dictionary.
        """
        data = {
            "name": values.get("description"),
            "tag_name": values.get("tag_name"),
            "tag_message": values.get("tag_message"),
            "description": values.get("description"),
            "ref": values.get("ref"),
            "milestones": values.get("milestones"),
            "assets:links": values.get("assets:links"),
            "assets:links:name": values.get("assets:links:name"),
            "assets:links:url": values.get("assets:links:url"),
            "assets:links:direct_asset_path": values.get("assets:links:direct_asset_path"),
            "released_at": values.get("released_at"),
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if not data:
            raise ValueError("At least one key is required in the data dictionary.")

        return data


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
    description: str = None
    active: bool = None
    paused: bool = None
    tag_list: List[str] = None
    run_untagged: bool = None
    locked: bool = None
    access_level: str = None
    maintenance_note: str = None
    info: str = None
    token: str = None
    project_id: Union[int, str] = None
    group_id: Union[int, str] = None
    maximum_timeout: int = None
    runner_type: str = None
    status: str = None
    all_runners: bool = False
    api_parameters: str = None
    data: Dict = None

    @field_validator("api_parameters")
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

        if values.get("tag_list") is not None:
            filters.append(f'tag_list={values["tag_list"]}')

        if values.get("runner_type") is not None:
            filters.append(f'runner_type={values["runner_type"]}')

        if values.get("status") is not None:
            filters.append(f'status={values["status"]}')

        if values.get("paused") is not None:
            filters.append(f'paused={values["paused"]}')

        if values.get("tag_list") is not None:
            filters.append(f'tag_list={values["tag_list"]}')

        if values.get("all_runners"):
            filters = ['/all']

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None

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
        if value not in ['instance_type', 'group_type', 'project_type']:
            raise ValueError("Invalid runner_type")
        return value

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
        if value not in ['online', 'offline', 'stale', 'never_contacted', 'active', 'paused']:
            raise ValueError("Invalid status")
        return value

    @field_validator("data")
    def construct_data_dict(cls, values):
        """
        Construct data dictionary.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed data dictionary.

        Raises:
        - ValueError: If no key is present in the data dictionary.
        """
        data = {
            "description": values.get("description"),
            "active": values.get("active"),
            "paused": values.get("paused"),
            "tag_list": values.get("tag_list"),
            "run_untagged": values.get("run_untagged"),
            "locked": values.get("locked"),
            "access_level": values.get("access_level"),
            "maximum_timeout": values.get("maximum_timeout"),
            "info": values.get("info"),
            "maintenance_note": values.get("maximum_timeout"),
            "token": values.get("token"),
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if not data:
            raise ValueError("At least one key is required in the data dictionary.")

        return data


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
    username: str = None
    active: bool = None
    blocked: bool = None
    external: bool = None
    exclude_internal: bool = None
    exclude_external: bool = None
    without_project_bots: bool = None
    extern_uid: str = None
    provider: str = None
    created_before: str = None
    created_after: str = None
    with_custom_attributes: str = None
    sort: str = None
    order_by: str = None
    two_factor: str = None
    without_projects: bool = None
    admins: bool = None
    saml_provider_id: str = None
    max_pages: int = 0
    page: int = 1
    per_page: int = 100
    sudo: bool = False
    user_id: Union[str, int] = None
    api_parameters: str = None

    @field_validator("api_parameters")
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

        if values.get("username") is not None:
            filters.append(f'username={values["username"]}')

        if values.get("active") is not None:
            filters.append(f'active={values["active"]}')

        if values.get("blocked") is not None:
            filters.append(f'blocked={values["blocked"]}')

        if values.get("external") is not None:
            filters.append(f'external={values["external"]}')

        if values.get("exclude_internal") is not None:
            filters.append(f'exclude_internal={values["exclude_internal"]}')

        if values.get("exclude_external") is not None:
            filters.append(f'exclude_external={values["exclude_external"]}')

        if values.get("without_project_bots") is not None:
            filters.append(f'without_project_bots={values["without_project_bots"]}')

        if values.get("order_by") is not None:
            filters.append(f'order_by={values["order_by"]}')

        if values.get("sort") is not None:
            filters.append(f'sort={values["sort"]}')

        if values.get("two_factor") is not None:
            filters.append(f'two_factor={values["two_factor"]}')

        if values.get("without_projects") is not None:
            filters.append(f'without_projects={values["without_projects"]}')

        if values.get("admins") is not None:
            filters.append(f'admins={values["admins"]}')

        if values.get("saml_provider_id") is not None:
            filters.append(f'saml_provider_id={values["saml_provider_id"]}')

        if values.get("extern_uid") is not None:
            filters.append(f'extern_uid={values["extern_uid"]}')

        if values.get("provider") is not None:
            filters.append(f'provider={values["provider"]}')

        if values.get("created_before") is not None:
            filters.append(f'created_before={values["created_before"]}')

        if values.get("created_after") is not None:
            filters.append(f'created_after={values["created_after"]}')

        if values.get("with_custom_attributes") is not None:
            filters.append(f'with_custom_attributes={values["with_custom_attributes"]}')

        if values.get("sudo") is not None:
            filters.append(f'sudo={values["user_id"]}')
        elif values.get("user_id") is not None:
            filters.append(f'{values["user_id"]}')

        if values.get("page") is not None:
            filters.append(f'page={values["page"]}')

        if values.get("per_page") is not None:
            filters.append(f'per_page={values["per_page"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None

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
        if value and value not in valid_two_factor:
            raise ValueError("Invalid two_factor value")
        return value


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
    slug: str = None
    content: str = None
    title: str = None
    format_type: str = None
    with_content: bool = None
    file: str = None
    branch: str = None
    api_parameters: str = None
    data: Dict = None

    @field_validator("api_parameters")
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

        if values.get("with_content") is not None:
            filters.append(f'with_content={values["1"]}')

        if values.get("render_html") is not None:
            filters.append(f'render_html={values["1"]}')

        if values.get("version") is not None:
            filters.append(f'version={values["version"]}')

        if filters:
            api_parameters = "?" + "&".join(filters)
            return api_parameters

        return None

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

    @field_validator("data")
    def construct_data_dict(cls, values):
        """
        Construct data dictionary.

        Args:
        - values: Dictionary of values.

        Returns:
        - The constructed data dictionary.

        Raises:
        - ValueError: If no key is present in the data dictionary.
        """
        data = {
            "content": values.get("content"),
            "title": values.get("title"),
            "format": values.get("format"),
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        if not data:
            raise ValueError("At least one key is required in the data dictionary.")

        return data
