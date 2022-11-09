#!/usr/bin/python
# coding: utf-8

import json
import requests
import urllib3
from base64 import b64encode

try:
    from gitlab_api.decorators import require_auth
except ModuleNotFoundError:
    from decorators import require_auth
try:
    from gitlab_api.exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)
except ModuleNotFoundError:
    from exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)


class Api(object):

    def __init__(self, url=None, username=None, password=None, token=None, verify=True):
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
    def get_branches(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/branches',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_branch(self, project_id=None, branch=None):
        if project_id is None or branch is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/branches/{branch}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_branch(self, project_id=None, branch=None, reference=None):
        if project_id is None or branch is None or reference is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/repository/'
                                      f'branches?branch={branch}&ref={reference}',
                                      headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_branch(self, project_id=None, branch=None):
        if project_id is None or branch is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}/repository/branches?branch={branch}',
                                        headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_merged_branches(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}/repository/merged_branches',
                                        headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                 Commits API                                                      #
    ####################################################################################################################
    @require_auth
    def get_commits(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/commits',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_commit(self, project_id=None, commit_hash=None):
        if project_id is None or commit_hash is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_commit_references(self, project_id=None, commit_hash=None):
        if project_id is None or commit_hash is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/refs',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def cherry_pick_commit(self, project_id=None, commit_hash=None, branch=None, dry_run=None, message=None):
        if project_id is None or commit_hash is None or branch is None:
            raise MissingParameterError
        data = {}
        if branch:
            if not isinstance(branch, str):
                raise ParameterError
            data['branch'] = branch
        if dry_run:
            if not isinstance(dry_run, bool):
                raise ParameterError
            data['dry_run'] = dry_run
        if message:
            if not isinstance(message, str):
                raise ParameterError
            data['message'] = message
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/cherry_pick',
                                      headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_commit(self, project_id=None, branch=None, commit_message=None, start_branch=None, start_sha=None,
                      start_project=None, actions=None, author_email=None, author_name=None, stats=None, force=None):
        if project_id is None or branch is None or commit_message is None or actions is None:
            raise MissingParameterError
        data = {}
        if branch:
            if not isinstance(branch, str):
                raise ParameterError
            data['branch'] = branch
        if commit_message:
            if not isinstance(commit_message, str):
                raise ParameterError
            data['commit_message'] = commit_message
        if start_branch:
            if not isinstance(start_branch, str):
                raise ParameterError
            data['start_branch'] = start_branch
        if start_sha:
            if not isinstance(start_sha, str):
                raise ParameterError
            data['start_sha'] = start_sha
        if start_project:
            if not isinstance(start_project, str) and not isinstance(start_project, int):
                raise ParameterError
            data['start_project'] = start_project
        if actions:
            if not isinstance(actions, list):
                raise ParameterError
            data['actions'] = actions
        if author_email:
            if not isinstance(author_email, str):
                raise ParameterError
            data['author_email'] = author_email
        if author_name:
            if not isinstance(author_name, str):
                raise ParameterError
            data['author_name'] = author_name
        if stats:
            if not isinstance(stats, bool):
                raise ParameterError
            data['stats'] = stats
        if force:
            if not isinstance(force, bool):
                raise ParameterError
            data['force'] = force
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/projects/{project_id}/repository/commits',
                                      headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def revert_commit(self, project_id=None, commit_hash=None, branch=None, dry_run=None):
        if project_id is None or commit_hash is None or branch is None:
            raise MissingParameterError
        data = {}
        if branch:
            if not isinstance(branch, str):
                raise ParameterError
            data['branch'] = branch
        if dry_run:
            if not isinstance(dry_run, bool):
                raise ParameterError
            data['dry_run'] = dry_run
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/revert',
                                      headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_commit_diff(self, project_id=None, commit_hash=None):
        if project_id is None or commit_hash is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/diff',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_commit_comments(self, project_id=None, commit_hash=None):
        if project_id is None or commit_hash is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/comments',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_commit_comment(self, project_id=None, commit_hash=None, note=None, path=None, line=None, line_type=None):
        if project_id is None or commit_hash is None or note is None:
            raise MissingParameterError
        data = {}
        if note:
            if not isinstance(note, str):
                raise ParameterError
            data['note'] = note
        if path:
            if not isinstance(path, str):
                raise ParameterError
            data['path'] = path
        if line:
            if not isinstance(line, int):
                raise ParameterError
            data['line'] = line
        if line_type:
            if line_type != 'new' or line_type != 'old':
                raise ParameterError
            else:
                data['line_type'] = line_type
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/comments',
                                      headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_commit_discussions(self, project_id=None, commit_hash=None):
        if project_id is None or commit_hash is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/discussions',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_commit_statuses(self, project_id=None, commit_hash=None):
        if project_id is None or commit_hash is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/statuses',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def post_build_status_to_commit(self, project_id=None, commit_hash=None, state=None, reference=None, name=None,
                                    context=None, target_url=None, description=None, coverage=None, pipeline_id=None):
        if project_id is None or commit_hash is None or state is None:
            raise MissingParameterError
        data = {}
        if state:
            if state not in ['pending', 'running', 'success', 'failed', 'canceled']:
                raise ParameterError
            else:
                data['state'] = state
        if reference:
            if not isinstance(reference, str):
                raise ParameterError
            data['ref'] = reference
        if name:
            if not isinstance(name, str):
                raise ParameterError
            data['name'] = name
        if context:
            if not isinstance(context, str):
                raise ParameterError
            data['context'] = context
        if target_url:
            if not isinstance(target_url, str):
                raise ParameterError
            data['target_url'] = target_url
        if description:
            if not isinstance(description, str):
                raise ParameterError
            data['description'] = description
        if coverage:
            if not isinstance(coverage, float):
                raise ParameterError
            data['coverage'] = coverage
        if pipeline_id:
            if not isinstance(pipeline_id, int):
                raise ParameterError
            data['pipeline_id'] = pipeline_id
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/projects/{project_id}/statuses/{commit_hash}/',
                                      headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_commit_merge_requests(self, project_id=None, commit_hash=None):
        if project_id is None or commit_hash is None:
            raise MissingParameterError
        response = self._session.get(
            f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/merge_requests',
            headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_commit_gpg_signature(self, project_id=None, commit_hash=None):
        if project_id is None or commit_hash is None:
            raise MissingParameterError
        response = self._session.get(
            f'{self.url}/projects/{project_id}/repository/commits/{commit_hash}/merge_requests',
            headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                Deploy Tokens API                                                 #
    ####################################################################################################################
    @require_auth
    def get_deploy_tokens(self):
        response = self._session.get(f'{self.url}/deploy_tokens', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_deploy_tokens(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/deploy_tokens',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_deploy_token(self, project_id=None, token=None):
        if project_id is None or token is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/deploy_tokens/{token}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_project_deploy_token(self, project_id=None, name=None, expires_at=None, username=None, scopes=None):
        if project_id is None or name is None or scopes is None:
            raise MissingParameterError
        data = {}
        if name:
            if not isinstance(name, str):
                raise ParameterError
            data['name'] = name
        if expires_at:
            if not isinstance(expires_at, str):
                raise ParameterError
            data['expires_at'] = expires_at
        if username:
            if not isinstance(username, str):
                raise ParameterError
            data['username'] = username
        if scopes:
            if scopes not in ['read_repository', 'read_registry', 'write_registry', 'read_package_registry',
                              'write_package_registry']:
                raise ParameterError
            else:
                data['scopes'] = scopes
        data = json.dumps(data, indent=4)
        response = self._session.get(f'{self.url}/projects/{project_id}/deploy_tokens',
                                     headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_project_deploy_token(self, project_id=None, token=None):
        if project_id is None or token is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}/deploy_tokens/{token}',
                                        headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_group_deploy_tokens(self, group_id=None):
        if group_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/groups/{group_id}/deploy_tokens',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_group_deploy_token(self, group_id=None, token=None):
        if group_id is None or token is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/groups/{group_id}/deploy_tokens/{token}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_group_deploy_token(self, group_id=None, name=None, expires_at=None, username=None, scopes=None):
        if group_id is None or name is None or scopes is None:
            raise MissingParameterError
        data = {}
        if name:
            if not isinstance(name, str):
                raise ParameterError
            data['name'] = name
        if expires_at:
            if not isinstance(expires_at, str):
                raise ParameterError
            data['expires_at'] = expires_at
        if username:
            if not isinstance(username, str):
                raise ParameterError
            data['username'] = username
        if scopes:
            if scopes not in ['read_repository', 'read_registry', 'write_registry', 'read_package_registry',
                              'write_package_registry']:
                raise ParameterError
            else:
                data['scopes'] = scopes
        data = json.dumps(data, indent=4)
        response = self._session.get(f'{self.url}/groups/{group_id}/deploy_tokens',
                                     headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_group_deploy_token(self, group_id=None, token=None):
        if group_id is None or token is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/groups/{group_id}/deploy_tokens/{token}',
                                        headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                Groups API                                                        #
    ####################################################################################################################
    @require_auth
    def get_groups(self, per_page=100):
        response = self._session.get(f'{self.url}/groups?per_page={per_page}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_group(self, group_id):
        if group_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/groups/{group_id}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_group_subgroups(self, group_id=None):
        if group_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/groups/{group_id}/subgroups', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_group_descendant_groups(self, group_id=None):
        if group_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/groups/{group_id}/descendant_groups',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_group_projects(self, group_id=None, per_page=100):
        if group_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/groups/{group_id}/projects?per_page={per_page}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_group_merge_requests(self, group_id=None, argument='state=opened', per_page=100):
        if group_id is None or argument is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/groups/{group_id}/merge_requests?{argument}&per_page={per_page}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                Jobs API                                                          #
    ####################################################################################################################
    @require_auth
    def get_project_jobs(self, project_id=None, scope=None, per_page=100):
        if project_id is None:
            raise MissingParameterError
        api_parameters = f'?per_page={per_page}'
        if scope:
            if isinstance(scope, list):
                for scope_value in scope:
                    if scope_value in ['created', 'pending', 'running', 'failed', 'success', 'canceled', 'skipped',
                                       'waiting_for_resource', 'manual']:
                        api_parameters = f'{api_parameters}&scope[]={scope_value}'
                    else:
                        raise ParameterError
            elif isinstance(scope, str) and scope in ['created', 'pending', 'running', 'failed', 'success', 'canceled',
                                                      'skipped', 'waiting_for_resource', 'manual']:
                api_parameters = f'{api_parameters}&scope[]={scope}'
            else:
                raise ParameterError

        response = self._session.get(f'{self.url}/projects/{project_id}/jobs{api_parameters}', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_job(self, project_id=None, job_id=None):
        if project_id is None or job_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/jobs/{job_id}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_job_log(self, project_id=None, job_id=None):
        if project_id is None or job_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/jobs/{job_id}/trace',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def cancel_project_job(self, project_id=None, job_id=None):
        if project_id is None or job_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/jobs/{job_id}/cancel',
                                      headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def retry_project_job(self, project_id=None, job_id=None):
        if project_id is None or job_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/jobs/{job_id}/retry',
                                      headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def erase_project_job(self, project_id=None, job_id=None):
        if project_id is None or job_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/jobs/{job_id}/erase',
                                      headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def run_project_job(self, project_id=None, job_id=None, job_variable_attributes=None):
        if project_id is None or job_id is None:
            raise MissingParameterError
        data = None
        if job_variable_attributes:
            if not isinstance(job_variable_attributes, dict) \
                    or "job_variable_attributes" not in job_variable_attributes.keys():
                raise ParameterError
            data = json.dumps(job_variable_attributes, indent=4)
        response = self._session.post(f'{self.url}/projects/{project_id}/jobs/{job_id}/play',
                                      headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_pipeline_jobs(self, project_id=None, pipeline_id=None, scope=None, include_retried=None, per_page=100):
        if project_id is None or pipeline_id is None:
            raise MissingParameterError
        api_parameters = f'?per_page={per_page}'
        if scope:
            if isinstance(scope, list):
                for scope_value in scope:
                    if scope_value in ['created', 'pending', 'running', 'failed', 'success', 'canceled', 'skipped',
                                       'waiting_for_resource', 'manual']:
                        api_parameters = f'{api_parameters}&scope[]={scope_value}'
                    else:
                        raise ParameterError
            elif isinstance(scope, str) and scope in ['created', 'pending', 'running', 'failed', 'success', 'canceled',
                                                      'skipped', 'waiting_for_resource', 'manual']:
                api_parameters = f'{api_parameters}&scope[]={scope}'
            else:
                raise ParameterError
        if include_retried:
            if isinstance(include_retried, bool):
                api_parameters = f'{api_parameters}&include_retried={str(include_retried).lower()}'
        else:
            raise ParameterError

        response = self._session.get(f'{self.url}/projects/{project_id}/pipelines/{pipeline_id}/jobs{api_parameters}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                               Members API                                                        #
    ####################################################################################################################
    @require_auth
    def get_group_members(self, group_id=None, per_page=100):
        if group_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/groups/{group_id}/members?per_page={per_page}', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_members(self, project_id=None, per_page=100):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/members?per_page={per_page}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                            Merge Request API                                                     #
    ####################################################################################################################
    @require_auth
    def create_merge_request(self, project_id=None, source_branch=None, target_branch=None, title=None,
                             allow_collaboration=None, allow_maintainer_to_push=None, approvals_before_merge=None,
                             assignee_id=None, assignee_ids=None, description=None, labels=None, milestone_id=None,
                             remove_source_branch=None, reviewer_ids=None, squash=None, target_project_id=None):
        if project_id is None or source_branch is None or target_branch is None or title is None:
            raise MissingParameterError
        data = {}
        if source_branch:
            if not isinstance(source_branch, str):
                raise ParameterError
            data['source_branch'] = source_branch
        if target_branch:
            if not isinstance(target_branch, str):
                raise ParameterError
            data['target_branch'] = target_branch
        if title:
            if not isinstance(title, str):
                raise ParameterError
            data['title'] = title
        if allow_collaboration:
            if not isinstance(allow_collaboration, bool):
                raise ParameterError
            data['allow_collaboration'] = allow_collaboration
        if allow_maintainer_to_push:
            if not isinstance(allow_maintainer_to_push, bool):
                raise ParameterError
            data['allow_maintainer_to_push'] = allow_maintainer_to_push
        if approvals_before_merge:
            if not isinstance(approvals_before_merge, int):
                raise ParameterError
            data['approvals_before_merge'] = approvals_before_merge
        if assignee_id:
            if not isinstance(assignee_id, int):
                raise ParameterError
            data['assignee_id'] = assignee_id
        if assignee_ids:
            if not isinstance(assignee_ids, list):
                raise ParameterError
            data['assignee_ids'] = assignee_ids
        if description:
            if not isinstance(description, str):
                raise ParameterError
            data['description'] = description
        if labels:
            if not isinstance(labels, str):
                raise ParameterError
            data['labels'] = labels
        if milestone_id:
            if not isinstance(milestone_id, int):
                raise ParameterError
            data['milestone_id'] = milestone_id
        if remove_source_branch:
            if not isinstance(remove_source_branch, str):
                raise ParameterError
            data['remove_source_branch'] = remove_source_branch
        if reviewer_ids:
            if not isinstance(reviewer_ids, list):
                raise ParameterError
            data['reviewer_ids'] = reviewer_ids
        if squash:
            if not isinstance(squash, bool):
                raise ParameterError
            data['squash'] = squash
        if target_project_id:
            if not isinstance(target_project_id, int):
                raise ParameterError
            data['target_project_id'] = target_project_id

        if len(data) > 0:
            data = json.dumps(data, indent=4)
            response = self._session.post(f'{self.url}/projects/{project_id}/merge_requests', headers=self.headers,
                                          data=data, verify=self.verify)
            try:
                return response.json()
            except ValueError:
                return response
        else:
            raise MissingParameterError

    @require_auth
    def get_merge_requests(self, approved_by_ids=None, approver_ids=None, assignee_id=None, author_id=None,
                           author_username=None, created_after=None, created_before=None, deployed_after=None,
                           deployed_before=None, environment=None, search_in=None, labels=None, milestone=None,
                           my_reaction_emoji=None, search_exclude=None, order_by=None, reviewer_id=None,
                           reviewer_username=None, scope=None, search=None, sort=None, source_branch=None, state=None,
                           target_branch=None, updated_after=None, updated_before=None, view=None,
                           with_labels_details=None, with_merge_status_recheck=None, wip=None, max_pages=0,
                           per_page=100):
        response = self._session.get(f'{self.url}/merge_requests?per_page={per_page}&x-total-pages',
                                     headers=self.headers,
                                     verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        merge_filter = None
        if approved_by_ids:
            if not isinstance(approved_by_ids, list):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&approved_by_ids={approved_by_ids}'
            else:
                merge_filter = f'?approved_by_ids={approved_by_ids}'
        if approver_ids:
            if not isinstance(approver_ids, list):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&approver_ids={approver_ids}'
            else:
                merge_filter = f'?approver_ids={approver_ids}'
        if assignee_id:
            if not isinstance(assignee_id, int):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&assignee_id={assignee_id}'
            else:
                merge_filter = f'?assignee_id={assignee_id}'
        if author_id:
            if not isinstance(author_id, int):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&author_id={author_id}'
            else:
                merge_filter = f'?author_id={author_id}'
        if author_username:
            if not isinstance(author_username, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&author_username={author_username}'
            else:
                merge_filter = f'?author_username={author_username}'
        if created_after:
            if not isinstance(created_after, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&created_after={created_after}'
            else:
                merge_filter = f'?created_after={created_after}'
        if created_before:
            if not isinstance(created_before, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&created_before={created_before}'
            else:
                merge_filter = f'?created_before={created_before}'
        if deployed_after:
            if not isinstance(deployed_after, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&deployed_after={deployed_after}'
            else:
                merge_filter = f'?deployed_after={deployed_after}'
        if deployed_before:
            if not isinstance(deployed_before, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&deployed_before={deployed_before}'
            else:
                merge_filter = f'?deployed_before={deployed_before}'
        if environment:
            if not isinstance(environment, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&environment={environment}'
            else:
                merge_filter = f'?environment={environment}'
        if search_in:
            if search_in not in ['title', 'description', 'title,description']:
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&in={search_in}'
            else:
                merge_filter = f'?in={search_in}'
        if labels:
            if not isinstance(labels, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&labels={labels}'
            else:
                merge_filter = f'?labels={labels}'
        if milestone:
            if not isinstance(milestone, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&milestone={milestone}'
            else:
                merge_filter = f'?milestone={milestone}'
        if my_reaction_emoji:
            if not isinstance(my_reaction_emoji, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&my_reaction_emoji={my_reaction_emoji}'
            else:
                merge_filter = f'?my_reaction_emoji={my_reaction_emoji}'
        if search_exclude:
            if search_exclude not in ['labels', 'milestone', 'author_id', 'assignee_id', 'author_username',
                                      'reviewer_id', 'reviewer_username', 'my_reaction_emoji']:
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&not={search_exclude}'
            else:
                merge_filter = f'?not={search_exclude}'
        if order_by:
            if order_by not in ['created_at', 'title', 'updated_at']:
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&order_by={order_by}'
            else:
                merge_filter = f'?order_by={order_by}'
        if reviewer_id:
            if not isinstance(reviewer_username, int) and not isinstance(reviewer_username, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&reviewer_id={reviewer_id}'
            else:
                merge_filter = f'?reviewer_id={reviewer_id}'
        if reviewer_username:
            if not isinstance(reviewer_username, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&reviewer_username={reviewer_username}'
            else:
                merge_filter = f'?reviewer_username={reviewer_username}'
        if scope:
            if scope not in ['created_by_me', 'assigned_to_me', 'all']:
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&scope={scope}'
            else:
                merge_filter = f'?scope={scope}'
        if search:
            if search not in ['title', 'description']:
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&search={search}'
            else:
                merge_filter = f'?search={search}'
        if sort:
            if sort not in ['asc', 'desc']:
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&sort={sort}'
            else:
                merge_filter = f'?sort={sort}'
        if source_branch:
            if not isinstance(source_branch, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&source_branch={source_branch}'
            else:
                merge_filter = f'?source_branch={source_branch}'
        if state:
            if sort not in ['opened', 'closed', 'locked', 'merged']:
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&state={state}'
            else:
                merge_filter = f'?state={state}'
        if target_branch:
            if not isinstance(target_branch, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&target_branch={target_branch}'
            else:
                merge_filter = f'?target_branch={target_branch}'
        if updated_after:
            if not isinstance(updated_after, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&updated_after={updated_after}'
            else:
                merge_filter = f'?updated_after={updated_after}'
        if updated_before:
            if not isinstance(updated_before, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&updated_before={updated_before}'
            else:
                merge_filter = f'?updated_before={updated_before}'
        if view:
            if not isinstance(view, str):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&view={view}'
            else:
                merge_filter = f'?view={view}'
        if with_labels_details:
            if not isinstance(with_labels_details, bool):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&with_labels_details={str(with_labels_details).lower()}'
            else:
                merge_filter = f'?with_labels_details={str(with_labels_details).lower()}'
        if with_merge_status_recheck:
            if not isinstance(with_merge_status_recheck, bool):
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&with_merge_status_recheck={str(with_merge_status_recheck).lower()}'
            else:
                merge_filter = f'?with_merge_status_recheck={str(with_merge_status_recheck).lower()}'
        if wip:
            if wip not in ['yes', 'no']:
                raise ParameterError
            if merge_filter:
                merge_filter = f'{merge_filter}&wip={wip}'
            else:
                merge_filter = f'?wip={wip}'
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, max_pages):
            response_page = self._session.get(
                f'{self.url}/merge_requests{merge_filter}&per_page={per_page}&page={page}',
                headers=self.headers, verify=self.verify)
            response_page = json.loads(response_page.text.replace("'", "\""))
            response = response + response_page
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_merge_requests(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/merge_requests',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_merge_request(self, project_id=None, merge_id=None):
        if project_id is None or merge_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/merge_requests/{merge_id}',
                                     headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                            Merge Rules API                                                       #
    ####################################################################################################################
    @require_auth
    def get_project_level_rules(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/approval_rules', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_level_rule(self, project_id=None, approval_rule_id=None):
        if project_id is None or approval_rule_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/approval_rules/{approval_rule_id}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_project_level_rule(self, project_id=None, approvals_required=None, name=None,
                                  applies_to_all_protected_branches=None, group_ids=None, protected_branch_ids=None,
                                  report_type=None, rule_type=None, user_ids=None):
        if project_id is None or approvals_required is None or name is None:
            raise MissingParameterError
        data = {}
        if approvals_required:
            if not isinstance(approvals_required, int):
                raise ParameterError
            data['approvals_required'] = approvals_required
        if name:
            if not isinstance(name, str):
                raise ParameterError
            data['name'] = name
        if applies_to_all_protected_branches:
            if not isinstance(applies_to_all_protected_branches, bool):
                raise ParameterError
            data['applies_to_all_protected_branches'] = applies_to_all_protected_branches
        if group_ids:
            if not isinstance(group_ids, list):
                raise ParameterError
            data['group_ids'] = group_ids
        if protected_branch_ids:
            if not isinstance(protected_branch_ids, list):
                raise ParameterError
            data['protected_branch_ids'] = protected_branch_ids
        if report_type:
            if report_type not in ['license_scanning', 'code_coverage']:
                raise ParameterError
            data['report_type'] = report_type
        if rule_type:
            if rule_type not in ['any_approver', 'regular']:
                raise ParameterError
            data['rule_type'] = rule_type
        if user_ids:
            if not isinstance(user_ids, list):
                raise ParameterError
            data['user_ids'] = user_ids
        if len(data) > 0:
            data = json.dumps(data, indent=4)
            response = self._session.post(f'{self.url}/projects/{project_id}/approval_rules', headers=self.headers,
                                          data=data,
                                          verify=self.verify)
            try:
                return response.json()
            except ValueError:
                return response
        else:
            raise MissingParameterError

    @require_auth
    def update_project_level_rule(self, project_id=None, approval_rule_id=None, approvals_required=None, name=None,
                                  applies_to_all_protected_branches=None, group_ids=None, protected_branch_ids=None,
                                  report_type=None, rule_type=None, user_ids=None):
        if project_id is None or approval_rule_id is None or approvals_required is None or name is None:
            raise MissingParameterError
        data = {}
        if approvals_required:
            if not isinstance(approvals_required, int):
                raise ParameterError
            data['approvals_required'] = approvals_required
        if name:
            if not isinstance(name, str):
                raise ParameterError
            data['name'] = name
        if applies_to_all_protected_branches:
            if not isinstance(applies_to_all_protected_branches, bool):
                raise ParameterError
            data['applies_to_all_protected_branches'] = applies_to_all_protected_branches
        if group_ids:
            if not isinstance(group_ids, list):
                raise ParameterError
            data['group_ids'] = group_ids
        if protected_branch_ids:
            if not isinstance(protected_branch_ids, list):
                raise ParameterError
            data['protected_branch_ids'] = protected_branch_ids
        if report_type:
            if report_type not in ['license_scanning', 'code_coverage']:
                raise ParameterError
            data['report_type'] = report_type
        if rule_type:
            if rule_type not in ['any_approver', 'regular']:
                raise ParameterError
            data['rule_type'] = rule_type
        if user_ids:
            if not isinstance(user_ids, list):
                raise ParameterError
            data['user_ids'] = user_ids
        if len(data) > 0:
            data = json.dumps(data, indent=4)
            response = self._session.put(f'{self.url}/projects/{project_id}/approval_rules/{approval_rule_id}',
                                         headers=self.headers, data=data, verify=self.verify)
            try:
                return response.json()
            except ValueError or AttributeError:
                return response
        else:
            raise MissingParameterError

    @require_auth
    def delete_project_level_rule(self, project_id=None, approval_rule_id=None):
        if project_id is None or approval_rule_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}/approval_rules/{approval_rule_id}',
                                        headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def merge_request_level_approvals(self, project_id=None, merge_request_iid=None):
        if project_id is None or merge_request_iid is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/merge_requests/{merge_request_iid}/approvals',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_approval_state_merge_requests(self, project_id=None, merge_request_iid=None):
        if project_id is None or merge_request_iid is None:
            raise MissingParameterError
        response = self._session.get(
            f'{self.url}/projects/{project_id}/merge_requests/{merge_request_iid}/approval_state',
            headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_merge_request_level_rules(self, project_id=None, merge_request_iid=None):
        if project_id is None or merge_request_iid is None:
            raise MissingParameterError
        response = self._session.get(
            f'{self.url}/projects/{project_id}/merge_requests/{merge_request_iid}/approval_rules',
            headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def approve_merge_request(self, project_id=None, merge_request_iid=None):
        if project_id is None or merge_request_iid is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/merge_requests/{merge_request_iid}/approve',
                                      headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def unapprove_merge_request(self, project_id=None, merge_request_iid=None):
        if project_id is None or merge_request_iid is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/merge_requests/{merge_request_iid}/unapprove',
                                      headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                               Packages API                                                       #
    ####################################################################################################################
    def get_repository_packages(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/packages', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                Pipeline API                                                      #
    ####################################################################################################################
    @require_auth
    def get_pipelines(self, project_id=None, per_page=100):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/pipelines?per_page={per_page}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_pipeline(self, project_id=None, pipeline_id=None):
        if project_id is None or pipeline_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/pipelines/{pipeline_id}', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def run_pipeline(self, project_id=None, reference=None, variables=None):
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                Projects API                                                      #
    ####################################################################################################################
    @require_auth
    def get_projects(self, max_pages=0, per_page=100, order_by='updated'):
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_nested_projects_by_group(self, group_id=None, max_pages=0, per_page=100):
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
    def get_project_contributors(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/contributors',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_statistics(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}?statistics=true',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def edit_project(self, project_id=None, allow_merge_on_skipped_pipeline=None,
                     only_allow_merge_if_all_status_checks_passed=None, analytics_access_level=None,
                     approvals_before_merge=None, auto_cancel_pending_pipelines=None, auto_devops_deploy_strategy=None,
                     auto_devops_enabled=None, autoclose_referenced_issues=None, avatar=None, build_git_strategy=None,
                     build_timeout=None, builds_access_level=None, ci_config_path=None, ci_default_git_depth=None,
                     ci_forward_deployment_enabled=None, ci_allow_fork_pipelines_to_run_in_parent_project=None,
                     ci_separated_caches=None, container_expiration_policy_attributes=None,
                     container_registry_access_level=None, default_branch=None, description=None, emails_disabled=None,
                     enforce_auth_checks_on_uploads=None,
                     external_authorization_classification_label=None, forking_access_level=None, import_url=None,
                     issues_access_level=None, issues_template=None, keep_latest_artifact=None, lfs_enabled=None,
                     merge_commit_template=None, merge_method=None, merge_pipelines_enabled=None,
                     merge_requests_access_level=None, merge_requests_template=None,
                     merge_trains_enabled=None, mirror_overwrites_diverged_branches=None, mirror_trigger_builds=None,
                     mirror_user_id=None, mirror=None, mr_default_target_self=None, name=None,
                     only_allow_merge_if_all_discussions_are_resolved=None, only_allow_merge_if_pipeline_succeeds=None,
                     only_mirror_protected_branches=None, operations_access_level=None, packages_enabled=None,
                     pages_access_level=None, path=None, printing_merge_request_link_enabled=None, public_builds=None,
                     releases_access_level=None, remove_source_branch_after_merge=None, repository_access_level=None,
                     repository_storage=None, request_access_enabled=None, requirements_access_level=None,
                     resolve_outdated_diff_discussions=None, restrict_user_defined_variables=None,
                     security_and_compliance_access_level=None, service_desk_enabled=None, shared_runners_enabled=None,
                     snippets_access_level=None, squash_commit_template=None, squash_option=None,
                     suggestion_commit_message=None, tag_list=None, topics=None, visibility=None,
                     wiki_access_level=None):
        if project_id is None:
            raise MissingParameterError

        data = {}
        if allow_merge_on_skipped_pipeline:
            if not isinstance(allow_merge_on_skipped_pipeline, bool):
                raise ParameterError
            data['allow_merge_on_skipped_pipeline'] = allow_merge_on_skipped_pipeline
        if only_allow_merge_if_all_status_checks_passed:
            if not isinstance(only_allow_merge_if_all_status_checks_passed, bool):
                raise ParameterError
            data['only_allow_merge_if_all_status_checks_passed'] = only_allow_merge_if_all_status_checks_passed
        if analytics_access_level:
            if analytics_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['analytics_access_level'] = analytics_access_level
        if approvals_before_merge:
            if not isinstance(approvals_before_merge, int):
                raise ParameterError
            data['approvals_before_merge'] = approvals_before_merge
        if auto_cancel_pending_pipelines:
            if auto_cancel_pending_pipelines not in ['disabled', 'enabled']:
                raise ParameterError
            data['auto_cancel_pending_pipelines'] = auto_cancel_pending_pipelines
        if auto_devops_deploy_strategy:
            if auto_devops_deploy_strategy not in ['continuous', 'manual', 'timed_incremental']:
                raise ParameterError
            data['auto_devops_deploy_strategy'] = auto_devops_deploy_strategy
        if auto_devops_enabled:
            if not isinstance(auto_devops_enabled, bool):
                raise ParameterError
            data['auto_devops_enabled'] = auto_devops_enabled
        if autoclose_referenced_issues:
            if not isinstance(autoclose_referenced_issues, bool):
                raise ParameterError
            data['autoclose_referenced_issues'] = autoclose_referenced_issues
        if avatar:
            if not isinstance(avatar, str):
                raise ParameterError
            data['avatar'] = avatar
        if build_git_strategy:
            if not isinstance(build_git_strategy, str):
                raise ParameterError
            data['build_git_strategy'] = build_git_strategy
        if build_timeout:
            if not isinstance(build_timeout, int):
                raise ParameterError
            data['build_timeout'] = build_timeout
        if builds_access_level:
            if builds_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['builds_access_level'] = builds_access_level
        if ci_config_path:
            if not isinstance(ci_config_path, str):
                raise ParameterError
            data['ci_config_path'] = ci_config_path
        if ci_default_git_depth:
            if not isinstance(ci_default_git_depth, int):
                raise ParameterError
            data['ci_default_git_depth'] = ci_default_git_depth
        if ci_forward_deployment_enabled:
            if not isinstance(ci_forward_deployment_enabled, bool):
                raise ParameterError
            data['ci_forward_deployment_enabled'] = ci_forward_deployment_enabled
        if ci_allow_fork_pipelines_to_run_in_parent_project:
            if not isinstance(ci_allow_fork_pipelines_to_run_in_parent_project, bool):
                raise ParameterError
            data['ci_allow_fork_pipelines_to_run_in_parent_project'] = ci_allow_fork_pipelines_to_run_in_parent_project
        if ci_separated_caches:
            if not isinstance(ci_separated_caches, bool):
                raise ParameterError
            data['ci_separated_caches'] = ci_separated_caches
        if container_expiration_policy_attributes:
            if not isinstance(container_expiration_policy_attributes, str):
                raise ParameterError
            data['container_expiration_policy_attributes'] = container_expiration_policy_attributes
        if container_registry_access_level:
            if not isinstance(container_registry_access_level, str):
                raise ParameterError
            data['container_registry_access_level'] = container_registry_access_level
        if default_branch:
            if not isinstance(default_branch, str):
                raise ParameterError
            data['default_branch'] = default_branch
        if description:
            if not isinstance(description, str):
                raise ParameterError
            data['description'] = description
        if emails_disabled:
            if not isinstance(emails_disabled, bool):
                raise ParameterError
            data['emails_disabled'] = emails_disabled
        if enforce_auth_checks_on_uploads:
            if not isinstance(enforce_auth_checks_on_uploads, bool):
                raise ParameterError
            data['enforce_auth_checks_on_uploads'] = enforce_auth_checks_on_uploads
        if external_authorization_classification_label:
            if not isinstance(external_authorization_classification_label, str):
                raise ParameterError
            data['external_authorization_classification_label'] = external_authorization_classification_label
        if forking_access_level:
            if forking_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['forking_access_level'] = forking_access_level
        if import_url:
            if not isinstance(import_url, str):
                raise ParameterError
            data['import_url'] = import_url
        if issues_access_level:
            if issues_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['issues_access_level'] = issues_access_level
        if issues_template:
            if not isinstance(issues_template, str):
                raise ParameterError
            data['issues_template'] = issues_template
        if keep_latest_artifact:
            if not isinstance(keep_latest_artifact, bool):
                raise ParameterError
            data['keep_latest_artifact'] = keep_latest_artifact
        if lfs_enabled:
            if not isinstance(lfs_enabled, bool):
                raise ParameterError
            data['lfs_enabled'] = lfs_enabled
        if merge_commit_template:
            if not isinstance(merge_commit_template, str):
                raise ParameterError
            data['merge_commit_template'] = merge_commit_template
        if merge_method:
            if not isinstance(merge_method, str):
                raise ParameterError
            data['merge_method'] = merge_method
        if merge_pipelines_enabled:
            if not isinstance(merge_pipelines_enabled, bool):
                raise ParameterError
            data['merge_pipelines_enabled'] = merge_pipelines_enabled
        if merge_requests_access_level:
            if merge_requests_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['merge_requests_access_level'] = merge_requests_access_level
        if merge_requests_template:
            if not isinstance(merge_requests_template, str):
                raise ParameterError
            data['merge_requests_template'] = merge_requests_template
        if merge_trains_enabled:
            if not isinstance(merge_trains_enabled, bool):
                raise ParameterError
            data['merge_trains_enabled'] = merge_trains_enabled
        if mirror_overwrites_diverged_branches:
            if not isinstance(mirror_overwrites_diverged_branches, bool):
                raise ParameterError
            data['mirror_overwrites_diverged_branches'] = mirror_overwrites_diverged_branches
        if mirror_trigger_builds:
            if not isinstance(mirror_trigger_builds, bool):
                raise ParameterError
            data['mirror_trigger_builds'] = mirror_trigger_builds
        if mirror_user_id:
            if not isinstance(mirror_user_id, int):
                raise ParameterError
            data['mirror_user_id'] = mirror_user_id
        if mirror:
            if not isinstance(mirror, bool):
                raise ParameterError
            data['mirror'] = mirror
        if mr_default_target_self:
            if not isinstance(mr_default_target_self, bool):
                raise ParameterError
            data['mr_default_target_self'] = mr_default_target_self
        if name:
            if not isinstance(name, str):
                raise ParameterError
            data['name'] = name
        if only_allow_merge_if_all_discussions_are_resolved:
            if not isinstance(only_allow_merge_if_all_discussions_are_resolved, bool):
                raise ParameterError
            data['only_allow_merge_if_all_discussions_are_resolved'] = only_allow_merge_if_all_discussions_are_resolved
        if only_allow_merge_if_pipeline_succeeds:
            if not isinstance(only_allow_merge_if_pipeline_succeeds, bool):
                raise ParameterError
            data['only_allow_merge_if_pipeline_succeeds'] = only_allow_merge_if_pipeline_succeeds
        if only_mirror_protected_branches:
            if not isinstance(only_mirror_protected_branches, bool):
                raise ParameterError
            data['only_mirror_protected_branches'] = only_mirror_protected_branches
        if operations_access_level:
            if operations_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['operations_access_level'] = operations_access_level
        if packages_enabled:
            if not isinstance(packages_enabled, bool):
                raise ParameterError
            data['packages_enabled'] = packages_enabled
        if pages_access_level:
            if pages_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['pages_access_level'] = pages_access_level
        if path:
            if not isinstance(path, str):
                raise ParameterError
            data['path'] = path
        if printing_merge_request_link_enabled:
            if not isinstance(printing_merge_request_link_enabled, bool):
                raise ParameterError
            data['printing_merge_request_link_enabled'] = printing_merge_request_link_enabled
        if public_builds:
            if not isinstance(public_builds, bool):
                raise ParameterError
            data['public_builds'] = public_builds
        if releases_access_level:
            if releases_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['releases_access_level'] = releases_access_level
        if remove_source_branch_after_merge:
            if not isinstance(remove_source_branch_after_merge, bool):
                raise ParameterError
            data['remove_source_branch_after_merge'] = remove_source_branch_after_merge
        if repository_access_level:
            if repository_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['repository_access_level'] = repository_access_level
        if repository_storage:
            if not isinstance(repository_storage, str):
                raise ParameterError
            data['repository_storage'] = repository_storage
        if request_access_enabled:
            if not isinstance(request_access_enabled, bool):
                raise ParameterError
            data['request_access_enabled'] = request_access_enabled
        if requirements_access_level:
            if requirements_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['requirements_access_level'] = requirements_access_level
        if resolve_outdated_diff_discussions:
            if not isinstance(resolve_outdated_diff_discussions, bool):
                raise ParameterError
            data['resolve_outdated_diff_discussions'] = resolve_outdated_diff_discussions
        if restrict_user_defined_variables:
            if not isinstance(restrict_user_defined_variables, bool):
                raise ParameterError
            data['restrict_user_defined_variables'] = restrict_user_defined_variables
        if security_and_compliance_access_level:
            if security_and_compliance_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['security_and_compliance_access_level'] = security_and_compliance_access_level
        if service_desk_enabled:
            if not isinstance(service_desk_enabled, bool):
                raise ParameterError
            data['service_desk_enabled'] = service_desk_enabled
        if shared_runners_enabled:
            if not isinstance(shared_runners_enabled, bool):
                raise ParameterError
            data['shared_runners_enabled'] = shared_runners_enabled
        if snippets_access_level:
            if snippets_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['snippets_access_level'] = snippets_access_level
        if squash_commit_template:
            if not isinstance(squash_commit_template, str):
                raise ParameterError
            data['squash_commit_template'] = squash_commit_template
        if squash_option:
            if snippets_access_level not in ['never', 'always', 'default_on', 'default_off']:
                raise ParameterError
            data['squash_option'] = squash_option
        if suggestion_commit_message:
            if not isinstance(suggestion_commit_message, str):
                raise ParameterError
            data['suggestion_commit_message'] = suggestion_commit_message
        if tag_list:
            if not isinstance(tag_list, list):
                raise ParameterError
            data['tag_list'] = tag_list
        if topics:
            if not isinstance(topics, list):
                raise ParameterError
            data['topics'] = topics
        if visibility:
            if not isinstance(visibility, str):
                raise ParameterError
            data['visibility'] = visibility
        if wiki_access_level:
            if wiki_access_level not in ['disabled', 'private', 'enabled']:
                raise ParameterError
            data['wiki_access_level'] = wiki_access_level
        if len(data) > 0:
            data = json.dumps(data, indent=4)
            response = self._session.put(f'{self.url}/projects/{project_id}', data=data, headers=self.headers,
                                         verify=self.verify)
            try:
                return response.json()
            except ValueError:
                return response
        else:
            raise MissingParameterError

    @require_auth
    def get_project_groups(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/groups', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def archive_project(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/archive', headers=self.headers,
                                      verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def unarchive_project(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/unarchive', headers=self.headers,
                                      verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_project(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def share_project(self, project_id=None, group_id=None, group_access=None, expires_at=None):
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                       Protected Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_protected_branches(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/protected_branches',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_protected_branch(self, project_id=None, branch=None):
        if project_id is None or branch is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/protected_branches/{branch}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def protect_branch(self, project_id=None, branch=None, push_access_level=None, merge_access_level=None,
                       unprotect_access_level=None, allow_force_push=None, allowed_to_push=None, allowed_to_merge=None,
                       allowed_to_unprotect=None, code_owner_approval_required=None):
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def unprotect_branch(self, project_id=None, branch=None):
        if project_id is None or branch is None:
            raise MissingParameterError
        self._session.delete(f'{self.url}/projects/{project_id}/protected_branches/{branch}',
                             headers=self.headers, verify=self.verify)

    @require_auth
    def require_code_owner_approvals_single_branch(self, project_id=None, branch=None):
        if project_id is None or branch is None:
            raise MissingParameterError
        response = self._session.patch(f'{self.url}/projects/{project_id}/protected_branches/{branch}',
                                       headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                Runners API                                                       #
    ####################################################################################################################
    @require_auth
    def get_runners(self, runner_type=None, status=None, paused=None, tag_list=None, all_runners=False):
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
    def get_runner(self, runner_id=None):
        if runner_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/runners/{runner_id}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def update_runner_details(self, runner_id=None, description=None, active=None, paused=None, tag_list=None,
                              run_untagged=None, locked=None, access_level=None, maximum_timeout=None):
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def pause_runner(self, runner_id=None, active=None):
        if runner_id is None or active is None:
            raise MissingParameterError
        data = {'active': active}
        data = json.dumps(data, indent=4)
        response = self._session.put(f'{self.url}/runners/{runner_id}', headers=self.headers, data=data,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_runner_jobs(self, runner_id=None):
        if runner_id is None:
            raise MissingParameterError
        response = self._session.put(f'{self.url}/runners/{runner_id}/jobs', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_project_runners(self, project_id=None, runner_type=None, status=None, paused=None, tag_list=None,
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def enable_project_runner(self, project_id=None, runner_id=None):
        if project_id is None or runner_id is None:
            raise MissingParameterError
        data = json.dumps({'runner_id': runner_id}, indent=4)
        response = self._session.put(f'{self.url}/projects/{project_id}/runners', headers=self.headers, data=data,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_project_runner(self, project_id=None, runner_id=None):
        if project_id is None or runner_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/projects/{project_id}/runners/{runner_id}', headers=self.headers,
                                        verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_group_runners(self, group_id=None, runner_type=None, status=None, paused=None, tag_list=None,
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def register_new_runner(self, token=None, description=None, info=None, paused=None, locked=None, run_untagged=None,
                            tag_list=None, access_level=None, maximum_timeout=None, maintenance_note=None):
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_runner(self, runner_id=None, token=None):
        if runner_id is None and token is None:
            raise MissingParameterError
        if runner_id:
            response = self._session.delete(f'{self.url}/runners/{runner_id}', headers=self.headers, verify=self.verify)
        else:
            data = {'token': token}
            data = json.dumps(data, indent=4)
            response = self._session.delete(f'{self.url}/runners', headers=self.headers, data=data,
                                            verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def verify_runner_authentication(self, token=None):
        if token is None:
            raise MissingParameterError
        data = {'token': token}
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/runners/verify', headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def reset_gitlab_runner_token(self):
        response = self._session.post(f'{self.url}/runners/reset_registration_token', headers=self.headers,
                                      verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def reset_project_runner_token(self, project_id):
        if project_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/projects/{project_id}/runners/reset_registration_token',
                                      headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def reset_group_runner_token(self, group_id):
        if group_id is None:
            raise MissingParameterError
        response = self._session.post(f'{self.url}/groups/{group_id}/runners/reset_registration_token',
                                      headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def reset_token(self, runner_id, token=None):
        if runner_id is None or token is None:
            raise MissingParameterError
        data = {'token': token}
        data = json.dumps(data, indent=4)
        response = self._session.post(f'{self.url}/runners/{runner_id}/reset_authentication_token',
                                      headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                Users API                                                         #
    ####################################################################################################################
    @require_auth
    def get_users(self, username=None, active=None, blocked=None, external=None, exclude_internal=None,
                  exclude_external=None, without_project_bots=None, extern_uid=None, provider=None, created_before=None,
                  created_after=None, with_custom_attributes=None, sort=None, order_by=None, two_factor=None,
                  without_projects=None, admins=None, saml_provider_id=None, max_pages=0, per_page=100):
        response = self._session.get(f'{self.url}/users?per_page={per_page}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        user_filter = f"?per_page={per_page}"
        if username:
            if not isinstance(username, str):
                raise ParameterError
            user_filter = f'{user_filter}&username={username}'
        if active:
            if not isinstance(active, str):
                raise ParameterError
            user_filter = f'{user_filter}&active={active}'
        if blocked:
            if not isinstance(blocked, str):
                raise ParameterError
            user_filter = f'{user_filter}&blocked={blocked}'
        if external:
            if not isinstance(external, str):
                raise ParameterError
            user_filter = f'{user_filter}&external={external}'
        if exclude_internal:
            if not isinstance(exclude_internal, str):
                raise ParameterError
            user_filter = f'{user_filter}&exclude_internal={exclude_internal}'
        if exclude_external:
            if not isinstance(exclude_external, str):
                raise ParameterError
            user_filter = f'{user_filter}&exclude_external={exclude_external}'
        if without_project_bots:
            if not isinstance(without_project_bots, str):
                raise ParameterError
            user_filter = f'{user_filter}&without_project_bots={without_project_bots}'
        if order_by:
            if order_by not in ['id', 'name', 'username', 'created_at', 'updated_at']:
                raise ParameterError
            user_filter = f'{user_filter}&order_by={order_by}'
        if sort:
            if sort not in ['asc', 'desc']:
                raise ParameterError
            user_filter = f'{user_filter}&sort={sort}'
        if two_factor:
            if two_factor not in ['enabled', 'disabled']:
                raise ParameterError
            user_filter = f'{user_filter}&two_factor={two_factor}'
        if without_projects:
            if not isinstance(without_projects, bool):
                raise ParameterError
            user_filter = f'{user_filter}&without_projects={without_projects}'
        if admins:
            if not isinstance(admins, bool):
                raise ParameterError
            user_filter = f'{user_filter}&admins={admins}'
        if saml_provider_id:
            if not isinstance(saml_provider_id, int):
                raise ParameterError
            user_filter = f'{user_filter}&saml_provider_id={saml_provider_id}'
        if extern_uid:
            if not isinstance(extern_uid, str):
                raise ParameterError
            user_filter = f'{user_filter}&extern_uid={extern_uid}'
        if provider:
            if not isinstance(provider, str):
                raise ParameterError
            user_filter = f'{user_filter}&provider={provider}'
        if created_before:
            if not isinstance(created_before, str):
                raise ParameterError
            user_filter = f'{user_filter}&created_before={created_before}'
        if created_after:
            if not isinstance(created_after, str):
                raise ParameterError
            user_filter = f'{user_filter}&created_after={created_after}'
        if with_custom_attributes:
            if not isinstance(with_custom_attributes, str):
                raise ParameterError
            user_filter = f'{user_filter}&with_custom_attributes={with_custom_attributes}'
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, max_pages):
            response_page = self._session.get(f'{self.url}/users{user_filter}&page={page}',
                                              headers=self.headers, verify=self.verify)
            response_page = json.loads(response_page.text.replace("'", "\""))
            response = response + response_page
        try:
            print(f"RESPONSE: {response}")
            return response.json()
        except ValueError or AttributeError:
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
        try:
            return response.json()
        except ValueError or AttributeError:
            return response
