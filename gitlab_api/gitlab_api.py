#!/usr/bin/python
# coding: utf-8
import re
from urllib.parse import urlparse, parse_qs
import requests
import urllib3
import logging
from base64 import b64encode
from typing import Union, Dict, Any, List, TypeVar
from pydantic import ValidationError
from concurrent.futures import ThreadPoolExecutor, as_completed

from gitlab_api.gitlab_input_models import (
    BranchModel,
    CommitModel,
    DeployTokenModel,
    GroupModel,
    JobModel,
    MembersModel,
    NamespaceModel,
    PackageModel,
    PipelineModel,
    ProjectModel,
    ProtectedBranchModel,
    MergeRequestModel,
    MergeRequestRuleModel,
    ReleaseModel,
    RunnerModel,
    UserModel,
    WikiModel,
)
from gitlab_api.gitlab_response_models import Response
from gitlab_api.decorators import require_auth
from gitlab_api.exceptions import (
    AuthError,
    UnauthorizedError,
    ParameterError,
    MissingParameterError,
)
from gitlab_api.utils import process_response

T = TypeVar("T")


class Api(object):

    def __init__(
        self,
        url: str = None,
        username: str = None,
        password: str = None,
        token: str = None,
        tokens: list = None,
        proxies: dict = None,
        verify: bool = True,
        debug: bool = False,
    ):
        if debug:
            logging.basicConfig(
                level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
            )
        else:
            logging.basicConfig(
                level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
            )
        if url is None:
            raise MissingParameterError

        self._session = requests.Session()
        self.url = url
        self.headers = None
        self.headers_parallel = None
        self.verify = verify
        self.proxies = proxies
        self.debug = debug
        self._current_header_index = 0

        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self.headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        elif tokens:
            self.headers_parallel = []
            for token in tokens:
                self.headers_parallel.append(
                    {
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    }
                )
            self.headers = self.headers_parallel[self._current_header_index]
        elif username and password:
            user_pass = f"{username}:{password}".encode()
            user_pass_encoded = b64encode(user_pass).decode()
            self.headers = {
                "Authorization": f"Basic {user_pass_encoded}",
                "Content-Type": "application/json",
            }
        else:
            raise MissingParameterError

        headers_to_check = (
            self.headers_parallel if self.headers_parallel else [self.headers]
        )
        for header in headers_to_check:
            response = self._session.get(
                url=f"{self.url}/projects",
                headers=header,
                verify=self.verify,
                proxies=self.proxies,
            )
            if response.status_code in (401, 403):
                print(f"Authentication Error with header: {response.content}")
                raise AuthError if response.status_code == 401 else UnauthorizedError
            elif response.status_code == 404:
                print(f"Parameter Error: {response.content}")
                raise ParameterError

    def switch_to_next_headers(self) -> bool:
        """
        Switches self.headers to the next set of headers in self.headers_parallel.

        Returns:
        - bool: True if headers were switched, False if no switch occurred (e.g., no parallel headers).
        """
        if not self.headers_parallel or len(self.headers_parallel) <= 1:
            logging.debug("No parallel headers available to switch to.")
            return False

        # Increment index and wrap around if at the end
        self._current_header_index = (self._current_header_index + 1) % len(
            self.headers_parallel
        )
        self.headers = self.headers_parallel[self._current_header_index]
        logging.debug(f"Switched to headers at index {self._current_header_index}")
        return True

    def _fetch_next_page(
        self, endpoint: str, model: T, header: dict, page: int
    ) -> List[dict]:
        """Fetch a single page of data from the specified endpoint"""
        model.page = page
        model.model_post_init(model)
        response = self._session.get(
            url=f"{self.url}{endpoint}",
            params=model.api_parameters,
            headers=header,
            verify=self.verify,
            proxies=self.proxies,
        )
        data = Response(data=response.json(), status_code=response.status_code)
        return data.data if isinstance(data.data, list) else []

    def _fetch_all_pages(
        self, endpoint: str, model: T, id_field: str, id_value: Any
    ) -> List[dict]:
        """Generic method to fetch all pages with parallelization"""
        if getattr(model, id_field) is None:
            raise MissingParameterError

        all_data = []
        headers_to_use = (
            self.headers_parallel if self.headers_parallel else [self.headers]
        )

        initial_endpoint = (
            endpoint.format(id=id_value) if "{id}" in endpoint else endpoint
        )
        total_pages_response = self._session.get(
            url=f"{self.url}{initial_endpoint}",
            params=model.api_parameters,
            headers=headers_to_use[0],
            verify=self.verify,
            proxies=self.proxies,
        )
        total_pages = int(total_pages_response.headers.get("X-Total-Pages", 1))
        initial_data = Response(data=total_pages_response.json(), status_code=200)
        if isinstance(initial_data.data, list):
            all_data.extend(initial_data.data)

        if not model.max_pages or model.max_pages == 0 or model.max_pages > total_pages:
            model.max_pages = total_pages

        if model.max_pages > 1:
            pages_per_header = max(1, (model.max_pages - 1) // len(headers_to_use))

            with ThreadPoolExecutor(max_workers=len(headers_to_use)) as executor:
                future_to_page = {}
                header_idx = 0

                for page in range(1, model.max_pages):
                    header = headers_to_use[header_idx % len(headers_to_use)]
                    future = executor.submit(
                        self._fetch_next_page, initial_endpoint, model, header, page
                    )
                    future_to_page[future] = page
                    header_idx += 1

                for future in as_completed(future_to_page):
                    try:
                        page_data = future.result()
                        all_data.extend(page_data)
                    except Exception as e:
                        logging.error(
                            f"Error fetching page {future_to_page[future]}: {str(e)}"
                        )

        return all_data

    ####################################################################################################################
    #                                                 Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_branches(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{branch.project_id}/repository/branches",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_branch(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{branch.project_id}/repository/branches/{branch.branch}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_branch(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{branch.project_id}/repository/branches",
                params=branch.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_branch(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.delete(
                url=f"{self.url}/projects/{branch.project_id}" f"/repository/branches",
                params=branch.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_merged_branches(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.delete(
                url=f"{self.url}/projects/{branch.project_id}"
                f"/repository/merged_branches",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                 Commits API                                                      #
    ####################################################################################################################
    @require_auth
    def get_commits(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_commit(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_commit_references(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/refs",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def cherry_pick_commit(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/cherry_pick",
                headers=self.headers,
                json=commit.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_commit(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits",
                headers=self.headers,
                json=commit.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def revert_commit(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/revert",
                headers=self.headers,
                json=commit.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_commit_diff(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/diff",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_commit_comments(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/comments",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_commit_comment(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/comments",
                headers=self.headers,
                json=commit.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_commit_discussions(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/discussions",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_commit_statuses(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/statuses",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def post_build_status_to_commit(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}"
                f"/statuses/{commit.commit_hash}/",
                headers=self.headers,
                json=commit.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_commit_merge_requests(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/merge_requests",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_commit_gpg_signature(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{commit.project_id}"
                f"/repository/commits/{commit.commit_hash}/merge_requests",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                Deploy Tokens API                                                 #
    ####################################################################################################################
    @require_auth
    def get_deploy_tokens(self) -> Union[Response, requests.Response]:
        """
        Get all deploy tokens.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """

        try:
            response = self._session.get(
                url=f"{self.url}/deploy_tokens",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_deploy_tokens(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_deploy_token(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.token}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_project_deploy_token(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
        if (
            deploy_token.project_id is None
            or deploy_token.name is None
            or deploy_token.scopes is None
        ):
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens",
                headers=self.headers,
                json=deploy_token.model_dump(),
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_project_deploy_token(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.token}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_group_deploy_tokens(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_group_deploy_token(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/groups/"
                f"{deploy_token.group_id}/deploy_tokens/{deploy_token.token}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_group_deploy_token(self, **kwargs) -> Union[Response, requests.Response]:
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
        if (
            deploy_token.group_id is None
            or deploy_token.name is None
            or deploy_token.scopes is None
        ):
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens",
                headers=self.headers,
                json=deploy_token.model_dump(),
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_group_deploy_token(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens/{deploy_token.token}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                Groups API                                                        #
    ####################################################################################################################
    @require_auth
    def get_groups(self, **kwargs) -> Union[Response, requests.Response]:
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
            all_groups = self._fetch_all_pages(
                "/groups", group, "group_id", group.group_id
            )
            response = Response(data=all_groups, status_code=200)
            return process_response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/groups/{group.group_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def edit_group(self, **kwargs) -> Union[Response, requests.Response]:
        """
        Edit a specific group.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        try:
            response = self._session.put(
                url=f"{self.url}/groups/{group.group_id}",
                json=group.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_group_subgroups(self, **kwargs) -> Union[Response, requests.Response]:
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
        try:
            all_subgroups = self._fetch_all_pages(
                "/groups/{id}/subgroups", group, "group_id", group.group_id
            )
            return Response(data=all_subgroups, status_code=200)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group_descendant_groups(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
        try:
            all_descendant_groups = self._fetch_all_pages(
                "/groups/{id}/descendant_groups", group, "group_id", group.group_id
            )
            return Response(data=all_descendant_groups, status_code=200)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group_projects(self, **kwargs) -> Union[Response, requests.Response]:
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
        try:
            all_projects = self._fetch_all_pages(
                "/groups/{id}/projects", group, "group_id", group.group_id
            )
            return Response(data=all_projects, status_code=200)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group_merge_requests(self, **kwargs) -> Union[Response, requests.Response]:
        """Get merge requests associated with a specific group."""
        group = GroupModel(**kwargs)
        try:
            all_merge_requests = self._fetch_all_pages(
                "/groups/{id}/merge_requests", group, "group_id", group.group_id
            )
            return Response(data=all_merge_requests, status_code=200)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Jobs API                                                          #
    ####################################################################################################################
    @require_auth
    def get_project_jobs(self, **kwargs) -> Union[Response, requests.Response]:
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
        all_jobs = []
        try:
            if job.project_id is None:
                raise MissingParameterError
            total_pages_response = self._session.get(
                url=f"{self.url}/projects/{job.project_id}/jobs",
                params=job.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            next_page = extract_next_page(total_pages_response.headers)
            jobs = Response(data=total_pages_response.json(), status_code=200)
            if isinstance(jobs.data, list) and jobs.data and len(jobs.data) > 0:
                all_jobs = all_jobs + jobs.data
            if job.max_pages and next_page and job.max_pages < next_page:
                next_page = None
            elif not job.max_pages and not next_page:
                job.max_pages = 1
            job.model_post_init(job)
            while next_page:
                job.page = next_page
                job.model_post_init(job)
                jobs_response = self._session.get(
                    url=f"{self.url}/projects/{job.project_id}/jobs",
                    params=job.api_parameters,
                    headers=self.headers,
                    verify=self.verify,
                    proxies=self.proxies,
                )
                self.switch_to_next_headers()
                next_page = extract_next_page(jobs_response.headers)
                if job.max_pages and next_page and job.max_pages < next_page:
                    next_page = None
                jobs = Response(data=jobs_response.json(), status_code=200)
                if isinstance(jobs.data, list) and jobs.data and len(jobs.data) > 0:
                    all_jobs = all_jobs + jobs.data
            response = Response(data=all_jobs, status_code=200)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_job(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_job_log(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/trace",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def cancel_project_job(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/cancel",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def retry_project_job(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/retry",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def erase_project_job(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/erase",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def run_project_job(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/play",
                headers=self.headers,
                json=job.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_pipeline_jobs(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{job.project_id}/pipelines/{job.pipeline_id}/jobs",
                params=job.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                               Members API                                                        #
    ####################################################################################################################
    @require_auth
    def get_group_members(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/groups/{members.group_id}/members",
                params=members.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_members(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{members.project_id}/members",
                params=members.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                            Merge Request API                                                     #
    ####################################################################################################################
    @require_auth
    def create_merge_request(self, **kwargs) -> Union[Response, requests.Response]:
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
        if (
            merge_request.project_id is None
            or merge_request.source_branch is None
            or merge_request.target_branch is None
            or merge_request.title is None
        ):
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects"
                f"/{merge_request.project_id}/merge_requests",
                headers=self.headers,
                json=merge_request.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_merge_requests(self, **kwargs) -> Union[Response, requests.Response]:
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
            all_merge_requests = self._fetch_all_pages(
                "/merge_requests", merge_request, "group_id", merge_request.group_id
            )
            response = Response(data=all_merge_requests, status_code=200)
            return process_response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_project_merge_requests(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{merge_request.project_id}/merge_requests",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_merge_request(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{merge_request.project_id}"
                f"/merge_requests/{merge_request.merge_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                            Merge Rules API                                                       #
    ####################################################################################################################
    @require_auth
    def get_project_level_rules(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_level_rule(self, **kwargs) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_project_level_rule(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules",
                headers=self.headers,
                json=merge_rule.data,
                verify=self.verify,
                proxies=self.proxies,
            )

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def update_project_level_rule(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/projects/{merge_rule.project_id}"
                f"/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
                json=merge_rule.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_project_level_rule(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/projects/{merge_rule.project_id}"
                f"/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
                json=merge_rule.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def merge_request_level_approvals(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/"
                f"{merge_rule.merge_request_iid}/approvals",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_approval_state_merge_requests(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{merge_rule.project_id}"
                f"/merge_requests/{merge_rule.merge_request_iid}/approval_state",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_merge_request_level_rules(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
                url=f"{self.url}/projects/{merge_rule.project_id}"
                f"/merge_requests/{merge_rule.merge_request_iid}/approval_rules",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def approve_merge_request(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}"
                f"/merge_requests/{merge_rule.merge_request_iid}/approve",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def unapprove_merge_request(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}"
                f"/merge_requests/{merge_rule.merge_request_iid}/unapprove",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                               Packages API                                                       #
    ####################################################################################################################
    def get_repository_packages(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{package.project_id}/packages",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    def publish_repository_package(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
        if (
            package.project_id is None
            or package.package_name is None
            or package.package_version is None
            or package.file_name is None
        ):
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{package.project_id}"
                f"/packages/generic/{package.package_name}/{package.package_version}/{package.file_name}",
                params=package.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    def download_repository_package(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
        if (
            package.project_id is None
            or package.package_name is None
            or package.package_version is None
            or package.file_name is None
        ):
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{package.project_id}"
                f"/packages/generic/{package.package_name}/{package.package_version}"
                f"/{package.file_name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                Pipeline API                                                      #
    ####################################################################################################################
    @require_auth
    def get_pipelines(self, **kwargs) -> Union[Response, requests.Response]:
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
        all_pipelines = []
        try:
            if pipeline.project_id is None:
                raise MissingParameterError
            total_pages_response = self._session.get(
                url=f"{self.url}/projects/{pipeline.project_id}/pipelines",
                params=pipeline.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            total_pages = int(total_pages_response.headers.get("X-Total-Pages"))
            pipelines = Response(data=total_pages_response.json(), status_code=200)
            if (
                isinstance(pipelines.data, list)
                and pipelines.data
                and len(pipelines.data) > 0
            ):
                all_pipelines = all_pipelines + pipelines.data
            if (
                not pipeline.max_pages
                or pipeline.max_pages == 0
                or pipeline.max_pages > total_pages
            ):
                pipeline.max_pages = total_pages
            for page in range(
                1, pipeline.max_pages
            ):  # Start index at 1 because we already got the first page to get total pages
                pipeline.page = page
                pipeline.model_post_init(pipeline)
                pipelines_response = self._session.get(
                    url=f"{self.url}/projects/{pipeline.project_id}/pipelines",
                    params=pipeline.api_parameters,
                    headers=self.headers,
                    verify=self.verify,
                    proxies=self.proxies,
                )
                pipelines = Response(data=pipelines_response.json(), status_code=200)
                if (
                    isinstance(pipelines.data, list)
                    and pipelines.data
                    and len(pipelines.data) > 0
                ):
                    all_pipelines = all_pipelines + pipelines.data
            response = Response(data=all_pipelines, status_code=200)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_pipeline(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{pipeline.project_id}"
                f"/pipelines/{pipeline.pipeline_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def run_pipeline(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{pipeline.project_id}/pipeline",
                params=pipeline.api_parameters,
                headers=self.headers,
                json=pipeline.variables,
                verify=self.verify,
                proxies=self.proxies,
            )
        else:
            response = self._session.post(
                url=f"{self.url}/projects/{pipeline.project_id}/pipeline",
                params=pipeline.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                Projects API                                                      #
    ####################################################################################################################
    @require_auth
    def get_projects(self, **kwargs) -> Union[Response, requests.Response]:
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
        all_projects = []
        if project.project_id is None:
            raise MissingParameterError
        try:
            if project.project_id is None:
                raise MissingParameterError
            total_pages_response = self._session.get(
                url=f"{self.url}" f"/projects/{project.project_id}/projects",
                params=project.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            total_pages = int(total_pages_response.headers.get("X-Total-Pages"))
            projects = Response(data=total_pages_response.json(), status_code=200)
            if (
                isinstance(projects.data, list)
                and projects.data
                and len(projects.data) > 0
            ):
                all_projects = all_projects + projects.data
            if (
                not project.max_pages
                or project.max_pages == 0
                or project.max_pages > total_pages
            ):
                project.max_pages = total_pages
            for page in range(
                1, project.max_pages
            ):  # Start index at 1 because we get the first one from getting total_pages
                project.page = page
                project.model_post_init(project)
                projects_response = self._session.get(
                    url=f"{self.url}/projects/{project.project_id}/projects",
                    params=project.api_parameters,
                    headers=self.headers,
                    verify=self.verify,
                    proxies=self.proxies,
                )
                projects = Response(data=projects_response.json(), status_code=200)
                if (
                    isinstance(projects.data, list)
                    and projects.data
                    and len(projects.data) > 0
                ):
                    all_projects = all_projects + projects.data
            response = Response(data=all_projects, status_code=200)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project(self, **kwargs) -> Union[Response, requests.Response]:
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
        response = self._session.get(
            url=f"{self.url}/projects/{project.project_id}",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def get_nested_projects_by_group(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
        all_groups = []
        all_projects = []

        if project.group_id is None:
            raise MissingParameterError

        project_group = self.get_group(group_id=project.group_id)
        if project_group.data:
            all_groups.append(project_group.data)

        groups = self.get_group_descendant_groups(
            group_id=project.group_id, per_page=project.per_page
        )
        if groups.data:
            all_groups.extend(groups.data)

        for group in all_groups:
            endpoint = f"/groups/{group.id}/projects"
            group_projects = self._fetch_all_pages(
                endpoint, project, "group_id", group.id
            )
            all_projects.extend(group_projects)

        return Response(data=all_projects, status_code=200)

    @require_auth
    def get_project_contributors(self, **kwargs) -> Union[Response, requests.Response]:
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
        response = self._session.get(
            url=f"{self.url}/projects/{project.project_id}/repository/contributors",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_statistics(self, **kwargs) -> Union[Response, requests.Response]:
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
        response = self._session.get(
            url=f"{self.url}/projects/{project.project_id}?statistics=true",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def edit_project(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_groups(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}/groups",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def archive_project(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/archive",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def unarchive_project(self, **kwargs) -> Union[Response, requests.Response]:
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
        response = self._session.post(
            url=f"{self.url}/projects/{project.project_id}/unarchive",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def delete_project(self, **kwargs) -> Union[Response, requests.Response]:
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
        response = self._session.delete(
            url=f"{self.url}/projects/{project.project_id}",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def share_project(self, **kwargs) -> Union[Response, requests.Response]:
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
        if (
            project.project_id is None
            or project.group_id is None
            or project.group_access is None
        ):
            raise MissingParameterError
        response = self._session.post(
            url=f"{self.url}/projects/{project.project_id}/share",
            params=project.api_parameters,
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                       Protected Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_protected_branches(self, **kwargs) -> Union[Response, requests.Response]:
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
        response = self._session.get(
            url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def get_protected_branch(self, **kwargs) -> Union[Response, requests.Response]:
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
        response = self._session.get(
            url=f"{self.url}/projects/{protected_branch.project_id}"
            f"/protected_branches/{protected_branch.branch}",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def protect_branch(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches",
                params=protected_branch.api_parameters,
                headers=self.headers,
                json=protected_branch.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        else:
            response = self._session.post(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches",
                params=protected_branch.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        response = process_response(response=response)
        return response

    @require_auth
    def unprotect_branch(self, **kwargs) -> Union[Response, requests.Response]:
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
        response = self._session.delete(
            url=f"{self.url}/projects/{protected_branch.project_id}"
            f"/protected_branches/{protected_branch.branch}",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def require_code_owner_approvals_single_branch(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
        response = self._session.patch(
            url=f"{self.url}/projects/{protected_branch.project_id}"
            f"/protected_branches/{protected_branch.branch}",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                Release API                                                       #
    ####################################################################################################################
    @require_auth
    def get_releases(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_latest_release(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}"
                f"/projects/{release.project_id}/releases"
                f"/permalink/latest",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_latest_release_evidence(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}"
                f"/projects/{release.project_id}/releases"
                f"/permalink/latest/evidence",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_latest_release_asset(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}"
                f"/projects/{release.project_id}/releases"
                f"/permalink/latest/{release.direct_asset_path}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_group_releases(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/groups/{release.group_id}/releases",
                params=release.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def download_release_asset(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}"
                f"/groups/{release.group_id}"
                f"/releases/{release.tag_name}"
                f"/downloads/{release.direct_asset_path}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_release_by_tag(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}"
                f"/projects/{release.project_id}/releases/{release.tag_name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_release(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{release.project_id}/releases",
                json=release.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_release_evidence(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}"
                f"/projects/{release.project_id}"
                f"/releases/{release.tag_name}/evidence",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def update_release(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}"
                f"/projects/{release.project_id}/releases/{release.tag_name}",
                json=release.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_release(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.delete(
                url=f"{self.url}"
                f"/projects/{release.project_id}/releases/{release.tag_name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                Runners API                                                       #
    ####################################################################################################################
    @require_auth
    def get_runners(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/runners",
                params=runner.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_runner(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def update_runner_details(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def pause_runner(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_runner_jobs(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/runners/{runner.runner_id}/jobs",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_project_runners(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{runner.project_id}/runners",
                params=runner.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def enable_project_runner(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/projects/{runner.project_id}/runners",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_project_runner(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.delete(
                url=f"{self.url}/projects/{runner.project_id}"
                f"/runners/{runner.runner_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_group_runners(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/groups/{runner.group_id}/runners",
                params=runner.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def register_new_runner(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/runners",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_runner(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.delete(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        else:
            try:
                response = self._session.delete(
                    url=f"{self.url}/runners",
                    headers=self.headers,
                    json=runner.data,
                    verify=self.verify,
                )
            except ValidationError as e:
                raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def verify_runner_authentication(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/runners/verify",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def reset_gitlab_runner_token(self) -> Union[Response, requests.Response]:
        """
        Reset GitLab runner registration token.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If there are invalid parameters.
        """
        try:
            response = self._session.post(
                url=f"{self.url}/runners/reset_registration_token",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def reset_project_runner_token(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{runner.project_id}"
                f"/runners/reset_registration_token",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def reset_group_runner_token(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/groups/{runner.group_id}"
                f"/runners/reset_registration_token",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def reset_token(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/runners/{runner.runner_id}"
                f"/reset_authentication_token",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                Users API                                                         #
    ####################################################################################################################
    @require_auth
    def get_users(self, **kwargs) -> Union[Response, requests.Response]:
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
        if not user.per_page:
            user.per_page = 100
        if not user.page:
            user.page = 1

        response = self._session.get(
            url=f"{self.url}/users",
            params=user.api_parameters,
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        second_response = None
        while (
            second_response is None
            or isinstance(second_response.data, list)
            and len(second_response.data) > 1
        ):
            try:
                user.page = user.page + 1
                user.model_post_init(user)
                second_response = self._session.get(
                    url=f"{self.url}/users",
                    params=user.api_parameters,
                    headers=self.headers,
                    verify=self.verify,
                )
                if user.max_pages and user.page > user.max_pages:
                    break
            except ValidationError or Exception as e:
                raise e
            second_response = process_response(response=second_response)
            # Check if the list of users being returned is already inside the list of total users
            if all(item in response.data for item in second_response.data):
                break
            else:
                response.data.extend(second_response.data)
        return response

    @require_auth
    def get_user(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/users",
                params=user.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                 Wiki API                                                         #
    ####################################################################################################################
    @require_auth
    def get_wiki_list(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{wiki.project_id}/wikis",
                params=wiki.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def get_wiki_page(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.get(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}",
                params=wiki.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def create_wiki_page(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.post(
                url=f"{self.url}/projects/{wiki.project_id}/wikis",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
                json=wiki.data,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def update_wiki_page(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.put(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
                json=wiki.data,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def delete_wiki_page(self, **kwargs) -> Union[Response, requests.Response]:
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
            response = self._session.delete(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    @require_auth
    def upload_wiki_page_attachment(
        self, **kwargs
    ) -> Union[Response, requests.Response]:
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
        headers = self.headers
        headers["Content-Type"] = "multipart/form-data"
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/attachments",
                headers=headers,
                verify=self.verify,
                proxies=self.proxies,
                json=wiki.data,
            )
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                              Namespaces API                                                      #
    ####################################################################################################################
    @require_auth
    def get_namespaces(self, **kwargs) -> Union[Response, requests.Response]:
        """
        Get information about namespaces.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - ParameterError: If invalid parameters are provided.
        """
        namespace = NamespaceModel(**kwargs)
        response = self._session.get(
            url=f"{self.url}/namespaces/",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
            params=namespace.api_parameters,
        )
        response = process_response(response=response)
        return response

    @require_auth
    def get_namespace(self, **kwargs) -> Union[Response, requests.Response]:
        """
        Get information about a specific namespace.

        Args:
        - **kwargs: Additional parameters for the request.

        Returns:
        - The response from the server.

        Raises:
        - MissingParameterError: If required parameters are missing.
        - ParameterError: If invalid parameters are provided.
        """

        namespace = NamespaceModel(**kwargs)
        if namespace.namespace_id is None:
            raise MissingParameterError
        response = self._session.get(
            url=f"{self.url}/namespaces/{namespace.namespace_id}",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response = process_response(response=response)
        return response

    ####################################################################################################################
    #                                                 Custom API                                                       #
    ####################################################################################################################
    @require_auth
    def api_request(
        self,
        method: str,
        endpoint: str,
        data: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
    ) -> Union[Response, Dict[str, Any]]:
        if method.upper() not in ["GET", "POST", "PUT", "DELETE"]:
            raise ValueError(f"Unsupported HTTP method: {method.upper()}")
        try:
            request_func = getattr(self._session, method.lower())
            response = request_func(
                url=f"{self.url}/{endpoint}",
                headers=self.headers,
                data=data,
                json=json,
                verify=self.verify,
                proxies=self.proxies,
            )
        except ValidationError or Exception as e:
            print(f"Invalid parameters: {e.errors()}")
            raise e
        try:
            response.raise_for_status()
        except Exception as response_error:
            print(f"Response Error: {response_error}")
        status_code = response.status_code
        raw_output = response.content
        try:
            response = response.json()
        except Exception as response_error:
            print(f"JSON Conversion Error: {response_error}")
        try:
            response.status_code = status_code
            response.raw_output = raw_output
            response.json_output = response
        except Exception as response_error:
            print(f"Response Model Application Error: {response_error}")
        return response


def extract_next_page(headers):
    link_header = headers.get("Link")
    if not link_header:
        return None

    links = link_header.split(", ")

    next_link = None
    for link in links:
        if 'rel="next"' in link:
            next_link = link
            break

    if not next_link:
        return None

    url_match = re.match(r"<(.+?)>", next_link)
    if not url_match:
        return None
    next_url = url_match.group(1)

    parsed_url = urlparse(next_url)
    query_params = parse_qs(parsed_url.query)
    page = query_params.get("page", [None])[0]

    return int(page) if page else None
