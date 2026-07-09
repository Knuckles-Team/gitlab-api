#!/usr/bin/python

from typing import TypeVar

from agent_utilities.base_utilities import get_logger

logger = get_logger(__name__)


T = TypeVar("T")

from gitlab_api.api.api_client_environments import GitLabApiEnvironments
from gitlab_api.api.api_client_issues import GitLabApiIssues
from gitlab_api.api.api_client_merge_requests import GitLabApiMergeRequests
from gitlab_api.api.api_client_other import GitLabApiOther
from gitlab_api.api.api_client_pipelines import GitLabApiPipelines
from gitlab_api.api.api_client_projects import GitLabApiProjects
from gitlab_api.api.api_client_repositories import GitLabApiRepositories
from gitlab_api.api.api_client_system import GitLabApiSystem
from gitlab_api.api.api_client_users_groups import GitLabApiUsersGroups
from gitlab_api.api.api_client_vulnerabilities import GitLabApiVulnerabilities


class Api(
    GitLabApiSystem,
    GitLabApiProjects,
    GitLabApiRepositories,
    GitLabApiIssues,
    GitLabApiMergeRequests,
    GitLabApiPipelines,
    GitLabApiUsersGroups,
    GitLabApiEnvironments,
    GitLabApiVulnerabilities,
    GitLabApiOther,
):
    __slots__ = ()
