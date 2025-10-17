#!/usr/bin/python
# coding: utf-8

import logging
from typing import Dict, Any, Optional, Union, List
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from .exceptions import ParameterError, MissingParameterError
from .decorators import require_auth
from .utils import process_response
from .gitlab_response_models import Response
from .gitlab_input_models import (
    ProjectModel,
    BranchModel,
    TagModel,
    CommitModel,
    MergeRequestModel,
    PipelineModel,
    PipelineScheduleModel,
    JobModel,
    PackageModel,
    UserModel,
    MembersModel,
    ReleaseModel,
    IssueModel,
    NamespaceModel,
    GroupModel,
    WikiModel,
)


class GraphQL:
    """
    A class to interact with GitLab's GraphQL API, providing parity with REST API methods.

    This class provides methods to execute GraphQL queries and mutations corresponding to the REST endpoints in gitlab_api.py.
    """

    def __init__(
        self,
        url: str = None,
        token: str = None,
        proxies: Dict = None,
        verify: bool = True,
        debug: bool = False,
    ):
        if not url:
            raise MissingParameterError("URL is required")
        if not token:
            raise MissingParameterError("Token is required")

        self.url = f"{url.rstrip('/')}/api/graphql"
        self.token = token
        self.proxies = proxies
        self.verify = verify
        self.debug = debug

        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG if debug else logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

        # Set up gql transport with auth
        headers = {"Authorization": f"Bearer {token}"}
        self.transport = RequestsHTTPTransport(
            url=self.url,
            headers=headers,
            verify=verify,
            proxies=proxies,
        )
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    @require_auth
    def execute_gql(
        self,
        query_str: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> Response:
        """
        Execute a GraphQL query or mutation.

        Args:
            query_str: The GraphQL query or mutation string.
            variables: Optional dictionary of variables for the query.
            operation_name: Optional name of the operation.

        Returns:
            Response: A Response object containing the GraphQL result.
        """
        try:
            query = gql(query_str)
            result = self.client.execute(
                query, variable_values=variables, operation_name=operation_name
            )
            if "errors" in result:
                raise ParameterError(f"GraphQL errors: {result['errors']}")

            response = Response(
                data=result.get("data", {}),
                status_code=200,
                headers=self.transport.headers,
                json_output=result,
                raw_output=None,
            )
            return process_response(response)
        except Exception as e:
            logging.error(f"GraphQL execution failed: {str(e)}")
            raise ParameterError(f"Query execution failed: {str(e)}")

    # Branches Tools
    @require_auth
    def get_branches(
        self,
        project_id: Union[int, str],
        search: Optional[str] = None,
        regex: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        branch = BranchModel(project_id=project_id, search=search)
        query = """
        query ($fullPath: ID!, $search: String, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                repository {
                    branches(search: $search, first: $first, after: $after) {
                        nodes {
                            name
                        }
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if search:
            variables["search"] = search
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_branch(
        self, project_id: Union[int, str], branch: str, ref: str
    ) -> Response:
        branch_model = BranchModel(project_id=project_id, branch=branch, ref=ref)
        query = """
        mutation ($input: CreateBranchInput!) {
            createBranch(input: $input) {
                branch {
                    name
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(branch_model.project_id),
                "name": branch_model.branch,
                "ref": branch_model.ref,
            }
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_branch(
        self,
        project_id: Union[int, str],
        branch: str,
        delete_merged_branches: Optional[bool] = False,
    ) -> Response:
        branch_model = BranchModel(project_id=project_id, branch=branch)
        query = """
        mutation ($input: DestroyBranchInput!) {
            destroyBranch(input: $input) {
                branch {
                    name
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(branch_model.project_id),
                "name": branch_model.branch,
            }
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_branch(self, project_id: Union[int, str], branch: str) -> Response:
        branch_model = BranchModel(project_id=project_id, branch=branch)
        query = """
        query ($fullPath: ID!, $branch: String!) {
            project(fullPath: $fullPath) {
                repository {
                    branch(name: $branch) {
                        name
                        commit {
                            id
                            sha
                            message
                        }
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "branch": branch}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def protect_branch(
        self,
        project_id: Union[int, str],
        branch: str,
        push_access_level: Optional[str] = None,
        merge_access_level: Optional[str] = None,
        unprotect_access_level: Optional[str] = None,
        allow_force_push: Optional[bool] = False,
    ) -> Response:
        # Note: GitLab GraphQL may not have a direct mutation for protecting branches; use commit rules or branch protection mutation if available.
        # For parity, assume a mutation like updateBranchProtection.
        # If not, note that some features may not have exact parity.
        raise NotImplementedError(
            "Protect branch mutation not directly available in GitLab GraphQL; use REST for this."
        )

    @require_auth
    def unprotect_branch(self, project_id: Union[int, str], branch: str) -> Response:
        # Similar to protect, may require deleting protection rule.
        raise NotImplementedError(
            "Unprotect branch mutation not directly available in GitLab GraphQL; use REST for this."
        )

    @require_auth
    def get_protected_branches(
        self, project_id: Union[int, str], search: Optional[str] = None
    ) -> Response:
        query = """
        query ($fullPath: ID!, $search: String) {
            project(fullPath: $fullPath) {
                branchRules(search: $search) {
                    nodes {
                        name
                        isProtected
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id)}
        if search:
            variables["search"] = search
        return self.execute_gql(query, variables=variables)

    # Tags Tools
    @require_auth
    def get_tags(
        self,
        project_id: Union[int, str],
        search: Optional[str] = None,
        sort: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        tag = TagModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $search: String, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                repository {
                    tags(search: $search, first: $first, after: $after) {
                        nodes {
                            name
                            message
                            targetCommit {
                                sha
                            }
                        }
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if search:
            variables["search"] = search
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_tag(
        self,
        project_id: Union[int, str],
        tag: str,
        ref: str,
        message: Optional[str] = None,
    ) -> Response:
        tag_model = TagModel(project_id=project_id, tag=tag, ref=ref, message=message)
        query = """
        mutation ($input: CreateTagInput!) {
            createTag(input: $input) {
                tag {
                    name
                    message
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(tag_model.project_id),
                "tagName": tag_model.tag,
                "ref": tag_model.ref,
                "message": tag_model.message,
            }
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_tag(self, project_id: Union[int, str], tag: str) -> Response:
        tag_model = TagModel(project_id=project_id, tag=tag)
        query = """
        mutation ($input: DestroyTagInput!) {
            destroyTag(input: $input) {
                tag {
                    name
                }
                errors
            }
        }
        """
        variables = {
            "input": {"projectPath": str(tag_model.project_id), "name": tag_model.tag}
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_tag(self, project_id: Union[int, str], tag: str) -> Response:
        tag_model = TagModel(project_id=project_id, tag=tag)
        query = """
        query ($fullPath: ID!, $tagName: String!) {
            project(fullPath: $fullPath) {
                repository {
                    tag(name: $tagName) {
                        name
                        message
                        targetCommit {
                            sha
                        }
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "tagName": tag}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_protected_tags(
        self, project_id: Union[int, str], name: Optional[str] = None
    ) -> Response:
        # Protected tags are handled via branchRules or tag protection.
        query = """
        query ($fullPath: ID!, $name: String) {
            project(fullPath: $fullPath) {
                branchRules(name: $name) {
                    nodes {
                        name
                        isProtected
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id)}
        if name:
            variables["name"] = name
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_protected_tag(self, project_id: Union[int, str], name: str) -> Response:
        query = """
        query ($fullPath: ID!, $name: String!) {
            project(fullPath: $fullPath) {
                branchRule(name: $name) {
                    name
                    isProtected
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "name": name}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def protect_tag(
        self,
        project_id: Union[int, str],
        name: str,
        create_access_level: Optional[str] = None,
        allowed_to_create: Optional[List[Dict]] = None,
    ) -> Response:
        # Use updateBranchRule or similar for tags.
        raise NotImplementedError(
            "Protect tag mutation not directly available; use branchRuleUpdate for patterns like 'v*'."
        )

    @require_auth
    def unprotect_tag(self, project_id: Union[int, str], name: str) -> Response:
        raise NotImplementedError(
            "Unprotect tag mutation not directly available; use branchRuleUpdate."
        )

    # Commit Tools
    @require_auth
    def get_commits(
        self,
        project_id: Union[int, str],
        ref: Optional[str] = None,
        path: Optional[str] = None,
        author: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        all: Optional[bool] = False,
        with_stats: Optional[bool] = False,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        commit = CommitModel(project_id=project_id, ref=ref)
        query = """
        query ($fullPath: ID!, $ref: String, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                repository {
                    tree(ref: $ref) {
                        commits(first: $first, after: $after) {
                            nodes {
                                sha
                                message
                                authoredDate
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if ref:
            variables["ref"] = ref
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_commit(self, project_id: Union[int, str], commit_hash: str) -> Response:
        commit = CommitModel(project_id=project_id, commit_hash=commit_hash)
        query = """
        query ($fullPath: ID!, $sha: String!) {
            project(fullPath: $fullPath) {
                repository {
                    commit(sha: $sha) {
                        sha
                        message
                        authoredDate
                        authorName
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "sha": commit_hash}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_commit(
        self,
        project_id: Union[int, str],
        branch: str,
        message: str,
        actions: List[Dict],
        start_branch: Optional[str] = None,
        start_sha: Optional[str] = None,
        start_project: Optional[Union[int, str]] = None,
        author_email: Optional[str] = None,
        author_name: Optional[str] = None,
        stats: Optional[bool] = False,
        force: Optional[bool] = False,
    ) -> Response:
        commit = CommitModel(
            project_id=project_id, branch=branch, message=message, actions=actions
        )
        query = """
        mutation ($input: CommitCreateInput!) {
            commitCreate(input: $input) {
                commit {
                    sha
                    message
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "branch": branch,
                "message": message,
                "actions": actions,
            }
        }
        return self.execute_gql(query, variables=variables)

    # Add similar methods for cherry_pick_commit, revert_commit, etc.

    # For cherry_pick
    @require_auth
    def cherry_pick_commit(
        self,
        project_id: Union[int, str],
        commit_hash: str,
        branch: str,
        message: Optional[str] = None,
        dry_run: Optional[bool] = False,
    ) -> Response:
        query = """
        mutation ($input: CherryPickCommitInput!) {
            cherryPickCommit(input: $input) {
                commit {
                    sha
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "sha": commit_hash,
                "branch": branch,
                "message": message or "",
                "dryRun": dry_run,
            }
        }
        return self.execute_gql(query, variables=variables)

    # Add revert_commit similarly.

    # For commit comments, discussions, etc., use noteCreate, noteUpdate on commit.

    # Merge Request Tools
    @require_auth
    def get_merge_requests(
        self,
        project_id: Union[int, str],
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        milestone: Optional[str] = None,
        author_username: Optional[str] = None,
        reviewer_username: Optional[str] = None,
        source_branch: Optional[str] = None,
        target_branch: Optional[str] = None,
        search: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        mr = MergeRequestModel(project_id=project_id, state=state)
        query = """
        query ($fullPath: ID!, $state: MergeRequestState, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                mergeRequests(state: $state, first: $first, after: $after) {
                    nodes {
                        iid
                        title
                        description
                        state
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if state:
            variables["state"] = state
        if after:
            variables["after"] = after
        # Add other filters as available in GraphQL.
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_merge_request(
        self, project_id: Union[int, str], merge_request_iid: int
    ) -> Response:
        mr = MergeRequestModel(
            project_id=project_id, merge_request_iid=merge_request_iid
        )
        query = """
        query ($fullPath: ID!, $iid: String!) {
            project(fullPath: $fullPath) {
                mergeRequest(iid: $iid) {
                    iid
                    title
                    description
                    state
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "iid": str(merge_request_iid)}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_merge_request(
        self,
        project_id: Union[int, str],
        source_branch: str,
        target_branch: str,
        title: str,
        description: Optional[str] = None,
        labels: Optional[List[str]] = None,
        milestone_id: Optional[int] = None,
        assignee_ids: Optional[List[int]] = None,
        remove_source_branch: Optional[bool] = False,
    ) -> Response:
        mr = MergeRequestModel(
            project_id=project_id,
            source_branch=source_branch,
            target_branch=target_branch,
            title=title,
        )
        query = """
        mutation ($input: MergeRequestCreateInput!) {
            mergeRequestCreate(input: $input) {
                mergeRequest {
                    iid
                    title
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "sourceBranch": source_branch,
                "targetBranch": target_branch,
                "title": title,
                "description": description,
            }
        }
        return self.execute_gql(query, variables=variables)

    # Add update_merge_request, delete_merge_request, accept_merge_request, etc.

    # For update
    @require_auth
    def update_merge_request(
        self,
        project_id: Union[int, str],
        merge_request_iid: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        target_branch: Optional[str] = None,
    ) -> Response:
        query = """
        mutation ($input: MergeRequestUpdateInput!) {
            mergeRequestUpdate(input: $input) {
                mergeRequest {
                    iid
                    title
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "iid": str(merge_request_iid),
                "title": title,
                "description": description,
                "targetBranch": target_branch,
            }
        }
        return self.execute_gql(query, variables=variables)

    # For delete, there is no direct delete, but close or reopen.

    # For accept, mergeRequestAccept.

    # Continue adding for other categories like pipelines, jobs, packages, deploy tokens, users, memberships, releases, issues, to dos, environments, test reports, namespaces.

    # For pipelines
    @require_auth
    def get_pipelines(
        self,
        project_id: Union[int, str],
        ref: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        username: Optional[str] = None,
        updated_after: Optional[str] = None,
        updated_before: Optional[str] = None,
        order_by: Optional[str] = None,
        sort: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        pipeline = PipelineModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                pipelines(first: $first, after: $after) {
                    nodes {
                        id
                        status
                        duration
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_pipeline(
        self, project_id: Union[int, str], ref: str, variables: Optional[Dict] = None
    ) -> Response:
        pipeline = PipelineModel(project_id=project_id, ref=ref)
        query = """
        mutation ($input: CiPipelineCreateInput!) {
            ciPipelineCreate(input: $input) {
                pipeline {
                    id
                }
                errors
            }
        }
        """
        variables_dict = {"input": {"projectPath": str(project_id), "ref": ref}}
        if variables:
            variables_dict["input"]["variables"] = variables
        return self.execute_gql(query, variables=variables_dict)

    # Add delete_pipeline, retry_pipeline, cancel_pipeline.

    # For delete
    @require_auth
    def delete_pipeline(
        self, project_id: Union[int, str], pipeline_id: int
    ) -> Response:
        query = """
        mutation ($id: CiPipelineID!) {
            pipelineDestroy(input: {id: $id}) {
                errors
            }
        }
        """
        variables = {"id": f"gid://gitlab/Ci::Pipeline/{pipeline_id}"}
        return self.execute_gql(query, variables=variables)

    # Similarly for other pipeline methods.

    # For pipeline schedules, job, package, deploy token, user, etc., follow similar pattern.

    # Note: Some features like deploy tokens may not have GraphQL support; in those cases, raise NotImplementedError or note in comments.

    # Branch Tools (Completing protect/unprotect)
    @require_auth
    def protect_branch(
        self,
        project_id: Union[int, str],
        branch: str,
        push_access_level: Optional[str] = None,
        merge_access_level: Optional[str] = None,
        unprotect_access_level: Optional[str] = None,
        allow_force_push: Optional[bool] = False,
    ) -> Response:
        """
        Protect a branch in a project.

        Args:
            project_id: Project ID or full path.
            branch: Name of the branch to protect.
            push_access_level: Access level for pushing (e.g., 'maintainer').
            merge_access_level: Access level for merging.
            unprotect_access_level: Access level for unprotecting.
            allow_force_push: Whether to allow force pushes.

        Returns:
            Response: Result of the protection operation.

        Note:
            Uses branchRuleUpdate mutation, but some parameters may not be fully supported.
        """
        branch_model = BranchModel(project_id=project_id, branch=branch)
        query = """
        mutation ($input: BranchRuleUpdateInput!) {
            branchRuleUpdate(input: $input) {
                branchRule {
                    name
                    isProtected
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(branch_model.project_id),
                "name": branch_model.branch,
                "isProtected": True,
            }
        }
        if allow_force_push is not None:
            variables["input"]["allowForcePush"] = allow_force_push
        # Note: push_access_level, merge_access_level, unprotect_access_level may require additional configuration or REST API.
        return self.execute_gql(query, variables=variables)

    @require_auth
    def unprotect_branch(self, project_id: Union[int, str], branch: str) -> Response:
        """
        Unprotect a branch in a project.

        Args:
            project_id: Project ID or full path.
            branch: Name of the branch to unprotect.

        Returns:
            Response: Result of the unprotection operation.
        """
        branch_model = BranchModel(project_id=project_id, branch=branch)
        query = """
        mutation ($input: BranchRuleUpdateInput!) {
            branchRuleUpdate(input: $input) {
                branchRule {
                    name
                    isProtected
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(branch_model.project_id),
                "name": branch_model.branch,
                "isProtected": False,
            }
        }
        return self.execute_gql(query, variables=variables)

    # Tag Tools (Completing protect/unprotect)
    @require_auth
    def protect_tag(
        self,
        project_id: Union[int, str],
        name: str,
        create_access_level: Optional[str] = None,
        allowed_to_create: Optional[List[Dict]] = None,
    ) -> Response:
        """
        Protect a tag in a project.

        Args:
            project_id: Project ID or full path.
            name: Name of the tag to protect.
            create_access_level: Access level for creating the tag.
            allowed_to_create: List of users or groups allowed to create the tag.

        Returns:
            Response: Result of the protection operation.

        Note:
            Tag protection is limited in GraphQL; may need to use branchRuleUpdate for patterns (e.g., 'v*').
        """
        tag_model = TagModel(project_id=project_id, tag=name)
        query = """
        mutation ($input: BranchRuleUpdateInput!) {
            branchRuleUpdate(input: $input) {
                branchRule {
                    name
                    isProtected
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(tag_model.project_id),
                "name": name,  # Use tag name as a pattern
                "isProtected": True,
            }
        }
        # Note: create_access_level, allowed_to_create require additional configuration via REST API.
        return self.execute_gql(query, variables=variables)

    @require_auth
    def unprotect_tag(self, project_id: Union[int, str], name: str) -> Response:
        """
        Unprotect a tag in a project.

        Args:
            project_id: Project ID or full path.
            name: Name of the tag to unprotect.

        Returns:
            Response: Result of the unprotection operation.
        """
        tag_model = TagModel(project_id=project_id, tag=name)
        query = """
        mutation ($input: BranchRuleUpdateInput!) {
            branchRuleUpdate(input: $input) {
                branchRule {
                    name
                    isProtected
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(tag_model.project_id),
                "name": name,
                "isProtected": False,
            }
        }
        return self.execute_gql(query, variables=variables)

    # Commit Tools (Completing revert_commit and comments)
    @require_auth
    def revert_commit(
        self, project_id: Union[int, str], commit_hash: str, branch: str
    ) -> Response:
        """
        Revert a commit in a project.

        Args:
            project_id: Project ID or full path.
            commit_hash: SHA of the commit to revert.
            branch: Target branch for the revert.

        Returns:
            Response: Result of the revert operation.
        """
        commit = CommitModel(
            project_id=project_id, commit_hash=commit_hash, branch=branch
        )
        query = """
        mutation ($input: CommitCreateInput!) {
            commitCreate(input: $input) {
                commit {
                    sha
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "branch": branch,
                "message": f"Revert commit {commit_hash}",
                "actions": [{"action": "delete", "filePath": "", "sha": commit_hash}],
            }
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_commit_comment(
        self,
        project_id: Union[int, str],
        commit_hash: str,
        note: str,
        path: Optional[str] = None,
        line: Optional[int] = None,
        line_type: Optional[str] = None,
    ) -> Response:
        """
        Create a comment on a commit.

        Args:
            project_id: Project ID or full path.
            commit_hash: SHA of the commit.
            note: Comment text.
            path: Optional file path for the comment.
            line: Optional line number.
            line_type: Optional line type (e.g., 'new', 'old').

        Returns:
            Response: Result of the comment creation.
        """
        commit = CommitModel(project_id=project_id, commit_hash=commit_hash, note=note)
        query = """
        mutation ($input: NoteCreateInput!) {
            noteCreate(input: $input) {
                note {
                    id
                    body
                }
                errors
            }
        }
        """
        variables = {
            "input": {"noteableId": f"gid://gitlab/Commit/{commit_hash}", "body": note}
        }
        if path and line:
            variables["input"]["position"] = {
                "baseSha": commit_hash,
                "startSha": commit_hash,
                "headSha": commit_hash,
                "newPath": path,
                "newLine": line,
                "positionType": line_type or "text",
            }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_commit_comments(
        self,
        project_id: Union[int, str],
        commit_hash: str,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get comments on a commit.

        Args:
            project_id: Project ID or full path.
            commit_hash: SHA of the commit.
            first: Number of comments to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of comments.
        """
        commit = CommitModel(project_id=project_id, commit_hash=commit_hash)
        query = """
        query ($fullPath: ID!, $sha: String!, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                repository {
                    commit(sha: $sha) {
                        notes(first: $first, after: $after) {
                            nodes {
                                id
                                body
                                author {
                                    username
                                }
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "sha": commit_hash, "first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    # Merge Request Tools (Completing delete, accept, and others)
    @require_auth
    def delete_merge_request(
        self, project_id: Union[int, str], merge_request_iid: int
    ) -> Response:
        """
        Close a merge request (GitLab GraphQL doesn't support direct deletion).

        Args:
            project_id: Project ID or full path.
            merge_request_iid: Internal ID of the merge request.

        Returns:
            Response: Result of the close operation.
        """
        mr = MergeRequestModel(
            project_id=project_id, merge_request_iid=merge_request_iid
        )
        query = """
        mutation ($input: MergeRequestUpdateInput!) {
            mergeRequestUpdate(input: $input) {
                mergeRequest {
                    iid
                    state
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "iid": str(merge_request_iid),
                "stateEvent": "CLOSE",
            }
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def accept_merge_request(
        self,
        project_id: Union[int, str],
        merge_request_iid: int,
        merge_commit_message: Optional[str] = None,
        squash: Optional[bool] = False,
        squash_commit_message: Optional[str] = None,
    ) -> Response:
        """
        Accept a merge request.

        Args:
            project_id: Project ID or full path.
            merge_request_iid: Internal ID of the merge request.
            merge_commit_message: Optional merge commit message.
            squash: Whether to squash commits.
            squash_commit_message: Optional squash commit message.

        Returns:
            Response: Result of the accept operation.
        """
        mr = MergeRequestModel(
            project_id=project_id, merge_request_iid=merge_request_iid
        )
        query = """
        mutation ($input: MergeRequestAcceptInput!) {
            mergeRequestAccept(input: $input) {
                mergeRequest {
                    iid
                    state
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "iid": str(merge_request_iid),
                "mergeCommitMessage": merge_commit_message,
                "squash": squash,
                "squashCommitMessage": squash_commit_message,
            }
        }
        return self.execute_gql(query, variables=variables)

    # Pipeline Tools (Completing retry, cancel)
    @require_auth
    def retry_pipeline(self, project_id: Union[int, str], pipeline_id: int) -> Response:
        """
        Retry a pipeline.

        Args:
            project_id: Project ID or full path.
            pipeline_id: ID of the pipeline.

        Returns:
            Response: Result of the retry operation.
        """
        pipeline = PipelineModel(project_id=project_id)
        query = """
        mutation ($input: PipelineRetryInput!) {
            pipelineRetry(input: $input) {
                pipeline {
                    id
                    status
                }
                errors
            }
        }
        """
        variables = {"input": {"id": f"gid://gitlab/Ci::Pipeline/{pipeline_id}"}}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def cancel_pipeline(
        self, project_id: Union[int, str], pipeline_id: int
    ) -> Response:
        """
        Cancel a pipeline.

        Args:
            project_id: Project ID or full path.
            pipeline_id: ID of the pipeline.

        Returns:
            Response: Result of the cancel operation.
        """
        pipeline = PipelineModel(project_id=project_id)
        query = """
        mutation ($input: PipelineCancelInput!) {
            pipelineCancel(input: $input) {
                pipeline {
                    id
                    status
                }
                errors
            }
        }
        """
        variables = {"input": {"id": f"gid://gitlab/Ci::Pipeline/{pipeline_id}"}}
        return self.execute_gql(query, variables=variables)

    # Pipeline Schedules
    @require_auth
    def get_pipeline_schedules(
        self,
        project_id: Union[int, str],
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get pipeline schedules for a project.

        Args:
            project_id: Project ID or full path.
            first: Number of schedules to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of pipeline schedules.
        """
        pipeline_schedule = PipelineScheduleModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                pipelineSchedules(first: $first, after: $after) {
                    nodes {
                        id
                        description
                        ref
                        cron
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_pipeline_schedule(
        self, project_id: Union[int, str], pipeline_schedule_id: int
    ) -> Response:
        """
        Get a specific pipeline schedule.

        Args:
            project_id: Project ID or full path.
            pipeline_schedule_id: ID of the pipeline schedule.

        Returns:
            Response: Pipeline schedule details.
        """
        pipeline_schedule = PipelineScheduleModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $id: CiPipelineScheduleID!) {
            project(fullPath: $fullPath) {
                pipelineSchedule(id: $id) {
                    id
                    description
                    ref
                    cron
                }
            }
        }
        """
        variables = {
            "fullPath": str(project_id),
            "id": f"gid://gitlab/Ci::PipelineSchedule/{pipeline_schedule_id}",
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_pipeline_schedule(
        self,
        project_id: Union[int, str],
        description: str,
        ref: str,
        cron: str,
        cron_timezone: Optional[str] = None,
        active: Optional[bool] = True,
    ) -> Response:
        """
        Create a pipeline schedule.

        Args:
            project_id: Project ID or full path.
            description: Description of the schedule.
            ref: Branch or tag to run the pipeline on.
            cron: Cron expression for the schedule.
            cron_timezone: Optional timezone for the cron.
            active: Whether the schedule is active.

        Returns:
            Response: Created pipeline schedule.
        """
        pipeline_schedule = PipelineScheduleModel(project_id=project_id, ref=ref)
        query = """
        mutation ($input: PipelineScheduleCreateInput!) {
            pipelineScheduleCreate(input: $input) {
                pipelineSchedule {
                    id
                    description
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "description": description,
                "ref": ref,
                "cron": cron,
                "cronTimezone": cron_timezone,
                "active": active,
            }
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def update_pipeline_schedule(
        self,
        project_id: Union[int, str],
        pipeline_schedule_id: int,
        description: Optional[str] = None,
        ref: Optional[str] = None,
        cron: Optional[str] = None,
        cron_timezone: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> Response:
        """
        Update a pipeline schedule.

        Args:
            project_id: Project ID or full path.
            pipeline_schedule_id: ID of the pipeline schedule.
            description: Updated description.
            ref: Updated branch or tag.
            cron: Updated cron expression.
            cron_timezone: Updated timezone.
            active: Updated active status.

        Returns:
            Response: Updated pipeline schedule.
        """
        query = """
        mutation ($input: PipelineScheduleUpdateInput!) {
            pipelineScheduleUpdate(input: $input) {
                pipelineSchedule {
                    id
                    description
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "id": f"gid://gitlab/Ci::PipelineSchedule/{pipeline_schedule_id}",
                "description": description,
                "ref": ref,
                "cron": cron,
                "cronTimezone": cron_timezone,
                "active": active,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_pipeline_schedule(
        self, project_id: Union[int, str], pipeline_schedule_id: int
    ) -> Response:
        """
        Delete a pipeline schedule.

        Args:
            project_id: Project ID or full path.
            pipeline_schedule_id: ID of the pipeline schedule.

        Returns:
            Response: Result of the deletion.
        """
        query = """
        mutation ($input: PipelineScheduleDeleteInput!) {
            pipelineScheduleDelete(input: $input) {
                errors
            }
        }
        """
        variables = {
            "input": {"id": f"gid://gitlab/Ci::PipelineSchedule/{pipeline_schedule_id}"}
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_projects(
        self,
        project_model: Optional[ProjectModel] = None,
        ids: Optional[List[Union[int, str]]] = None,
        full_paths: Optional[List[str]] = None,
        search: Optional[str] = None,
        membership: Optional[bool] = False,
        sort: Optional[str] = "id_desc",
        first: Optional[int] = 20,
        after: Optional[str] = None,
        archived: Optional[str] = None,
        visibility_level: Optional[str] = None,
        min_access_level: Optional[int] = None,
    ) -> Response:
        """
        Fetch a list of projects visible to the current user.

        Args:
            project_model: Optional ProjectModel instance with filter parameters.
            ids: Optional list of project IDs to filter by.
            full_paths: Optional list of full paths to filter by (max 50).
            search: Optional search query for name, path, or description.
            membership: Return only projects the user is a member of.
            sort: Sort order (e.g., 'id_desc', 'name_asc').
            first: Number of projects to fetch.
            after: Cursor for pagination.
            archived: Filter by archived status (e.g., 'ALL', 'YES', 'NO').
            visibility_level: Filter by visibility (e.g., 'PRIVATE').
            min_access_level: Minimum access level for the user.

        Returns:
            Response: List of projects wrapped in Response model.
        """
        if project_model:
            project = project_model
        else:
            project = ProjectModel()

        query = """
        query ($ids: [ID!], $fullPaths: [String!], $search: String, $membership: Boolean, $sort: String, $first: Int, $after: String, $archived: ProjectArchived, $visibilityLevel: VisibilityLevelsEnum, $minAccessLevel: AccessLevelEnum) {
            projects(ids: $ids, fullPaths: $fullPaths, search: $search, membership: $membership, sort: $sort, archived: $archived, visibilityLevel: $visibilityLevel, minAccessLevel: $minAccessLevel, first: $first, after: $after) {
                nodes {
                    id
                    fullPath
                    name
                    description
                    createdAt
                    visibility
                    archived
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
        """
        variables = {"first": first, "sort": sort}

        if ids:
            variables["ids"] = [
                f"gid://gitlab/Project/{id}" if isinstance(id, int) else id
                for id in ids
            ]
        if full_paths:
            if len(full_paths) > 50:
                raise ParameterError("Cannot provide more than 50 full paths")
            variables["fullPaths"] = full_paths
        if search:
            variables["search"] = search
        if membership is not None:
            variables["membership"] = membership
        if after:
            variables["after"] = after
        if archived:
            variables["archived"] = archived.upper()
        if visibility_level:
            variables["visibilityLevel"] = visibility_level.upper()
        if min_access_level:
            variables["minAccessLevel"] = min_access_level

        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_project(self, project_model: ProjectModel) -> Response:
        """
        Fetch a single project by ID or full path.

        Args:
            project_model: ProjectModel instance with project_id or full_path.

        Returns:
            Response: Project data wrapped in Response model.
        """
        query = """
        query ($fullPath: ID!) {
            project(fullPath: $fullPath) {
                id
                fullPath
                name
                description
                createdAt
                visibility
                archived
                repository {
                    rootRef
                }
            }
        }
        """
        variables = {"fullPath": str(project_model.project_id)}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_admin_projects(
        self,
        project_model: Optional[ProjectModel] = None,
        ids: Optional[List[Union[int, str]]] = None,
        full_paths: Optional[List[str]] = None,
        search: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Fetch a list of projects visible to admins (experimental).

        Args:
            project_model: Optional ProjectModel instance with filter parameters.
            ids: Optional list of project IDs.
            full_paths: Optional list of full paths (max 50).
            search: Optional search query.
            first: Number of projects to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of projects.

        Note: Admin-only; experimental in GitLab 18.4+.
        """
        if project_model:
            project = project_model
        else:
            project = ProjectModel()

        query = """
        query ($ids: [ID!], $fullPaths: [String!], $search: String, $first: Int, $after: String) {
            adminProjects(ids: $ids, fullPaths: $fullPaths, search: $search, first: $first, after: $after) {
                nodes {
                    id
                    fullPath
                    name
                    description
                    createdAt
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
        """
        variables = {"first": first}

        if ids:
            variables["ids"] = [
                f"gid://gitlab/Project/{id}" if isinstance(id, int) else id
                for id in ids
            ]
        if full_paths:
            if len(full_paths) > 50:
                raise ParameterError("Cannot provide more than 50 full paths")
            variables["fullPaths"] = full_paths
        if search:
            variables["search"] = search
        if after:
            variables["after"] = after

        return self.execute_gql(query, variables=variables)

    # Jobs
    @require_auth
    def get_jobs(
        self,
        project_id: Union[int, str],
        scope: Optional[List[str]] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get jobs for a project.

        Args:
            project_id: Project ID or full path.
            scope: Optional list of job scopes (e.g., ['success', 'failed']).
            first: Number of jobs to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of jobs.
        """
        job = JobModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                jobs(first: $first, after: $after) {
                    nodes {
                        id
                        name
                        status
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_job(self, project_id: Union[int, str], job_id: int) -> Response:
        """
        Get a specific job.

        Args:
            project_id: Project ID or full path.
            job_id: ID of the job.

        Returns:
            Response: Job details.
        """
        job = JobModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $id: CiJobID!) {
            project(fullPath: $fullPath) {
                job(id: $id) {
                    id
                    name
                    status
                }
            }
        }
        """
        variables = {
            "fullPath": str(project_id),
            "id": f"gid://gitlab/Ci::Job/{job_id}",
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def retry_job(self, project_id: Union[int, str], job_id: int) -> Response:
        """
        Retry a job.

        Args:
            project_id: Project ID or full path.
            job_id: ID of the job.

        Returns:
            Response: Result of the retry operation.
        """
        query = """
        mutation ($input: JobRetryInput!) {
            jobRetry(input: $input) {
                job {
                    id
                    status
                }
                errors
            }
        }
        """
        variables = {"input": {"id": f"gid://gitlab/Ci::Job/{job_id}"}}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def cancel_job(self, project_id: Union[int, str], job_id: int) -> Response:
        """
        Cancel a job.

        Args:
            project_id: Project ID or full path.
            job_id: ID of the job.

        Returns:
            Response: Result of the cancel operation.
        """
        query = """
        mutation ($input: JobCancelInput!) {
            jobCancel(input: $input) {
                job {
                    id
                    status
                }
                errors
            }
        }
        """
        variables = {"input": {"id": f"gid://gitlab/Ci::Job/{job_id}"}}
        return self.execute_gql(query, variables=variables)

    # Packages
    @require_auth
    def get_packages(
        self,
        project_id: Union[int, str],
        package_type: Optional[str] = None,
        package_name: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get packages for a project.

        Args:
            project_id: Project ID or full path.
            package_type: Optional package type filter.
            package_name: Optional package name filter.
            first: Number of packages to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of packages.
        """
        package = PackageModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                packages(first: $first, after: $after) {
                    nodes {
                        id
                        name
                        version
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_package(self, project_id: Union[int, str], package_id: int) -> Response:
        """
        Get a specific package.

        Args:
            project_id: Project ID or full path.
            package_id: ID of the package.

        Returns:
            Response: Package details.
        """
        package = PackageModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $id: PackagesPackageID!) {
            project(fullPath: $fullPath) {
                package(id: $id) {
                    id
                    name
                    version
                }
            }
        }
        """
        variables = {
            "fullPath": str(project_id),
            "id": f"gid://gitlab/Packages::Package/{package_id}",
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_package(self, project_id: Union[int, str], package_id: int) -> Response:
        """
        Delete a package.

        Args:
            project_id: Project ID or full path.
            package_id: ID of the package.

        Returns:
            Response: Result of the deletion.
        """
        query = """
        mutation ($input: PackageDeleteInput!) {
            packageDelete(input: $input) {
                errors
            }
        }
        """
        variables = {"input": {"id": f"gid://gitlab/Packages::Package/{package_id}"}}
        return self.execute_gql(query, variables=variables)

    # Deploy Tokens (Note: Limited GraphQL support)
    @require_auth
    def get_deploy_tokens(
        self,
        project_id: Union[int, str],
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get deploy tokens for a project.

        Args:
            project_id: Project ID or full path.
            first: Number of tokens to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of deploy tokens.

        Note:
            Deploy tokens are not fully supported in GraphQL; consider using REST API.
        """
        raise NotImplementedError(
            "Deploy tokens not available in GitLab GraphQL; use REST API."
        )

    @require_auth
    def create_deploy_token(
        self,
        project_id: Union[int, str],
        name: str,
        scopes: List[str],
        expires_at: Optional[str] = None,
        username: Optional[str] = None,
    ) -> Response:
        """
        Create a deploy token.

        Args:
            project_id: Project ID or full path.
            name: Name of the deploy token.
            scopes: List of scopes for the token.
            expires_at: Optional expiration date.
            username: Optional username for the token.

        Returns:
            Response: Created deploy token.

        Note:
            Deploy tokens are not supported in GraphQL; use REST API.
        """
        raise NotImplementedError(
            "Deploy token creation not available in GitLab GraphQL; use REST API."
        )

    @require_auth
    def delete_deploy_token(
        self, project_id: Union[int, str], deploy_token_id: int
    ) -> Response:
        """
        Delete a deploy token.

        Args:
            project_id: Project ID or full path.
            deploy_token_id: ID of the deploy token.

        Returns:
            Response: Result of the deletion.

        Note:
            Deploy tokens are not supported in GraphQL; use REST API.
        """
        raise NotImplementedError(
            "Deploy token deletion not available in GitLab GraphQL; use REST API."
        )

    # Users
    @require_auth
    def get_users(
        self,
        search: Optional[str] = None,
        username: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get users.

        Args:
            search: Optional search term for users.
            username: Optional specific username filter.
            first: Number of users to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of users.
        """
        user = UserModel()
        query = """
        query ($search: String, $first: Int, $after: String) {
            users(search: $search, first: $first, after: $after) {
                nodes {
                    id
                    username
                    name
                    email
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
        """
        variables = {"first": first}
        if search:
            variables["search"] = search
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_user(self, user_id: int) -> Response:
        """
        Get a specific user.

        Args:
            user_id: ID of the user.

        Returns:
            Response: User details.
        """
        user = UserModel(user_id=user_id)
        query = """
        query ($id: UserID!) {
            user(id: $id) {
                id
                username
                name
                email
            }
        }
        """
        variables = {"id": f"gid://gitlab/User/{user_id}"}
        return self.execute_gql(query, variables=variables)

    # Memberships
    @require_auth
    def get_members(
        self,
        project_id: Union[int, str],
        include_inherited: Optional[bool] = False,
        search: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get members of a project.

        Args:
            project_id: Project ID or full path.
            include_inherited: Include inherited members.
            search: Optional search term.
            first: Number of members to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of members.
        """
        members = MembersModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                projectMembers(first: $first, after: $after) {
                    nodes {
                        id
                        user {
                            username
                        }
                        accessLevel {
                            stringValue
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def add_member(
        self,
        project_id: Union[int, str],
        user_id: int,
        access_level: str,
        expires_at: Optional[str] = None,
    ) -> Response:
        """
        Add a member to a project.

        Args:
            project_id: Project ID or full path.
            user_id: ID of the user to add.
            access_level: Access level (e.g., 'DEVELOPER').
            expires_at: Optional expiration date.

        Returns:
            Response: Added member details.
        """
        members = MembersModel(project_id=project_id)
        query = """
        mutation ($input: ProjectMemberCreateInput!) {
            projectMemberCreate(input: $input) {
                member {
                    id
                    accessLevel {
                        stringValue
                    }
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "userId": f"gid://gitlab/User/{user_id}",
                "accessLevel": access_level,
                "expiresAt": expires_at,
            }
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def update_member(
        self,
        project_id: Union[int, str],
        user_id: int,
        access_level: Optional[str] = None,
        expires_at: Optional[str] = None,
    ) -> Response:
        """
        Update a project member.

        Args:
            project_id: Project ID or full path.
            user_id: ID of the user.
            access_level: Updated access level.
            expires_at: Updated expiration date.

        Returns:
            Response: Updated member details.
        """
        query = """
        mutation ($input: ProjectMemberUpdateInput!) {
            projectMemberUpdate(input: $input) {
                member {
                    id
                    accessLevel {
                        stringValue
                    }
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "id": f"gid://gitlab/ProjectMember/{project_id}:{user_id}",
                "accessLevel": access_level,
                "expiresAt": expires_at,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_member(self, project_id: Union[int, str], user_id: int) -> Response:
        """
        Remove a member from a project.

        Args:
            project_id: Project ID or full path.
            user_id: ID of the user to remove.

        Returns:
            Response: Result of the deletion.
        """
        query = """
        mutation ($input: ProjectMemberDeleteInput!) {
            projectMemberDelete(input: $input) {
                errors
            }
        }
        """
        variables = {
            "input": {"id": f"gid://gitlab/ProjectMember/{project_id}:{user_id}"}
        }
        return self.execute_gql(query, variables=variables)

    # Releases
    @require_auth
    def get_releases(
        self,
        project_id: Union[int, str],
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get releases for a project.

        Args:
            project_id: Project ID or full path.
            first: Number of releases to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of releases.
        """
        release = ReleaseModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                releases(first: $first, after: $after) {
                    nodes {
                        tagName
                        name
                        description
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_release(self, project_id: Union[int, str], tag_name: str) -> Response:
        """
        Get a specific release.

        Args:
            project_id: Project ID or full path.
            tag_name: Name of the release tag.

        Returns:
            Response: Release details.
        """
        release = ReleaseModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $tagName: String!) {
            project(fullPath: $fullPath) {
                release(tagName: $tagName) {
                    tagName
                    name
                    description
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "tagName": tag_name}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_release(
        self,
        project_id: Union[int, str],
        tag_name: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        ref: Optional[str] = None,
    ) -> Response:
        """
        Create a release.

        Args:
            project_id: Project ID or full path.
            tag_name: Name of the tag for the release.
            name: Optional name of the release.
            description: Optional description.
            ref: Optional reference (commit SHA, branch).

        Returns:
            Response: Created release.
        """
        release = ReleaseModel(project_id=project_id)
        query = """
        mutation ($input: ReleaseCreateInput!) {
            releaseCreate(input: $input) {
                release {
                    tagName
                    name
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "tagName": tag_name,
                "name": name,
                "description": description,
                "ref": ref,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def update_release(
        self,
        project_id: Union[int, str],
        tag_name: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Response:
        """
        Update a release.

        Args:
            project_id: Project ID or full path.
            tag_name: Name of the release tag.
            name: Updated name.
            description: Updated description.

        Returns:
            Response: Updated release.
        """
        query = """
        mutation ($input: ReleaseUpdateInput!) {
            releaseUpdate(input: $input) {
                release {
                    tagName
                    name
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "tagName": tag_name,
                "name": name,
                "description": description,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_release(self, project_id: Union[int, str], tag_name: str) -> Response:
        """
        Delete a release.

        Args:
            project_id: Project ID or full path.
            tag_name: Name of the release tag.

        Returns:
            Response: Result of the deletion.
        """
        query = """
        mutation ($input: ReleaseDeleteInput!) {
            releaseDelete(input: $input) {
                errors
            }
        }
        """
        variables = {"input": {"projectPath": str(project_id), "tagName": tag_name}}
        return self.execute_gql(query, variables=variables)

    # Issues
    @require_auth
    def get_issues(
        self,
        project_id: Union[int, str],
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        milestone: Optional[str] = None,
        author_username: Optional[str] = None,
        assignee_username: Optional[str] = None,
        search: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get issues for a project.

        Args:
            project_id: Project ID or full path.
            state: Optional issue state (e.g., 'opened', 'closed').
            labels: Optional list of labels.
            milestone: Optional milestone title.
            author_username: Optional author username.
            assignee_username: Optional assignee username.
            search: Optional search term.
            first: Number of issues to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of issues.
        """
        issue = IssueModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $state: IssueState, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                issues(state: $state, first: $first, after: $after) {
                    nodes {
                        iid
                        title
                        state
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if state:
            variables["state"] = state
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_issue(self, project_id: Union[int, str], issue_iid: int) -> Response:
        """
        Get a specific issue.

        Args:
            project_id: Project ID or full path.
            issue_iid: Internal ID of the issue.

        Returns:
            Response: Issue details.
        """
        issue = IssueModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $iid: String!) {
            project(fullPath: $fullPath) {
                issue(iid: $iid) {
                    iid
                    title
                    state
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "iid": str(issue_iid)}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_issue(
        self,
        project_id: Union[int, str],
        title: str,
        description: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Response:
        """
        Create an issue.

        Args:
            project_id: Project ID or full path.
            title: Title of the issue.
            description: Optional description.
            labels: Optional list of labels.

        Returns:
            Response: Created issue.
        """
        issue = IssueModel(project_id=project_id)
        query = """
        mutation ($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                issue {
                    iid
                    title
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "title": title,
                "description": description,
                "labels": labels,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def update_issue(
        self,
        project_id: Union[int, str],
        issue_iid: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        state_event: Optional[str] = None,
    ) -> Response:
        """
        Update an issue.

        Args:
            project_id: Project ID or full path.
            issue_iid: Internal ID of the issue.
            title: Updated title.
            description: Updated description.
            state_event: Optional state change (e.g., 'CLOSE').

        Returns:
            Response: Updated issue.
        """
        query = """
        mutation ($input: IssueUpdateInput!) {
            issueUpdate(input: $input) {
                issue {
                    iid
                    title
                    state
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "iid": str(issue_iid),
                "title": title,
                "description": description,
                "stateEvent": state_event,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_issue(self, project_id: Union[int, str], issue_iid: int) -> Response:
        """
        Delete an issue.

        Args:
            project_id: Project ID or full path.
            issue_iid: Internal ID of the issue.

        Returns:
            Response: Result of the deletion.
        """
        query = """
        mutation ($input: IssueDeleteInput!) {
            issueDelete(input: $input) {
                errors
            }
        }
        """
        variables = {"input": {"projectPath": str(project_id), "iid": str(issue_iid)}}
        return self.execute_gql(query, variables=variables)

    # To-Dos
    @require_auth
    def get_to_dos(
        self,
        project_id: Union[int, str] = None,
        state: Optional[str] = None,
        type: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get to-dos for a user or project.

        Args:
            project_id: Optional project ID or full path.
            state: Optional to-do state (e.g., 'pending').
            type: Optional to-do type.
            first: Number of to-dos to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of to-dos.
        """
        query = """
        query ($first: Int, $after: String) {
            currentUser {
                todos(first: $first, after: $after) {
                    nodes {
                        id
                        state
                        targetType
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    # Environments
    @require_auth
    def get_environments(
        self,
        project_id: Union[int, str],
        name: Optional[str] = None,
        search: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get environments for a project.

        Args:
            project_id: Project ID or full path.
            name: Optional environment name filter.
            search: Optional search term.
            first: Number of environments to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of environments.
        """
        query = """
        query ($fullPath: ID!, $name: String, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                environments(name: $name, first: $first, after: $after) {
                    nodes {
                        id
                        name
                        state
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if name:
            variables["name"] = name
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_environment(
        self, project_id: Union[int, str], name: str, external_url: Optional[str] = None
    ) -> Response:
        """
        Create an environment.

        Args:
            project_id: Project ID or full path.
            name: Name of the environment.
            external_url: Optional external URL.

        Returns:
            Response: Created environment.
        """
        query = """
        mutation ($input: EnvironmentCreateInput!) {
            environmentCreate(input: $input) {
                environment {
                    id
                    name
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "name": name,
                "externalUrl": external_url,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def update_environment(
        self,
        project_id: Union[int, str],
        environment_id: int,
        name: Optional[str] = None,
        external_url: Optional[str] = None,
    ) -> Response:
        """
        Update an environment.

        Args:
            project_id: Project ID or full path.
            environment_id: ID of the environment.
            name: Updated name.
            external_url: Updated external URL.

        Returns:
            Response: Updated environment.
        """
        query = """
        mutation ($input: EnvironmentUpdateInput!) {
            environmentUpdate(input: $input) {
                environment {
                    id
                    name
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "id": f"gid://gitlab/Environment/{environment_id}",
                "name": name,
                "externalUrl": external_url,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_environment(
        self, project_id: Union[int, str], environment_id: int
    ) -> Response:
        """
        Delete an environment.

        Args:
            project_id: Project ID or full path.
            environment_id: ID of the environment.

        Returns:
            Response: Result of the deletion.
        """
        query = """
        mutation ($input: EnvironmentDeleteInput!) {
            environmentDelete(input: $input) {
                errors
            }
        }
        """
        variables = {"input": {"id": f"gid://gitlab/Environment/{environment_id}"}}
        return self.execute_gql(query, variables=variables)

    # Test Reports
    @require_auth
    def get_test_reports(
        self,
        project_id: Union[int, str],
        pipeline_id: Optional[int] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get test reports for a project or pipeline.

        Args:
            project_id: Project ID or full path.
            pipeline_id: Optional pipeline ID.
            first: Number of test reports to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of test reports.
        """
        query = """
        query ($fullPath: ID!, $pipelineId: CiPipelineID, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                pipelines(id: $pipelineId, first: $first, after: $after) {
                    nodes {
                        testReports {
                            totalTime
                            totalCount
                            successCount
                            failedCount
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if pipeline_id:
            variables["pipelineId"] = f"gid://gitlab/Ci::Pipeline/{pipeline_id}"
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    # Namespaces
    @require_auth
    def get_namespaces(
        self,
        search: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get namespaces.

        Args:
            search: Optional search term.
            first: Number of namespaces to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of namespaces.
        """
        namespace = NamespaceModel()
        query = """
        query ($search: String, $first: Int, $after: String) {
            namespaces(search: $search, first: $first, after: $after) {
                nodes {
                    id
                    fullPath
                    name
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
        """
        variables = {"first": first}
        if search:
            variables["search"] = search
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_namespace(self, namespace_id: Union[int, str]) -> Response:
        """
        Get a specific namespace.

        Args:
            namespace_id: ID or full path of the namespace.

        Returns:
            Response: Namespace details.
        """
        namespace = NamespaceModel(namespace_id=namespace_id)
        query = """
        query ($fullPath: ID!) {
            namespace(fullPath: $fullPath) {
                id
                fullPath
                name
            }
        }
        """
        variables = {"fullPath": str(namespace_id)}
        return self.execute_gql(query, variables=variables)

    # Groups
    @require_auth
    def get_groups(
        self,
        search: Optional[str] = None,
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get groups.

        Args:
            search: Optional search term.
            first: Number of groups to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of groups.
        """
        group = GroupModel()
        query = """
        query ($search: String, $first: Int, $after: String) {
            groups(search: $search, first: $first, after: $after) {
                nodes {
                    id
                    fullPath
                    name
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
        """
        variables = {"first": first}
        if search:
            variables["search"] = search
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_group(self, group_id: Union[int, str]) -> Response:
        """
        Get a specific group.

        Args:
            group_id: ID or full path of the group.

        Returns:
            Response: Group details.
        """
        group = GroupModel(group_id=group_id)
        query = """
        query ($fullPath: ID!) {
            group(fullPath: $fullPath) {
                id
                fullPath
                name
            }
        }
        """
        variables = {"fullPath": str(group_id)}
        return self.execute_gql(query, variables=variables)

    # Wikis
    @require_auth
    def get_wiki_pages(
        self,
        project_id: Union[int, str],
        first: Optional[int] = 20,
        after: Optional[str] = None,
    ) -> Response:
        """
        Get wiki pages for a project.

        Args:
            project_id: Project ID or full path.
            first: Number of wiki pages to fetch.
            after: Cursor for pagination.

        Returns:
            Response: List of wiki pages.
        """
        wiki = WikiModel(project_id=project_id)
        query = """
        query ($fullPath: ID!, $first: Int, $after: String) {
            project(fullPath: $fullPath) {
                wiki {
                    pages(first: $first, after: $after) {
                        nodes {
                            slug
                            title
                            content
                        }
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "first": first}
        if after:
            variables["after"] = after
        return self.execute_gql(query, variables=variables)

    @require_auth
    def get_wiki_page(self, project_id: Union[int, str], slug: str) -> Response:
        """
        Get a specific wiki page.

        Args:
            project_id: Project ID or full path.
            slug: Slug of the wiki page.

        Returns:
            Response: Wiki page details.
        """
        wiki = WikiModel(project_id=project_id, slug=slug)
        query = """
        query ($fullPath: ID!, $slug: String!) {
            project(fullPath: $fullPath) {
                wiki {
                    page(slug: $slug) {
                        slug
                        title
                        content
                    }
                }
            }
        }
        """
        variables = {"fullPath": str(project_id), "slug": slug}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def create_wiki_page(
        self,
        project_id: Union[int, str],
        title: str,
        content: str,
        format_type: Optional[str] = None,
    ) -> Response:
        """
        Create a wiki page.

        Args:
            project_id: Project ID or full path.
            title: Title of the wiki page.
            content: Content of the wiki page.
            format_type: Optional format (e.g., 'markdown').

        Returns:
            Response: Created wiki page.
        """
        wiki = WikiModel(project_id=project_id, title=title, content=content)
        query = """
        mutation ($input: WikiPageCreateInput!) {
            wikiPageCreate(input: $input) {
                wikiPage {
                    slug
                    title
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "title": title,
                "content": content,
                "format": format_type or "MARKDOWN",
            }
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def update_wiki_page(
        self,
        project_id: Union[int, str],
        slug: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        format_type: Optional[str] = None,
    ) -> Response:
        """
        Update a wiki page.

        Args:
            project_id: Project ID or full path.
            slug: Slug of the wiki page.
            title: Updated title.
            content: Updated content.
            format_type: Updated format.

        Returns:
            Response: Updated wiki page.
        """
        wiki = WikiModel(project_id=project_id, slug=slug)
        query = """
        mutation ($input: WikiPageUpdateInput!) {
            wikiPageUpdate(input: $input) {
                wikiPage {
                    slug
                    title
                }
                errors
            }
        }
        """
        variables = {
            "input": {
                "projectPath": str(project_id),
                "slug": slug,
                "title": title,
                "content": content,
                "format": format_type,
            }
        }
        variables["input"] = {
            k: v for k, v in variables["input"].items() if v is not None
        }
        return self.execute_gql(query, variables=variables)

    @require_auth
    def delete_wiki_page(self, project_id: Union[int, str], slug: str) -> Response:
        """
        Delete a wiki page.

        Args:
            project_id: Project ID or full path.
            slug: Slug of the wiki page.

        Returns:
            Response: Result of the deletion.
        """
        wiki = WikiModel(project_id=project_id, slug=slug)
        query = """
        mutation ($input: WikiPageDeleteInput!) {
            wikiPageDelete(input: $input) {
                errors
            }
        }
        """
        variables = {"input": {"projectPath": str(project_id), "slug": slug}}
        return self.execute_gql(query, variables=variables)

    @require_auth
    def upload_wiki_page_attachment(
        self, project_id: Union[int, str], file: str, branch: Optional[str] = None
    ) -> Response:
        """
        Upload an attachment to a wiki page.

        Args:
            project_id: Project ID or full path.
            file: Path to the file to upload.
            branch: Optional branch for the wiki.

        Returns:
            Response: Result of the upload.

        Note:
            File uploads are not directly supported in GraphQL; use REST API.
        """
        raise NotImplementedError(
            "Wiki attachment upload not available in GitLab GraphQL; use REST API."
        )

    def close(self):
        if hasattr(self, "client") and self.client:
            self.client.close()
            logging.debug("GraphQL client closed")
