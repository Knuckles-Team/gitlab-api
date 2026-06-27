#!/usr/bin/python

from typing import TypeVar

import requests
from agent_utilities.base_utilities import get_logger
from pydantic import ValidationError

logger = get_logger(__name__)

from agent_utilities.core.exceptions import (
    MissingParameterError,
    ParameterError,
)

from gitlab_api.gitlab_input_models import (
    DeployTokenModel,
    GroupModel,
    JobModel,
    MembersModel,
    MergeRequestModel,
    MergeRequestRuleModel,
    MergeRequestRuleSettingsModel,
    ProjectModel,
    RunnerModel,
)
from gitlab_api.gitlab_response_models import (
    ApprovalRule,
    DeployToken,
    Group,
    Job,
    Membership,
    MergeRequest,
    MergeRequestRuleSettings,
    Project,
    Response,
    Runner,
    User,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiProjects(GitLabApiBase):
    def get_project_deploy_tokens(self, **kwargs) -> Response:
        """
        Get deploy tokens for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of DeployToken models.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.project_id is None:
            raise MissingParameterError("project_id is required")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{deploy_token.project_id}/deploy_tokens",
                model=deploy_token,
                id_field="project_id",
                id_value=deploy_token.project_id,
            )
            parsed_data = [DeployToken(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to get project deploy tokens: {str(e)}"
            ) from e

    def get_project_deploy_token(self, **kwargs) -> Response:
        """
        Get a specific deploy token for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, deploy_token_id).

        Returns:
            Response: A wrapper containing the original response and a DeployToken model.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.project_id is None or deploy_token.deploy_token_id is None:  # type: ignore
            raise MissingParameterError("project_id and deploy_token_id are required")
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.deploy_token_id}",  # type: ignore
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = DeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get project deploy token: {str(e)}") from e

    def create_project_deploy_token(self, **kwargs) -> Response:
        """
        Create a deploy token for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name, scopes).

        Returns:
            Response: A wrapper containing the original response and a DeployToken model.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if (
            deploy_token.project_id is None
            or deploy_token.name is None
            or deploy_token.scopes is None
        ):
            raise MissingParameterError("project_id, name, and scopes are required")
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens",
                headers=self.headers,
                json=deploy_token.model_dump(exclude_none=True),
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = DeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to create project deploy token: {str(e)}"
            ) from e

    def delete_project_deploy_token(self, **kwargs) -> Response:
        """
        Delete a deploy token for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, deploy_token_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.project_id is None or deploy_token.deploy_token_id is None:  # type: ignore
            raise MissingParameterError("project_id and deploy_token_id are required")
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.deploy_token_id}",  # type: ignore
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to delete project deploy token: {str(e)}"
            ) from e

    def get_group_projects(self, **kwargs) -> Response:
        """
        Get projects associated with a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Project models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint="/groups/{id}/projects",
                model=group,
                id_field="group_id",
                id_value=group.group_id,
            )
            parsed_data = [Project(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_jobs(self, **kwargs) -> Response:
        """
        Get jobs associated with a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Job models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        job = JobModel(**kwargs)
        if job.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{job.project_id}/jobs",
                model=job,
                id_field="project_id",
                id_value=job.project_id,
            )
            parsed_data = [Job(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_job(self, **kwargs) -> Response:
        """
        Get details of a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_job_log(self, **kwargs) -> Response:
        """
        Get the log of a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and the raw job log data.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/trace",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.text
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def cancel_project_job(self, **kwargs) -> Response:
        """
        Cancel a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/cancel",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def retry_project_job(self, **kwargs) -> Response:
        """
        Retry a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/retry",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def erase_project_job(self, **kwargs) -> Response:
        """
        Erase a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/erase",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def run_project_job(self, **kwargs) -> Response:
        """
        Run a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/play",
                headers=self.headers,
                json=job.data,  # type: ignore
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_members(self, **kwargs) -> Response:
        """
        Get members of a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Membership models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        members = MembersModel(**kwargs)
        if members.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{members.project_id}/members",
                model=members,
                id_field="project_id",
                id_value=members.project_id,
            )
            parsed_data = [Membership(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_merge_requests(self, **kwargs) -> Response:
        """
        Get merge requests for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_request = MergeRequestModel(**kwargs)
        if merge_request.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{merge_request.project_id}/merge_requests",
                model=merge_request,
                id_field="project_id",
                id_value=merge_request.project_id,
            )
            parsed_data = [MergeRequest(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_merge_request(self, **kwargs) -> Response:
        """
        Get details of a specific merge request in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_request = MergeRequestModel(**kwargs)
        if merge_request.project_id is None or merge_request.merge_request_iid is None:  # type: ignore
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_request.project_id}/merge_requests/{merge_request.merge_request_iid}",  # type: ignore
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_level_merge_request_rules(self, **kwargs) -> Response:
        """
        Get project-level merge request approval rules.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of ApprovalRule models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{merge_rule.project_id}/approval_rules",
                model=merge_rule,
                id_field="project_id",
                id_value=merge_rule.project_id,
            )
            parsed_data = [ApprovalRule(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_level_merge_request_rule(self, **kwargs) -> Response:
        """
        Get details of a specific project-level merge request approval rule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, approval_rule_id).

        Returns:
            Response: A wrapper containing the original response and an ApprovalRule model.

        Raises:
            MissingParameterError: If the project_id or approval_rule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.approval_rule_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = ApprovalRule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_project_level_rule(self, **kwargs) -> Response:
        """
        Create a new project-level merge request approval rule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name, approvals_required).

        Returns:
            Response: A wrapper containing the original response and an ApprovalRule model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules",
                headers=self.headers,
                json=merge_rule.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = ApprovalRule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_project_level_rule(self, **kwargs) -> Response:
        """
        Update an existing project-level merge request approval rule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, approval_rule_id).

        Returns:
            Response: A wrapper containing the original response and an ApprovalRule model.

        Raises:
            MissingParameterError: If the project_id or approval_rule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.approval_rule_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
                json=merge_rule.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = ApprovalRule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_project_level_rule(self, **kwargs) -> Response:
        """
        Delete a project-level merge request approval rule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, approval_rule_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or approval_rule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.approval_rule_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_level_rule(self, **kwargs) -> Response:
        """
        Get details of a project-level merge request approval setting.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a MergeRequestRuleSettings model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule_setting = MergeRequestRuleSettingsModel(**kwargs)
        if merge_rule_setting.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule_setting.project_id}/merge_request_approval_setting",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequestRuleSettings(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def edit_project_level_rule(self, **kwargs) -> Response:
        """
        Edit a project-level merge request approval setting.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a MergeRequestRuleSettings model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule_setting = MergeRequestRuleSettingsModel(**kwargs)
        if merge_rule_setting.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{merge_rule_setting.project_id}/merge_request_approval_setting",
                headers=self.headers,
                json=merge_rule_setting.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequestRuleSettings(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_projects(self, **kwargs) -> Response:
        """
        Get information about projects.

        Args:
            **kwargs: Additional parameters for the request (e.g., owned, membership).

        Returns:
            Response: A wrapper containing the original response and a list of Project models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/projects",
                model=project,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Project(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project(self, **kwargs) -> Response:
        """
        Get information about a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_nested_projects_by_group(self, **kwargs) -> Response:
        """
        Get information about nested projects within a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, per_page).

        Returns:
            Response: A wrapper containing the original response and a list of Project models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        all_groups = []
        all_projects = []

        if project.group_id is None:
            raise MissingParameterError

        try:
            group_response = self.get_group(group_id=project.group_id)  # type: ignore
            all_groups.append(group_response.data)

            groups_response = self.get_group_descendant_groups(  # type: ignore
                group_id=project.group_id, per_page=project.per_page
            )
            all_groups.extend(groups_response.data)

            last_response = None
            for group in all_groups:
                response, data = self._fetch_all_pages(
                    endpoint=f"/groups/{group.id}/projects",
                    model=project,
                    id_field="group_id",
                    id_value=group.id,
                )
                parsed_data = [Project(**item) for item in data]
                all_projects.extend(parsed_data)
                last_response = response

            return Response(response=last_response, data=all_projects)  # type: ignore
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_contributors(self, **kwargs) -> Response:
        """
        Get information about contributors to a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of User models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/repository/contributors",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [User(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_statistics(self, **kwargs) -> Response:
        """
        Get statistics for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and the raw statistics data.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}?statistics=true",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_project(self, **kwargs) -> Response:
        """
        Create a new project.

        Args:
            **kwargs: GitLab POST /projects body fields. Common: name (required
                unless path given), path, namespace_id (group/user namespace),
                visibility ('private'|'internal'|'public'), description,
                initialize_with_readme. A flexible body is sent so any documented
                create field is accepted (ProjectModel does not cover namespace_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If neither name nor path is provided.
            ParameterError: If invalid parameters are provided.
        """
        if not kwargs.get("name") and not kwargs.get("path"):
            raise MissingParameterError
        body = {k: v for k, v in kwargs.items() if v is not None}
        try:
            response = self._session.post(
                url=f"{self.url}/projects",
                json=body,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def edit_project(self, **kwargs) -> Response:
        """
        Edit a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_groups(self, **kwargs) -> Response:
        """
        Get groups associated with a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/groups",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Group(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def archive_project(self, **kwargs) -> Response:
        """
        Archive a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/archive",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def unarchive_project(self, **kwargs) -> Response:
        """
        Unarchive a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/unarchive",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_project(self, **kwargs) -> Response:
        """
        Delete a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def share_project(self, **kwargs) -> Response:
        """
        Share a specific project with a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, group_id, group_access).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id, group_id, or group_access is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if (
            project.project_id is None
            or project.group_id is None
            or project.group_access is None
        ):
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/share",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_shared_project_link(self, **kwargs) -> Response:
        """
        Unshare a specific project from a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, group_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/share/{project.group_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_runners(self, **kwargs) -> Response:
        """
        Get information about runners in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Runner models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{runner.project_id}/runners",
                model=runner,
                id_field="project_id",
                id_value=runner.project_id,
            )
            parsed_data = [Runner(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def enable_project_runner(self, **kwargs) -> Response:
        """
        Enable a runner in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, runner_id).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the project_id or runner_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.project_id is None or runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{runner.project_id}/runners",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_project_runner(self, **kwargs) -> Response:
        """
        Delete a runner from a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, runner_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or runner_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.project_id is None or runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{runner.project_id}/runners/{runner.runner_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def reset_project_runner_token(self, **kwargs) -> Response:
        """
        Reset registration token for a project's runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and the raw token data.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{runner.project_id}/runners/reset_registration_token",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
