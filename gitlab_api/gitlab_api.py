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
        try:
            response = self._session.get(
                f'{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approvals',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_approval_state_merge_requests(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                f'{self.url}/projects/{merge_rule.project_id}'
                f'/merge_requests/{merge_rule.merge_request_iid}/approval_state',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_merge_request_level_rules(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                f'{self.url}/projects/{merge_rule.project_id}'
                f'/merge_requests/{merge_rule.merge_request_iid}/approval_rules',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def approve_merge_request(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{merge_rule.project_id}'
                                          f'/merge_requests/{merge_rule.merge_request_iid}/approve',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def unapprove_merge_request(self, merge_rule: MergeRequestRuleModel):
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{merge_rule.project_id}'
                                          f'/merge_requests/{merge_rule.merge_request_iid}/unapprove',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                               Packages API                                                       #
    ####################################################################################################################
    def get_repository_packages(self, package: PackageModel):
        if package.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{package.project_id}/packages', headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    def publish_repository_package(self, package: PackageModel):
        if (package.project_id is None
                or package.package_name is None
                or package.package_version is None
                or package.file_name is None):
            raise MissingParameterError
        try:
            response = self._session.put(f'{self.url}/projects/{package.project_id}'
                                         f'/packages/generic/{package.package_name}/{package.package_version}'
                                         f'/{package.file_name}{package.api_parameters}', headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    def download_repository_package(self, package: PackageModel):
        if (package.project_id is None
                or package.package_name is None
                or package.package_version is None
                or package.file_name is None):
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{package.project_id}'
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
    def get_pipelines(self, pipeline: PipelineModel):
        if pipeline.project_id is None:
            raise MissingParameterError
        api_parameters = f"?per_page={pipeline.per_page}"
        try:
            response = self._session.get(
                f'{self.url}/projects/{pipeline.project_id}/pipelines{pipeline.api_parameters}',
                headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_pipeline(self, pipeline: PipelineModel):
        if pipeline.project_id is None or pipeline.pipeline_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{pipeline.project_id}'
                                         f'/pipelines/{pipeline.pipeline_id}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def run_pipeline(self, pipeline: PipelineModel):
        if pipeline.project_id is None or pipeline.reference is None:
            raise MissingParameterError
        if pipeline.variables:
            response = self._session.post(f'{self.url}/projects/{pipeline.project_id}'
                                          f'/pipeline{pipeline.api_parameters}',
                                          headers=self.headers,
                                          data=json.dumps(pipeline.variables, indent=2), verify=self.verify)
        else:
            response = self._session.post(f'{self.url}/projects/{pipeline.project_id}'
                                          f'/pipeline{pipeline.api_parameters}',
                                          headers=self.headers,
                                          verify=self.verify)
        return response

    ####################################################################################################################
    #                                                Projects API                                                      #
    ####################################################################################################################
    @require_auth
    def get_projects(self, project: ProjectModel):
        response = self._session.get(f'{self.url}/projects?per_page={project.per_page}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        if project.max_pages == 0 or project.max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, project.max_pages):
            response_page = self._session.get(
                f'{self.url}/projects?per_page={project.per_page}&page={page}&order_by={project.order_by}',
                headers=self.headers, verify=self.verify)
            response_page = json.loads(response_page.text.replace("'", "\""))
            response = response + response_page
        return response

    @require_auth
    def get_project(self, project: ProjectModel):
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project.project_id}',
                                     headers=self.headers,
                                     verify=self.verify)
        return response

    @require_auth
    def get_nested_projects_by_group(self, project: ProjectModel):
        if project.group_id is None:
            raise MissingParameterError
        projects = []
        groups = [self.get_group(group_id=project.group_id)]
        groups = groups + self.get_group_subgroups(group_id=project.group_id)
        for group in groups:
            response = self._session.get(f'{self.url}'
                                         f'/groups/{group["id"]}'
                                         f'/projects?per_page={project.per_page}&x-total-pages',
                                         headers=self.headers, verify=self.verify)
            total_pages = int(response.headers['X-Total-Pages'])
            if project.max_pages == 0 or project.max_pages > total_pages:
                project.max_pages = total_pages
            for page in range(0, project.max_pages):
                group_projects = self._session.get(f'{self.url}/groups/{group["id"]}/'
                                                   f'projects?per_page={project.per_page}&page={page}',
                                                   headers=self.headers, verify=self.verify)
                group_projects = json.loads(group_projects.text)
                projects = projects + group_projects
        return projects

    @require_auth
    def get_project_contributors(self, project: ProjectModel):
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}'
                                     f'/projects/{project.project_id}/repository/contributors',
                                     headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def get_project_statistics(self, project: ProjectModel):
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}'
                                     f'/projects/{project.project_id}?statistics=true',
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
    def unarchive_project(self, project: ProjectModel):
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project.project_id}/unarchive',
                                      headers=self.headers,
                                      verify=self.verify)
        return response

    @require_auth
    def delete_project(self, project: ProjectModel):
        if project.project_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project.project_id}',
                                        headers=self.headers,
                                        verify=self.verify)
        return response

    @require_auth
    def share_project(self, project: ProjectModel):
        if project.project_id is None or project.group_id is None or project.group_access is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project.project_id}'
                                      f'/share{project.api_parameters}',
                                      headers=self.headers,
                                      verify=self.verify)
        return response

    ####################################################################################################################
    #                                       Protected Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_protected_branches(self, protected_branch: ProtectedBranchModel):
        if protected_branch.project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{protected_branch.project_id}/protected_branches',
                                     headers=self.headers,
                                     verify=self.verify)
        return response

    @require_auth
    def get_protected_branch(self, protected_branch: ProtectedBranchModel):
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{protected_branch.project_id}'
                                     f'/protected_branches/{protected_branch.branch}',
                                     headers=self.headers,
                                     verify=self.verify)
        return response

    @require_auth
    def protect_branch(self, protected_branch: ProtectedBranchModel):
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError

        if protected_branch.data:
            response = self._session.post(f'{self.url}/projects/{protected_branch.project_id}'
                                          f'/protected_branches{protected_branch.branch_filter}',
                                          headers=self.headers,
                                          data=json.dumps(protected_branch.data, indent=2),
                                          verify=self.verify)
        else:
            response = self._session.post(f'{self.url}/projects/{protected_branch.project_id}'
                                          f'/protected_branches{protected_branch.branch_filter}',
                                          headers=self.headers, verify=self.verify)
        return response

    @require_auth
    def unprotect_branch(self, protected_branch: ProtectedBranchModel):
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        self._session.delete(f'{self.url}/projects/{protected_branch.project_id}'
                             f'/protected_branches/{protected_branch.branch}',
                             headers=self.headers,
                             verify=self.verify)

    @require_auth
    def require_code_owner_approvals_single_branch(self, protected_branch: ProtectedBranchModel):
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        response = self._session.patch(f'{self.url}/projects/{protected_branch.project_id}'
                                       f'/protected_branches/{protected_branch.branch}',
                                       headers=self.headers,
                                       verify=self.verify)
        return response

    ####################################################################################################################
    #                                                Release API                                                       #
    ####################################################################################################################
    @require_auth
    def get_releases(self, release: ReleaseModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/projects/{release.project_id}/releases',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_latest_release(self, release: ReleaseModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/projects/{release.project_id}/releases'
                                         f'/permalink/latest',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_latest_release_evidence(self, release: ReleaseModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/projects/{release.project_id}/releases'
                                         f'/permalink/latest/evidence',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_latest_release_asset(self, release: ReleaseModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/projects/{release.project_id}/releases'
                                         f'/permalink/latest/{release.direct_asset_path}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_releases(self, release: ReleaseModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/groups/{release.group_id}/releases{release.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def download_release_asset(self, release: ReleaseModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/groups/{release.group_id}'
                                         f'/releases/{release.tag_name}'
                                         f'/downloads/{release.direct_asset_path}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_release_by_tag(self, release: ReleaseModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/projects/{release.project_id}/releases/{release.tag_name}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response


    @require_auth
    def create_release(self, release: ReleaseModel):
        try:
            response = self._session.post(f'{self.url}'
                                         f'/projects/{release.project_id}/releases',
                                         data=json.dumps(release.data, indent=2),
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_release_evidence(self, release: ReleaseModel):
        try:
            response = self._session.post(f'{self.url}'
                                          f'/projects/{release.project_id}'
                                          f'/releases/{release.tag_name}/evidence',
                                          headers=self.headers,
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_release(self, release: ReleaseModel):
        try:
            response = self._session.put(f'{self.url}'
                                         f'/projects/{release.project_id}/releases/{release.tag_name}',
                                         data=json.dumps(release.data, indent=2),
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_release(self, release: ReleaseModel):
        try:
            response = self._session.delete(f'{self.url}'
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
    def get_runners(self, runner: RunnerModel):
        try:
            response = self._session.get(f'{self.url}'
                                         f'/runners{runner.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_runner(self, runner: RunnerModel):
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}'
                                         f'/runners/{runner.runner_id}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_runner_details(self, runner: RunnerModel):
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(f'{self.url}/runners/{runner.runner_id}',
                                         headers=self.headers,
                                         data=json.dumps(runner.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def pause_runner(self, runner: RunnerModel):
        if runner.runner_id is None or runner.active is None:
            raise MissingParameterError
        try:
            response = self._session.put(f'{self.url}/runners/{runner.runner_id}',
                                         headers=self.headers,
                                         data=json.dumps(runner.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_runner_jobs(self, runner: RunnerModel):
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(f'{self.url}/runners'
                                         f'/{runner.runner_id}/jobs',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_project_runners(self, runner: RunnerModel):
        if runner.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{runner.project_id}'
                                         f'/runners{runner.runner_filter}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def enable_project_runner(self, runner: RunnerModel):
        if runner.project_id is None or runner.runner_id is None:
            raise MissingParameterError

        try:
            response = self._session.put(f'{self.url}/projects'
                                         f'/{runner.project_id}/runners',
                                         headers=self.headers,
                                         data=json.dumps(runner.data, indent=2),
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_project_runner(self, runner: RunnerModel):
        if runner.project_id is None or runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(f'{self.url}/projects/{runner.project_id}'
                                            f'/runners/{runner.runner_id}',
                                            headers=self.headers,
                                            verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_group_runners(self, runner: RunnerModel):
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/groups/{runner.group_id}'
                                         f'/runners{runner.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def register_new_runner(self, runner: RunnerModel):
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.put(f'{self.url}/runners',
                                         headers=self.headers,
                                         data=runner.data,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_runner(self, runner: RunnerModel):
        if runner.runner_id is None and runner.token is None:
            raise MissingParameterError
        if runner.runner_id:
            response = self._session.delete(f'{self.url}/runners/{runner.runner_id}',
                                            headers=self.headers,
                                            verify=self.verify)
        else:
            try:
                response = self._session.delete(f'{self.url}/runners',
                                                headers=self.headers,
                                                data=json.dumps(runner.data, indent=2),
                                                verify=self.verify)
            except ValidationError as e:
                raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def verify_runner_authentication(self, runner: RunnerModel):
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/runners/verify',
                                          headers=self.headers,
                                          data=json.dumps(runner.data, indent=2),
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def reset_gitlab_runner_token(self):
        try:
            response = self._session.post(f'{self.url}/runners'
                                          f'/reset_registration_token', headers=self.headers,
                                          verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def reset_project_runner_token(self, runner: RunnerModel):
        if runner.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{runner.project_id}'
                                          f'/runners/reset_registration_token',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def reset_group_runner_token(self, runner: RunnerModel):
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/groups/{runner.group_id}'
                                          f'/runners/reset_registration_token',
                                          headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def reset_token(self, runner: RunnerModel):
        if runner.runner_id is None or runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/runners/{runner.runner_id}'
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
    def get_users(self, user: UserModel):
        api_parameters = f"?per_page={user.per_page}"
        response = self._session.get(f'{self.url}/users{api_parameters}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []

        if user.max_pages == 0 or user.max_pages > total_pages:
            user.max_pages = total_pages
        for page in range(0, user.max_pages):
            response_page = self._session.get(f'{self.url}/users{user.api_parameters}&page={page}',
                                              headers=self.headers, verify=self.verify)
            response_page = json.loads(response_page.text.replace("'", "\""))
            response = response + response_page
        return response

    @require_auth
    def get_user(self, user: UserModel):
        if user.user_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/users{user.api_parameters}',
                                         headers=self.headers,
                                         verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    ####################################################################################################################
    #                                                 Wiki API                                                         #
    ####################################################################################################################
    @require_auth
    def get_wiki_list(self, wiki: WikiModel):
        if wiki.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{wiki.project_id}'
                                         f'/wikis{wiki.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def get_wiki_page(self, wiki: WikiModel):
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.get(f'{self.url}/projects/{wiki.project_id}'
                                         f'/wikis/{wiki.slug}{wiki.api_parameters}',
                                         headers=self.headers, verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def create_wiki_page(self, wiki: WikiModel):
        if wiki.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(f'{self.url}/projects/{wiki.project_id}/wikis',
                                          headers=self.headers,
                                          verify=self.verify,
                                          data=json.dumps(wiki.data, indent=2))
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def update_wiki_page(self, wiki: WikiModel):
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.put(f'{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}',
                                         headers=self.headers,
                                         verify=self.verify,
                                         data=json.dumps(wiki.data, indent=2))
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def delete_wiki_page(self, wiki: WikiModel):
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.delete(f'{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}',
                                            headers=self.headers,
                                            verify=self.verify)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response

    @require_auth
    def upload_wiki_page_attachment(self, wiki: WikiModel):
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
            response = self._session.put(f'{self.url}/projects/{wiki.project_id}/wikis/attachments',
                                         headers=headers,
                                         verify=self.verify,
                                         data=data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}")
        return response
