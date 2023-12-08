#!/usr/bin/python
# coding: utf-8

import json
import requests
import urllib3
from base64 import b64encode
from typing import Union
from gitlab_models import (BranchModel, CommitModel, DeployTokenModel, GroupModel, JobModel, MembersModel,
                           PackageModel, ProjectModel, MergeRequestModel, MergeRequestRuleModel)
from pydantic import ValidationError

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

        response = self._session.get(f'{self.url}/projects', headers=self.headers, verify=self.verify)

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
    def get_branches(self, branch: BranchModel):
        try:
            response = self._session.get(
                f'{self.url}/projects/{branch.project_id}/repository/branches',
                headers=self.headers,
                verify=self.verify)

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_branch(self, branch: BranchModel):
        try:
            response = self._session.get(
                f'{self.url}/projects/{branch.project_id}/repository/branches/{branch.branch}',
                headers=self.headers,
                verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_branch(self, branch: BranchModel):
        try:
            response = self._session.post(
                f'{self.url}/projects/{branch.project_id}/repository/branches/{branch.branch}',
                headers=self.headers,
                verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_branch(self, branch: BranchModel):
        try:
            response = self._session.delete(f'{self.url}/projects/{branch.project_id}'
                                            f'/repository/branches?branch={branch.branch}',
                                            headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_merged_branches(self, branch: BranchModel):
        try:
            response = self._session.delete(f'{self.url}/projects/{branch.project_id}'
                                            f'/repository/merged_branches',
                                            headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                 Commits API                                                      #
    ####################################################################################################################
    @require_auth
    def get_commits(self, commit: CommitModel):
        try:
            response = self._session.get(f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit(self, commit: CommitModel):
        try:
            response = self._session.get(f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_references(self, commit: CommitModel):
        try:
            response = self._session.get(f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/refs',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def cherry_pick_commit(self, commit: CommitModel):
        try:
            response = self._session.post(f'{self.url}/projects/{commit.project_id}'
                                          f'/repository/commits/{commit.commit_hash}/cherry_pick',
                                          headers=self.headers, data=commit.data, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_commit(self, commit: CommitModel):
        try:
            response = self._session.post(f'{self.url}/projects/{commit.project_id}'
                                          f'/repository/commits',
                                          headers=self.headers, data=commit.data, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def revert_commit(self, commit: CommitModel):
        try:
            response = self._session.post(f'{self.url}/projects/{commit.project_id}'
                                          f'/repository/commits/{commit.commit_hash}/revert',
                                          headers=self.headers, data=commit.data, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_diff(self, commit: CommitModel):
        try:
            response = self._session.get(f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/diff',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_comments(self, commit: CommitModel):
        try:
            response = self._session.get(f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/comments',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_commit_comment(self, commit: CommitModel):
        try:
            response = self._session.post(f'{self.url}/projects/{commit.project_id}'
                                          f'/repository/commits/{commit.commit_hash}/comments',
                                          headers=self.headers, data=commit.data, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_discussions(self, commit: CommitModel):
        try:
            response = self._session.get(f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/discussions',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_statuses(self, commit: CommitModel):
        try:
            response = self._session.get(f'{self.url}/projects/{commit.project_id}'
                                         f'/repository/commits/{commit.commit_hash}/statuses',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def post_build_status_to_commit(self, commit: CommitModel):
        try:
            response = self._session.post(f'{self.url}/projects/{commit.project_id}'
                                          f'/statuses/{commit.commit_hash}/',
                                          headers=self.headers, data=commit.data, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_merge_requests(self, commit: CommitModel):
        try:
            response = self._session.get(
                f'{self.url}/projects/{commit.project_id}'
                f'/repository/commits/{commit.commit_hash}/merge_requests',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_commit_gpg_signature(self, commit: CommitModel):
        try:
            response = self._session.get(
                f'{self.url}/projects/{commit.project_id}'
                f'/repository/commits/{commit.commit_hash}/merge_requests',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                Deploy Tokens API                                                 #
    ####################################################################################################################
    @require_auth
    def get_deploy_tokens(self, deploy_token: DeployTokenModel):
        try:
            response = self._session.get(f'{self.url}/deploy_tokens', headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_deploy_tokens(self, deploy_token: DeployTokenModel):
        try:
            response = self._session.get(f'{self.url}/projects/{deploy_token.project_id}/deploy_tokens',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_deploy_token(self, deploy_token: DeployTokenModel):
        try:
            response = self._session.get(
                f'{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.token}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_project_deploy_token(self, deploy_token: DeployTokenModel):
        if deploy_token.project_id is None or deploy_token.name is None or deploy_token.scopes is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{deploy_token.project_id}/deploy_tokens',
                                          headers=self.headers,
                                          data=json.dumps(deploy_token.model_dump(exclude_none=True), indent=4),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_project_deploy_token(self, deploy_token: DeployTokenModel):
        if deploy_token.project_id is None or deploy_token.token is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                f'{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.token}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_deploy_tokens(self, deploy_token: DeployTokenModel):
        if deploy_token.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/groups/{deploy_token.group_id}/deploy_tokens',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_deploy_token(self, deploy_token: DeployTokenModel):
        if deploy_token.group_id is None or deploy_token.token is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                f'{self.url}/groups/{deploy_token.group_id}/deploy_tokens/{deploy_token.token}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_group_deploy_token(self, deploy_token: DeployTokenModel):
        deploy_token_dict = deploy_token.dict(exclude_none=True)
        if deploy_token.group_id is None or deploy_token.name is None or deploy_token.scopes is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/groups/{deploy_token.group_id}/deploy_tokens',
                                          headers=self.headers, data=json.dumps(deploy_token_dict, indent=4),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_group_deploy_token(self, deploy_token: DeployTokenModel):
        if deploy_token.group_id is None or deploy_token.token is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                f'{self.url}/groups/{deploy_token.group_id}/deploy_tokens/{deploy_token.token}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                Groups API                                                        #
    ####################################################################################################################
    @require_auth
    def get_groups(self, group: GroupModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/groups{group.api_parameters}', headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group(self, group: GroupModel):
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}'
                                         f'/groups/{group.group_id}', headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_subgroups(self, group: GroupModel):
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}'
                                         f'/groups/{group.group_id}'
                                         f'/subgroups', headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_descendant_groups(self, group: GroupModel):
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}'
                                         f'/groups/{group.group_id}'
                                         f'/descendant_groups',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_projects(self, group: GroupModel):
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}'
                                         f'/groups/{group.group_id}'
                                         f'/projects{group.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_merge_requests(self, group: GroupModel):
        if group.group_id is None or group.argument is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}'
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
    def get_project_jobs(self, job: JobModel):
        if job.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{job.project_id}/jobs{job.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_job(self, job: JobModel):
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_job_log(self, job: JobModel):
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/trace',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def cancel_project_job(self, job: JobModel):
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/cancel',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def retry_project_job(self, job: JobModel):
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/retry',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def erase_project_job(self, job: JobModel):
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/erase',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def run_project_job(self, job: JobModel):
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{job.project_id}/jobs/{job.job_id}/play',
                                          headers=self.headers, data=job.data, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_pipeline_jobs(self, job: JobModel):
        if job.project_id is None or job.pipeline_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                f'{self.url}/projects/{job.project_id}/pipelines/{job.pipeline_id}/jobs{job.api_parameters}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                               Members API                                                        #
    ####################################################################################################################
    @require_auth
    def get_group_members(self, members: MembersModel):
        if members.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/groups/{members.group_id}/members{members.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_members(self, members: MembersModel):
        if members.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{members.project_id}/members{members.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                            Merge Request API                                                     #
    ####################################################################################################################
    @require_auth
    def create_merge_request(self, merge_request: MergeRequestModel):
        if (merge_request.project_id is None
                or merge_request.source_branch is None
                or merge_request.target_branch is None
                or merge_request.title is None):
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{merge_request.project_id}/merge_requests',
                                          headers=self.headers,
                                          data=json.dumps(merge_request.data, indent=2), verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_merge_requests(self, merge_request: MergeRequestModel):
        try:
            response = self._session.get(f'{self.url}/merge_requests?per_page={merge_request.per_page}&x-total-pages',
                                         headers=self.headers,
                                         verify=self.verify)
            total_pages = int(response.headers['X-Total-Pages'])
            response = []
            if merge_request.max_pages == 0 or merge_request.max_pages > total_pages:
                merge_request.max_pages = total_pages
            for page in range(0, merge_request.max_pages):
                response_page = self._session.get(
                    f'{self.url}/merge_requests{merge_request.api_parameters}&per_page={merge_request.per_page}&page={page}',
                    headers=self.headers, verify=self.verify)
                response_page = json.loads(response_page.text.replace("'", "\""))
                response = response + response_page
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_merge_requests(self, merge_request: MergeRequestModel):
        try:
            response = self._session.get(f'{self.url}/projects/{merge_request.project_id}/merge_requests',
                                         headers=self.headers, verify=self.verify)

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_merge_request(self, merge_request: MergeRequestModel):
        if merge_request.project_id is None or merge_request.merge_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{merge_request.project_id}'
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
    def get_project_level_rules(self, merge_rule: MergeRequestRuleModel):
        try:
            response = self._session.get(f'{self.url}/projects/{merge_rule.project_id}/approval_rules',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_level_rule(self, merge_rule: MergeRequestRuleModel):
        try:
            response = self._session.get(
                f'{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}',
                headers=self.headers,
                verify=self.verify)

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_project_level_rule(self, merge_rule: MergeRequestRuleModel):
        try:
            response = self._session.post(f'{self.url}/projects/{merge_rule.project_id}/approval_rules',
                                          headers=self.headers,
                                          data=merge_rule.data,
                                          verify=self.verify)

        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_project_level_rule(self, merge_rule: MergeRequestRuleModel):
        try:
            response = self._session.put(f'{self.url}/projects/{merge_rule.project_id}'
                                         f'/approval_rules/{merge_rule.approval_rule_id}',
                                         headers=self.headers, data=merge_rule.data, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_project_level_rule(self, merge_rule: MergeRequestRuleModel):
        try:
            response = self._session.put(f'{self.url}/projects/{merge_rule.project_id}'
                                         f'/approval_rules/{merge_rule.approval_rule_id}',
                                         headers=self.headers, data=merge_rule.data, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def merge_request_level_approvals(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approvals',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_approval_state_merge_requests(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        response = self._session.get(
            f'{self.url}/projects/{merge_rule.project_id}'
            f'/merge_requests/{merge_rule.merge_request_iid}/approval_state',
            headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_merge_request_level_rules(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        response = self._session.get(
            f'{self.url}/projects/{merge_rule.project_id}'
            f'/merge_requests/{merge_rule.merge_request_iid}/approval_rules',
            headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def approve_merge_request(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{merge_rule.project_id}'
                                      f'/merge_requests/{merge_rule.merge_request_iid}/approve',
                                      headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def unapprove_merge_request(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{merge_rule.project_id}'
                                      f'/merge_requests/{merge_rule.merge_request_iid}/unapprove',
                                      headers=self.headers, verify=self.verify)
        return response

    ####################################################################################################################
    #                                               Packages API                                                       #
    ####################################################################################################################
    def get_repository_packages(self, package: PackageModel):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/packages', headers=self.headers,
                                     verify=self.verify)
        return response


    ####################################################################################################################
    #                                                Pipeline API                                                      #
    ####################################################################################################################
    @require_auth
    def get_pipelines(self, project_id: Union[int, str] = None, per_page: int = 100, page: int = 1):
        if project_id is None:
            raise MissingParameterError
        api_parameters = f"?per_page={per_page}"
        response = self._session.get(f'{self.url}/projects/{project_id}/pipelines?per_page={per_page}',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_pipeline(self, project_id: Union[int, str] = None, pipeline_id: Union[int, str] = None):
        if project_id is None or pipeline_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/pipelines/{pipeline_id}', headers=self.headers,
                                     verify=self.verify)
        return response

    @require_auth
    def run_pipeline(self, project_id: Union[int, str] = None, reference: str = None, variables: dict = None):
        if project_id is None or reference is None:
            raise MissingParameterError
        if variables:
            data = json.dumps(variables, indent=4)
            response = self._session.post(f'{self.url}/projects/{project_id}/pipeline?ref={reference}',
                                          headers=self.headers,
                                          data=data, verify=self.verify)
        else:
            response = self._session.post(f'{self.url}/projects/{project_id}/pipeline?ref={reference}',
                                          headers=self.headers,
                                          verify=self.verify)
        return response

    ####################################################################################################################
    #                                                Projects API                                                      #
    ####################################################################################################################
    @require_auth
    def get_projects(self, max_pages: int = 0, per_page: int = 100,
                     order_by: str = 'updated'):
        response = self._session.get(f'{self.url}/projects?per_page={per_page}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        if order_by == 'updated':
            order_by = 'updated_at'
        else:
            order_by = 'updated_at'
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, max_pages):
            response_page = self._session.get(
                f'{self.url}/projects?per_page={per_page}&page={page}&order_by={order_by}',
                headers=self.headers, verify=self.verify)
            response_page = json.loads(response_page.text.replace("'", "\""))
            response = response + response_page
        return response

    @require_auth
    def get_project(self, project_id: Union[int, str] = None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}', headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_nested_projects_by_group(self, group_id: Union[int, str] = None, max_pages: int = 0, per_page: int = 100):
        if group_id is None:
            raise MissingParameterError
        projects = []
        groups = [self.get_group(group_id=group_id)]
        groups = groups + self.get_group_subgroups(group_id=group_id)
        for group in groups:
            response = self._session.get(f'{self.url}/groups/{group["id"]}/projects?per_page={per_page}&x-total-pages',
                                         headers=self.headers, verify=self.verify)
            total_pages = int(response.headers['X-Total-Pages'])
            if max_pages == 0 or max_pages > total_pages:
                max_pages = total_pages
            for page in range(0, max_pages):
                group_projects = self._session.get(f'{self.url}/groups/{group["id"]}/'
                                                   f'projects?per_page={per_page}&page={page}',
                                                   headers=self.headers, verify=self.verify)
                group_projects = json.loads(group_projects.text)
                projects = projects + group_projects
        return projects

    @require_auth
    def get_project_contributors(self, project_id: Union[int, str] = None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/contributors',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_project_statistics(self, project_id: Union[int, str] = None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}?statistics=true',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def edit_project(self, project: ProjectModel):
        try:
            response = self._session.put(f'{self.url}/projects/{project.project_id}',
                                         data=project.model_dump_json(),
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_groups(self, project: ProjectModel):
        try:
            response = self._session.get(f'{self.url}/projects/{project.project_id}/groups',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def archive_project(self, project: ProjectModel):
        try:
            response = self._session.post(f'{self.url}/projects/{project.project_id}/archive',
                                          headers=self.headers,
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def unarchive_project(self, project_id: Union[int, str] = None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/unarchive', headers=self.headers,
                                      verify=self.verify)
        return response

    @require_auth
    def delete_project(self, project_id: Union[int, str] = None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}', headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def share_project(self, project_id: Union[int, str] = None, group_id: Union[int, str] = None,
                      group_access: int = None,
                      expires_at: str = None):
        if project_id is None or group_id is None or group_access is None:
            raise MissingParameterError
        share_filter = None
        if group_id:
            if not isinstance(group_id, int):
                raise ParameterError
            if share_filter:
                share_filter = f'{share_filter}&group_id={group_id}'
            else:
                share_filter = f'?group_id={group_id}'
        if group_access:
            if not isinstance(group_access, int):
                raise ParameterError
            if share_filter:
                share_filter = f'{share_filter}&group_access={group_access}'
            else:
                share_filter = f'?group_access={group_access}'
        if expires_at:
            if not isinstance(expires_at, str):
                raise ParameterError
            if share_filter:
                share_filter = f'{share_filter}&expires_at={expires_at}'
            else:
                share_filter = f'?expires_at={expires_at}'
        response = self._session.post(f'{self.url}/projects/{project_id}/share{share_filter}',
                                      headers=self.headers, verify=self.verify)
        return response

    ####################################################################################################################
    #                                       Protected Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_protected_branches(self, project_id: Union[int, str] = None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/protected_branches',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_protected_branch(self, project_id: Union[int, str] = None, branch: str = None):
        if project_id is None or branch is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/protected_branches/{branch}',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def protect_branch(self, project_id: Union[int, str] = None, branch: str = None, push_access_level: int = None,
                       merge_access_level: int = None, unprotect_access_level: int = None,
                       allow_force_push: list = None,
                       allowed_to_push: list = None, allowed_to_merge: list = None,
                       allowed_to_unprotect: list = None, code_owner_approval_required: bool = None):
        if project_id is None or branch is None:
            raise MissingParameterError
        branch_filter = None
        data = {}
        if branch:
            if not isinstance(branch, str):
                raise ParameterError
            branch_filter = f'?name={branch}'
        if push_access_level:
            if not isinstance(push_access_level, int):
                raise ParameterError
            branch_filter = f'{branch_filter}&push_access_level={push_access_level}'
        if merge_access_level:
            if not isinstance(merge_access_level, int):
                raise ParameterError
            branch_filter = f'{branch_filter}&merge_access_level={merge_access_level}'
        if unprotect_access_level:
            if not isinstance(branch, int):
                raise ParameterError
            branch_filter = f'{branch_filter}&unprotect_access_level={unprotect_access_level}'
        if allow_force_push:
            if not isinstance(allow_force_push, list):
                raise ParameterError
            data['allow_force_push'] = allow_force_push
        if allowed_to_push:
            if not isinstance(allowed_to_push, list):
                raise ParameterError
            data['allowed_to_push'] = allowed_to_push
        if allowed_to_merge:
            if not isinstance(allowed_to_merge, list):
                raise ParameterError
            data['allowed_to_merge'] = allowed_to_merge
        if allowed_to_unprotect:
            if not isinstance(allowed_to_unprotect, list):
                raise ParameterError
            data['allowed_to_unprotect'] = allowed_to_unprotect
        if code_owner_approval_required:
            if not isinstance(code_owner_approval_required, bool):
                raise ParameterError
            data['code_owner_approval_required'] = code_owner_approval_required

        if len(data) > 0:
            data = json.dumps(data, indent=4)
            response = self._session.post(f'{self.url}/projects/{project_id}/protected_branches{branch_filter}',
                                          headers=self.headers, data=data, verify=self.verify)
        else:
            response = self._session.post(f'{self.url}/projects/{project_id}/protected_branches{branch_filter}',
                                          headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def unprotect_branch(self, project_id: Union[int, str] = None, branch: str = None):
        if project_id is None or branch is None:
            raise MissingParameterError
        self._session.delete(f'{self.url}/projects/{project_id}/protected_branches/{branch}',
                             headers=self.headers, verify=self.verify)

    @require_auth
    def require_code_owner_approvals_single_branch(self, project_id: Union[int, str] = None, branch: str = None):
        if project_id is None or branch is None:
            raise MissingParameterError
        response = self._session.patch(f'{self.url}/projects/{project_id}/protected_branches/{branch}',
                                       headers=self.headers, verify=self.verify)
        return response

    ####################################################################################################################
    #                                                Runners API                                                       #
    ####################################################################################################################
    @require_auth
    def get_runners(self, runner_type: str = None, status: str = None, paused: bool = None, tag_list: list = None,
                    all_runners: bool = False):
        runner_filter = None
        if all_runners:
            runner_filter = '/all'
        if runner_type:
            if runner_type not in ['instance_type', 'group_type', 'project_type']:
                raise ParameterError
            if runner_filter and runner_filter != "/all":
                runner_filter = f'{runner_filter}&type={runner_type}'
            else:
                runner_filter = f'?type={runner_type}'
        if status:
            if status not in ['online', 'offline', 'stale', 'never_contacted', 'active', 'paused']:
                raise ParameterError
            if runner_filter and runner_filter != "/all":
                runner_filter = f'{runner_filter}&status={status}'
            else:
                runner_filter = f'?status={status}'
        if paused:
            if not isinstance(paused, bool):
                raise ParameterError
            if runner_filter and runner_filter != "/all":
                runner_filter = f'{runner_filter}&paused={paused}'
            else:
                runner_filter = f'?paused={paused}'
        if tag_list:
            if not isinstance(tag_list, list):
                raise ParameterError
            if runner_filter and runner_filter != "/all":
                runner_filter = f'{runner_filter}&tag_list={tag_list}'
            else:
                runner_filter = f'?tag_list={tag_list}'
        if runner_filter and runner_filter != "/all":
            print(f"REQUEST: {self.url}/runners{runner_filter}")
            response = self._session.get(f'{self.url}/runners{runner_filter}', headers=self.headers, verify=self.verify)
            try:
                return response.json()
            except ValueError:
                return response
        else:
            raise ParameterError

    @require_auth
    def get_runner(self, runner_id: Union[int, str] = None):
        if runner_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/runners/{runner_id}', headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def update_runner_details(self, runner_id: Union[int, str] = None, description: str = None, active: bool = None,
                              paused: bool = None, tag_list: list = None, run_untagged: bool = None,
                              locked: bool = None,
                              access_level: str = None, maximum_timeout: int = None):
        if runner_id is None:
            raise MissingParameterError
        data = {}
        if description:
            if not isinstance(active, str):
                raise ParameterError
            data['description'] = description
        if active:
            if not isinstance(active, bool):
                raise ParameterError
            data['active'] = active
        if paused:
            if not isinstance(paused, bool):
                raise ParameterError
            data['paused'] = paused
        if tag_list:
            if not isinstance(tag_list, list):
                raise ParameterError
            data['tag_list'] = tag_list
        if run_untagged:
            if not isinstance(run_untagged, bool):
                raise ParameterError
            data['run_untagged'] = run_untagged
        if locked:
            if not isinstance(locked, bool):
                raise ParameterError
            data['locked'] = locked
        if access_level:
            if access_level not in ['not_protected', 'ref_protected']:
                raise ParameterError
            data['access_level'] = access_level
        if maximum_timeout:
            if not isinstance(maximum_timeout, int):
                raise ParameterError
            data['maximum_timeout'] = maximum_timeout
        data = json.dumps(data, indent=4)
        response = self._session.put(f'{self.url}/runners/{runner_id}', headers=self.headers, data=data,
                                     verify=self.verify)
        return response

    @require_auth
    def pause_runner(self, runner_id: Union[int, str] = None, active: bool = None):
        if runner_id is None or active is None:
            raise MissingParameterError
        data = {'active': active}
        data = json.dumps(data, indent=4)
        response = self._session.put(f'{self.url}/runners/{runner_id}', headers=self.headers, data=data,
                                     verify=self.verify)
        return response

    @require_auth
    def get_runner_jobs(self, runner_id: Union[int, str] = None):
        if runner_id is None:
            raise MissingParameterError
        response = self._session.put(f'{self.url}/runners/{runner_id}/jobs', headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_project_runners(self, project_id: Union[int, str] = None, runner_type=None, status=None, paused=None,
                            tag_list=None,
                            all_runners=False):
        if project_id is None:
            raise MissingParameterError
        runner_filter = None
        if all_runners:
            runner_filter = '/all'
        if runner_type:
            if runner_type not in ['instance_type', 'group_type', 'project_type']:
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&type={runner_type}'
            else:
                runner_filter = f'?type={runner_type}'
        if status:
            if status not in ['online', 'offline', 'stale', 'never_contacted', 'active', 'paused']:
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&status={status}'
            else:
                runner_filter = f'?status={status}'
        if paused:
            if not isinstance(paused, bool):
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&paused={paused}'
            else:
                runner_filter = f'?paused={paused}'
        if tag_list:
            if not isinstance(tag_list, list):
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&tag_list={tag_list}'
            else:
                runner_filter = f'?tag_list={tag_list}'
        response = self._session.get(f'{self.url}/projects/{project_id}/runners{runner_filter}',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def enable_project_runner(self, project_id: Union[int, str] = None, runner_id: Union[int, str] = None):
        if project_id is None or runner_id is None:
            raise MissingParameterError
        data = json.dumps({'runner_id': runner_id}, indent=4)
        response = self._session.put(f'{self.url}/projects/{project_id}/runners', headers=self.headers, data=data,
                                     verify=self.verify)
        return response

    @require_auth
    def delete_project_runner(self, project_id: Union[int, str] = None, runner_id: Union[int, str] = None):
        if project_id is None or runner_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}/runners/{runner_id}', headers=self.headers,
                                        verify=self.verify)
        return response

    @require_auth
    def get_group_runners(self, group_id: Union[int, str] = None, runner_type=None, status=None, paused=None,
                          tag_list=None,
                          all_runners=False):
        if group_id is None:
            raise MissingParameterError
        runner_filter = None
        if all_runners:
            runner_filter = '/all'
        if runner_type:
            if runner_type not in ['instance_type', 'group_type', 'project_type']:
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&type={runner_type}'
            else:
                runner_filter = f'?type={runner_type}'
        if status:
            if status not in ['online', 'offline', 'stale', 'never_contacted', 'active', 'paused']:
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&status={status}'
            else:
                runner_filter = f'?status={status}'
        if paused:
            if not isinstance(paused, bool):
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&paused={paused}'
            else:
                runner_filter = f'?paused={paused}'
        if tag_list:
            if not isinstance(tag_list, list):
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&tag_list={tag_list}'
            else:
                runner_filter = f'?tag_list={tag_list}'
        response = self._session.get(f'{self.url}/groups/{group_id}/runners{runner_filter}',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def register_new_runner(self, token: str = None, description: str = None, info=None, paused=None, locked=None,
                            run_untagged=None,
                            tag_list=None, access_level=None, maximum_timeout=None, maintenance_note: str = None):
        if token is None:
            raise MissingParameterError
        data = {}
        if description:
            data['description'] = description
        if info:
            if not isinstance(info, str):
                raise ParameterError
            data['info'] = info
        if paused:
            if not isinstance(paused, bool):
                raise ParameterError
            data['paused'] = paused
        if locked:
            if not isinstance(locked, bool):
                raise ParameterError
            data['locked'] = locked
        if run_untagged:
            if not isinstance(run_untagged, bool):
                raise ParameterError
            data['run_untagged'] = run_untagged
        if tag_list:
            if not isinstance(tag_list, list):
                raise ParameterError
            data['tag_list'] = tag_list
        if access_level:
            if not isinstance(access_level, str):
                raise ParameterError
            data['access_level'] = access_level
        if maximum_timeout:
            if not isinstance(maximum_timeout, int):
                raise ParameterError
            data['maximum_timeout'] = maximum_timeout
        if maintenance_note:
            if not isinstance(maintenance_note, str):
                raise ParameterError
            data['maintenance_note'] = maintenance_note
        data = json.dumps(data, indent=4)
        response = self._session.put(f'{self.url}/runners', headers=self.headers, data=data, verify=self.verify)
        return response

    @require_auth
    def delete_runner(self, runner_id: Union[int, str] = None, token: str = None):
        if runner_id is None and token is None:
            raise MissingParameterError
        if runner_id:
            response = self._session.delete(f'{self.url}/runners/{runner_id}', headers=self.headers, verify=self.verify)
        else:
            data = {'token': token}
            data = json.dumps(data, indent=4)
            response = self._session.delete(f'{self.url}/runners', headers=self.headers, data=data,
                                            verify=self.verify)
        return response

    @require_auth
    def verify_runner_authentication(self, token: str = None):
        if token is None:
            raise MissingParameterError
        data = {'token': token}
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/runners/verify', headers=self.headers, data=data, verify=self.verify)
        return response

    @require_auth
    def reset_gitlab_runner_token(self):
        response = self._session.post(f'{self.url}/runners/reset_registration_token', headers=self.headers,
                                      verify=self.verify)
        return response

    @require_auth
    def reset_project_runner_token(self, project_id: Union[int, str] = None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/runners/reset_registration_token',
                                      headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def reset_group_runner_token(self, group_id: Union[int, str] = None):
        if group_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/groups/{group_id}/runners/reset_registration_token',
                                      headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def reset_token(self, runner_id: Union[int, str] = None, token: str = None):
        if runner_id is None or token is None:
            raise MissingParameterError
        data = {'token': token}
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/runners/{runner_id}/reset_authentication_token',
                                      headers=self.headers, data=data, verify=self.verify)
        return response

    ####################################################################################################################
    #                                                Users API                                                         #
    ####################################################################################################################
    @require_auth
    def get_users(self, username=None, active=None, blocked=None, external=None, exclude_internal=None,
                  exclude_external=None, without_project_bots=None, extern_uid=None, provider=None, created_before=None,
                  created_after=None, with_custom_attributes=None, sort=None, order_by=None, two_factor=None,
                  without_projects=None, admins=None, saml_provider_id=None,
                  max_pages: int = 0, page: int = 1, per_page: int = 100):
        api_parameters = f"?per_page={per_page}"
        response = self._session.get(f'{self.url}/users{api_parameters}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []

        if username:
            if not isinstance(username, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&username={username}'
        if active:
            if not isinstance(active, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&active={active}'
        if blocked:
            if not isinstance(blocked, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&blocked={blocked}'
        if external:
            if not isinstance(external, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&external={external}'
        if exclude_internal:
            if not isinstance(exclude_internal, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&exclude_internal={exclude_internal}'
        if exclude_external:
            if not isinstance(exclude_external, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&exclude_external={exclude_external}'
        if without_project_bots:
            if not isinstance(without_project_bots, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&without_project_bots={without_project_bots}'
        if order_by:
            if order_by not in ['id', 'name', 'username', 'created_at', 'updated_at']:
                raise ParameterError
            api_parameters = f'{api_parameters}&order_by={order_by}'
        if sort:
            if sort not in ['asc', 'desc']:
                raise ParameterError
            api_parameters = f'{api_parameters}&sort={sort}'
        if two_factor:
            if two_factor not in ['enabled', 'disabled']:
                raise ParameterError
            api_parameters = f'{api_parameters}&two_factor={two_factor}'
        if without_projects:
            if not isinstance(without_projects, bool):
                raise ParameterError
            api_parameters = f'{api_parameters}&without_projects={without_projects}'
        if admins:
            if not isinstance(admins, bool):
                raise ParameterError
            api_parameters = f'{api_parameters}&admins={admins}'
        if saml_provider_id:
            if not isinstance(saml_provider_id, int):
                raise ParameterError
            api_parameters = f'{api_parameters}&saml_provider_id={saml_provider_id}'
        if extern_uid:
            if not isinstance(extern_uid, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&extern_uid={extern_uid}'
        if provider:
            if not isinstance(provider, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&provider={provider}'
        if created_before:
            if not isinstance(created_before, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&created_before={created_before}'
        if created_after:
            if not isinstance(created_after, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&created_after={created_after}'
        if with_custom_attributes:
            if not isinstance(with_custom_attributes, str):
                raise ParameterError
            api_parameters = f'{api_parameters}&with_custom_attributes={with_custom_attributes}'
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, max_pages):
            response_page = self._session.get(f'{self.url}/users{api_parameters}&page={page}',
                                              headers=self.headers, verify=self.verify)
            response_page = json.loads(response_page.text.replace("'", "\""))
            response = response + response_page
        return response

    @require_auth
    def get_user(self, user_id=None, sudo=False):
        if user_id is None:
            raise MissingParameterError
        if sudo:
            user_url = f'?sudo={user_id}'
        else:
            user_url = f'/{user_id}'
        response = self._session.get(f'{self.url}/users{user_url}', headers=self.headers, verify=self.verify)
        return response

    ####################################################################################################################
    #                                                 Wiki API                                                         #
    ####################################################################################################################
    @require_auth
    def get_wiki_list(self, project_id: Union[int, str] = None, with_content: bool = None):
        if project_id is None:
            raise MissingParameterError
        runner_filter = None
        if with_content:
            if not isinstance(with_content, bool):
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&with_content=1'
            else:
                runner_filter = f'?with_content=1'
        response = self._session.get(f'{self.url}/projects/{project_id}/wikis{runner_filter}',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_wiki_page(self, project_id: Union[int, str] = None, slug: str = None, render_html: bool = None,
                      version: str = None):
        if project_id is None or slug is None:
            raise MissingParameterError
        runner_filter = None
        if render_html:
            if not isinstance(render_html, bool):
                raise ParameterError
            if runner_filter:
                runner_filter = f'{runner_filter}&render_html=1'
            else:
                runner_filter = f'?render_html=1'
        if version:
            if not isinstance(version, bool):
                raise ParameterError
            if runner_filter:
                runner_filter = f'{version}&version'
            else:
                runner_filter = f'?version'
        response = self._session.get(f'{self.url}/projects/{project_id}/wikis/{slug}{runner_filter}',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def create_wiki_page(self, project_id: Union[int, str] = None, content: str = None, title: str = None,
                         format_type: str = None):
        if project_id is None:
            raise MissingParameterError
        data = {}
        if content:
            if not isinstance(content, str):
                raise ParameterError
            data['content'] = content
        if title:
            if not isinstance(title, bool):
                raise ParameterError
            data['title'] = title
        if format_type:
            if not isinstance(format_type, str):
                raise ParameterError
            data['format'] = format_type
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/projects/{project_id}/wikis',
                                      headers=self.headers, verify=self.verify, data=data)
        return response

    @require_auth
    def update_wiki_page(self, project_id: Union[int, str] = None, slug: str = None, content: str = None,
                         title: str = None, format_type: str = None):
        if project_id is None or slug is None:
            raise MissingParameterError
        data = {}
        if content:
            if not isinstance(content, str):
                raise ParameterError
            data['content'] = content
        if title:
            if not isinstance(title, bool):
                raise ParameterError
            data['title'] = title
        if format_type:
            if not isinstance(format_type, str):
                raise ParameterError
            data['format'] = format_type
        data = json.dumps(data, indent=4)
        response = self._session.put(f'{self.url}/projects/{project_id}/wikis/{slug}',
                                     headers=self.headers, verify=self.verify, data=data)
        return response

    @require_auth
    def delete_wiki_page(self, project_id: Union[int, str] = None, slug: str = None):
        if project_id is None or slug is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}/wikis/{slug}',
                                        headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def upload_wiki_page_attachment(self, project_id: Union[int, str] = None, file: str = None, branch: str = None):
        if project_id is None or file is None or branch is None:
            raise MissingParameterError
        data = {}
        if file:
            if not isinstance(file, str):
                raise ParameterError
            data['file'] = f"@{file}"
        data = json.dumps(data, indent=4)
        headers = self.headers
        headers['Content-Type'] = "multipart/form-data"
        response = self._session.delete(f'{self.url}/projects/{project_id}/wikis/attachments',
                                        headers=headers, verify=self.verify, data=data)
        return response
