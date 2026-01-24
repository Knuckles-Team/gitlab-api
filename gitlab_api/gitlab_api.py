#!/usr/bin/python
# coding: utf-8
import re
from urllib.parse import urlparse, parse_qs
import requests
import urllib3
import logging
from base64 import b64encode
from typing import Dict, Any, List, TypeVar, Tuple
from pydantic import ValidationError
from concurrent.futures import ThreadPoolExecutor, as_completed

from gitlab_api.gitlab_input_models import (
    CommitModel,
    GroupModel,
    JobModel,
    MembersModel,
    NamespaceModel,
    PackageModel,
    PipelineModel,
    ProjectModel,
    BranchModel,
    MergeRequestModel,
    MergeRequestRuleModel,
    MergeRequestRuleSettingsModel,
    ReleaseModel,
    RunnerModel,
    UserModel,
    WikiModel,
    DeployTokenModel,
    TagModel,
)
from gitlab_api.gitlab_response_models import (
    Branch,
    Commit,
    Diff,
    Comment,
    MergeRequest,
    CommitSignature,
    Environment,
    Group,
    Project,
    Job,
    Membership,
    ApprovalRule,
    Package,
    Pipeline,
    PipelineSchedule,
    User,
    Release,
    Runner,
    Tag,
    WikiPage,
    Namespace,
    DeployToken,
    Response,
    MergeRequestRuleSettings,
    PipelineVariable,
)
from gitlab_api.decorators import require_auth
from gitlab_api.exceptions import (
    AuthError,
    UnauthorizedError,
    ParameterError,
    MissingParameterError,
)

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
        self.url = url.rstrip("/")  # remove trailing slash
        forbidden = ["/api/v4", "/api/v4/"]
        for end in forbidden:
            if url.endswith(end):
                self.url = url[: -len(end)]
        self.url = self.url + "/api/v4/"
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
        page_data = response.json()
        return page_data if isinstance(page_data, list) else []

    def _fetch_all_pages(
        self, endpoint: str, model: T, id_field: str = None, id_value: Any = None
    ) -> Tuple[requests.Response, List[dict]]:
        """Generic method to fetch all pages with parallelization"""
        if id_field and getattr(model, id_field) is None:
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
        try:
            initial_data = total_pages_response.json()
        except Exception:
            logging.error(f"Failed to decode JSON from {self.url}{initial_endpoint}")
            logging.error(f"Status Code: {total_pages_response.status_code}")
            logging.error(f"Response Content: {total_pages_response.text}")
            raise
        if isinstance(initial_data, list):
            all_data.extend(initial_data)

        if not model.max_pages or model.max_pages == 0 or model.max_pages > total_pages:
            model.max_pages = total_pages

        if model.max_pages > 1:
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

        return total_pages_response, all_data

    ####################################################################################################################
    #                                                 Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_branches(self, **kwargs) -> Response:
        """
        Retrieve information about branches in a project.

        Args:
            **kwargs: Additional keyword arguments to initialize the BranchModel.

        Returns:
            Response: The response object containing a list of Branch models.

        Raises:
            ParameterError: If the provided parameters are invalid based on the BranchModel.
        """
        branch = BranchModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{branch.project_id}/repository/branches",
                model=branch,
                id_field="project_id",
                id_value=branch.project_id,
            )
            parsed_data = [Branch(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_branch(self, **kwargs) -> Response:
        """
        Retrieve information about a specific branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: The response object containing a Branch model.

        Raises:
            MissingParameterError: If the project ID or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        branch = BranchModel(**kwargs)
        if branch.project_id is None or branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{branch.project_id}/repository/branches/{branch.branch}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_branch(self, **kwargs) -> Response:
        """
        Create a new branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch, ref).

        Returns:
            Response: The response object containing a Branch model.

        Raises:
            MissingParameterError: If required parameters are missing.
            ParameterError: If invalid parameters are provided.
        """
        branch = BranchModel(**kwargs)
        if branch.project_id is None or branch.branch is None or branch.ref is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{branch.project_id}/repository/branches",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
                json=branch.api_parameters,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_branch(self, **kwargs) -> Response:
        """
        Delete a branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: The response object (no data for successful deletion).

        Raises:
            MissingParameterError: If required parameters are missing.
            ParameterError: If invalid parameters are provided.
        """
        branch = BranchModel(**kwargs)
        if branch.project_id is None or branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{branch.project_id}/repository/branches/{branch.branch}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_merged_branches(self, **kwargs) -> Response:
        """
        Delete all merged branches in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: The response object (no data for successful deletion).

        Raises:
            MissingParameterError: If required parameters are missing.
            ParameterError: If invalid parameters are provided.
        """
        branch = BranchModel(**kwargs)
        if branch.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{branch.project_id}/repository/merged_branches",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                 Commits API                                                      #
    ####################################################################################################################
    @require_auth
    def get_commits(self, **kwargs) -> Response:
        """
        Get commits.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Commit models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{commit.project_id}/repository/commits",
                model=commit,
                id_field="project_id",
                id_value=commit.project_id,
            )
            parsed_data = [Commit(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_commit(self, **kwargs) -> Response:
        """
        Get a specific commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_commit_references(self, **kwargs) -> Response:
        """
        Get references of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of reference dictionaries.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/refs",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def cherry_pick_commit(self, **kwargs) -> Response:
        """
        Cherry-pick a commit into a new branch.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/cherry_pick",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_commit(self, **kwargs) -> Response:
        """
        Create a new commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def revert_commit(self, **kwargs) -> Response:
        """
        Revert a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/revert",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_commit_diff(self, **kwargs) -> Response:
        """
        Get the diff of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Diff models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/diff",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = [Diff(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_commit_comments(self, **kwargs) -> Response:
        """
        Get comments on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Comment models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/comments",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = [Comment(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_commit_comment(self, **kwargs) -> Response:
        """
        Create a comment on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Comment model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/comments",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Comment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_commit_discussions(self, **kwargs) -> Response:
        """
        Get discussions on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Discussion models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/discussions",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = [Comment(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_commit_statuses(self, **kwargs) -> Response:
        """
        Get statuses of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Status models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/statuses",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = [Commit(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def post_build_status_to_commit(self, **kwargs) -> Response:
        """
        Post build status to a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/statuses/{commit.commit_hash}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_commit_merge_requests(self, **kwargs) -> Response:
        """
        Get merge requests associated with a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/merge_requests",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = [MergeRequest(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_commit_gpg_signature(self, **kwargs) -> Response:
        """
        Get GPG signature of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a CommitSignature model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/signatures",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = CommitSignature(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Deploy Tokens API                                                 #
    ####################################################################################################################

    @require_auth
    def get_deploy_tokens(self, **kwargs) -> Response:
        """
        Get all deploy tokens.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of DeployToken models.

        Raises:
            ParameterError: If the request fails or returns invalid data.
        """
        deploy_token = DeployTokenModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/deploy_tokens",
                model=deploy_token,
                id_field=None,
                id_value=None,
            )
            parsed_data = [DeployToken(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get deploy tokens: {str(e)}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get project deploy tokens: {str(e)}")

    @require_auth
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
        if deploy_token.project_id is None or deploy_token.deploy_token_id is None:
            raise MissingParameterError("project_id and deploy_token_id are required")
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.deploy_token_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = DeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get project deploy token: {str(e)}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to create project deploy token: {str(e)}")

    @require_auth
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
        if deploy_token.project_id is None or deploy_token.deploy_token_id is None:
            raise MissingParameterError("project_id and deploy_token_id are required")
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.deploy_token_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to delete project deploy token: {str(e)}")

    @require_auth
    def get_group_deploy_tokens(self, **kwargs) -> Response:
        """
        Get deploy tokens for a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of DeployToken models.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None:
            raise MissingParameterError("group_id is required")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{deploy_token.group_id}/deploy_tokens",
                model=deploy_token,
                id_field="group_id",
                id_value=deploy_token.group_id,
            )
            parsed_data = [DeployToken(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get group deploy tokens: {str(e)}")

    @require_auth
    def get_group_deploy_token(self, **kwargs) -> Response:
        """
        Get a specific deploy token for a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, deploy_token_id).

        Returns:
            Response: A wrapper containing the original response and a DeployToken model.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None or deploy_token.deploy_token_id is None:
            raise MissingParameterError("group_id and deploy_token_id are required")
        try:
            response = self._session.get(
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens/{deploy_token.deploy_token_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = DeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get group deploy token: {str(e)}")

    @require_auth
    def create_group_deploy_token(self, **kwargs) -> Response:
        """
        Create a deploy token for a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, name, scopes).

        Returns:
            Response: A wrapper containing the original response and a DeployToken model.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if (
            deploy_token.group_id is None
            or deploy_token.name is None
            or deploy_token.scopes is None
        ):
            raise MissingParameterError("group_id, name, and scopes are required")
        try:
            response = self._session.post(
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens",
                headers=self.headers,
                json=deploy_token.model_dump(exclude_none=True),
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = DeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to create group deploy token: {str(e)}")

    @require_auth
    def delete_group_deploy_token(self, **kwargs) -> Response:
        """
        Delete a deploy token for a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, deploy_token_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None or deploy_token.deploy_token_id is None:
            raise MissingParameterError("group_id and deploy_token_id are required")
        try:
            response = self._session.delete(
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens/{deploy_token.deploy_token_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except requests.RequestException as e:
            raise ParameterError(f"Failed to delete group deploy token: {str(e)}")

    ####################################################################################################################
    #                                           Environments API                                                       #
    ####################################################################################################################
    @require_auth
    def get_environments(self, **kwargs) -> Response:
        """
        Get a list of environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Environment models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/environments",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Environment(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_environment(self, **kwargs) -> Response:
        """
        Get details of a specific environment.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.environment_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}/environments/{project.environment_id}",
                headers=self.headers,
                params=project.api_parameters,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_environment(self, **kwargs) -> Response:
        """
        Create a new environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/environments",
                headers=self.headers,
                json=project.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def update_environment(self, **kwargs) -> Response:
        """
        Update an existing environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.environment_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/environments/{project.environment_id}",
                headers=self.headers,
                json=project.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_environment(self, **kwargs) -> Response:
        """
        Delete an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.environment_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/environments/{project.environment_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def stop_environment(self, **kwargs) -> Response:
        """
        Stop an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.environment_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/environments/{project.environment_id}/stop",
                headers=self.headers,
                params=project.api_parameters,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def stop_stale_environments(self, **kwargs) -> Response:
        """
        Stop stale environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/environments/stop_stale",
                headers=self.headers,
                params=project.api_parameters,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_stopped_environments(self, **kwargs) -> Response:
        """
        Delete stopped environments (review apps) for a project.

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
                url=f"{self.url}/projects/{project.project_id}/environments/review_apps",
                headers=self.headers,
                params=project.api_parameters,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_protected_environments(self, **kwargs) -> Response:
        """
        Get a list of protected environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Environment models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/protected_environments",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Environment(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_protected_environment(self, **kwargs) -> Response:
        """
        Get details of a specific protected environment.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.name is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}/protected_environments/{project.name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def protect_environment(self, **kwargs) -> Response:
        """
        Protect an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/protected_environments",
                headers=self.headers,
                json=project.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def update_protected_environment(self, **kwargs) -> Response:
        """
        Update a protected environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/protected_environments/{project.name}",
                headers=self.headers,
                json=project.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def unprotect_environment(self, **kwargs) -> Response:
        """
        Unprotect an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

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
                url=f"{self.url}/projects/{project.project_id}/protected_environments/{project.name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Groups API                                                        #
    ####################################################################################################################
    @require_auth
    def get_groups(self, **kwargs) -> Response:
        """
        Get a list of groups.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/groups",
                model=group,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Group(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group(self, **kwargs) -> Response:
        """
        Get details of a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a Group model.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
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
            response.raise_for_status()
            parsed_data = Group(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def edit_group(self, **kwargs) -> Response:
        """
        Edit a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a Group model.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/groups/{group.group_id}",
                json=group.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Group(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group_subgroups(self, **kwargs) -> Response:
        """
        Get subgroups of a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint="/groups/{id}/subgroups",
                model=group,
                id_field="group_id",
                id_value=group.group_id,
            )
            parsed_data = [Group(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group_descendant_groups(self, **kwargs) -> Response:
        """
        Get descendant groups of a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint="/groups/{id}/descendant_groups",
                model=group,
                id_field="group_id",
                id_value=group.group_id,
            )
            parsed_data = [Group(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Jobs API                                                          #
    ####################################################################################################################
    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            parsed_data = response.text  # Job log is plain text, not JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
                json=job.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_pipeline_jobs(self, **kwargs) -> Response:
        """
        Get jobs associated with a specific pipeline within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_id).

        Returns:
            Response: A wrapper containing the original response and a list of Job models.

        Raises:
            MissingParameterError: If the project_id or pipeline_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        job = JobModel(**kwargs)
        if job.project_id is None or job.pipeline_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{job.project_id}/pipelines/{job.pipeline_id}/jobs",
                model=job,
                id_field="project_id",
                id_value=job.project_id,
            )
            parsed_data = [Job(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                               Members API                                                        #
    ####################################################################################################################
    @require_auth
    def get_group_members(self, **kwargs) -> Response:
        """
        Get members of a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Membership models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        members = MembersModel(**kwargs)
        if members.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{members.group_id}/members",
                model=members,
                id_field="group_id",
                id_value=members.group_id,
            )
            parsed_data = [Membership(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                            Merge Request API                                                     #
    ####################################################################################################################
    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
        if merge_request.project_id is None or merge_request.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_request.project_id}/merge_requests/{merge_request.merge_request_iid}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                            Merge Rules API                                                       #
    ####################################################################################################################
    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            parsed_data = (
                response.json()
            )  # No specific Pydantic model for approvals, keeping as raw JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            parsed_data = (
                response.json()
            )  # No specific Pydantic model for approval state, keeping as raw JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                     Merge Rules Settings API                                                     #
    ####################################################################################################################
    @require_auth
    def get_group_level_rule(self, **kwargs) -> Response:
        """
        Get details of a group-level merge request approval setting.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a MergeRequestRuleSettings model.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule_setting = MergeRequestRuleSettingsModel(**kwargs)
        if merge_rule_setting.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/groups/{merge_rule_setting.group_id}/merge_request_approval_setting",
                headers=self.headers,
                params=merge_rule_setting.api_parameters,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequestRuleSettings(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def edit_group_level_rule(self, **kwargs) -> Response:
        """
        Edit a group-level merge request approval setting.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a MergeRequestRuleSettings model.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule_setting = MergeRequestRuleSettingsModel(**kwargs)
        if merge_rule_setting.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/groups/{merge_rule_setting.group_id}/merge_request_approval_setting",
                headers=self.headers,
                json=merge_rule_setting.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = MergeRequestRuleSettings(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                               Packages API                                                       #
    ####################################################################################################################
    @require_auth
    def get_repository_packages(self, **kwargs) -> Response:
        """
        Get information about repository packages for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Package models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        package = PackageModel(**kwargs)
        if package.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{package.project_id}/packages",
                model=package,
                id_field="project_id",
                id_value=package.project_id,
            )
            parsed_data = [Package(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def publish_repository_package(self, **kwargs) -> Response:
        """
        Publish a repository package for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, package_name, package_version, file_name).

        Returns:
            Response: A wrapper containing the original response and a Package model.

        Raises:
            MissingParameterError: If the project_id, package_name, package_version, or file_name is missing.
            ParameterError: If invalid parameters are provided.
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
                url=f"{self.url}/projects/{package.project_id}/packages/generic/{package.package_name}/{package.package_version}/{package.file_name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Package(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def download_repository_package(self, **kwargs) -> Response:
        """
        Download a repository package for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, package_name, package_version, file_name).

        Returns:
            Response: A wrapper containing the original response and the raw package file data.

        Raises:
            MissingParameterError: If the project_id, package_name, package_version, or file_name is missing.
            ParameterError: If invalid parameters are provided.
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
                url=f"{self.url}/projects/{package.project_id}/packages/generic/{package.package_name}/{package.package_version}/{package.file_name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.content  # Package file is binary data, not JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Pipeline API                                                      #
    ####################################################################################################################
    @require_auth
    def get_pipelines(self, **kwargs) -> Response:
        """
        Get information about pipelines for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Pipeline models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{pipeline.project_id}/pipelines",
                model=pipeline,
                id_field="project_id",
                id_value=pipeline.project_id,
            )
            parsed_data = [Pipeline(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_pipeline(self, **kwargs) -> Response:
        """
        Get information about a specific pipeline in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_id).

        Returns:
            Response: A wrapper containing the original response and a Pipeline model.

        Raises:
            MissingParameterError: If the project_id or pipeline_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None or pipeline.pipeline_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{pipeline.project_id}/pipelines/{pipeline.pipeline_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Pipeline(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def run_pipeline(self, **kwargs) -> Response:
        """
        Run a pipeline for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, ref).

        Returns:
            Response: A wrapper containing the original response and a Pipeline model.

        Raises:
            MissingParameterError: If the project_id or ref is missing.
            ParameterError: If invalid parameters are provided.
        """
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None or pipeline.ref is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{pipeline.project_id}/pipeline",
                headers=self.headers,
                json=pipeline.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Pipeline(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                          Pipeline Schedules API                                                  #
    ####################################################################################################################
    @require_auth
    def get_pipeline_schedules(self, **kwargs) -> Response:
        """
        Get pipeline schedules for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of PipelineSchedule models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint="/projects/{id}/pipeline_schedules",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [PipelineSchedule(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_pipeline_schedule(self, **kwargs) -> Response:
        """
        Get information about a specific pipeline schedule in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response and a PipelineSchedule model.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_pipelines_triggered_from_schedule(self, **kwargs) -> Response:
        """
        Get pipelines triggered from a specific pipeline schedule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response and a list of Pipeline models.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/pipelines",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Pipeline(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_pipeline_schedule(self, **kwargs) -> Response:
        """
        Create a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a PipelineSchedule model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def edit_pipeline_schedule(self, **kwargs) -> Response:
        """
        Edit a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response and a PipelineSchedule model.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def take_pipeline_schedule_ownership(self, **kwargs) -> Response:
        """
        Take ownership of a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response and a PipelineSchedule model.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/take_ownership",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_pipeline_schedule(self, **kwargs) -> Response:
        """
        Delete a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def run_pipeline_schedule(self, **kwargs) -> Response:
        """
        Run a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/play",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_pipeline_schedule_variable(self, **kwargs) -> Response:
        """
        Create a variable for a pipeline schedule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id, key).

        Returns:
            Response: A wrapper containing the original response and a PipelineVariable model.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/variables",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineVariable(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_pipeline_schedule_variable(self, **kwargs) -> Response:
        """
        Delete a variable from a pipeline schedule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id, key).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id, pipeline_schedule_id, or key is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if (
            project.project_id is None
            or project.pipeline_schedule_id is None
            or project.key is None
        ):
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/variables/{project.key}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Projects API                                                      #
    ####################################################################################################################
    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            # Fetch the specified group
            group_response = self.get_group(group_id=project.group_id)
            all_groups.append(group_response.data)

            # Fetch all descendant groups
            groups_response = self.get_group_descendant_groups(
                group_id=project.group_id, per_page=project.per_page
            )
            all_groups.extend(groups_response.data)

            # Fetch projects for each group
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
                last_response = (
                    response  # Keep track of the last response for the Response object
                )

            return Response(response=last_response, data=all_projects)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            parsed_data = (
                response.json()
            )  # No specific Pydantic model for statistics, keeping as raw JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                       Protected Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_protected_branches(self, **kwargs) -> Response:
        """
        Get information about protected branches in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Branch models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{protected_branch.project_id}/protected_branches",
                model=protected_branch,
                id_field="project_id",
                id_value=protected_branch.project_id,
            )
            parsed_data = [Branch(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_protected_branch(self, **kwargs) -> Response:
        """
        Get information about a specific protected branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: A wrapper containing the original response and a Branch model.

        Raises:
            MissingParameterError: If the project_id or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches/{protected_branch.branch}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def protect_branch(self, **kwargs) -> Response:
        """
        Protect a specific branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: A wrapper containing the original response and a Branch model.

        Raises:
            MissingParameterError: If the project_id or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches",
                json=protected_branch.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def unprotect_branch(self, **kwargs) -> Response:
        """
        Unprotect a specific branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches/{protected_branch.branch}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def require_code_owner_approvals_single_branch(self, **kwargs) -> Response:
        """
        Require code owner approvals for a specific branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: A wrapper containing the original response and a Branch model.

        Raises:
            MissingParameterError: If the project_id or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.patch(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches/{protected_branch.branch}",
                json=protected_branch.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Release API                                                       #
    ####################################################################################################################
    @require_auth
    def get_releases(self, **kwargs) -> Response:
        """
        Get information about releases in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Release models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{release.project_id}/releases",
                model=release,
                id_field="project_id",
                id_value=release.project_id,
            )
            parsed_data = [Release(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_latest_release(self, **kwargs) -> Response:
        """
        Get information about the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases/permalink/latest",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Release(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_latest_release_evidence(self, **kwargs) -> Response:
        """
        Get evidence for the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and the raw evidence data.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases/permalink/latest/evidence",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = (
                response.json()
            )  # No specific Pydantic model for evidence, keeping as raw JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_latest_release_asset(self, **kwargs) -> Response:
        """
        Get the asset for the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, direct_asset_path).

        Returns:
            Response: A wrapper containing the original response and the raw asset data.

        Raises:
            MissingParameterError: If the project_id or direct_asset_path is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.direct_asset_path is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases/permalink/latest/{release.direct_asset_path}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.content  # Asset is binary data, not JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group_releases(self, **kwargs) -> Response:
        """
        Get information about releases in a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Release models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{release.group_id}/releases",
                model=release,
                id_field="group_id",
                id_value=release.group_id,
            )
            parsed_data = [Release(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def download_release_asset(self, **kwargs) -> Response:
        """
        Download a release asset from a group's release.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, tag_name, direct_asset_path).

        Returns:
            Response: A wrapper containing the original response and the raw asset data.

        Raises:
            MissingParameterError: If the group_id, tag_name, or direct_asset_path is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if (
            release.group_id is None
            or release.tag_name is None
            or release.direct_asset_path is None
        ):
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/groups/{release.group_id}/releases/{release.tag_name}/downloads/{release.direct_asset_path}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.content  # Asset is binary data, not JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_release_by_tag(self, **kwargs) -> Response:
        """
        Get information about a release by its tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases/{release.tag_name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Release(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_release(self, **kwargs) -> Response:
        """
        Create a new release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{release.project_id}/releases",
                json=release.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Release(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_release_evidence(self, **kwargs) -> Response:
        """
        Create evidence for a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{release.project_id}/releases/{release.tag_name}/evidence",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def update_release(self, **kwargs) -> Response:
        """
        Update information about a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{release.project_id}/releases/{release.tag_name}",
                json=release.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Release(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_release(self, **kwargs) -> Response:
        """
        Delete a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{release.project_id}/releases/{release.tag_name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Runners API                                                       #
    ####################################################################################################################
    @require_auth
    def get_runners(self, **kwargs) -> Response:
        """
        Get information about runners.

        Args:
            **kwargs: Additional parameters for the request (e.g., scope, status).

        Returns:
            Response: A wrapper containing the original response and a list of Runner models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/runners",
                model=runner,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Runner(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_runner(self, **kwargs) -> Response:
        """
        Get information about a specific runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the runner_id is missing.
            ParameterError: If invalid parameters are provided.
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
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def update_runner_details(self, **kwargs) -> Response:
        """
        Update details for a specific runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the runner_id is missing.
            ParameterError: If invalid parameters are provided.
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
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def pause_runner(self, **kwargs) -> Response:
        """
        Pause or unpause a specific runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id, active).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the runner_id or active status is missing.
            ParameterError: If invalid parameters are provided.
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
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_runner_jobs(self, **kwargs) -> Response:
        """
        Get jobs for a specific runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id).

        Returns:
            Response: A wrapper containing the original response and a list of Job models.

        Raises:
            MissingParameterError: If the runner_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/runners/{runner.runner_id}/jobs",
                model=runner,
                id_field="runner_id",
                id_value=runner.runner_id,
            )
            parsed_data = [Job(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_group_runners(self, **kwargs) -> Response:
        """
        Get information about runners in a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Runner models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{runner.group_id}/runners",
                model=runner,
                id_field="group_id",
                id_value=runner.group_id,
            )
            parsed_data = [Runner(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def register_new_runner(self, **kwargs) -> Response:
        """
        Register a new runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., token).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the token is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/runners",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_runner(self, **kwargs) -> Response:
        """
        Delete a runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id, token).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the runner_id or token is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None and runner.token is None:
            raise MissingParameterError
        try:
            if runner.runner_id:
                response = self._session.delete(
                    url=f"{self.url}/runners/{runner.runner_id}",
                    headers=self.headers,
                    verify=self.verify,
                    proxies=self.proxies,
                )
            else:
                response = self._session.delete(
                    url=f"{self.url}/runners",
                    headers=self.headers,
                    json=runner.data,
                    verify=self.verify,
                    proxies=self.proxies,
                )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def verify_runner_authentication(self, **kwargs) -> Response:
        """
        Verify runner authentication.

        Args:
            **kwargs: Additional parameters for the request (e.g., token).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the token is missing.
            ParameterError: If invalid parameters are provided.
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
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def reset_gitlab_runner_token(self) -> Response:
        """
        Reset GitLab runner registration token.

        Returns:
            Response: A wrapper containing the original response and the raw token data.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        try:
            response = self._session.post(
                url=f"{self.url}/runners/reset_registration_token",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = (
                response.json()
            )  # No specific Pydantic model for token, keeping as raw JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
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
            parsed_data = (
                response.json()
            )  # No specific Pydantic model for token, keeping as raw JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def reset_group_runner_token(self, **kwargs) -> Response:
        """
        Reset registration token for a group's runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and the raw token data.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/groups/{runner.group_id}/runners/reset_registration_token",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = (
                response.json()
            )  # No specific Pydantic model for token, keeping as raw JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def reset_token(self, **kwargs) -> Response:
        """
        Reset authentication token for a runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id, token).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the runner_id or token is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None or runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/runners/{runner.runner_id}/reset_authentication_token",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                 Tags API                                                         #
    ####################################################################################################################
    @require_auth
    def get_tags(self, **kwargs) -> Response:
        """
        Get information about tags in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Tag models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        tag = TagModel(**kwargs)
        if tag.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{tag.project_id}/repository/tags",
                model=tag,
                id_field="project_id",
                id_value=tag.project_id,
            )
            parsed_data = [Tag(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_tag(self, **kwargs) -> Response:
        """
        Get information about a specific tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and a Tag model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{tag.project_id}/repository/tags/{tag.name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Tag(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_tag(self, **kwargs) -> Response:
        """
        Create a tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and a Tag model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{tag.project_id}/repository/tags",
                json=tag.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Tag(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_tag(self, **kwargs) -> Response:
        """
        Delete a tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{tag.project_id}/repository/tags/{tag.name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_protected_tags(self, **kwargs) -> Response:
        """
        Get information about protected tags in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Tag models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        tag = TagModel(**kwargs)
        if tag.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{tag.project_id}/protected_tags",
                model=tag,
                id_field="project_id",
                id_value=tag.project_id,
            )
            parsed_data = [Tag(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_protected_tag(self, **kwargs) -> Response:
        """
        Get information about a specific protected tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and a Tag model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{tag.project_id}/protected_tags/{tag.name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Tag(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def protect_tag(self, **kwargs) -> Response:
        """
        Protect a tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and a Tag model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{tag.project_id}/protected_tags",
                json=tag.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Tag(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def unprotect_tag(self, **kwargs) -> Response:
        """
        Unprotect a tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{tag.project_id}/protected_tags/{tag.name}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                Users API                                                         #
    ####################################################################################################################
    @require_auth
    def get_users(self, **kwargs) -> Response:
        """
        Get information about users.

        Args:
            **kwargs: Additional parameters for the request (e.g., per_page, page).

        Returns:
            Response: A wrapper containing the original response and a list of User models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        user = UserModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/users",
                model=user,
                id_field=None,
                id_value=None,
            )
            parsed_data = [User(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_user(self, **kwargs) -> Response:
        """
        Get information about a specific user.

        Args:
            **kwargs: Additional parameters for the request (e.g., user_id).

        Returns:
            Response: A wrapper containing the original response and a User model.

        Raises:
            MissingParameterError: If the user_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        user = UserModel(**kwargs)
        if user.user_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/users/{user.user_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = User(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                                 Wiki API                                                         #
    ####################################################################################################################
    @require_auth
    def get_wiki_list(self, **kwargs) -> Response:
        """
        Get a list of wiki pages for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of WikiPage models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{wiki.project_id}/wikis",
                model=wiki,
                id_field="project_id",
                id_value=wiki.project_id,
            )
            parsed_data = [WikiPage(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_wiki_page(self, **kwargs) -> Response:
        """
        Get information about a specific wiki page.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, slug).

        Returns:
            Response: A wrapper containing the original response and a WikiPage model.

        Raises:
            MissingParameterError: If the project_id or slug is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = WikiPage(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def create_wiki_page(self, **kwargs) -> Response:
        """
        Create a new wiki page for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a WikiPage model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
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
            response.raise_for_status()
            parsed_data = WikiPage(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def update_wiki_page(self, **kwargs) -> Response:
        """
        Update an existing wiki page for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, slug).

        Returns:
            Response: A wrapper containing the original response and a WikiPage model.

        Raises:
            MissingParameterError: If the project_id or slug is missing.
            ParameterError: If invalid parameters are provided.
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
            response.raise_for_status()
            parsed_data = WikiPage(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def delete_wiki_page(self, **kwargs) -> Response:
        """
        Delete a wiki page for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, slug).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or slug is missing.
            ParameterError: If invalid parameters are provided.
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
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def upload_wiki_page_attachment(self, **kwargs) -> Response:
        """
        Upload an attachment to a wiki page for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, file, branch).

        Returns:
            Response: A wrapper containing the original response and the raw attachment data.

        Raises:
            MissingParameterError: If the project_id, file, or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.file is None or wiki.branch is None:
            raise MissingParameterError
        try:
            headers = self.headers.copy()
            headers["Content-Type"] = "multipart/form-data"
            response = self._session.post(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/attachments",
                headers=headers,
                verify=self.verify,
                proxies=self.proxies,
                files={"file": wiki.file},
            )
            response.raise_for_status()
            parsed_data = (
                response.json()
            )  # No specific Pydantic model for attachment, keeping as raw JSON
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    ####################################################################################################################
    #                                              Namespaces API                                                      #
    ####################################################################################################################
    @require_auth
    def get_namespaces(self, **kwargs) -> Response:
        """
        Get information about namespaces.

        Args:
            **kwargs: Additional parameters for the request (e.g., per_page).

        Returns:
            Response: A wrapper containing the original response and a list of Namespace models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        namespace = NamespaceModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/namespaces",
                model=namespace,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Namespace(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

    @require_auth
    def get_namespace(self, **kwargs) -> Response:
        """
        Get information about a specific namespace.

        Args:
            **kwargs: Additional parameters for the request (e.g., namespace_id).

        Returns:
            Response: A wrapper containing the original response and a Namespace model.

        Raises:
            MissingParameterError: If the namespace_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        namespace = NamespaceModel(**kwargs)
        if namespace.namespace_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/namespaces/{namespace.namespace_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Namespace(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")

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
    ) -> Response:
        """
        Make a custom API request to the GitLab server.

        Args:
            method: The HTTP method to use (GET, POST, PUT, DELETE).
            endpoint: The API endpoint to call.
            data: The data to send in the request body (for form data).
            json: The JSON data to send in the request body.

        Returns:
            Response: A wrapper containing the original response and the response data (if applicable).

        Raises:
            ValueError: If an unsupported HTTP method is provided.
            ParameterError: If invalid parameters are provided.
            HTTPError: If the API request fails.
        """
        if method.upper() not in ["GET", "POST", "PUT", "DELETE"]:
            raise ValueError(f"Unsupported HTTP method: {method.upper()}")
        try:
            request_func = getattr(self._session, method.lower())
            response = request_func(
                url=f"{self.url}/{endpoint.lstrip('/')}",
                headers=self.headers,
                data=data,
                json=json,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = (
                response.json()
                if response.content
                and "application/json" in response.headers.get("Content-Type", "")
                else None
            )
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        except Exception as e:
            print(f"Request Error: {str(e)}")
            raise


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
