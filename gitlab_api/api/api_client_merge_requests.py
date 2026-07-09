#!/usr/bin/python

from typing import TypeVar

from agent_utilities.base_utilities import get_logger
from pydantic import ValidationError

logger = get_logger(__name__)

from agent_utilities.core.exceptions import (
    MissingParameterError,
    ParameterError,
)

from gitlab_api.gitlab_input_models import (
    GroupModel,
    MergeRequestModel,
    MergeRequestRuleModel,
)
from gitlab_api.gitlab_response_models import (
    ApprovalRule,
    MergeRequest,
    Response,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiMergeRequests(GitLabApiBase):
    def get_group_merge_requests(self, **kwargs) -> Response:
        """
        Get merge requests associated with a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint="/groups/{id}/merge_requests",
                model=group,
                id_field="group_id",
                id_value=group.group_id,
            )
            parsed_data = [MergeRequest(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_merge_request(self, **kwargs) -> Response:
        """
        Create a new merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, source_branch, target_branch, title).

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id, source_branch, target_branch, or title is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_request = MergeRequestModel(**kwargs)
        if (
            merge_request.project_id is None
            or merge_request.source_branch is None
            or merge_request.target_branch is None
            or merge_request.title is None
        ):
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_request.project_id}/merge_requests",
                headers=self.headers,
                json=merge_request.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_merge_requests(self, **kwargs) -> Response:
        """
        Get a list of merge requests.

        Args:
            **kwargs: Additional parameters for the request (e.g., state, scope).

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        merge_request = MergeRequestModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/merge_requests",
                model=merge_request,
                id_field=None,
                id_value=None,
            )
            parsed_data = [MergeRequest(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def merge_request_level_approvals(self, **kwargs) -> Response:
        """
        Get approvals for a specific merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and the raw approval data.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approvals",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_approval_state_merge_requests(self, **kwargs) -> Response:
        """
        Get the approval state of merge requests for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and the raw approval state data.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approval_state",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_merge_request_level_rules(self, **kwargs) -> Response:
        """
        Get merge request-level approval rules for a specific project and merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and a list of ApprovalRule models.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approval_rules",
                model=merge_rule,
                id_field="project_id",
                id_value=merge_rule.project_id,
            )
            parsed_data = [ApprovalRule(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def approve_merge_request(self, **kwargs) -> Response:
        """
        Approve a specific merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approve",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def accept_merge_request(self, **kwargs) -> Response:
        """
        Accept (merge) a merge request.

        Pass ``merge_when_pipeline_succeeds=True`` to set auto-merge (merge once
        the pipeline succeeds) rather than merging immediately. Optional body
        params: merge_commit_message, squash_commit_message, squash,
        should_remove_source_branch, sha.

        Args:
            **kwargs: project_id and merge_request_iid (required) plus optional
                merge parameters listed above.

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        payload = {
            key: kwargs[key]
            for key in (
                "merge_commit_message",
                "squash_commit_message",
                "squash",
                "should_remove_source_branch",
                "merge_when_pipeline_succeeds",
                "sha",
            )
            if key in kwargs
        }
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/merge",
                headers=self.headers,
                json=payload or None,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def cancel_merge_when_pipeline_succeeds(self, **kwargs) -> Response:
        """
        Cancel a merge request's queued "merge when pipeline succeeds" (auto-merge).

        Args:
            **kwargs: project_id and merge_request_iid (required).

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/cancel_merge_when_pipeline_succeeds",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def unapprove_merge_request(self, **kwargs) -> Response:
        """
        Unapprove a specific merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/unapprove",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
