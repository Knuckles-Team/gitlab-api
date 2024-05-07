#!/usr/bin/python
# coding: utf-8

import json
import requests
import urllib3
from base64 import b64encode
from typing import Union
from pydantic import ValidationError

try:
    from gitlab_api.gitlab_models import (BranchModel, CommitModel, DeployTokenModel, GroupModel, JobModel,
                                          MembersModel, PackageModel, PipelineModel, ProjectModel, ProtectedBranchModel,
                                          MergeRequestModel, MergeRequestRuleModel, ReleaseModel, RunnerModel,
                                          UserModel, WikiModel)
except ModuleNotFoundError:
    from gitlab_models import (BranchModel, CommitModel, DeployTokenModel, GroupModel, JobModel, MembersModel,
                               PackageModel, PipelineModel, ProjectModel, ProtectedBranchModel, MergeRequestModel,
                               MergeRequestRuleModel, ReleaseModel, RunnerModel, UserModel, WikiModel)
try:
    from gitlab_api.decorators import require_auth
except ModuleNotFoundError:
    from decorators import require_auth
try:
    from gitlab_api.exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)
except ModuleNotFoundError:
    from exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)


class Api(object):

    def __init__(self, url: str = None, username: str = None, password: str = None, token: str = None,
                 verify: bool = True):
        if url is None:
            raise MissingParameterError

        self._session = requests.Session()
        self.url = url
        self.headers = None
        self.verify = verify

        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self.headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        elif username and password:
            user_pass = f'{username}:{password}'.encode()
            user_pass_encoded = b64encode(user_pass).decode()
            self.headers = {
                'Authorization': f'Basic {user_pass_encoded}',
                'Content-Type': 'application/json'
            }
        else:
            raise MissingParameterError

        response = self._session.get(url=f'{self.url}/projects', headers=self.headers, verify=self.verify)

        if response.status_code == 403:
            raise UnauthorizedError
        elif response.status_code == 401:
            raise AuthError
        elif response.status_code == 404:
            raise ParameterError

    ####################################################################################################################
    #                                                 Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_branches(self, **kwargs):
        """
        Retrieve information about branches in a project.

        Args:
            **kwargs: Additional keyword arguments to initialize the BranchModel.

        Returns:
            Response: The response object from the GET request.

        Raises:
            ParameterError: If the provided parameters are invalid based on the BranchModel.
        """
        branch = BranchModel(**kwargs)
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{branch.project_id}/repository/branches',
                headers=self.headers,
                verify=self.verify)

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_branch(self, **kwargs):
        """
        Retrieve information about a specific branch in a project.

        Args:
            **kwargs: Additional keyword arguments to initialize the BranchModel.

        Returns:
            Response: The response object from the GET request.

        Raises:
            ParameterError: If the provided parameters are invalid based on the BranchModel.
        """
        branch = BranchModel(**kwargs)
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{branch.project_id}/repository/branches/{branch.branch}',
                headers=self.headers,
                verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_branch(self, **kwargs):
        """
        Create a new branch in a project.

        Args:
            **kwargs: Additional keyword arguments to initialize the BranchModel.

        Returns:
            Response: The response object from the POST request.

        Raises:
            ParameterError: If the provided parameters are invalid based on the BranchModel.
        """
        branch = BranchModel(**kwargs)
        try:
            response = self._session.post(
                url=f'{self.url}/projects/{branch.project_id}/repository/branches{branch.api_parameters}',
                headers=self.headers,
                verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_branch(self, **kwargs):
        """
        Delete a specific branch in a project.

        Args:
            **kwargs: Additional keyword arguments to initialize the BranchModel.

        Returns:
            Response: The response object from the DELETE request.

        Raises:
            ParameterError: If the provided parameters are invalid based on the BranchModel.
        """
        branch = BranchModel(**kwargs)
        try:
            response = self._session.delete(url=f'{self.url}/projects/{branch.project_id}'
                                            f'/repository/branches?branch={branch.branch}',
                                            headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_merged_branches(self, **kwargs):
        """
        Delete merged branches in a project.

        Args:
            **kwargs: Additional keyword arguments to initialize the BranchModel.

        Returns:
            Response: The response object from the DELETE request.

        Raises:
            ParameterError: If the provided parameters are invalid based on the BranchModel.
        """
        branch = BranchModel(**kwargs)
        try:
            response = self._session.delete(url=f'{self.url}/projects/{branch.project_id}'
                                            f'/repository/merged_branches',
                                            headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                 Commits API                                                      #
    ####################################################################################################################
    @require_auth
    def get_commits(self, **kwargs):
        """
        Get commits.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit(self, **kwargs):
        """
        Get a specific commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_references(self, **kwargs):
        """
        Get references of a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/refs',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def cherry_pick_commit(self, **kwargs):
        """
        Cherry-pick a commit into a new branch.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}/projects/{commit.project_id}'
                                          f'/repository/commits/{commit.commit_hash}/cherry_pick',
                                          headers=self.headers,
                                          data=json.dumps(commit.data, indent=2),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_commit(self, **kwargs):
        """
        Create a new commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}/projects/{commit.project_id}'
                                          f'/repository/commits',
                                          headers=self.headers,
                                          data=json.dumps(commit.data, indent=2),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def revert_commit(self, **kwargs):
        """
        Revert a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}/projects/{commit.project_id}'
                                          f'/repository/commits/{commit.commit_hash}/revert',
                                          headers=self.headers,
                                          data=json.dumps(commit.data, indent=2),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_diff(self, **kwargs):
        """
        Get the diff of a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/diff',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_comments(self, **kwargs):
        """
        Get comments on a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/comments',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_commit_comment(self, **kwargs):
        """
        Create a comment on a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}/projects/{commit.project_id}'
                                          f'/repository/commits/{commit.commit_hash}/comments',
                                          headers=self.headers,
                                          data=json.dumps(commit.data, indent=2),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_discussions(self, **kwargs):
        """
        Get discussions on a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/discussions',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_statuses(self, **kwargs):
        """
        Get statuses of a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/statuses',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def post_build_status_to_commit(self, **kwargs):
        """
        Post build status to a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}/projects/{commit.project_id}'
                                          f'/statuses/{commit.commit_hash}/',
                                          headers=self.headers,
                                          data=json.dumps(commit.data, indent=2),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_merge_requests(self, **kwargs):
        """
        Get merge requests associated with a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{commit.project_id}'
                f'/repository/commits/{commit.commit_hash}/merge_requests',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_gpg_signature(self, **kwargs):
        """
        Get GPG signature of a commit.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{commit.project_id}'
                f'/repository/commits/{commit.commit_hash}/merge_requests',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                Deploy Tokens API                                                 #
    ####################################################################################################################
    @require_auth
    def get_deploy_tokens(self):
        """
        Get all deploy tokens.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """

        try:
            response = self._session.get(url=f'{self.url}/deploy_tokens', headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_deploy_tokens(self, **kwargs):
        """
        Get deploy tokens for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        deploy_token = DeployTokenModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{deploy_token.project_id}/deploy_tokens',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_deploy_token(self, **kwargs):
        """
        Get a specific deploy token for a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        deploy_token = DeployTokenModel(**kwargs)
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.token}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_project_deploy_token(self, **kwargs):
        """
        Create a deploy token for a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.project_id is None or deploy_token.name is None or deploy_token.scopes is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{deploy_token.project_id}/deploy_tokens',
                                          headers=self.headers,
                                          data=json.dumps(deploy_token.model_dump(exclude_none=True), indent=4),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_project_deploy_token(self, **kwargs):
        """
        Delete a deploy token for a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.project_id is None or deploy_token.token is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f'{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.token}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_deploy_tokens(self, **kwargs):
        """
        Get deploy tokens for a specific group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/groups/{deploy_token.group_id}/deploy_tokens',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_deploy_token(self, **kwargs):
        """
        Get a specific deploy token for a group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None or deploy_token.token is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/groups/'
                                         f'{deploy_token.group_id}/deploy_tokens/{deploy_token.token}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_group_deploy_token(self, **kwargs):
        """
        Create a deploy token for a group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        deploy_token_dict = deploy_token.model_dump(exclude_none=True)
        if deploy_token.group_id is None or deploy_token.name is None or deploy_token.scopes is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/groups/{deploy_token.group_id}/deploy_tokens',
                                          headers=self.headers, data=json.dumps(deploy_token_dict, indent=4),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_group_deploy_token(self, **kwargs):
        """
        Delete a deploy token for a group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None or deploy_token.token is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f'{self.url}/groups/{deploy_token.group_id}/deploy_tokens/{deploy_token.token}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                Groups API                                                        #
    ####################################################################################################################
    @require_auth
    def get_groups(self, **kwargs):
        """
        Get a list of groups.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups{group.api_parameters}', headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group(self, **kwargs):
        """
        Get details of a specific group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups/{group.group_id}', headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_subgroups(self, **kwargs):
        """
        Get subgroups of a specific group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups/{group.group_id}'
                                         f'/subgroups', headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_descendant_groups(self, **kwargs):
        """
        Get descendant groups of a specific group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups/{group.group_id}'
                                         f'/descendant_groups',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_projects(self, **kwargs):
        """
        Get projects associated with a specific group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups/{group.group_id}'
                                         f'/projects{group.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_merge_requests(self, **kwargs):
        """
        Get merge requests associated with a specific group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None or group.argument is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups/{group.group_id}'
                                         f'/merge_requests{group.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                Jobs API                                                          #
    ####################################################################################################################
    @require_auth
    def get_project_jobs(self, **kwargs):
        """
        Get jobs associated with a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        job = JobModel(**kwargs)
        if job.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{job.project_id}/jobs{job.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_job(self, **kwargs):
        """
        Get details of a specific job within a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """

        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_job_log(self, **kwargs):
        """
        Get the log of a specific job within a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/trace',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def cancel_project_job(self, **kwargs):
        """
        Cancel a specific job within a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/cancel',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def retry_project_job(self, **kwargs):
        """
        Retry a specific job within a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/retry',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def erase_project_job(self, **kwargs):
        """
        Erase a specific job within a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/erase',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def run_project_job(self, **kwargs):
        """
        Run a specific job within a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """

        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/play',
                                          headers=self.headers, data=json.dumps(job.data, indent=2), verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_pipeline_jobs(self, **kwargs):
        """
        Get jobs associated with a specific pipeline within a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.pipeline_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{job.project_id}/pipelines/{job.pipeline_id}/jobs{job.api_parameters}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                               Members API                                                        #
    ####################################################################################################################
    @require_auth
    def get_group_members(self, **kwargs):
        """
        Get members of a specific group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        members = MembersModel(**kwargs)
        if members.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/groups/{members.group_id}/members{members.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_members(self, **kwargs):
        """
        Get members of a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        members = MembersModel(**kwargs)
        if members.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{members.project_id}/members{members.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                            Merge Request API                                                     #
    ####################################################################################################################
    @require_auth
    def create_merge_request(self, **kwargs):
        """
        Create a new merge request.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_request = MergeRequestModel(**kwargs)
        if (merge_request.project_id is None
                or merge_request.source_branch is None
                or merge_request.target_branch is None
                or merge_request.title is None):
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects'
                                              f'/{merge_request.project_id}/merge_requests',
                                          headers=self.headers,
                                          data=json.dumps(merge_request.data, indent=2), verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_merge_requests(self, **kwargs):
        """
        Get a list of merge requests.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_request = MergeRequestModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/merge_requests'
                                             f'?per_page={merge_request.per_page}&x-total-pages',
                                         headers=self.headers,
                                         verify=self.verify)
            total_pages = int(response.headers['X-Total-Pages'])
            response = []
            if merge_request.max_pages == 0 or merge_request.max_pages > total_pages:
                merge_request.max_pages = total_pages
            for page in range(0, merge_request.max_pages):
                response_page = self._session.get(
                    url=f'{self.url}/merge_requests'
                    f'{merge_request.api_parameters}&per_page={merge_request.per_page}&page={page}',
                    headers=self.headers, verify=self.verify)
                response_page = json.loads(response_page.text.replace("'", "\""))
                response = response + response_page
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_merge_requests(self, **kwargs):
        """
        Get merge requests for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_request = MergeRequestModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{merge_request.project_id}/merge_requests',
                                         headers=self.headers, verify=self.verify)

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_merge_request(self, **kwargs):
        """
        Get details of a specific merge request in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_request = MergeRequestModel(**kwargs)
        if merge_request.project_id is None or merge_request.merge_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{merge_request.project_id}'
                                         f'/merge_requests/{merge_request.merge_id}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                            Merge Rules API                                                       #
    ####################################################################################################################
    @require_auth
    def get_project_level_rules(self, **kwargs):
        """
        Get project-level merge request approval rules.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{merge_rule.project_id}/approval_rules',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_level_rule(self, **kwargs):
        """
        Get details of a specific project-level merge request approval rule.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}',
                headers=self.headers,
                verify=self.verify)

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_project_level_rule(self, **kwargs):
        """
        Create a new project-level merge request approval rule.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}/projects/{merge_rule.project_id}/approval_rules',
                                          headers=self.headers,
                                          data=json.dumps(merge_rule.data, indent=2),
                                          verify=self.verify)

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_project_level_rule(self, **kwargs):
        """
        Update an existing project-level merge request approval rule.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        try:
            response = self._session.put(url=f'{self.url}/projects/{merge_rule.project_id}'
                                         f'/approval_rules/{merge_rule.approval_rule_id}',
                                         headers=self.headers, data=json.dumps(merge_rule.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_project_level_rule(self, **kwargs):
        """
        Delete a project-level merge request approval rule.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        try:
            response = self._session.put(url=f'{self.url}/projects/{merge_rule.project_id}'
                                         f'/approval_rules/{merge_rule.approval_rule_id}',
                                         headers=self.headers, data=json.dumps(merge_rule.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def merge_request_level_approvals(self, **kwargs):
        """
        Get approvals for a specific merge request.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approvals',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_approval_state_merge_requests(self, **kwargs):
        """
        Get the approval state of merge requests for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{merge_rule.project_id}'
                f'/merge_requests/{merge_rule.merge_request_iid}/approval_state',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_merge_request_level_rules(self, **kwargs):
        """
        Get merge request-level approval rules for a specific project and merge request.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{merge_rule.project_id}'
                f'/merge_requests/{merge_rule.merge_request_iid}/approval_rules',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def approve_merge_request(self, **kwargs):
        """
        Approve a specific merge request.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{merge_rule.project_id}'
                                          f'/merge_requests/{merge_rule.merge_request_iid}/approve',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def unapprove_merge_request(self, **kwargs):
        """
        Unapprove a specific merge request.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        - MissingParameterError: If required parameters are missing.
        """
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{merge_rule.project_id}'
                                          f'/merge_requests/{merge_rule.merge_request_iid}/unapprove',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                               Packages API                                                       #
    ####################################################################################################################
    def get_repository_packages(self, **kwargs):
        """
        Get information about repository packages for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        package = PackageModel(**kwargs)
        if package.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{package.project_id}/packages', headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    def publish_repository_package(self, **kwargs):
        """
        Publish a repository package for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        package = PackageModel(**kwargs)
        if (package.project_id is None
                or package.package_name is None
                or package.package_version is None
                or package.file_name is None):
            raise MissingParameterError
        try:
            response = self._session.put(url=f'{self.url}/projects/{package.project_id}'
                                         f'/packages/generic/{package.package_name}/{package.package_version}'
                                         f'/{package.file_name}{package.api_parameters}', headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    def download_repository_package(self, **kwargs):
        """
        Download a repository package for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        package = PackageModel(**kwargs)
        if (package.project_id is None
                or package.package_name is None
                or package.package_version is None
                or package.file_name is None):
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{package.project_id}'
                                         f'/packages/generic/{package.package_name}/{package.package_version}'
                                         f'/{package.file_name}', headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                Pipeline API                                                      #
    ####################################################################################################################
    @require_auth
    def get_pipelines(self, **kwargs):
        """
        Get information about pipelines for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f'{self.url}/projects/{pipeline.project_id}/pipelines{pipeline.api_parameters}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_pipeline(self, **kwargs):
        """
        Get information about a specific pipeline in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None or pipeline.pipeline_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{pipeline.project_id}'
                                         f'/pipelines/{pipeline.pipeline_id}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def run_pipeline(self, **kwargs):
        """
        Run a pipeline for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None or pipeline.reference is None:
            raise MissingParameterError
        if pipeline.variables:
            response = self._session.post(url=f'{self.url}/projects/{pipeline.project_id}'
                                          f'/pipeline{pipeline.api_parameters}',
                                          headers=self.headers,
                                          data=json.dumps(pipeline.variables, indent=2), verify=self.verify)
        else:
            response = self._session.post(url=f'{self.url}/projects/{pipeline.project_id}'
                                          f'/pipeline{pipeline.api_parameters}',
                                          headers=self.headers,
                                          verify=self.verify)
        return response

    ####################################################################################################################
    #                                                Projects API                                                      #
    ####################################################################################################################
    @require_auth
    def get_projects(self, **kwargs):
        """
        Get information about projects.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        response = self._session.get(url=f'{self.url}/projects?per_page={project.per_page}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        if project.max_pages == 0 or project.max_pages > total_pages:
            project.max_pages = total_pages
        for page in range(0, project.max_pages):
            response_page = self._session.get(
                url=f'{self.url}/projects?per_page={project.per_page}&page={page}&order_by={project.order_by}',
                headers=self.headers, verify=self.verify)
            response_page = json.loads(response_page.text.replace("'", "\""))
            response = response + response_page
        return response

    @require_auth
    def get_project(self, **kwargs):
        """
        Get information about a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """

        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.get(url=f'{self.url}/projects/{project.project_id}',
                                     headers=self.headers,
                                     verify=self.verify)
        return response

    @require_auth
    def get_nested_projects_by_group(self, **kwargs):
        """
        Get information about nested projects within a group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.group_id is None:
            raise MissingParameterError
        projects = []
        groups = [self.get_group(group_id=project.group_id).json()]
        groups = groups + self.get_group_subgroups(group_id=project.group_id).json()
        for group in groups:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups/{group["id"]}'
                                         f'/projects?per_page={project.per_page}&x-total-pages',
                                         headers=self.headers, verify=self.verify)
            total_pages = int(response.headers['X-Total-Pages'])
            if project.max_pages == 0 or project.max_pages > total_pages:
                project.max_pages = total_pages
            for page in range(0, project.max_pages):
                group_projects = self._session.get(url=f'{self.url}/groups/{group["id"]}/'
                                                   f'projects?per_page={project.per_page}&page={page}',
                                                   headers=self.headers, verify=self.verify)
                group_projects = json.loads(group_projects.text)
                projects = projects + group_projects
        return projects

    @require_auth
    def get_project_contributors(self, **kwargs):
        """
        Get information about contributors to a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.get(url=f'{self.url}'
                                     f'/projects/{project.project_id}/repository/contributors',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_project_statistics(self, **kwargs):
        """
        Get statistics for a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.get(url=f'{self.url}'
                                     f'/projects/{project.project_id}?statistics=true',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def edit_project(self, **kwargs):
        """
        Edit a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        try:
            response = self._session.put(url=f'{self.url}/projects/{project.project_id}',
                                         data=project.model_dump_json(),
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_groups(self, **kwargs):
        """
        Get groups associated with a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}/projects/{project.project_id}/groups',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def archive_project(self, **kwargs):
        """
        Archive a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}/projects/{project.project_id}/archive',
                                          headers=self.headers,
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def unarchive_project(self, **kwargs):
        """
        Unarchive a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.post(url=f'{self.url}/projects/{project.project_id}/unarchive',
                                      headers=self.headers,
                                      verify=self.verify)
        return response

    @require_auth
    def delete_project(self, **kwargs):
        """
        Delete a specific project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.delete(url=f'{self.url}/projects/{project.project_id}',
                                        headers=self.headers,
                                        verify=self.verify)
        return response

    @require_auth
    def share_project(self, **kwargs):
        """
        Share a specific project with a group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.group_id is None or project.group_access is None:
            raise MissingParameterError
        response = self._session.post(url=f'{self.url}/projects/{project.project_id}'
                                      f'/share{project.api_parameters}',
                                      headers=self.headers,
                                      verify=self.verify)
        return response

    ####################################################################################################################
    #                                       Protected Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_protected_branches(self, **kwargs):
        """
        Get information about protected branches in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        """
        protected_branch = ProtectedBranchModel(**kwargs)
        if protected_branch.project_id is None:
            raise MissingParameterError
        response = self._session.get(url=f'{self.url}/projects/{protected_branch.project_id}/protected_branches',
                                     headers=self.headers,
                                     verify=self.verify)
        return response

    @require_auth
    def get_protected_branch(self, **kwargs):
        """
        Get information about a specific protected branch in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        """
        protected_branch = ProtectedBranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        response = self._session.get(url=f'{self.url}/projects/{protected_branch.project_id}'
                                     f'/protected_branches/{protected_branch.branch}',
                                     headers=self.headers,
                                     verify=self.verify)
        return response

    @require_auth
    def protect_branch(self, **kwargs):
        """
        Protect a specific branch in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        """
        protected_branch = ProtectedBranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError

        if protected_branch.data:
            response = self._session.post(url=f'{self.url}/projects/{protected_branch.project_id}'
                                          f'/protected_branches{protected_branch.api_parameters}',
                                          headers=self.headers,
                                          data=json.dumps(protected_branch.data, indent=2),
                                          verify=self.verify)
        else:
            response = self._session.post(url=f'{self.url}/projects/{protected_branch.project_id}'
                                          f'/protected_branches{protected_branch.api_parameters}',
                                          headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def unprotect_branch(self, **kwargs):
        """
        Unprotect a specific branch in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Raises:
        - MissingParameterError: If required parameters are missing.
        """
        protected_branch = ProtectedBranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        self._session.delete(url=f'{self.url}/projects/{protected_branch.project_id}'
                             f'/protected_branches/{protected_branch.branch}',
                             headers=self.headers,
                             verify=self.verify)

    @require_auth
    def require_code_owner_approvals_single_branch(self, **kwargs):
        """
        Require code owner approvals for a specific branch in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        """
        protected_branch = ProtectedBranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        response = self._session.patch(url=f'{self.url}/projects/{protected_branch.project_id}'
                                       f'/protected_branches/{protected_branch.branch}',
                                       headers=self.headers,
                                       verify=self.verify)
        return response

    ####################################################################################################################
    #                                                Release API                                                       #
    ####################################################################################################################
    @require_auth
    def get_releases(self, **kwargs):
        """
        Get information about releases in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/projects/{release.project_id}/releases',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_latest_release(self, **kwargs):
        """
        Get information about the latest release in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/projects/{release.project_id}/releases'
                                         f'/permalink/latest',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_latest_release_evidence(self, **kwargs):
        """
        Get evidence for the latest release in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/projects/{release.project_id}/releases'
                                         f'/permalink/latest/evidence',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_latest_release_asset(self, **kwargs):
        """
        Get the asset for the latest release in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/projects/{release.project_id}/releases'
                                         f'/permalink/latest/{release.direct_asset_path}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_releases(self, **kwargs):
        """
        Get information about releases in a group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups/{release.group_id}/releases{release.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def download_release_asset(self, **kwargs):
        """
        Download a release asset from a group's release.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/groups/{release.group_id}'
                                         f'/releases/{release.tag_name}'
                                         f'/downloads/{release.direct_asset_path}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_release_by_tag(self, **kwargs):
        """
        Get information about a release by its tag in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/projects/{release.project_id}/releases/{release.tag_name}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_release(self, **kwargs):
        """
        Create a new release in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}'
                                          f'/projects/{release.project_id}/releases',
                                          data=json.dumps(release.data, indent=2),
                                          headers=self.headers,
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_release_evidence(self, **kwargs):
        """
        Create evidence for a release in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.post(url=f'{self.url}'
                                          f'/projects/{release.project_id}'
                                          f'/releases/{release.tag_name}/evidence',
                                          headers=self.headers,
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_release(self, **kwargs):
        """
        Update information about a release in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.put(url=f'{self.url}'
                                         f'/projects/{release.project_id}/releases/{release.tag_name}',
                                         data=json.dumps(release.data, indent=2),
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_release(self, **kwargs):
        """
        Delete a release in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        release = ReleaseModel(**kwargs)
        try:
            response = self._session.delete(url=f'{self.url}'
                                            f'/projects/{release.project_id}/releases/{release.tag_name}',
                                            headers=self.headers,
                                            verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                Runners API                                                       #
    ####################################################################################################################
    @require_auth
    def get_runners(self, **kwargs):
        """
        Get information about runners.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/runners{runner.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_runner(self, **kwargs):
        """
        Get information about a specific runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the runner ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}'
                                         f'/runners/{runner.runner_id}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_runner_details(self, **kwargs):
        """
        Update details for a specific runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the runner ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(url=f'{self.url}/runners/{runner.runner_id}',
                                         headers=self.headers,
                                         data=json.dumps(runner.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def pause_runner(self, **kwargs):
        """
        Pause or unpause a specific runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the runner ID or active status is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None or runner.active is None:
            raise MissingParameterError
        try:
            response = self._session.put(url=f'{self.url}/runners/{runner.runner_id}',
                                         headers=self.headers,
                                         data=json.dumps(runner.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_runner_jobs(self, **kwargs):
        """
        Get jobs for a specific runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the runner ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(url=f'{self.url}/runners'
                                         f'/{runner.runner_id}/jobs',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_runners(self, **kwargs):
        """
        Get information about runners in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{runner.project_id}'
                                         f'/runners{runner.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def enable_project_runner(self, **kwargs):
        """
        Enable or disable a runner in a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID or runner ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.project_id is None or runner.runner_id is None:
            raise MissingParameterError

        try:
            response = self._session.put(url=f'{self.url}/projects'
                                         f'/{runner.project_id}/runners',
                                         headers=self.headers,
                                         data=json.dumps(runner.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_project_runner(self, **kwargs):
        """
        Delete a runner from a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID or runner ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.project_id is None or runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(url=f'{self.url}/projects/{runner.project_id}'
                                            f'/runners/{runner.runner_id}',
                                            headers=self.headers,
                                            verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_runners(self, **kwargs):
        """
        Get information about runners in a group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the group ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/groups/{runner.group_id}'
                                         f'/runners{runner.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def register_new_runner(self, **kwargs):
        """
        Register a new runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the token is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.put(url=f'{self.url}/runners',
                                         headers=self.headers,
                                         data=json.dumps(runner.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_runner(self, **kwargs):
        """
        Delete a runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the runner ID or token is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None and runner.token is None:
            raise MissingParameterError
        if runner.runner_id:
            response = self._session.delete(url=f'{self.url}/runners/{runner.runner_id}',
                                            headers=self.headers,
                                            verify=self.verify)
        else:
            try:
                response = self._session.delete(url=f'{self.url}/runners',
                                                headers=self.headers,
                                                data=json.dumps(runner.data, indent=2),
                                                verify=self.verify)
            except ValidationError as e:
                raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def verify_runner_authentication(self, **kwargs):
        """
        Verify runner authentication.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the token is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/runners/verify',
                                          headers=self.headers,
                                          data=json.dumps(runner.data, indent=2),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def reset_gitlab_runner_token(self):
        """
        Reset GitLab runner registration token.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        try:
            response = self._session.post(url=f'{self.url}/runners'
                                          f'/reset_registration_token', headers=self.headers,
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def reset_project_runner_token(self, **kwargs):
        """
        Reset registration token for a project's runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID is missing.
        - ParameterError: If there are invalid parameters.
        """

        runner = RunnerModel(**kwargs)
        if runner.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{runner.project_id}'
                                          f'/runners/reset_registration_token',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def reset_group_runner_token(self, **kwargs):
        """
        Reset registration token for a group's runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the group ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/groups/{runner.group_id}'
                                          f'/runners/reset_registration_token',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def reset_token(self, **kwargs):
        """
        Reset authentication token for a runner.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the runner ID or token is missing.
        - ParameterError: If there are invalid parameters.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None or runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/runners/{runner.runner_id}'
                                          f'/reset_authentication_token',
                                          headers=self.headers,
                                          data=json.dumps(runner.data,
                                                          indent=2),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                Users API                                                         #
    ####################################################################################################################
    @require_auth
    def get_users(self, **kwargs):
        """
        Get information about users.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        user = UserModel(**kwargs)
        api_parameters = f"?per_page={user.per_page}"
        response = self._session.get(url=f'{self.url}/users{api_parameters}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []

        if user.max_pages == 0 or user.max_pages > total_pages:
            user.max_pages = total_pages
        for page in range(0, user.max_pages):
            response_page = self._session.get(url=f'{self.url}/users{user.api_parameters}&page={page}',
                                              headers=self.headers, verify=self.verify)
            response_page = json.loads(response_page.text.replace("'", "\""))
            response = response + response_page
        return response

    @require_auth
    def get_user(self, **kwargs):
        """
        Get information about a specific user.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the user ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        user = UserModel(**kwargs)
        if user.user_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/users{user.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                 Wiki API                                                         #
    ####################################################################################################################
    @require_auth
    def get_wiki_list(self, **kwargs):
        """
        Get a list of wiki pages for a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{wiki.project_id}'
                                         f'/wikis{wiki.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_wiki_page(self, **kwargs):
        """
        Get information about a specific wiki page.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID or slug is missing.
        - ParameterError: If there are invalid parameters.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.get(url=f'{self.url}/projects/{wiki.project_id}'
                                         f'/wikis/{wiki.slug}{wiki.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_wiki_page(self, **kwargs):
        """
        Create a new wiki page for a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID is missing.
        - ParameterError: If there are invalid parameters.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(url=f'{self.url}/projects/{wiki.project_id}/wikis',
                                          headers=self.headers,
                                          verify=self.verify,
                                          data=json.dumps(wiki.data, indent=2))
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_wiki_page(self, **kwargs):
        """
        Update an existing wiki page for a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID or slug is missing.
        - ParameterError: If there are invalid parameters.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.put(url=f'{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}',
                                         headers=self.headers,
                                         verify=self.verify,
                                         data=json.dumps(wiki.data, indent=2))
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_wiki_page(self, **kwargs):
        """
        Delete a wiki page for a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID or slug is missing.
        - ParameterError: If there are invalid parameters.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.delete(url=f'{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}',
                                            headers=self.headers,
                                            verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def upload_wiki_page_attachment(self, **kwargs):
        """
        Upload an attachment to a wiki page for a project.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If the project ID, file, or branch is missing.
        - ParameterError: If there are invalid parameters.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.file is None or wiki.branch is None:
            raise MissingParameterError
        data = {}
        if wiki.file:
            if not isinstance(wiki.file, str):
                raise ParameterError
            data['file'] = f"@{wiki.file}"
        data = json.dumps(data, indent=4)
        headers = self.headers
        headers['Content-Type'] = "multipart/form-data"
        try:
            response = self._session.put(url=f'{self.url}/projects/{wiki.project_id}/wikis/attachments',
                                         headers=headers,
                                         verify=self.verify,
                                         data=json.dumps(data, indent=2))
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response
