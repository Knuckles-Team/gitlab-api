#!/usr/bin/python
# coding: utf-8

import os
import sys

import pytest
from conftest import reason

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    import gitlab_api
    from gitlab_api.gitlab_input_models import (
        BranchModel,
        CommitModel,
        DeployTokenModel,
        GroupModel,
        JobModel,
        PackageModel,
        PipelineModel,
        ProjectModel,
        ProtectedBranchModel,
        MergeRequestRuleModel,
        MergeRequestModel,
        ReleaseModel,
        RunnerModel,
        UserModel,
        WikiModel,
    )
    from gitlab_api.gitlab_response_models import (
        Response,
    )

except ImportError:
    skip = True
    raise ("ERROR IMPORTING", ImportError)
else:
    skip = False


reason = "do not run on MacOS or windows OR dependency is not installed OR " + reason


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_branch_model():
    project_id = 2
    branch_name = "test_branch"
    reference = "main"
    branch = BranchModel(project_id=project_id, branch=branch_name, reference=reference)
    assert branch.project_id == project_id
    assert branch.api_parameters == {"branch": "test_branch", "ref": "main"}


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_model():
    project_id = 2
    branch_name = "test_branch"
    commit = CommitModel(project_id=project_id, branch_name=branch_name)
    assert commit.project_id == project_id


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_model():
    project_id = 2
    title = "test merge"
    author_id = 12341
    source_branch = "development"
    target_branch = "production"
    merge_request_rule = MergeRequestModel(
        project_id=project_id,
        title=title,
        author_id=author_id,
        source_branch=source_branch,
        target_branch=target_branch,
    )
    assert merge_request_rule.project_id == project_id
    assert merge_request_rule.title == title
    assert merge_request_rule.author_id == author_id
    assert merge_request_rule.target_branch == target_branch
    assert merge_request_rule.source_branch == source_branch


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_rule_model():
    project_id = 2
    group_ids = [1, 2, 3, 4]
    name = "test rule"
    merge_request_rule = MergeRequestRuleModel(
        project_id=project_id, name=name, approvals_required=9, group_ids=group_ids
    )
    assert merge_request_rule.project_id == project_id
    assert merge_request_rule.name == name
    assert merge_request_rule.approvals_required == 9


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_model():
    project_id = 1234
    pipeline = PipelineModel(project_id=project_id, per_page=100, reference="test")
    assert project_id == pipeline.project_id
    assert pipeline.api_parameters == {"page": 1, "per_page": 100, "ref": "test"}


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_project_model():
    group_id = 1234
    project_id = 5679
    project = ProjectModel(group_id=group_id)
    assert group_id == project.group_id
    project = ProjectModel(project_id=project_id)
    assert project_id == project.project_id
    project = ProjectModel(project_id=project_id, group_id=group_id)
    assert project_id == project.project_id
    assert group_id == project.group_id
    assert project.api_parameters == {"group_id": 1234}
    releases = [
        {
            "tag_name": "v0.2",
            "description": "## CHANGELOG\r\n\r\n- Escape label and milestone titles to prevent XSS in GLFM autocomplete. !2740\r\n- Prevent private snippets from being embeddable.\r\n- Add subresources removal to member destroy service.",
            "name": "Awesome app v0.2 beta",
            "created_at": "2019-01-03T01:56:19.539Z",
            "released_at": "2019-01-03T01:56:19.539Z",
            "author": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                "web_url": "https://gitlab.example.com/root",
            },
            "commit": {
                "id": "079e90101242458910cccd35eab0e211dfc359c0",
                "short_id": "079e9010",
                "title": "Update README.md",
                "created_at": "2019-01-03T01:55:38.000Z",
                "parent_ids": ["f8d3d94cbd347e924aa7b715845e439d00e80ca4"],
                "message": "Update README.md",
                "author_name": "Administrator",
                "author_email": "admin@example.com",
                "authored_date": "2019-01-03T01:55:38.000Z",
                "committer_name": "Administrator",
                "committer_email": "admin@example.com",
                "committed_date": "2019-01-03T01:55:38.000Z",
            },
            "milestones": [
                {
                    "id": 51,
                    "iid": 1,
                    "project_id": 24,
                    "title": "v1.0-rc",
                    "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                    "state": "closed",
                    "created_at": "2019-07-12T19:45:44.256Z",
                    "updated_at": "2019-07-12T19:45:44.256Z",
                    "due_date": "2019-08-16",
                    "start_date": "2019-07-30",
                    "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/1",
                    "issue_stats": {"total": 98, "closed": 76},
                },
                {
                    "id": 52,
                    "iid": 2,
                    "project_id": 24,
                    "title": "v1.0",
                    "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                    "state": "closed",
                    "created_at": "2019-07-16T14:00:12.256Z",
                    "updated_at": "2019-07-16T14:00:12.256Z",
                    "due_date": "2019-08-16",
                    "start_date": "2019-07-30",
                    "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/2",
                    "issue_stats": {"total": 24, "closed": 21},
                },
            ],
            "commit_path": "/root/awesome-app/commit/588440f66559714280628a4f9799f0c4eb880a4a",
            "tag_path": "/root/awesome-app/-/tags/v0.11.1",
            "assets": {
                "count": 6,
                "sources": [
                    {
                        "format": "zip",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.2/awesome-app-v0.2.zip",
                    },
                    {
                        "format": "tar.gz",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.2/awesome-app-v0.2.tar.gz",
                    },
                    {
                        "format": "tar.bz2",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.2/awesome-app-v0.2.tar.bz2",
                    },
                    {
                        "format": "tar",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.2/awesome-app-v0.2.tar",
                    },
                ],
                "links": [
                    {
                        "id": 2,
                        "name": "awesome-v0.2.msi",
                        "url": "http://192.168.10.15:3000/msi",
                        "link_type": "other",
                    },
                    {
                        "id": 1,
                        "name": "awesome-v0.2.dmg",
                        "url": "http://192.168.10.15:3000",
                        "link_type": "other",
                    },
                ],
                "evidence_file_path": "https://gitlab.example.com/root/awesome-app/-/releases/v0.2/evidence.json",
            },
            "evidences": [
                {
                    "sha": "760d6cdfb0879c3ffedec13af470e0f71cf52c6cde4d",
                    "filepath": "https://gitlab.example.com/root/awesome-app/-/releases/v0.2/evidence.json",
                    "collected_at": "2019-01-03T01:56:19.539Z",
                }
            ],
        },
        {
            "tag_name": "v0.1",
            "description": "## CHANGELOG\r\n\r\n-Remove limit of 100 when searching repository code. !8671\r\n- Show error message when attempting to reopen an MR and there is an open MR for the same branch. !16447 (Akos Gyimesi)\r\n- Fix a bug where internal email pattern wasn't respected. !22516",
            "name": "Awesome app v0.1 alpha",
            "created_at": "2019-01-03T01:55:18.203Z",
            "released_at": "2019-01-03T01:55:18.203Z",
            "author": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                "web_url": "https://gitlab.example.com/root",
            },
            "commit": {
                "id": "f8d3d94cbd347e924aa7b715845e439d00e80ca4",
                "short_id": "f8d3d94c",
                "title": "Initial commit",
                "created_at": "2019-01-03T01:53:28.000Z",
                "parent_ids": [],
                "message": "Initial commit",
                "author_name": "Administrator",
                "author_email": "admin@example.com",
                "authored_date": "2019-01-03T01:53:28.000Z",
                "committer_name": "Administrator",
                "committer_email": "admin@example.com",
                "committed_date": "2019-01-03T01:53:28.000Z",
            },
            "assets": {
                "count": 4,
                "sources": [
                    {
                        "format": "zip",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.zip",
                    },
                    {
                        "format": "tar.gz",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.gz",
                    },
                    {
                        "format": "tar.bz2",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.bz2",
                    },
                    {
                        "format": "tar",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar",
                    },
                ],
                "links": [],
                "evidence_file_path": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/evidence.json",
            },
            "evidences": [
                {
                    "sha": "c3ffedec13af470e760d6cdfb08790f71cf52c6cde4d",
                    "filepath": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/evidence.json",
                    "collected_at": "2019-01-03T01:55:18.203Z",
                }
            ],
            "_links": {
                "closed_issues_url": "https://gitlab.example.com/root/awesome-app/-/issues?release_tag=v0.1&scope=all&state=closed",
                "closed_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=closed",
                "edit_url": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/edit",
                "merged_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=merged",
                "opened_issues_url": "https://gitlab.example.com/root/awesome-app/-/issues?release_tag=v0.1&scope=all&state=opened",
                "opened_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=opened",
                "self": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1",
            },
        },
    ]


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_model():
    group_id = 6
    group = GroupModel(group_id=group_id, per_page=100, page=0)
    assert group_id == group.group_id
    assert group.api_parameters == {"per_page": 100}


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branches_model():
    project_id = 5679
    branch = "test"
    protected_branch = ProtectedBranchModel(
        project_id=project_id,
        branch=branch,
        allow_force_push=False,
        code_owner_approval_required=False,
        allowed_to_push=[{"access_level": 40}],
        allowed_to_merge=[{"access_level": 20}],
        all_runners=True,
    )
    assert project_id == protected_branch.project_id
    assert protected_branch.allowed_to_push == [{"access_level": 40}]
    assert protected_branch.allowed_to_merge == [{"access_level": 20}]


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_release_model():
    project_id = 5679
    release = ReleaseModel(project_id=project_id, simple=True)
    assert project_id == release.project_id
    assert release.api_parameters == {"simple": True}


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_model():
    project_id = 5679
    runner = RunnerModel(project_id=project_id, active=True, status="Online")
    assert project_id == runner.project_id
    assert runner.api_parameters == {"status": "online"}


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_user_model():
    username = "test_user"
    user = UserModel(username=username, active=True)
    assert user.username == username
    assert user.active
    assert user.api_parameters == {"username": "test_user"}


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_wiki_model():
    project_id = 5679
    wiki = WikiModel(project_id=project_id, with_content=True)
    assert project_id == wiki.project_id
    assert wiki.api_parameters == {"with_content": True}


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_project_response_1():
    example_data = [
        {
            "id": 4,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "description_html": '<p data-sourcepos="1:1-1:56" dir="auto">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>',
            "name": "Diaspora Client",
            "name_with_namespace": "Diaspora / Diaspora Client",
            "path": "diaspora-client",
            "path_with_namespace": "diaspora/diaspora-client",
            "created_at": "2013-09-30T13:46:02Z",
            "updated_at": "2013-09-30T13:46:02Z",
            "default_branch": "main",
            "tag_list": ["example", "disapora client"],
            "topics": ["example", "disapora client"],
            "ssh_url_to_repo": "git@gitlab.example.com:diaspora/diaspora-client.git",
            "http_url_to_repo": "https://gitlab.example.com/diaspora/diaspora-client.git",
            "web_url": "https://gitlab.example.com/diaspora/diaspora-client",
            "readme_url": "https://gitlab.example.com/diaspora/diaspora-client/blob/main/README.md",
            "avatar_url": "https://gitlab.example.com/uploads/project/avatar/4/uploads/avatar.png",
            "forks_count": 0,
            "star_count": 0,
            "last_activity_at": "2022-06-24T17:11:26.841Z",
            "namespace": {
                "id": 3,
                "name": "Diaspora",
                "path": "diaspora",
                "kind": "group",
                "full_path": "diaspora",
                "parent_id": None,
                "avatar_url": "https://gitlab.example.com/uploads/project/avatar/6/uploads/avatar.png",
                "web_url": "https://gitlab.example.com/diaspora",
            },
            "container_registry_image_prefix": "registry.gitlab.example.com/diaspora/diaspora-client",
            "_links": {
                "self": "https://gitlab.example.com/api/v4/projects/4",
                "issues": "https://gitlab.example.com/api/v4/projects/4/issues",
                "merge_requests": "https://gitlab.example.com/api/v4/projects/4/merge_requests",
                "repo_branches": "https://gitlab.example.com/api/v4/projects/4/repository/branches",
                "labels": "https://gitlab.example.com/api/v4/projects/4/labels",
                "events": "https://gitlab.example.com/api/v4/projects/4/events",
                "members": "https://gitlab.example.com/api/v4/projects/4/members",
                "cluster_agents": "https://gitlab.example.com/api/v4/projects/4/cluster_agents",
            },
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "public",
            "resolve_outdated_diff_discussions": False,
            "repository_object_format": "test",
            "merge_pipelines_enabled": True,
            "merge_trains_skip_train_allowed": True,
            "allow_pipeline_trigger_approve_deployment": True,
            "mr_default_target_self": True,
            "forked_from_project": {},
            "container_expiration_policy": {
                "cadence": "1month",
                "enabled": True,
                "keep_n": 1,
                "older_than": "14d",
                "name_regex": "",
                "name_regex_keep": ".*-main",
                "next_run_at": "2022-06-25T17:11:26.865Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": True,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "enabled",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "emails_disabled": None,
            "emails_enabled": None,
            "shared_runners_enabled": True,
            "group_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 1,
            "import_url": None,
            "import_type": None,
            "import_status": "none",
            "import_error": None,
            "open_issues_count": 0,
            "ci_default_git_depth": 20,
            "ci_forward_deployment_enabled": True,
            "ci_forward_deployment_rollback_allowed": True,
            "ci_allow_fork_pipelines_to_run_in_parent_project": True,
            "ci_job_token_scope_enabled": False,
            "ci_separated_caches": True,
            "ci_restrict_pipeline_cancellation_role": "developer",
            "public_jobs": True,
            "build_timeout": 3600,
            "auto_cancel_pending_pipelines": "enabled",
            "ci_config_path": "",
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "restrict_user_defined_variables": False,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": "gitlab/%{id}-%{title}",
            "auto_devops_enabled": False,
            "auto_devops_deploy_strategy": "continuous",
            "autoclose_referenced_issues": True,
            "keep_latest_artifact": True,
            "runner_token_expiration_interval": None,
            "external_authorization_classification_label": "",
            "requirements_enabled": False,
            "requirements_access_level": "enabled",
            "security_and_compliance_enabled": False,
            "compliance_frameworks": [],
            "warn_about_potentially_unwanted_characters": True,
            "permissions": {"project_access": None, "group_access": None},
        },
        {
            "id": 4,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "description_html": '<p data-sourcepos="1:1-1:56" dir="auto">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>',
            "default_branch": "main",
            "visibility": "private",
            "ssh_url_to_repo": "git@example.com:diaspora/diaspora-client.git",
            "http_url_to_repo": "http://example.com/diaspora/diaspora-client.git",
            "web_url": "http://example.com/diaspora/diaspora-client",
            "readme_url": "http://example.com/diaspora/diaspora-client/blob/main/README.md",
            "tag_list": ["example", "disapora client"],
            "topics": ["example", "disapora client"],
            "owner": {
                "id": 3,
                "name": "Diaspora",
                "created_at": "2013-09-30T13:46:02Z",
            },
            "name": "Diaspora Client",
            "name_with_namespace": "Diaspora / Diaspora Client",
            "path": "diaspora-client",
            "path_with_namespace": "diaspora/diaspora-client",
            "issues_enabled": True,
            "open_issues_count": 1,
            "merge_requests_enabled": True,
            "jobs_enabled": True,
            "wiki_enabled": True,
            "snippets_enabled": False,
            "can_create_merge_request_in": True,
            "resolve_outdated_diff_discussions": False,
            "container_registry_enabled": False,
            "container_registry_access_level": "disabled",
            "security_and_compliance_access_level": "disabled",
            "created_at": "2013-09-30T13:46:02Z",
            "updated_at": "2013-09-30T13:46:02Z",
            "last_activity_at": "2013-09-30T13:46:02Z",
            "creator_id": 3,
            "import_url": None,
            "import_type": None,
            "import_status": "none",
            "import_error": None,
            "namespace": {
                "id": 3,
                "name": "Diaspora",
                "path": "diaspora",
                "kind": "group",
                "full_path": "diaspora",
            },
            "archived": False,
            "avatar_url": "http://example.com/uploads/project/avatar/4/uploads/avatar.png",
            "shared_runners_enabled": True,
            "group_runners_enabled": True,
            "forks_count": 0,
            "star_count": 0,
            "runners_token": "b8547b1dc37721d05889db52fa2f02",
            "ci_default_git_depth": 50,
            "ci_forward_deployment_enabled": True,
            "ci_forward_deployment_rollback_allowed": True,
            "ci_allow_fork_pipelines_to_run_in_parent_project": True,
            "ci_separated_caches": True,
            "ci_restrict_pipeline_cancellation_role": "developer",
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": False,
            "restrict_user_defined_variables": False,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": False,
            "request_access_enabled": False,
            "merge_method": "merge",
            "squash_option": "default_on",
            "autoclose_referenced_issues": True,
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": "gitlab/%{id}-%{title}",
            "marked_for_deletion_at": "2020-04-03",
            "marked_for_deletion_on": "2020-04-03",
            "statistics": {
                "commit_count": 37,
                "storage_size": 1038090,
                "repository_size": 1038090,
                "wiki_size": 0,
                "lfs_objects_size": 0,
                "job_artifacts_size": 0,
                "pipeline_artifacts_size": 0,
                "packages_size": 0,
                "snippets_size": 0,
                "uploads_size": 0,
            },
            "container_registry_image_prefix": "registry.example.com/diaspora/diaspora-client",
            "_links": {
                "self": "http://example.com/api/v4/projects",
                "issues": "http://example.com/api/v4/projects/1/issues",
                "merge_requests": "http://example.com/api/v4/projects/1/merge_requests",
                "repo_branches": "http://example.com/api/v4/projects/1/repository_branches",
                "labels": "http://example.com/api/v4/projects/1/labels",
                "events": "http://example.com/api/v4/projects/1/events",
                "members": "http://example.com/api/v4/projects/1/members",
                "cluster_agents": "http://example.com/api/v4/projects/1/cluster_agents",
            },
        },
        {
            "id": 6,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "description_html": '<p data-sourcepos="1:1-1:56" dir="auto">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>',
            "default_branch": "main",
            "visibility": "private",
            "ssh_url_to_repo": "git@example.com:brightbox/puppet.git",
            "http_url_to_repo": "http://example.com/brightbox/puppet.git",
            "web_url": "http://example.com/brightbox/puppet",
            "readme_url": "http://example.com/brightbox/puppet/blob/main/README.md",
            "tag_list": ["example", "puppet"],
            "topics": ["example", "puppet"],
            "owner": {
                "id": 4,
                "name": "Brightbox",
                "created_at": "2013-09-30T13:46:02Z",
            },
            "name": "Puppet",
            "name_with_namespace": "Brightbox / Puppet",
            "path": "puppet",
            "path_with_namespace": "brightbox/puppet",
            "issues_enabled": True,
            "open_issues_count": 1,
            "merge_requests_enabled": True,
            "jobs_enabled": True,
            "wiki_enabled": True,
            "snippets_enabled": False,
            "can_create_merge_request_in": True,
            "resolve_outdated_diff_discussions": False,
            "container_registry_enabled": False,
            "container_registry_access_level": "disabled",
            "security_and_compliance_access_level": "disabled",
            "created_at": "2013-09-30T13:46:02Z",
            "updated_at": "2013-09-30T13:46:02Z",
            "last_activity_at": "2013-09-30T13:46:02Z",
            "creator_id": 3,
            "import_url": None,
            "import_type": None,
            "namespace": {
                "id": 4,
                "name": "Brightbox",
                "path": "brightbox",
                "kind": "group",
                "full_path": "brightbox",
            },
            "import_status": "none",
            "import_error": None,
            "permissions": {
                "project_access": {"access_level": 10, "notification_level": 3},
                "group_access": {"access_level": 50, "notification_level": 3},
            },
            "archived": False,
            "avatar_url": None,
            "shared_runners_enabled": True,
            "group_runners_enabled": True,
            "forks_count": 0,
            "star_count": 0,
            "runners_token": "b8547b1dc37721d05889db52fa2f02",
            "ci_default_git_depth": 0,
            "ci_forward_deployment_enabled": True,
            "ci_forward_deployment_rollback_allowed": True,
            "ci_allow_fork_pipelines_to_run_in_parent_project": True,
            "ci_separated_caches": True,
            "ci_restrict_pipeline_cancellation_role": "developer",
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": False,
            "restrict_user_defined_variables": False,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": False,
            "request_access_enabled": False,
            "merge_method": "merge",
            "squash_option": "default_on",
            "auto_devops_enabled": True,
            "auto_devops_deploy_strategy": "continuous",
            "repository_storage": "default",
            "approvals_before_merge": 0,
            "mirror": False,
            "mirror_user_id": 45,
            "mirror_trigger_builds": False,
            "only_mirror_protected_branches": False,
            "mirror_overwrites_diverged_branches": False,
            "external_authorization_classification_label": None,
            "packages_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "autoclose_referenced_issues": True,
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": "gitlab/%{id}-%{title}",
            "statistics": {
                "commit_count": 12,
                "storage_size": 2066080,
                "repository_size": 2066080,
                "wiki_size": 0,
                "lfs_objects_size": 0,
                "job_artifacts_size": 0,
                "pipeline_artifacts_size": 0,
                "packages_size": 0,
                "snippets_size": 0,
                "uploads_size": 0,
            },
            "container_registry_image_prefix": "registry.example.com/brightbox/puppet",
            "_links": {
                "self": "http://example.com/api/v4/projects",
                "issues": "http://example.com/api/v4/projects/1/issues",
                "merge_requests": "http://example.com/api/v4/projects/1/merge_requests",
                "repo_branches": "http://example.com/api/v4/projects/1/repository_branches",
                "labels": "http://example.com/api/v4/projects/1/labels",
                "events": "http://example.com/api/v4/projects/1/events",
                "members": "http://example.com/api/v4/projects/1/members",
                "cluster_agents": "http://example.com/api/v4/projects/1/cluster_agents",
            },
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Project"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_project_response_3():
    example_data = [
        {
            "id": 89,
            "description": None,
            "name": "Immich",
            "name_with_namespace": "Homelab / Containers / Immich",
            "path": "immich",
            "path_with_namespace": "homelab/containers/immich",
            "created_at": "2024-05-26T15:35:04.767Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/immich.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/immich.git",
            "web_url": "http://gitlab.arpa/homelab/containers/immich",
            "readme_url": "http://gitlab.arpa/homelab/containers/immich/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-05-26T15:35:04.767Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/89",
                "issues": "http://gitlab.arpa/api/v4/projects/89/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/89/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/89/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/89/labels",
                "events": "http://gitlab.arpa/api/v4/projects/89/events",
                "members": "http://gitlab.arpa/api/v4/projects/89/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/89/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-05-27T15:35:04.842Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-05-26T16:25:48.455Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 87,
            "description": None,
            "name": "Ubuntu",
            "name_with_namespace": "Homelab / Containers / Ubuntu",
            "path": "ubuntu",
            "path_with_namespace": "homelab/containers/ubuntu",
            "created_at": "2024-03-16T15:07:06.719Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/ubuntu.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/ubuntu.git",
            "web_url": "http://gitlab.arpa/homelab/containers/ubuntu",
            "readme_url": "http://gitlab.arpa/homelab/containers/ubuntu/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T15:07:06.719Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/87",
                "issues": "http://gitlab.arpa/api/v4/projects/87/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/87/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/87/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/87/labels",
                "events": "http://gitlab.arpa/api/v4/projects/87/events",
                "members": "http://gitlab.arpa/api/v4/projects/87/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/87/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-03-17T15:07:06.796Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T15:09:52.871Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 86,
            "description": None,
            "name": "Ansible",
            "name_with_namespace": "Homelab / Containers / Ansible",
            "path": "ansible",
            "path_with_namespace": "homelab/containers/ansible",
            "created_at": "2024-03-16T14:38:07.498Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/ansible.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/ansible.git",
            "web_url": "http://gitlab.arpa/homelab/containers/ansible",
            "readme_url": "http://gitlab.arpa/homelab/containers/ansible/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T14:38:07.498Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/86",
                "issues": "http://gitlab.arpa/api/v4/projects/86/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/86/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/86/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/86/labels",
                "events": "http://gitlab.arpa/api/v4/projects/86/events",
                "members": "http://gitlab.arpa/api/v4/projects/86/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/86/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-03-17T14:38:07.523Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T15:01:28.640Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 85,
            "description": None,
            "name": "Python",
            "name_with_namespace": "Homelab / Containers / Python",
            "path": "python",
            "path_with_namespace": "homelab/containers/python",
            "created_at": "2024-03-16T14:34:42.232Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/python.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/python.git",
            "web_url": "http://gitlab.arpa/homelab/containers/python",
            "readme_url": "http://gitlab.arpa/homelab/containers/python/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T14:34:42.232Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/85",
                "issues": "http://gitlab.arpa/api/v4/projects/85/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/85/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/85/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/85/labels",
                "events": "http://gitlab.arpa/api/v4/projects/85/events",
                "members": "http://gitlab.arpa/api/v4/projects/85/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/85/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-03-17T14:34:42.363Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T14:37:00.955Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 83,
            "description": None,
            "name": "Postfix Admin",
            "name_with_namespace": "Homelab / Containers / Postfix Admin",
            "path": "postfix-admin",
            "path_with_namespace": "homelab/containers/postfix-admin",
            "created_at": "2024-01-29T03:59:06.988Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/postfix-admin.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/postfix-admin.git",
            "web_url": "http://gitlab.arpa/homelab/containers/postfix-admin",
            "readme_url": "http://gitlab.arpa/homelab/containers/postfix-admin/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-01-29T03:59:06.988Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/83",
                "issues": "http://gitlab.arpa/api/v4/projects/83/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/83/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/83/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/83/labels",
                "events": "http://gitlab.arpa/api/v4/projects/83/events",
                "members": "http://gitlab.arpa/api/v4/projects/83/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/83/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-01-30T03:59:07.095Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-01-29T03:59:10.250Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 75,
            "description": None,
            "name": "Gosec",
            "name_with_namespace": "Homelab / Containers / Gosec",
            "path": "gosec",
            "path_with_namespace": "homelab/containers/gosec",
            "created_at": "2024-01-03T07:33:48.854Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/gosec.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/gosec.git",
            "web_url": "http://gitlab.arpa/homelab/containers/gosec",
            "readme_url": "http://gitlab.arpa/homelab/containers/gosec/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:48:22.545Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/75",
                "issues": "http://gitlab.arpa/api/v4/projects/75/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/75/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/75/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/75/labels",
                "events": "http://gitlab.arpa/api/v4/projects/75/events",
                "members": "http://gitlab.arpa/api/v4/projects/75/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/75/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-01-04T07:33:48.897Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:54:18.407Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 74,
            "description": "",
            "name": "Golang",
            "name_with_namespace": "Homelab / Containers / Golang",
            "path": "golang",
            "path_with_namespace": "homelab/containers/golang",
            "created_at": "2024-01-03T04:48:54.843Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/golang.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/golang.git",
            "web_url": "http://gitlab.arpa/homelab/containers/golang",
            "readme_url": "http://gitlab.arpa/homelab/containers/golang/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:48:05.723Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/74",
                "issues": "http://gitlab.arpa/api/v4/projects/74/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/74/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/74/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/74/labels",
                "events": "http://gitlab.arpa/api/v4/projects/74/events",
                "members": "http://gitlab.arpa/api/v4/projects/74/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/74/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-01-04T04:48:54.877Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:54:52.580Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 72,
            "description": None,
            "name": "Semgrep",
            "name_with_namespace": "Homelab / Containers / Semgrep",
            "path": "semgrep",
            "path_with_namespace": "homelab/containers/semgrep",
            "created_at": "2024-01-03T03:26:54.279Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/semgrep.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/semgrep.git",
            "web_url": "http://gitlab.arpa/homelab/containers/semgrep",
            "readme_url": "http://gitlab.arpa/homelab/containers/semgrep/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:51:25.867Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/72",
                "issues": "http://gitlab.arpa/api/v4/projects/72/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/72/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/72/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/72/labels",
                "events": "http://gitlab.arpa/api/v4/projects/72/events",
                "members": "http://gitlab.arpa/api/v4/projects/72/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/72/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-01-04T03:26:54.340Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:55:14.303Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 70,
            "description": None,
            "name": "Genius Web",
            "name_with_namespace": "Homelab / Containers / Genius Web",
            "path": "genius-web",
            "path_with_namespace": "homelab/containers/genius-web",
            "created_at": "2023-11-20T06:11:28.211Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/genius-web.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/genius-web.git",
            "web_url": "http://gitlab.arpa/homelab/containers/genius-web",
            "readme_url": "http://gitlab.arpa/homelab/containers/genius-web/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 1,
            "last_activity_at": "2023-12-10T01:57:13.785Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/70",
                "issues": "http://gitlab.arpa/api/v4/projects/70/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/70/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/70/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/70/labels",
                "events": "http://gitlab.arpa/api/v4/projects/70/events",
                "members": "http://gitlab.arpa/api/v4/projects/70/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/70/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-21T06:11:28.281Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2023-12-10T01:57:13.785Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 69,
            "description": "",
            "name": "Genius Agent Service",
            "name_with_namespace": "Homelab / Containers / Genius Agent Service",
            "path": "genius-agent",
            "path_with_namespace": "homelab/containers/genius-agent",
            "created_at": "2023-11-20T06:03:12.564Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/genius-agent.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/genius-agent.git",
            "web_url": "http://gitlab.arpa/homelab/containers/genius-agent",
            "readme_url": "http://gitlab.arpa/homelab/containers/genius-agent/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2023-11-20T06:03:12.564Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/69",
                "issues": "http://gitlab.arpa/api/v4/projects/69/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/69/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/69/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/69/labels",
                "events": "http://gitlab.arpa/api/v4/projects/69/events",
                "members": "http://gitlab.arpa/api/v4/projects/69/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/69/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-21T06:03:12.719Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2023-11-20T06:10:12.594Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 67,
            "description": None,
            "name": "Baserow",
            "name_with_namespace": "Homelab / Containers / Baserow",
            "path": "baserow",
            "path_with_namespace": "homelab/containers/baserow",
            "created_at": "2023-11-13T21:00:05.601Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/baserow.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/baserow.git",
            "web_url": "http://gitlab.arpa/homelab/containers/baserow",
            "readme_url": "http://gitlab.arpa/homelab/containers/baserow/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:45:11.288Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/67",
                "issues": "http://gitlab.arpa/api/v4/projects/67/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/67/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/67/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/67/labels",
                "events": "http://gitlab.arpa/api/v4/projects/67/events",
                "members": "http://gitlab.arpa/api/v4/projects/67/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/67/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T21:00:05.622Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:54:30.802Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 66,
            "description": None,
            "name": "Docker Registry WebUI",
            "name_with_namespace": "Homelab / Containers / Docker Registry WebUI",
            "path": "docker-registry-webui",
            "path_with_namespace": "homelab/containers/docker-registry-webui",
            "created_at": "2023-11-13T18:37:27.064Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/docker-registry-webui.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/docker-registry-webui.git",
            "web_url": "http://gitlab.arpa/homelab/containers/docker-registry-webui",
            "readme_url": "http://gitlab.arpa/homelab/containers/docker-registry-webui/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:46:39.415Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/66",
                "issues": "http://gitlab.arpa/api/v4/projects/66/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/66/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/66/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/66/labels",
                "events": "http://gitlab.arpa/api/v4/projects/66/events",
                "members": "http://gitlab.arpa/api/v4/projects/66/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/66/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T18:37:27.087Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:50:21.223Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 65,
            "description": None,
            "name": "Stable Diffusion",
            "name_with_namespace": "Homelab / Containers / Stable Diffusion",
            "path": "stable-diffusion",
            "path_with_namespace": "homelab/containers/stable-diffusion",
            "created_at": "2023-11-13T14:49:01.426Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/stable-diffusion.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/stable-diffusion.git",
            "web_url": "http://gitlab.arpa/homelab/containers/stable-diffusion",
            "readme_url": "http://gitlab.arpa/homelab/containers/stable-diffusion/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:50:36.589Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/65",
                "issues": "http://gitlab.arpa/api/v4/projects/65/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/65/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/65/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/65/labels",
                "events": "http://gitlab.arpa/api/v4/projects/65/events",
                "members": "http://gitlab.arpa/api/v4/projects/65/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/65/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:49:01.458Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:50:36.589Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 64,
            "description": None,
            "name": "Portainer",
            "name_with_namespace": "Homelab / Containers / Portainer",
            "path": "portainer",
            "path_with_namespace": "homelab/containers/portainer",
            "created_at": "2023-11-13T14:47:42.246Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/portainer.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/portainer.git",
            "web_url": "http://gitlab.arpa/homelab/containers/portainer",
            "readme_url": "http://gitlab.arpa/homelab/containers/portainer/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2023-11-13T14:47:42.246Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/64",
                "issues": "http://gitlab.arpa/api/v4/projects/64/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/64/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/64/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/64/labels",
                "events": "http://gitlab.arpa/api/v4/projects/64/events",
                "members": "http://gitlab.arpa/api/v4/projects/64/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/64/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:47:42.274Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2023-11-13T14:47:43.330Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 63,
            "description": None,
            "name": "PGVector",
            "name_with_namespace": "Homelab / Containers / PGVector",
            "path": "pgvector",
            "path_with_namespace": "homelab/containers/pgvector",
            "created_at": "2023-11-13T14:46:45.234Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/pgvector.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/pgvector.git",
            "web_url": "http://gitlab.arpa/homelab/containers/pgvector",
            "readme_url": "http://gitlab.arpa/homelab/containers/pgvector/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-05-02T02:41:09.085Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/63",
                "issues": "http://gitlab.arpa/api/v4/projects/63/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/63/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/63/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/63/labels",
                "events": "http://gitlab.arpa/api/v4/projects/63/events",
                "members": "http://gitlab.arpa/api/v4/projects/63/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/63/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:46:45.265Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-05-02T02:43:31.680Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 62,
            "description": None,
            "name": "NGINX Proxy",
            "name_with_namespace": "Homelab / Containers / NGINX Proxy",
            "path": "nginx-proxy",
            "path_with_namespace": "homelab/containers/nginx-proxy",
            "created_at": "2023-11-13T14:44:57.315Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/nginx-proxy.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/nginx-proxy.git",
            "web_url": "http://gitlab.arpa/homelab/containers/nginx-proxy",
            "readme_url": "http://gitlab.arpa/homelab/containers/nginx-proxy/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:53:19.722Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/62",
                "issues": "http://gitlab.arpa/api/v4/projects/62/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/62/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/62/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/62/labels",
                "events": "http://gitlab.arpa/api/v4/projects/62/events",
                "members": "http://gitlab.arpa/api/v4/projects/62/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/62/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:44:57.348Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:57:43.317Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 61,
            "description": None,
            "name": "JDownloader",
            "name_with_namespace": "Homelab / Containers / JDownloader",
            "path": "jdownloader",
            "path_with_namespace": "homelab/containers/jdownloader",
            "created_at": "2023-11-13T14:43:37.229Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/jdownloader.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/jdownloader.git",
            "web_url": "http://gitlab.arpa/homelab/containers/jdownloader",
            "readme_url": "http://gitlab.arpa/homelab/containers/jdownloader/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:48:50.338Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/61",
                "issues": "http://gitlab.arpa/api/v4/projects/61/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/61/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/61/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/61/labels",
                "events": "http://gitlab.arpa/api/v4/projects/61/events",
                "members": "http://gitlab.arpa/api/v4/projects/61/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/61/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:43:37.259Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:52:54.042Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 60,
            "description": None,
            "name": "Home Assistant",
            "name_with_namespace": "Homelab / Containers / Home Assistant",
            "path": "home-assistant",
            "path_with_namespace": "homelab/containers/home-assistant",
            "created_at": "2023-11-13T14:41:56.049Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/home-assistant.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/home-assistant.git",
            "web_url": "http://gitlab.arpa/homelab/containers/home-assistant",
            "readme_url": "http://gitlab.arpa/homelab/containers/home-assistant/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2023-11-13T14:41:56.049Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/60",
                "issues": "http://gitlab.arpa/api/v4/projects/60/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/60/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/60/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/60/labels",
                "events": "http://gitlab.arpa/api/v4/projects/60/events",
                "members": "http://gitlab.arpa/api/v4/projects/60/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/60/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:41:56.081Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2023-11-13T14:41:57.573Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 59,
            "description": None,
            "name": "GitHub Runner",
            "name_with_namespace": "Homelab / Containers / GitHub Runner",
            "path": "github-runner",
            "path_with_namespace": "homelab/containers/github-runner",
            "created_at": "2023-11-13T14:39:42.027Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/github-runner.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/github-runner.git",
            "web_url": "http://gitlab.arpa/homelab/containers/github-runner",
            "readme_url": "http://gitlab.arpa/homelab/containers/github-runner/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-30T15:01:09.667Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/59",
                "issues": "http://gitlab.arpa/api/v4/projects/59/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/59/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/59/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/59/labels",
                "events": "http://gitlab.arpa/api/v4/projects/59/events",
                "members": "http://gitlab.arpa/api/v4/projects/59/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/59/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:39:42.052Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-30T15:01:09.667Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 58,
            "description": None,
            "name": "File Browser",
            "name_with_namespace": "Homelab / Containers / File Browser",
            "path": "file-browser",
            "path_with_namespace": "homelab/containers/file-browser",
            "created_at": "2023-11-13T14:39:08.984Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/file-browser.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/file-browser.git",
            "web_url": "http://gitlab.arpa/homelab/containers/file-browser",
            "readme_url": "http://gitlab.arpa/homelab/containers/file-browser/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:46:52.522Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/58",
                "issues": "http://gitlab.arpa/api/v4/projects/58/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/58/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/58/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/58/labels",
                "events": "http://gitlab.arpa/api/v4/projects/58/events",
                "members": "http://gitlab.arpa/api/v4/projects/58/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/58/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:39:09.022Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:49:58.044Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 57,
            "description": None,
            "name": "Docker Registry",
            "name_with_namespace": "Homelab / Containers / Docker Registry",
            "path": "docker-registry",
            "path_with_namespace": "homelab/containers/docker-registry",
            "created_at": "2023-11-13T14:36:44.543Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/docker-registry.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/docker-registry.git",
            "web_url": "http://gitlab.arpa/homelab/containers/docker-registry",
            "readme_url": "http://gitlab.arpa/homelab/containers/docker-registry/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T14:44:50.762Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/57",
                "issues": "http://gitlab.arpa/api/v4/projects/57/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/57/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/57/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/57/labels",
                "events": "http://gitlab.arpa/api/v4/projects/57/events",
                "members": "http://gitlab.arpa/api/v4/projects/57/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/57/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T14:36:44.577Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T14:45:04.107Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 55,
            "description": "",
            "name": "AdGuard Home",
            "name_with_namespace": "Homelab / Containers / AdGuard Home",
            "path": "adguard-home",
            "path_with_namespace": "homelab/containers/adguard-home",
            "created_at": "2023-11-13T05:00:09.110Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/adguard-home.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/adguard-home.git",
            "web_url": "http://gitlab.arpa/homelab/containers/adguard-home",
            "readme_url": "http://gitlab.arpa/homelab/containers/adguard-home/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:18:01.747Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/55",
                "issues": "http://gitlab.arpa/api/v4/projects/55/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/55/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/55/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/55/labels",
                "events": "http://gitlab.arpa/api/v4/projects/55/events",
                "members": "http://gitlab.arpa/api/v4/projects/55/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/55/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T05:00:09.132Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:45:18.623Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 54,
            "description": None,
            "name": "Adminer",
            "name_with_namespace": "Homelab / Containers / Adminer",
            "path": "adminer",
            "path_with_namespace": "homelab/containers/adminer",
            "created_at": "2023-11-13T04:59:11.973Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/adminer.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/adminer.git",
            "web_url": "http://gitlab.arpa/homelab/containers/adminer",
            "readme_url": "http://gitlab.arpa/homelab/containers/adminer/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T15:18:06.450Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/54",
                "issues": "http://gitlab.arpa/api/v4/projects/54/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/54/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/54/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/54/labels",
                "events": "http://gitlab.arpa/api/v4/projects/54/events",
                "members": "http://gitlab.arpa/api/v4/projects/54/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/54/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:59:12.020Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T15:19:44.612Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 53,
            "description": None,
            "name": "Cloudflare Connector",
            "name_with_namespace": "Homelab / Containers / Cloudflare Connector",
            "path": "cloudflare-connector",
            "path_with_namespace": "homelab/containers/cloudflare-connector",
            "created_at": "2023-11-13T04:58:14.333Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/cloudflare-connector.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/cloudflare-connector.git",
            "web_url": "http://gitlab.arpa/homelab/containers/cloudflare-connector",
            "readme_url": "http://gitlab.arpa/homelab/containers/cloudflare-connector/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:46:15.624Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/53",
                "issues": "http://gitlab.arpa/api/v4/projects/53/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/53/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/53/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/53/labels",
                "events": "http://gitlab.arpa/api/v4/projects/53/events",
                "members": "http://gitlab.arpa/api/v4/projects/53/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/53/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:58:14.359Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:50:07.583Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 52,
            "description": None,
            "name": "GitLab",
            "name_with_namespace": "Homelab / Containers / GitLab",
            "path": "gitlab",
            "path_with_namespace": "homelab/containers/gitlab",
            "created_at": "2023-11-13T04:57:16.322Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/gitlab.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/gitlab.git",
            "web_url": "http://gitlab.arpa/homelab/containers/gitlab",
            "readme_url": "http://gitlab.arpa/homelab/containers/gitlab/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-02-05T05:00:22.813Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/52",
                "issues": "http://gitlab.arpa/api/v4/projects/52/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/52/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/52/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/52/labels",
                "events": "http://gitlab.arpa/api/v4/projects/52/events",
                "members": "http://gitlab.arpa/api/v4/projects/52/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/52/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:57:16.365Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-02-05T05:00:23.325Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 51,
            "description": None,
            "name": "GitLab Runner",
            "name_with_namespace": "Homelab / Containers / GitLab Runner",
            "path": "gitlab-runner",
            "path_with_namespace": "homelab/containers/gitlab-runner",
            "created_at": "2023-11-13T04:56:24.206Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/gitlab-runner.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/gitlab-runner.git",
            "web_url": "http://gitlab.arpa/homelab/containers/gitlab-runner",
            "readme_url": "http://gitlab.arpa/homelab/containers/gitlab-runner/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-01T19:52:39.461Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/51",
                "issues": "http://gitlab.arpa/api/v4/projects/51/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/51/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/51/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/51/labels",
                "events": "http://gitlab.arpa/api/v4/projects/51/events",
                "members": "http://gitlab.arpa/api/v4/projects/51/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/51/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:56:24.231Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-01T19:57:25.677Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 50,
            "description": None,
            "name": "Heimdall",
            "name_with_namespace": "Homelab / Containers / Heimdall",
            "path": "heimdall",
            "path_with_namespace": "homelab/containers/heimdall",
            "created_at": "2023-11-13T04:55:38.049Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/heimdall.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/heimdall.git",
            "web_url": "http://gitlab.arpa/homelab/containers/heimdall",
            "readme_url": "http://gitlab.arpa/homelab/containers/heimdall/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:48:33.683Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/50",
                "issues": "http://gitlab.arpa/api/v4/projects/50/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/50/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/50/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/50/labels",
                "events": "http://gitlab.arpa/api/v4/projects/50/events",
                "members": "http://gitlab.arpa/api/v4/projects/50/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/50/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:55:38.082Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:54:55.563Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 49,
            "description": None,
            "name": "Jellyfin",
            "name_with_namespace": "Homelab / Containers / Jellyfin",
            "path": "jellyfin",
            "path_with_namespace": "homelab/containers/jellyfin",
            "created_at": "2023-11-13T04:54:50.500Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/jellyfin.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/jellyfin.git",
            "web_url": "http://gitlab.arpa/homelab/containers/jellyfin",
            "readme_url": "http://gitlab.arpa/homelab/containers/jellyfin/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 1,
            "last_activity_at": "2024-05-26T21:34:06.655Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/49",
                "issues": "http://gitlab.arpa/api/v4/projects/49/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/49/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/49/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/49/labels",
                "events": "http://gitlab.arpa/api/v4/projects/49/events",
                "members": "http://gitlab.arpa/api/v4/projects/49/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/49/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:54:50.519Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-05-26T21:39:18.792Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 48,
            "description": None,
            "name": "Postgres",
            "name_with_namespace": "Homelab / Containers / Postgres",
            "path": "postgres",
            "path_with_namespace": "homelab/containers/postgres",
            "created_at": "2023-11-13T04:54:03.315Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/postgres.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/postgres.git",
            "web_url": "http://gitlab.arpa/homelab/containers/postgres",
            "readme_url": "http://gitlab.arpa/homelab/containers/postgres/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:52:38.585Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/48",
                "issues": "http://gitlab.arpa/api/v4/projects/48/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/48/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/48/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/48/labels",
                "events": "http://gitlab.arpa/api/v4/projects/48/events",
                "members": "http://gitlab.arpa/api/v4/projects/48/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/48/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:54:03.366Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:57:19.735Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 47,
            "description": None,
            "name": "RetroArch Web",
            "name_with_namespace": "Homelab / Containers / RetroArch Web",
            "path": "retroarch-web",
            "path_with_namespace": "homelab/containers/retroarch-web",
            "created_at": "2023-11-13T04:53:14.910Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/retroarch-web.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/retroarch-web.git",
            "web_url": "http://gitlab.arpa/homelab/containers/retroarch-web",
            "readme_url": "http://gitlab.arpa/homelab/containers/retroarch-web/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:51:50.042Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/47",
                "issues": "http://gitlab.arpa/api/v4/projects/47/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/47/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/47/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/47/labels",
                "events": "http://gitlab.arpa/api/v4/projects/47/events",
                "members": "http://gitlab.arpa/api/v4/projects/47/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/47/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:53:14.980Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:57:33.317Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 46,
            "description": None,
            "name": "Selenoid",
            "name_with_namespace": "Homelab / Containers / Selenoid",
            "path": "selenoid",
            "path_with_namespace": "homelab/containers/selenoid",
            "created_at": "2023-11-13T04:52:09.793Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/selenoid.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/selenoid.git",
            "web_url": "http://gitlab.arpa/homelab/containers/selenoid",
            "readme_url": "http://gitlab.arpa/homelab/containers/selenoid/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2023-11-13T04:52:09.793Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/46",
                "issues": "http://gitlab.arpa/api/v4/projects/46/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/46/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/46/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/46/labels",
                "events": "http://gitlab.arpa/api/v4/projects/46/events",
                "members": "http://gitlab.arpa/api/v4/projects/46/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/46/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:52:09.837Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2023-11-13T04:52:12.028Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 45,
            "description": "",
            "name": "Server Fan Controller",
            "name_with_namespace": "Homelab / Containers / Server Fan Controller",
            "path": "server-fan-speed",
            "path_with_namespace": "homelab/containers/server-fan-speed",
            "created_at": "2023-11-13T04:50:20.991Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/server-fan-speed.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/server-fan-speed.git",
            "web_url": "http://gitlab.arpa/homelab/containers/server-fan-speed",
            "readme_url": "http://gitlab.arpa/homelab/containers/server-fan-speed/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:51:03.111Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/45",
                "issues": "http://gitlab.arpa/api/v4/projects/45/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/45/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/45/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/45/labels",
                "events": "http://gitlab.arpa/api/v4/projects/45/events",
                "members": "http://gitlab.arpa/api/v4/projects/45/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/45/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:50:21.049Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:57:08.798Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 44,
            "description": None,
            "name": "Wireguard",
            "name_with_namespace": "Homelab / Containers / Wireguard",
            "path": "wireguard",
            "path_with_namespace": "homelab/containers/wireguard",
            "created_at": "2023-11-13T04:48:25.294Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/wireguard.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/wireguard.git",
            "web_url": "http://gitlab.arpa/homelab/containers/wireguard",
            "readme_url": "http://gitlab.arpa/homelab/containers/wireguard/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-05-04T16:37:17.684Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/44",
                "issues": "http://gitlab.arpa/api/v4/projects/44/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/44/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/44/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/44/labels",
                "events": "http://gitlab.arpa/api/v4/projects/44/events",
                "members": "http://gitlab.arpa/api/v4/projects/44/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/44/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T04:48:25.342Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-05-04T16:37:18.289Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 43,
            "description": None,
            "name": "Ubuntu Docker In Docker",
            "name_with_namespace": "Homelab / Containers / Ubuntu Docker In Docker",
            "path": "ubuntu-dind",
            "path_with_namespace": "homelab/containers/ubuntu-dind",
            "created_at": "2023-11-13T02:58:01.169Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/ubuntu-dind.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/ubuntu-dind.git",
            "web_url": "http://gitlab.arpa/homelab/containers/ubuntu-dind",
            "readme_url": "http://gitlab.arpa/homelab/containers/ubuntu-dind/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-30T14:05:32.290Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/43",
                "issues": "http://gitlab.arpa/api/v4/projects/43/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/43/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/43/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/43/labels",
                "events": "http://gitlab.arpa/api/v4/projects/43/events",
                "members": "http://gitlab.arpa/api/v4/projects/43/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/43/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-14T02:58:01.217Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-30T14:25:48.605Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 41,
            "description": "",
            "name": "NetbootXYZ",
            "name_with_namespace": "Homelab / Containers / NetbootXYZ",
            "path": "netboot.xyz",
            "path_with_namespace": "homelab/containers/netboot.xyz",
            "created_at": "2023-11-12T16:07:29.655Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/netboot.xyz.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/netboot.xyz.git",
            "web_url": "http://gitlab.arpa/homelab/containers/netboot.xyz",
            "readme_url": None,
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:53:34.898Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/41",
                "issues": "http://gitlab.arpa/api/v4/projects/41/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/41/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/41/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/41/labels",
                "events": "http://gitlab.arpa/api/v4/projects/41/events",
                "members": "http://gitlab.arpa/api/v4/projects/41/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/41/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-11-13T16:07:29.710Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T16:57:14.495Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 40,
            "description": ":robot: The free, Open Source OpenAI alternative. Self-hosted, community-driven and local-first. Drop-in replacement for OpenAI running on consumer-grade hardware. No GPU required. Runs ggml, gguf, GPTQ, onnx, TF compatible models: llama, llama2, rwkv, whisper, vicuna, koala, cerebras, falcon, dolly, starcoder, and many others",
            "name": "LocalAI",
            "name_with_namespace": "Homelab / Containers / LocalAI",
            "path": "localai",
            "path_with_namespace": "homelab/containers/localai",
            "created_at": "2023-10-29T05:38:49.852Z",
            "default_branch": "master",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/localai.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/localai.git",
            "web_url": "http://gitlab.arpa/homelab/containers/localai",
            "readme_url": "http://gitlab.arpa/homelab/containers/localai/-/blob/master/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:49:37.672Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/40",
                "issues": "http://gitlab.arpa/api/v4/projects/40/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/40/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/40/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/40/labels",
                "events": "http://gitlab.arpa/api/v4/projects/40/events",
                "members": "http://gitlab.arpa/api/v4/projects/40/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/40/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-10-30T05:38:49.906Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "finished",
            "open_issues_count": 0,
            "description_html": '<p data-sourcepos="1:1-1:328" dir="auto"><gl-emoji title="robot face" data-name="robot" data-unicode-version="8.0">🤖</gl-emoji> The free, Open Source OpenAI alternative. Self-hosted, community-driven and local-first. Drop-in replacement for OpenAI running on consumer-grade hardware. No GPU required. Runs ggml, gguf, GPTQ, onnx, TF compatible models: llama, llama2, rwkv, whisper, vicuna, koala, cerebras, falcon, dolly, starcoder, and many others</p>',
            "updated_at": "2024-03-16T16:49:37.672Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
        {
            "id": 20,
            "description": "Service running transmission-openvpn",
            "name": "Transmission OpenVPN",
            "name_with_namespace": "Homelab / Containers / Transmission OpenVPN",
            "path": "transmission-openvpn",
            "path_with_namespace": "homelab/containers/transmission-openvpn",
            "created_at": "2023-10-29T05:17:54.453Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/transmission-openvpn.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/transmission-openvpn.git",
            "web_url": "http://gitlab.arpa/homelab/containers/transmission-openvpn",
            "readme_url": "http://gitlab.arpa/homelab/containers/transmission-openvpn/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": None,
            "star_count": 0,
            "last_activity_at": "2024-03-16T16:50:23.333Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": None,
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/20",
                "issues": "http://gitlab.arpa/api/v4/projects/20/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/20/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/20/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/20/labels",
                "events": "http://gitlab.arpa/api/v4/projects/20/events",
                "members": "http://gitlab.arpa/api/v4/projects/20/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/20/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2023-10-30T05:17:54.500Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "finished",
            "open_issues_count": 0,
            "description_html": '<p data-sourcepos="1:1-1:36" dir="auto">Service running transmission-openvpn</p>',
            "updated_at": "2024-03-16T16:55:51.683Z",
            "ci_config_path": None,
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "autoclose_referenced_issues": True,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Project"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_project_response_2():
    example_data = {
        "id": 4,
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "description_html": '<p data-sourcepos="1:1-1:56" dir="auto">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>',
        "name": "Diaspora Client",
        "name_with_namespace": "Diaspora / Diaspora Client",
        "path": "diaspora-client",
        "path_with_namespace": "diaspora/diaspora-client",
        "created_at": "2013-09-30T13:46:02Z",
        "updated_at": "2013-09-30T13:46:02Z",
        "default_branch": "main",
        "tag_list": ["example", "disapora client"],
        "topics": ["example", "disapora client"],
        "ssh_url_to_repo": "git@gitlab.example.com:diaspora/diaspora-client.git",
        "http_url_to_repo": "https://gitlab.example.com/diaspora/diaspora-client.git",
        "web_url": "https://gitlab.example.com/diaspora/diaspora-client",
        "readme_url": "https://gitlab.example.com/diaspora/diaspora-client/blob/main/README.md",
        "avatar_url": "https://gitlab.example.com/uploads/project/avatar/4/uploads/avatar.png",
        "forks_count": 0,
        "star_count": 0,
        "last_activity_at": "2022-06-24T17:11:26.841Z",
        "namespace": {
            "id": 3,
            "name": "Diaspora",
            "path": "diaspora",
            "kind": "group",
            "full_path": "diaspora",
            "parent_id": None,
            "avatar_url": "https://gitlab.example.com/uploads/project/avatar/6/uploads/avatar.png",
            "web_url": "https://gitlab.example.com/diaspora",
        },
        "container_registry_image_prefix": "registry.gitlab.example.com/diaspora/diaspora-client",
        "_links": {
            "self": "https://gitlab.example.com/api/v4/projects/4",
            "issues": "https://gitlab.example.com/api/v4/projects/4/issues",
            "merge_requests": "https://gitlab.example.com/api/v4/projects/4/merge_requests",
            "repo_branches": "https://gitlab.example.com/api/v4/projects/4/repository/branches",
            "labels": "https://gitlab.example.com/api/v4/projects/4/labels",
            "events": "https://gitlab.example.com/api/v4/projects/4/events",
            "members": "https://gitlab.example.com/api/v4/projects/4/members",
            "cluster_agents": "https://gitlab.example.com/api/v4/projects/4/cluster_agents",
        },
        "packages_enabled": True,
        "empty_repo": False,
        "archived": False,
        "visibility": "public",
        "resolve_outdated_diff_discussions": False,
        "container_expiration_policy": {
            "cadence": "1month",
            "enabled": True,
            "keep_n": 1,
            "older_than": "14d",
            "name_regex": "",
            "name_regex_keep": ".*-main",
            "next_run_at": "2022-06-25T17:11:26.865Z",
        },
        "issues_enabled": True,
        "merge_requests_enabled": True,
        "wiki_enabled": True,
        "jobs_enabled": True,
        "snippets_enabled": True,
        "container_registry_enabled": True,
        "service_desk_enabled": True,
        "can_create_merge_request_in": True,
        "issues_access_level": "enabled",
        "repository_access_level": "enabled",
        "merge_requests_access_level": "enabled",
        "forking_access_level": "enabled",
        "wiki_access_level": "enabled",
        "builds_access_level": "enabled",
        "snippets_access_level": "enabled",
        "pages_access_level": "enabled",
        "analytics_access_level": "enabled",
        "container_registry_access_level": "enabled",
        "security_and_compliance_access_level": "private",
        "emails_disabled": None,
        "emails_enabled": None,
        "shared_runners_enabled": True,
        "group_runners_enabled": True,
        "lfs_enabled": True,
        "creator_id": 1,
        "import_url": None,
        "import_type": None,
        "import_status": "none",
        "import_error": None,
        "open_issues_count": 0,
        "ci_default_git_depth": 20,
        "ci_forward_deployment_enabled": True,
        "ci_forward_deployment_rollback_allowed": True,
        "ci_allow_fork_pipelines_to_run_in_parent_project": True,
        "ci_job_token_scope_enabled": False,
        "ci_separated_caches": True,
        "ci_restrict_pipeline_cancellation_role": "developer",
        "public_jobs": True,
        "build_timeout": 3600,
        "auto_cancel_pending_pipelines": "enabled",
        "ci_config_path": "",
        "shared_with_groups": [],
        "only_allow_merge_if_pipeline_succeeds": False,
        "allow_merge_on_skipped_pipeline": None,
        "restrict_user_defined_variables": False,
        "request_access_enabled": True,
        "only_allow_merge_if_all_discussions_are_resolved": False,
        "remove_source_branch_after_merge": True,
        "printing_merge_request_link_enabled": True,
        "merge_method": "merge",
        "squash_option": "default_off",
        "enforce_auth_checks_on_uploads": True,
        "suggestion_commit_message": None,
        "merge_commit_template": None,
        "squash_commit_template": None,
        "issue_branch_template": "gitlab/%{id}-%{title}",
        "auto_devops_enabled": False,
        "auto_devops_deploy_strategy": "continuous",
        "autoclose_referenced_issues": True,
        "keep_latest_artifact": True,
        "runner_token_expiration_interval": None,
        "external_authorization_classification_label": "",
        "requirements_enabled": False,
        "requirements_access_level": "enabled",
        "security_and_compliance_enabled": False,
        "compliance_frameworks": [],
        "warn_about_potentially_unwanted_characters": True,
        "permissions": {"project_access": None, "group_access": None},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Project"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_user_response_1():
    example_data = [
        {
            "id": 1,
            "username": "john_smith",
            "name": "John Smith",
            "state": "active",
            "locked": False,
            "avatar_url": "http://localhost:3000/uploads/user/avatar/1/cd8.jpeg",
            "web_url": "http://localhost:3000/john_smith",
        },
        {
            "id": 2,
            "username": "jack_smith",
            "name": "Jack Smith",
            "state": "blocked",
            "locked": False,
            "avatar_url": "http://gravatar.com/../e32131cd8.jpeg",
            "web_url": "http://localhost:3000/jack_smith",
        },
        {
            "id": 4,
            "username": "john_smith",
            "email": "john@example.com",
            "name": "John Smith",
            "state": "active",
            "locked": False,
            "avatar_url": "http://localhost:3000/uploads/user/avatar/1/index.jpg",
            "web_url": "http://localhost:3000/john_smith",
            "created_at": "2012-05-23T08:00:58Z",
            "is_admin": False,
            "bio": "",
            "location": None,
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "discord": "",
            "website_url": "",
            "organization": "",
            "job_title": "",
            "last_sign_in_at": "2012-06-01T11:41:01Z",
            "confirmed_at": "2012-05-23T09:05:22Z",
            "theme_id": 1,
            "last_activity_on": "2012-05-23",
            "color_scheme_id": 2,
            "projects_limit": 100,
            "current_sign_in_at": "2012-06-02T06:36:55Z",
            "note": "DMCA Request: 2018-11-05 | DMCA Violation | Abuse | https://gitlab.zendesk.com/agent/tickets/123",
            "identities": [
                {"provider": "github", "extern_uid": "2435223452345"},
                {"provider": "bitbucket", "extern_uid": "john.smith"},
                {
                    "provider": "google_oauth2",
                    "extern_uid": "8776128412476123468721346",
                },
            ],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": True,
            "external": False,
            "private_profile": False,
            "current_sign_in_ip": "196.165.1.102",
            "last_sign_in_ip": "172.127.2.22",
            "namespace_id": 1,
            "created_by": None,
            "email_reset_offered_at": None,
        },
        {
            "id": 3,
            "username": "jack_smith",
            "email": "jack@example.com",
            "name": "Jack Smith",
            "state": "blocked",
            "locked": False,
            "avatar_url": "http://localhost:3000/uploads/user/avatar/2/index.jpg",
            "web_url": "http://localhost:3000/jack_smith",
            "created_at": "2012-05-23T08:01:01Z",
            "is_admin": False,
            "bio": "",
            "location": None,
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "discord": "",
            "website_url": "",
            "organization": "",
            "job_title": "",
            "last_sign_in_at": None,
            "confirmed_at": "2012-05-30T16:53:06.148Z",
            "theme_id": 1,
            "last_activity_on": "2012-05-23",
            "color_scheme_id": 3,
            "projects_limit": 100,
            "current_sign_in_at": "2014-03-19T17:54:13Z",
            "identities": [],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": True,
            "external": False,
            "private_profile": False,
            "current_sign_in_ip": "10.165.1.102",
            "last_sign_in_ip": "172.127.2.22",
            "namespace_id": 2,
            "created_by": None,
            "email_reset_offered_at": None,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_user_response_2():
    example_data = {
        "id": 1,
        "username": "john_smith",
        "name": "John Smith",
        "state": "active",
        "locked": False,
        "avatar_url": "http://localhost:3000/uploads/user/avatar/1/cd8.jpeg",
        "web_url": "http://localhost:3000/john_smith",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_branch_response_1():
    example_data = [
        {
            "name": "main",
            "merged": False,
            "protected": True,
            "default": True,
            "developers_can_push": False,
            "developers_can_merge": False,
            "can_push": True,
            "web_url": "https://gitlab.example.com/my-group/my-project/-/tree/main",
            "commit": {
                "id": "7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
                "short_id": "7b5c3cc",
                "created_at": "2012-06-28T03:44:20-07:00",
                "parent_ids": ["4ad91d3c1144c406e50c7b33bae684bd6837faf8"],
                "title": "add projects API",
                "message": "add projects API",
                "author_name": "John Smith",
                "author_email": "john@example.com",
                "authored_date": "2012-06-27T05:51:39-07:00",
                "committer_name": "John Smith",
                "committer_email": "john@example.com",
                "committed_date": "2012-06-28T03:44:20-07:00",
                "trailers": {},
                "web_url": "https://gitlab.example.com/my-group/my-project/-/commit/7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
            },
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Branch"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_branch_response_2():
    example_data = {
        "name": "main",
        "merged": False,
        "protected": True,
        "default": True,
        "developers_can_push": False,
        "developers_can_merge": False,
        "can_push": True,
        "web_url": "https://gitlab.example.com/my-group/my-project/-/tree/main",
        "commit": {
            "id": "7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
            "short_id": "7b5c3cc",
            "created_at": "2012-06-28T03:44:20-07:00",
            "parent_ids": ["4ad91d3c1144c406e50c7b33bae684bd6837faf8"],
            "title": "add projects API",
            "message": "add projects API",
            "author_name": "John Smith",
            "author_email": "john@example.com",
            "authored_date": "2012-06-27T05:51:39-07:00",
            "committer_name": "John Smith",
            "committer_email": "john@example.com",
            "committed_date": "2012-06-28T03:44:20-07:00",
            "trailers": {},
            "web_url": "https://gitlab.example.com/my-group/my-project/-/commit/7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Branch"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_branch_response_3():
    example_data = [
        {
            "name": "main",
            "merged": False,
            "protected": True,
            "default": True,
            "developers_can_push": False,
            "developers_can_merge": False,
            "can_push": True,
            "web_url": "https://gitlab.example.com/my-group/my-project/-/tree/main",
            "commit": {
                "id": "7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
                "short_id": "7b5c3cc",
                "created_at": "2012-06-28T03:44:20-07:00",
                "parent_ids": ["4ad91d3c1144c406e50c7b33bae684bd6837faf8"],
                "title": "add projects API",
                "message": "add projects API",
                "author_name": "John Smith",
                "author_email": "john@example.com",
                "authored_date": "2012-06-27T05:51:39-07:00",
                "committer_name": "John Smith",
                "committer_email": "john@example.com",
                "committed_date": "2012-06-28T03:44:20-07:00",
                "trailers": {},
                "web_url": "https://gitlab.example.com/my-group/my-project/-/commit/7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
            },
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Branch"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_branch_response_4():
    example_data = {
        "commit": {
            "id": "7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
            "short_id": "7b5c3cc",
            "created_at": "2012-06-28T03:44:20-07:00",
            "parent_ids": ["4ad91d3c1144c406e50c7b33bae684bd6837faf8"],
            "title": "add projects API",
            "message": "add projects API",
            "author_name": "Bob Smith",
            "author_email": "bob@example.com",
            "authored_date": "2012-06-27T05:51:39-07:00",
            "committer_name": "Susan Smith",
            "committer_email": "susan@example.com",
            "committed_date": "2012-06-28T03:44:20-07:00",
            "trailers": {},
            "web_url": "https://gitlab.example.com/my-group/my-project/-/commit/7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
        },
        "name": "newbranch",
        "merged": False,
        "protected": False,
        "default": False,
        "developers_can_push": False,
        "developers_can_merge": False,
        "can_push": True,
        "web_url": "https://gitlab.example.com/my-group/my-project/-/tree/newbranch",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Branch"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_1():
    example_data = [
        {
            "id": "ed899a2f4b50b4370feeea94676502b42383c746",
            "short_id": "ed899a2f4b5",
            "title": "Replace sanitize with escape once",
            "author_name": "Example User",
            "author_email": "user@example.com",
            "authored_date": "2021-09-20T11:50:22.001+00:00",
            "committer_name": "Administrator",
            "committer_email": "admin@example.com",
            "committed_date": "2021-09-20T11:50:22.001+00:00",
            "created_at": "2021-09-20T11:50:22.001+00:00",
            "message": "Replace sanitize with escape once",
            "parent_ids": ["6104942438c14ec7bd21c6cd5bd995272b3faff6"],
            "web_url": "https://gitlab.example.com/janedoe/gitlab-foss/-/commit/ed899a2f4b50b4370feeea94676502b42383c746",
            "trailers": {},
            "extended_trailers": {},
        },
        {
            "id": "6104942438c14ec7bd21c6cd5bd995272b3faff6",
            "short_id": "6104942438c",
            "title": "Sanitize for network graph",
            "author_name": "randx",
            "author_email": "user@example.com",
            "committer_name": "ExampleName",
            "committer_email": "user@example.com",
            "created_at": "2021-09-20T09:06:12.201+00:00",
            "message": "Sanitize for network graph\nCc: John Doe <johndoe@gitlab.com>\nCc: Jane Doe <janedoe@gitlab.com>",
            "parent_ids": ["ae1d9fb46aa2b07ee9836d49862ec4e2c46fbbba"],
            "web_url": "https://gitlab.example.com/janedoe/gitlab-foss/-/commit/ed899a2f4b50b4370feeea94676502b42383c746",
            "trailers": {"Cc": "Jane Doe <janedoe@gitlab.com>"},
            "extended_trailers": {
                "Cc": ["John Doe <johndoe@gitlab.com>", "Jane Doe <janedoe@gitlab.com>"]
            },
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)

    assert response.data[0].base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_2():
    example_data = {
        "id": "ed899a2f4b50b4370feeea94676502b42383c746",
        "short_id": "ed899a2f4b5",
        "title": "some commit message",
        "author_name": "Example User",
        "author_email": "user@example.com",
        "committer_name": "Example User",
        "committer_email": "user@example.com",
        "created_at": "2016-09-20T09:26:24.000-07:00",
        "message": "some commit message",
        "parent_ids": ["ae1d9fb46aa2b07ee9836d49862ec4e2c46fbbba"],
        "committed_date": "2016-09-20T09:26:24.000-07:00",
        "authored_date": "2016-09-20T09:26:24.000-07:00",
        "stats": {"additions": 2, "deletions": 2, "total": 4},
        "status": None,
        "web_url": "https://gitlab.example.com/janedoe/gitlab-foss/-/commit/ed899a2f4b50b4370feeea94676502b42383c746",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_3():
    example_data = {
        "id": "6104942438c14ec7bd21c6cd5bd995272b3faff6",
        "short_id": "6104942438c",
        "title": "Sanitize for network graph",
        "author_name": "randx",
        "author_email": "user@example.com",
        "committer_name": "Dmitriy",
        "committer_email": "user@example.com",
        "created_at": "2021-09-20T09:06:12.300+03:00",
        "message": "Sanitize for network graph",
        "committed_date": "2021-09-20T09:06:12.300+03:00",
        "authored_date": "2021-09-20T09:06:12.420+03:00",
        "parent_ids": ["ae1d9fb46aa2b07ee9836d49862ec4e2c46fbbba"],
        "last_pipeline": {
            "id": 8,
            "ref": "main",
            "sha": "2dc6aa325a317eda67812f05600bdf0fcdc70ab0",
            "status": "created",
        },
        "stats": {"additions": 15, "deletions": 10, "total": 25},
        "status": "running",
        "web_url": "https://gitlab.example.com/janedoe/gitlab-foss/-/commit/6104942438c14ec7bd21c6cd5bd995272b3faff6",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_4():
    example_data = {"count": 632}

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_5():
    example_data = {
        "id": "8b090c1b79a14f2bd9e8a738f717824ff53aebad",
        "short_id": "8b090c1b",
        "author_name": "Example User",
        "author_email": "user@example.com",
        "authored_date": "2016-12-12T20:10:39.000+01:00",
        "created_at": "2016-12-12T20:10:39.000+01:00",
        "committer_name": "Administrator",
        "committer_email": "admin@example.com",
        "committed_date": "2016-12-12T20:10:39.000+01:00",
        "title": "Feature added",
        "message": "Feature added\n\nSigned-off-by: Example User <user@example.com>\n",
        "parent_ids": ["a738f717824ff53aebad8b090c1b79a14f2bd9e8"],
        "web_url": "https://gitlab.example.com/janedoe/gitlab-foss/-/commit/8b090c1b79a14f2bd9e8a738f717824ff53aebad",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_6():
    example_data = {
        "id": "8b090c1b79a14f2bd9e8a738f717824ff53aebad",
        "short_id": "8b090c1b",
        "title": 'Revert "Feature added"',
        "created_at": "2018-11-08T15:55:26.000Z",
        "parent_ids": ["a738f717824ff53aebad8b090c1b79a14f2bd9e8"],
        "message": 'Revert "Feature added"\n\nThis reverts commit a738f717824ff53aebad8b090c1b79a14f2bd9e8',
        "author_name": "Administrator",
        "author_email": "admin@example.com",
        "authored_date": "2018-11-08T15:55:26.000Z",
        "committer_name": "Administrator",
        "committer_email": "admin@example.com",
        "committed_date": "2018-11-08T15:55:26.000Z",
        "web_url": "https://gitlab.example.com/janedoe/gitlab-foss/-/commit/8b090c1b79a14f2bd9e8a738f717824ff53aebad",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_7():
    example_data = {
        "message": "Sorry, we cannot revert this commit automatically. This commit may already have been reverted, or a more recent commit may have updated some of its content.",
        "error_code": "conflict",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_8():
    example_data = {"dry_run": "success"}

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_9():
    example_data = [
        {
            "diff": "@@ -71,6 +71,8 @@\n sudo -u git -H bundle exec rake migrate_keys RAILS_ENV=production\n sudo -u git -H bundle exec rake migrate_inline_notes RAILS_ENV=production\n \n+sudo -u git -H bundle exec rake gitlab:assets:compile RAILS_ENV=production\n+\n ```\n \n ### 6. Update config files",
            "new_path": "doc/update/5.4-to-6.0.md",
            "old_path": "doc/update/5.4-to-6.0.md",
            "a_mode": None,
            "b_mode": "100644",
            "new_file": False,
            "renamed_file": False,
            "deleted_file": False,
        }
    ]

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Diff"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_10():
    example_data = [
        {
            "note": "this code is really nice",
            "author": {
                "id": 11,
                "username": "admin",
                "email": "admin@local.host",
                "name": "Administrator",
                "state": "active",
                "created_at": "2014-03-06T08:17:35.000Z",
            },
        }
    ]

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Comment"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_11():
    example_data = {
        "author": {
            "web_url": "https://gitlab.example.com/janedoe",
            "avatar_url": "https://gitlab.example.com/uploads/user/avatar/28/jane-doe-400-400.png",
            "username": "janedoe",
            "state": "active",
            "name": "Jane Doe",
            "id": 28,
        },
        "created_at": "2016-01-19T09:44:55.600Z",
        "line_type": "new",
        "path": "README.md",
        "line": 11,
        "note": "Nice picture!",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Comment"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_12():
    example_data = [
        {
            "id": "4604744a1c64de00ff62e1e8a6766919923d2b41",
            "individual_note": True,
            "notes": [
                {
                    "id": 334686748,
                    "type": None,
                    "body": "Nice piece of code!",
                    "attachment": None,
                    "author": {
                        "id": 28,
                        "name": "Jane Doe",
                        "username": "janedoe",
                        "web_url": "https://gitlab.example.com/janedoe",
                        "state": "active",
                        "avatar_url": "https://gitlab.example.com/uploads/user/avatar/28/jane-doe-400-400.png",
                    },
                    "created_at": "2020-04-30T18:48:11.432Z",
                    "updated_at": "2020-04-30T18:48:11.432Z",
                    "system": False,
                    "noteable_id": None,
                    "noteable_type": "Commit",
                    "resolvable": False,
                    "confidential": None,
                    "noteable_iid": None,
                    "commands_changes": {},
                }
            ],
        }
    ]

    response = Response(data=example_data, status_code=200, json_output=example_data)

    assert response.data[0].base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_13():
    example_data = [
        {
            "status": "pending",
            "created_at": "2016-01-19T08:40:25.934Z",
            "started_at": None,
            "name": "bundler:audit",
            "allow_failure": True,
            "author": {
                "username": "janedoe",
                "state": "active",
                "web_url": "https://gitlab.example.com/janedoe",
                "avatar_url": "https://gitlab.example.com/uploads/user/avatar/28/jane-doe-400-400.png",
                "id": 28,
                "name": "Jane Doe",
            },
            "description": None,
            "sha": "18f3e63d05582537db6d183d9d557be09e1f90c8",
            "target_url": "https://gitlab.example.com/janedoe/gitlab-foss/builds/91",
            "finished_at": None,
            "id": 91,
            "ref": "main",
        },
        {
            "started_at": None,
            "name": "test",
            "allow_failure": False,
            "status": "pending",
            "created_at": "2016-01-19T08:40:25.832Z",
            "target_url": "https://gitlab.example.com/janedoe/gitlab-foss/builds/90",
            "id": 90,
            "finished_at": None,
            "ref": "main",
            "sha": "18f3e63d05582537db6d183d9d557be09e1f90c8",
            "author": {
                "id": 28,
                "name": "Jane Doe",
                "username": "janedoe",
                "web_url": "https://gitlab.example.com/janedoe",
                "state": "active",
                "avatar_url": "https://gitlab.example.com/uploads/user/avatar/28/jane-doe-400-400.png",
            },
            "description": None,
        },
    ]

    response = Response(data=example_data, status_code=200, json_output=example_data)

    assert response.data[0].base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_14():
    example_data = {
        "author": {
            "web_url": "https://gitlab.example.com/janedoe",
            "name": "Jane Doe",
            "avatar_url": "https://gitlab.example.com/uploads/user/avatar/28/jane-doe-400-400.png",
            "username": "janedoe",
            "state": "active",
            "id": 28,
        },
        "name": "default",
        "sha": "18f3e63d05582537db6d183d9d557be09e1f90c8",
        "status": "success",
        "coverage": 100.0,
        "description": None,
        "id": 93,
        "target_url": None,
        "ref": None,
        "started_at": None,
        "created_at": "2016-01-19T09:05:50.355Z",
        "allow_failure": False,
        "finished_at": "2016-01-19T09:05:50.365Z",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_15():
    example_data = [
        {
            "id": 45,
            "iid": 1,
            "project_id": 35,
            "title": "Add new file",
            "description": "",
            "state": "opened",
            "created_at": "2018-03-26T17:26:30.916Z",
            "updated_at": "2018-03-26T17:26:30.916Z",
            "target_branch": "main",
            "source_branch": "test-branch",
            "upvotes": 0,
            "downvotes": 0,
            "author": {
                "web_url": "https://gitlab.example.com/janedoe",
                "name": "Jane Doe",
                "avatar_url": "https://gitlab.example.com/uploads/user/avatar/28/jane-doe-400-400.png",
                "username": "janedoe",
                "state": "active",
                "id": 28,
            },
            "assignee": None,
            "source_project_id": 35,
            "target_project_id": 35,
            "labels": [],
            "draft": False,
            "work_in_progress": False,
            "milestone": None,
            "merge_when_pipeline_succeeds": False,
            "merge_status": "can_be_merged",
            "sha": "af5b13261899fb2c0db30abdd0af8b07cb44fdc5",
            "merge_commit_sha": None,
            "squash_commit_sha": None,
            "user_notes_count": 0,
            "discussion_locked": None,
            "should_remove_source_branch": None,
            "force_remove_source_branch": False,
            "web_url": "https://gitlab.example.com/root/test-project/merge_requests/1",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
        }
    ]

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_16():
    example_data = {
        "signature_type": "PGP",
        "verification_status": "verified",
        "gpg_key_id": 1,
        "gpg_key_primary_keyid": "8254AAB3FBD54AC9",
        "gpg_key_user_name": "John Doe",
        "gpg_key_user_email": "johndoe@example.com",
        "gpg_key_subkey_id": None,
        "commit_source": "gitaly",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "CommitSignature"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_17():
    example_data = {
        "signature_type": "SSH",
        "verification_status": "verified",
        "key": {
            "id": 11,
            "title": "Key",
            "created_at": "2023-05-08T09:12:38.503Z",
            "expires_at": "2024-05-07T00:00:00.000Z",
            "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILZzYDq6DhLp3aX84DGIV3F6Vf+Ae4yCTTz7RnqMJOlR MyKey)",
            "usage_type": "auth_and_signing",
        },
        "commit_source": "gitaly",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "CommitSignature"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_18():
    example_data = {
        "signature_type": "X509",
        "verification_status": "unverified",
        "x509_certificate": {
            "id": 1,
            "subject": "CN=gitlab@example.org,OU=Example,O=World",
            "subject_key_identifier": "BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC:BC",
            "email": "gitlab@example.org",
            "serial_number": 278969561018901340486471282831158785578,
            "certificate_status": "good",
            "x509_issuer": {
                "id": 1,
                "subject": "CN=PKI,OU=Example,O=World",
                "subject_key_identifier": "AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB:AB",
                "crl_url": "http://example.com/pki.crl",
            },
        },
        "commit_source": "gitaly",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "CommitSignature"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response_19():
    example_data = {"message": "404 GPG Signature Not Found"}

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "CommitSignature"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_deploy_token_response_0():
    example_data = [
        {
            "id": 1,
            "name": "MyToken",
            "username": "gitlab+deploy-token-1",
            "expires_at": "2020-02-14T00:00:00.000Z",
            "revoked": False,
            "expired": False,
            "scopes": ["read_repository", "read_registry"],
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_deploy_token_response_1():
    example_data = [
        {
            "id": 1,
            "name": "MyToken",
            "username": "gitlab+deploy-token-1",
            "expires_at": "2020-02-14T00:00:00.000Z",
            "revoked": False,
            "expired": False,
            "scopes": ["read_repository", "read_registry"],
        }
    ]

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_deploy_token_response_2():
    example_data = {
        "id": 1,
        "name": "MyToken",
        "username": "gitlab+deploy-token-1",
        "expires_at": "2020-02-14T00:00:00.000Z",
        "revoked": False,
        "expired": False,
        "scopes": ["read_repository", "read_registry"],
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_deploy_token_response_3():
    example_data = {
        "id": 1,
        "name": "My deploy token",
        "username": "custom-user",
        "expires_at": "2021-01-01T00:00:00.000Z",
        "token": "jMRvtPNxrn3crTAGukpZ",
        "revoked": False,
        "expired": False,
        "scopes": ["read_repository"],
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_deploy_token_response_4():
    example_data = [
        {
            "id": 1,
            "name": "MyToken",
            "username": "gitlab+deploy-token-1",
            "expires_at": "2020-02-14T00:00:00.000Z",
            "revoked": False,
            "expired": False,
            "scopes": ["read_repository", "read_registry"],
        }
    ]

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_deploy_token_response_5():
    example_data = {
        "id": 1,
        "name": "MyToken",
        "username": "gitlab+deploy-token-1",
        "expires_at": "2020-02-14T00:00:00.000Z",
        "revoked": False,
        "expired": False,
        "scopes": ["read_repository", "read_registry"],
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_1():
    example_data = [
        {
            "id": 1,
            "iid": 1,
            "project_id": 3,
            "title": "test1",
            "description": "fixed login page css paddings",
            "state": "merged",
            "imported": False,
            "imported_from": "none",
            "merged_by": {
                "id": 87854,
                "name": "Douwe Maan",
                "username": "DouweM",
                "state": "active",
                "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
                "web_url": "https://gitlab.com/DouweM",
            },
            "merge_user": {
                "id": 87854,
                "name": "Douwe Maan",
                "username": "DouweM",
                "state": "active",
                "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
                "web_url": "https://gitlab.com/DouweM",
            },
            "merged_at": "2018-09-07T11:16:17.520Z",
            "prepared_at": "2018-09-04T11:16:17.520Z",
            "closed_by": None,
            "closed_at": None,
            "created_at": "2017-04-29T08:46:00Z",
            "updated_at": "2017-04-29T08:46:00Z",
            "target_branch": "main",
            "source_branch": "test1",
            "upvotes": 0,
            "downvotes": 0,
            "author": {
                "id": 1,
                "name": "Administrator",
                "username": "admin",
                "state": "active",
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/admin",
            },
            "assignee": {
                "id": 1,
                "name": "Administrator",
                "username": "admin",
                "state": "active",
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/admin",
            },
            "assignees": [
                {
                    "name": "Miss Monserrate Beier",
                    "username": "axel.block",
                    "id": 12,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                    "web_url": "https://gitlab.example.com/axel.block",
                }
            ],
            "reviewers": [],
            "source_project_id": 2,
            "target_project_id": 3,
            "labels": ["Community contribution", "Manage"],
            "draft": False,
            "work_in_progress": False,
            "milestone": {
                "id": 5,
                "iid": 1,
                "project_id": 3,
                "title": "v2.0",
                "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
                "state": "closed",
                "created_at": "2015-02-02T19:49:26.013Z",
                "updated_at": "2015-02-02T19:49:26.013Z",
                "due_date": "2018-09-22",
                "start_date": "2018-08-08",
                "web_url": "https://gitlab.example.com/my-group/my-project/milestones/1",
            },
            "merge_when_pipeline_succeeds": True,
            "merge_status": "can_be_merged",
            "detailed_merge_status": "not_open",
            "sha": "8888888888888888888888888888888888888888",
            "merge_commit_sha": None,
            "squash_commit_sha": None,
            "user_notes_count": 1,
            "discussion_locked": None,
            "should_remove_source_branch": True,
            "force_remove_source_branch": False,
            "allow_collaboration": False,
            "allow_maintainer_to_push": False,
            "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
            "references": {
                "short": "!1",
                "relative": "my-group/my-project!1",
                "full": "my-group/my-project!1",
            },
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "squash": False,
            "task_completion_status": {"count": 0, "completed_count": 0},
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_2():
    example_data = [
        {
            "id": 1,
            "iid": 1,
            "project_id": 3,
            "title": "test1",
            "description": "fixed login page css paddings",
            "state": "merged",
            "imported": False,
            "imported_from": "none",
            "merged_by": {
                "id": 87854,
                "name": "Douwe Maan",
                "username": "DouweM",
                "state": "active",
                "locked": False,
                "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
                "web_url": "https://gitlab.com/DouweM",
            },
            "merge_user": {
                "id": 87854,
                "name": "Douwe Maan",
                "username": "DouweM",
                "state": "active",
                "locked": False,
                "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
                "web_url": "https://gitlab.com/DouweM",
            },
            "merged_at": "2018-09-07T11:16:17.520Z",
            "prepared_at": "2018-09-04T11:16:17.520Z",
            "closed_by": None,
            "closed_at": None,
            "created_at": "2017-04-29T08:46:00Z",
            "updated_at": "2017-04-29T08:46:00Z",
            "target_branch": "main",
            "source_branch": "test1",
            "upvotes": 0,
            "downvotes": 0,
            "author": {
                "id": 1,
                "name": "Administrator",
                "username": "admin",
                "state": "active",
                "locked": False,
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/admin",
            },
            "assignee": {
                "id": 1,
                "name": "Administrator",
                "username": "admin",
                "state": "active",
                "locked": False,
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/admin",
            },
            "assignees": [
                {
                    "name": "Miss Monserrate Beier",
                    "username": "axel.block",
                    "id": 12,
                    "state": "active",
                    "locked": False,
                    "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                    "web_url": "https://gitlab.example.com/axel.block",
                }
            ],
            "reviewers": [
                {
                    "id": 2,
                    "name": "Sam Bauch",
                    "username": "kenyatta_oconnell",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/956c92487c6f6f7616b536927e22c9a0?s=80&d=identicon",
                    "web_url": "http://gitlab.example.com//kenyatta_oconnell",
                }
            ],
            "source_project_id": 2,
            "target_project_id": 3,
            "labels": ["Community contribution", "Manage"],
            "draft": False,
            "work_in_progress": False,
            "milestone": {
                "id": 5,
                "iid": 1,
                "project_id": 3,
                "title": "v2.0",
                "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
                "state": "closed",
                "created_at": "2015-02-02T19:49:26.013Z",
                "updated_at": "2015-02-02T19:49:26.013Z",
                "due_date": "2018-09-22",
                "start_date": "2018-08-08",
                "web_url": "https://gitlab.example.com/my-group/my-project/milestones/1",
            },
            "merge_when_pipeline_succeeds": True,
            "merge_status": "can_be_merged",
            "detailed_merge_status": "not_open",
            "sha": "8888888888888888888888888888888888888888",
            "merge_commit_sha": None,
            "squash_commit_sha": None,
            "user_notes_count": 1,
            "discussion_locked": None,
            "should_remove_source_branch": True,
            "force_remove_source_branch": False,
            "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
            "reference": "!1",
            "references": {
                "short": "!1",
                "relative": "!1",
                "full": "my-group/my-project!1",
            },
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "squash": False,
            "squash_on_merge": False,
            "task_completion_status": {"count": 0, "completed_count": 0},
            "has_conflicts": False,
            "blocking_discussions_resolved": True,
            "approvals_before_merge": 2,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_3():
    example_data = [
        {
            "id": 1,
            "iid": 1,
            "project_id": 3,
            "title": "test1",
            "description": "fixed login page css paddings",
            "state": "merged",
            "imported": False,
            "imported_from": "none",
            "merged_by": {
                "id": 87854,
                "name": "Douwe Maan",
                "username": "DouweM",
                "state": "active",
                "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
                "web_url": "https://gitlab.com/DouweM",
            },
            "merge_user": {
                "id": 87854,
                "name": "Douwe Maan",
                "username": "DouweM",
                "state": "active",
                "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
                "web_url": "https://gitlab.com/DouweM",
            },
            "merged_at": "2018-09-07T11:16:17.520Z",
            "prepared_at": "2018-09-04T11:16:17.520Z",
            "closed_by": None,
            "closed_at": None,
            "created_at": "2017-04-29T08:46:00Z",
            "updated_at": "2017-04-29T08:46:00Z",
            "target_branch": "main",
            "source_branch": "test1",
            "upvotes": 0,
            "downvotes": 0,
            "author": {
                "id": 1,
                "name": "Administrator",
                "username": "admin",
                "state": "active",
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/admin",
            },
            "assignee": {
                "id": 1,
                "name": "Administrator",
                "username": "admin",
                "state": "active",
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/admin",
            },
            "assignees": [
                {
                    "name": "Miss Monserrate Beier",
                    "username": "axel.block",
                    "id": 12,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                    "web_url": "https://gitlab.example.com/axel.block",
                }
            ],
            "reviewers": [
                {
                    "id": 2,
                    "name": "Sam Bauch",
                    "username": "kenyatta_oconnell",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/956c92487c6f6f7616b536927e22c9a0?s=80&d=identicon",
                    "web_url": "http://gitlab.example.com//kenyatta_oconnell",
                }
            ],
            "source_project_id": 2,
            "target_project_id": 3,
            "labels": ["Community contribution", "Manage"],
            "draft": False,
            "work_in_progress": False,
            "milestone": {
                "id": 5,
                "iid": 1,
                "project_id": 3,
                "title": "v2.0",
                "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
                "state": "closed",
                "created_at": "2015-02-02T19:49:26.013Z",
                "updated_at": "2015-02-02T19:49:26.013Z",
                "due_date": "2018-10-22",
                "start_date": "2018-09-08",
                "web_url": "gitlab.example.com/my-group/my-project/milestones/1",
            },
            "merge_when_pipeline_succeeds": True,
            "merge_status": "can_be_merged",
            "detailed_merge_status": "not_open",
            "sha": "8888888888888888888888888888888888888888",
            "merge_commit_sha": None,
            "squash_commit_sha": None,
            "user_notes_count": 1,
            "discussion_locked": None,
            "should_remove_source_branch": True,
            "force_remove_source_branch": False,
            "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
            "references": {
                "short": "!1",
                "relative": "my-project!1",
                "full": "my-group/my-project!1",
            },
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "squash": False,
            "task_completion_status": {"count": 0, "completed_count": 0},
            "has_conflicts": False,
            "blocking_discussions_resolved": True,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_4():
    # Users Model
    example_data = [
        {
            "id": 1,
            "name": "John Doe1",
            "username": "user1",
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/c922747a93b40d1ea88262bf1aebee62?s=80&d=identicon",
            "web_url": "http://localhost/user1",
        },
        {
            "id": 2,
            "name": "John Doe2",
            "username": "user2",
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/10fc7f102be8de7657fb4d80898bbfe3?s=80&d=identicon",
            "web_url": "http://localhost/user2",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_5():
    # Reviewers
    example_data = [
        {
            "user": {
                "id": 1,
                "name": "John Doe1",
                "username": "user1",
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/c922747a93b40d1ea88262bf1aebee62?s=80&d=identicon",
                "web_url": "http://localhost/user1",
            },
            "state": "unreviewed",
            "created_at": "2022-07-27T17:03:27.684Z",
        },
        {
            "user": {
                "id": 2,
                "name": "John Doe2",
                "username": "user2",
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/10fc7f102be8de7657fb4d80898bbfe3?s=80&d=identicon",
                "web_url": "http://localhost/user2",
            },
            "state": "reviewed",
            "created_at": "2022-07-27T17:03:27.684Z",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_6():
    # Commits
    example_data = [
        {
            "id": "ed899a2f4b50b4370feeea94676502b42383c746",
            "short_id": "ed899a2f4b5",
            "title": "Replace sanitize with escape once",
            "author_name": "Example User",
            "author_email": "user@example.com",
            "created_at": "2012-09-20T11:50:22+03:00",
            "message": "Replace sanitize with escape once",
        },
        {
            "id": "6104942438c14ec7bd21c6cd5bd995272b3faff6",
            "short_id": "6104942438c",
            "title": "Sanitize for network graph",
            "author_name": "Example User",
            "author_email": "user@example.com",
            "created_at": "2012-09-20T09:06:12+03:00",
            "message": "Sanitize for network graph",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)

    assert response.data[0].base_type == "Commit"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_7():
    # Changes
    example_data = {
        "id": 21,
        "iid": 1,
        "project_id": 4,
        "title": "Blanditiis beatae suscipit hic assumenda et molestias nisi asperiores repellat et.",
        "state": "reopened",
        "created_at": "2015-02-02T19:49:39.159Z",
        "updated_at": "2015-02-02T20:08:49.959Z",
        "target_branch": "secret_token",
        "source_branch": "version-1-9",
        "upvotes": 0,
        "downvotes": 0,
        "author": {
            "name": "Chad Hamill",
            "username": "jarrett",
            "id": 5,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/b95567800f828948baf5f4160ebb2473?s=40&d=identicon",
            "web_url": "https://gitlab.example.com/jarrett",
        },
        "assignee": {
            "name": "Administrator",
            "username": "root",
            "id": 1,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=40&d=identicon",
            "web_url": "https://gitlab.example.com/root",
        },
        "assignees": [
            {
                "name": "Miss Monserrate Beier",
                "username": "axel.block",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/axel.block",
            }
        ],
        "reviewers": [
            {
                "name": "Miss Monserrate Beier",
                "username": "axel.block",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/axel.block",
            }
        ],
        "source_project_id": 4,
        "target_project_id": 4,
        "labels": [],
        "description": "Qui voluptatibus placeat ipsa alias quasi. Deleniti rem ut sint. Option velit qui distinctio.",
        "draft": False,
        "work_in_progress": False,
        "milestone": {
            "id": 5,
            "iid": 1,
            "project_id": 4,
            "title": "v2.0",
            "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
            "state": "closed",
            "created_at": "2015-02-02T19:49:26.013Z",
            "updated_at": "2015-02-02T19:49:26.013Z",
            "due_date": None,
        },
        "merge_when_pipeline_succeeds": True,
        "merge_status": "can_be_merged",
        "detailed_merge_status": "can_be_merged",
        "subscribed": True,
        "sha": "8888888888888888888888888888888888888888",
        "merge_commit_sha": None,
        "squash_commit_sha": None,
        "user_notes_count": 1,
        "changes_count": "1",
        "should_remove_source_branch": True,
        "force_remove_source_branch": False,
        "squash": False,
        "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
        "references": {
            "short": "!1",
            "relative": "!1",
            "full": "my-group/my-project!1",
        },
        "discussion_locked": False,
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "task_completion_status": {"count": 0, "completed_count": 0},
        "changes": [
            {
                "old_path": "VERSION",
                "new_path": "VERSION",
                "a_mode": "100644",
                "b_mode": "100644",
                "diff": "@@ -1 +1 @@ -1.9.7 +1.9.8",
                "new_file": False,
                "renamed_file": False,
                "deleted_file": False,
            }
        ],
        "overflow": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_8():
    # Diff
    example_data = [
        {
            "old_path": "README",
            "new_path": "README",
            "a_mode": "100644",
            "b_mode": "100644",
            "diff": "@@ -1 +1 @@ -Title +README",
            "new_file": False,
            "renamed_file": False,
            "deleted_file": False,
            "generated_file": False,
        },
        {
            "old_path": "VERSION",
            "new_path": "VERSION",
            "a_mode": "100644",
            "b_mode": "100644",
            "diff": "@@ -1.9.7 +1.9.8",
            "new_file": False,
            "renamed_file": False,
            "deleted_file": False,
            "generated_file": False,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Diff"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_9():
    # Pipelines
    example_data = [
        {
            "id": 77,
            "sha": "959e04d7c7a30600c894bd3c0cd0e1ce7f42c11d",
            "ref": "main",
            "status": "success",
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_10():
    # Merge Request
    example_data = {
        "id": 1,
        "iid": 1,
        "project_id": 3,
        "title": "test1",
        "description": "fixed login page css paddings",
        "state": "merged",
        "imported": False,
        "imported_from": "none",
        "created_at": "2017-04-29T08:46:00Z",
        "updated_at": "2017-04-29T08:46:00Z",
        "target_branch": "main",
        "source_branch": "test1",
        "upvotes": 0,
        "downvotes": 0,
        "author": {
            "id": 1,
            "name": "Administrator",
            "username": "admin",
            "state": "active",
            "avatar_url": None,
            "web_url": "https://gitlab.example.com/admin",
        },
        "assignee": {
            "id": 1,
            "name": "Administrator",
            "username": "admin",
            "state": "active",
            "avatar_url": None,
            "web_url": "https://gitlab.example.com/admin",
        },
        "source_project_id": 2,
        "target_project_id": 3,
        "labels": ["Community contribution", "Manage"],
        "draft": False,
        "work_in_progress": False,
        "milestone": {
            "id": 5,
            "iid": 1,
            "project_id": 3,
            "title": "v2.0",
            "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
            "state": "closed",
            "created_at": "2015-02-02T19:49:26.013Z",
            "updated_at": "2015-02-02T19:49:26.013Z",
            "due_date": "2018-09-22",
            "start_date": "2018-08-08",
            "web_url": "https://gitlab.example.com/my-group/my-project/milestones/1",
        },
        "merge_when_pipeline_succeeds": True,
        "merge_status": "can_be_merged",
        "detailed_merge_status": "not_open",
        "merge_error": None,
        "sha": "8888888888888888888888888888888888888888",
        "merge_commit_sha": None,
        "squash_commit_sha": None,
        "user_notes_count": 1,
        "discussion_locked": None,
        "should_remove_source_branch": True,
        "force_remove_source_branch": False,
        "allow_collaboration": False,
        "allow_maintainer_to_push": False,
        "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
        "references": {
            "short": "!1",
            "relative": "!1",
            "full": "my-group/my-project!1",
        },
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "squash": False,
        "subscribed": False,
        "changes_count": "1",
        "merged_by": {
            "id": 87854,
            "name": "Douwe Maan",
            "username": "DouweM",
            "state": "active",
            "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
            "web_url": "https://gitlab.com/DouweM",
        },
        "merge_user": {
            "id": 87854,
            "name": "Douwe Maan",
            "username": "DouweM",
            "state": "active",
            "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
            "web_url": "https://gitlab.com/DouweM",
        },
        "merged_at": "2018-09-07T11:16:17.520Z",
        "prepared_at": "2018-09-04T11:16:17.520Z",
        "closed_by": None,
        "closed_at": None,
        "latest_build_started_at": "2018-09-07T07:27:38.472Z",
        "latest_build_finished_at": "2018-09-07T08:07:06.012Z",
        "first_deployed_to_production_at": None,
        "pipeline": {
            "id": 29626725,
            "sha": "2be7ddb704c7b6b83732fdd5b9f09d5a397b5f8f",
            "ref": "patch-28",
            "status": "success",
            "web_url": "https://gitlab.example.com/my-group/my-project/pipelines/29626725",
        },
        "diff_refs": {
            "base_sha": "c380d3acebd181f13629a25d2e2acca46ffe1e00",
            "head_sha": "2be7ddb704c7b6b83732fdd5b9f09d5a397b5f8f",
            "start_sha": "c380d3acebd181f13629a25d2e2acca46ffe1e00",
        },
        "diverged_commits_count": 2,
        "task_completion_status": {"count": 0, "completed_count": 0},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_11():
    example_data = {
        "id": 1,
        "iid": 1,
        "project_id": 3,
        "title": "test1",
        "description": "fixed login page css paddings",
        "state": "merged",
        "created_at": "2017-04-29T08:46:00Z",
        "updated_at": "2017-04-29T08:46:00Z",
        "target_branch": "main",
        "source_branch": "test1",
        "upvotes": 0,
        "downvotes": 0,
        "author": {
            "id": 1,
            "name": "Administrator",
            "username": "admin",
            "state": "active",
            "avatar_url": None,
            "web_url": "https://gitlab.example.com/admin",
        },
        "assignee": {
            "id": 1,
            "name": "Administrator",
            "username": "admin",
            "state": "active",
            "avatar_url": None,
            "web_url": "https://gitlab.example.com/admin",
        },
        "assignees": [
            {
                "name": "Miss Monserrate Beier",
                "username": "axel.block",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/axel.block",
            }
        ],
        "reviewers": [
            {
                "name": "Miss Monserrate Beier",
                "username": "axel.block",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/axel.block",
            }
        ],
        "source_project_id": 2,
        "target_project_id": 3,
        "labels": ["Community contribution", "Manage"],
        "draft": False,
        "work_in_progress": False,
        "milestone": {
            "id": 5,
            "iid": 1,
            "project_id": 3,
            "title": "v2.0",
            "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
            "state": "closed",
            "created_at": "2015-02-02T19:49:26.013Z",
            "updated_at": "2015-02-02T19:49:26.013Z",
            "due_date": "2018-09-22",
            "start_date": "2018-08-08",
            "web_url": "https://gitlab.example.com/my-group/my-project/milestones/1",
        },
        "merge_when_pipeline_succeeds": True,
        "merge_status": "can_be_merged",
        "detailed_merge_status": "not_open",
        "merge_error": None,
        "sha": "8888888888888888888888888888888888888888",
        "merge_commit_sha": None,
        "squash_commit_sha": None,
        "user_notes_count": 1,
        "discussion_locked": None,
        "should_remove_source_branch": True,
        "force_remove_source_branch": False,
        "allow_collaboration": False,
        "allow_maintainer_to_push": False,
        "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
        "references": {
            "short": "!1",
            "relative": "!1",
            "full": "my-group/my-project!1",
        },
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "squash": False,
        "subscribed": False,
        "changes_count": "1",
        "merged_by": {
            "id": 87854,
            "name": "Douwe Maan",
            "username": "DouweM",
            "state": "active",
            "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
            "web_url": "https://gitlab.com/DouweM",
        },
        "merge_user": {
            "id": 87854,
            "name": "Douwe Maan",
            "username": "DouweM",
            "state": "active",
            "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
            "web_url": "https://gitlab.com/DouweM",
        },
        "merged_at": "2018-09-07T11:16:17.520Z",
        "prepared_at": "2018-09-04T11:16:17.520Z",
        "closed_by": None,
        "closed_at": None,
        "latest_build_started_at": "2018-09-07T07:27:38.472Z",
        "latest_build_finished_at": "2018-09-07T08:07:06.012Z",
        "first_deployed_to_production_at": None,
        "pipeline": {
            "id": 29626725,
            "sha": "2be7ddb704c7b6b83732fdd5b9f09d5a397b5f8f",
            "ref": "patch-28",
            "status": "success",
            "web_url": "https://gitlab.example.com/my-group/my-project/pipelines/29626725",
        },
        "diff_refs": {
            "base_sha": "c380d3acebd181f13629a25d2e2acca46ffe1e00",
            "head_sha": "2be7ddb704c7b6b83732fdd5b9f09d5a397b5f8f",
            "start_sha": "c380d3acebd181f13629a25d2e2acca46ffe1e00",
        },
        "diverged_commits_count": 2,
        "task_completion_status": {"count": 0, "completed_count": 0},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_12():
    example_data = {
        "id": 1,
        "iid": 1,
        "project_id": 3,
        "title": "test1",
        "description": "fixed login page css paddings",
        "state": "merged",
        "created_at": "2017-04-29T08:46:00Z",
        "updated_at": "2017-04-29T08:46:00Z",
        "target_branch": "main",
        "source_branch": "test1",
        "upvotes": 0,
        "downvotes": 0,
        "author": {
            "id": 1,
            "name": "Administrator",
            "username": "admin",
            "state": "active",
            "avatar_url": None,
            "web_url": "https://gitlab.example.com/admin",
        },
        "assignee": {
            "id": 1,
            "name": "Administrator",
            "username": "admin",
            "state": "active",
            "avatar_url": None,
            "web_url": "https://gitlab.example.com/admin",
        },
        "assignees": [
            {
                "name": "Miss Monserrate Beier",
                "username": "axel.block",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/axel.block",
            }
        ],
        "reviewers": [
            {
                "name": "Miss Monserrate Beier",
                "username": "axel.block",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/axel.block",
            }
        ],
        "source_project_id": 2,
        "target_project_id": 3,
        "labels": ["Community contribution", "Manage"],
        "draft": False,
        "work_in_progress": False,
        "milestone": {
            "id": 5,
            "iid": 1,
            "project_id": 3,
            "title": "v2.0",
            "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
            "state": "closed",
            "created_at": "2015-02-02T19:49:26.013Z",
            "updated_at": "2015-02-02T19:49:26.013Z",
            "due_date": "2018-09-22",
            "start_date": "2018-08-08",
            "web_url": "https://gitlab.example.com/my-group/my-project/milestones/1",
        },
        "merge_when_pipeline_succeeds": False,
        "merge_status": "can_be_merged",
        "detailed_merge_status": "not_open",
        "merge_error": None,
        "sha": "8888888888888888888888888888888888888888",
        "merge_commit_sha": None,
        "squash_commit_sha": None,
        "user_notes_count": 1,
        "discussion_locked": None,
        "should_remove_source_branch": True,
        "force_remove_source_branch": False,
        "allow_collaboration": False,
        "allow_maintainer_to_push": False,
        "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
        "references": {
            "short": "!1",
            "relative": "!1",
            "full": "my-group/my-project!1",
        },
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "squash": False,
        "subscribed": False,
        "changes_count": "1",
        "merged_by": {
            "id": 87854,
            "name": "Douwe Maan",
            "username": "DouweM",
            "state": "active",
            "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
            "web_url": "https://gitlab.com/DouweM",
        },
        "merge_user": {
            "id": 87854,
            "name": "Douwe Maan",
            "username": "DouweM",
            "state": "active",
            "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
            "web_url": "https://gitlab.com/DouweM",
        },
        "merged_at": "2018-09-07T11:16:17.520Z",
        "prepared_at": "2018-09-04T11:16:17.520Z",
        "closed_by": None,
        "closed_at": None,
        "latest_build_started_at": "2018-09-07T07:27:38.472Z",
        "latest_build_finished_at": "2018-09-07T08:07:06.012Z",
        "first_deployed_to_production_at": None,
        "pipeline": {
            "id": 29626725,
            "sha": "2be7ddb704c7b6b83732fdd5b9f09d5a397b5f8f",
            "ref": "patch-28",
            "status": "success",
            "web_url": "https://gitlab.example.com/my-group/my-project/pipelines/29626725",
        },
        "diff_refs": {
            "base_sha": "c380d3acebd181f13629a25d2e2acca46ffe1e00",
            "head_sha": "2be7ddb704c7b6b83732fdd5b9f09d5a397b5f8f",
            "start_sha": "c380d3acebd181f13629a25d2e2acca46ffe1e00",
        },
        "diverged_commits_count": 2,
        "task_completion_status": {"count": 0, "completed_count": 0},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_13():
    example_data = {"rebase_in_progress": True}
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_14():
    example_data = {"rebase_in_progress": True, "merge_error": None}
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_15():
    example_data = {"rebase_in_progress": False, "merge_error": None}
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_16():
    example_data = {
        "rebase_in_progress": False,
        "merge_error": "Rebase failed. Please rebase locally",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_17():
    # Issues
    example_data = [
        {
            "state": "opened",
            "description": "Ratione dolores corrupti mollitia soluta quia.",
            "author": {
                "state": "active",
                "id": 18,
                "web_url": "https://gitlab.example.com/eileen.lowe",
                "name": "Alexandra Bashirian",
                "avatar_url": None,
                "username": "eileen.lowe",
            },
            "milestone": {
                "project_id": 1,
                "description": "Ducimus nam enim ex consequatur cumque ratione.",
                "state": "closed",
                "due_date": None,
                "iid": 2,
                "created_at": "2016-01-04T15:31:39.996Z",
                "title": "v4.0",
                "id": 17,
                "updated_at": "2016-01-04T15:31:39.996Z",
            },
            "project_id": 1,
            "assignee": {
                "state": "active",
                "id": 1,
                "name": "Administrator",
                "web_url": "https://gitlab.example.com/root",
                "avatar_url": None,
                "username": "root",
            },
            "updated_at": "2016-01-04T15:31:51.081Z",
            "id": 76,
            "title": "Consequatur vero maxime deserunt laboriosam est voluptas dolorem.",
            "created_at": "2016-01-04T15:31:51.081Z",
            "iid": 6,
            "labels": [],
            "user_notes_count": 1,
            "changes_count": "1",
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_18():
    # Comments on Merge Request
    example_data = [
        {
            "state": "opened",
            "description": "Ratione dolores corrupti mollitia soluta quia.",
            "author": {
                "state": "active",
                "id": 18,
                "web_url": "https://gitlab.example.com/eileen.lowe",
                "name": "Alexandra Bashirian",
                "avatar_url": None,
                "username": "eileen.lowe",
            },
            "milestone": {
                "project_id": 1,
                "description": "Ducimus nam enim ex consequatur cumque ratione.",
                "state": "closed",
                "due_date": None,
                "iid": 2,
                "created_at": "2016-01-04T15:31:39.996Z",
                "title": "v4.0",
                "id": 17,
                "updated_at": "2016-01-04T15:31:39.996Z",
            },
            "project_id": 1,
            "assignee": {
                "state": "active",
                "id": 1,
                "name": "Administrator",
                "web_url": "https://gitlab.example.com/root",
                "avatar_url": None,
                "username": "root",
            },
            "updated_at": "2016-01-04T15:31:51.081Z",
            "id": 76,
            "title": "Consequatur vero maxime deserunt laboriosam est voluptas dolorem.",
            "created_at": "2016-01-04T15:31:51.081Z",
            "iid": 6,
            "labels": [],
            "user_notes_count": 1,
            "changes_count": "1",
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_19():
    # Time tracking for Merge Request
    example_data = {
        "human_time_estimate": "2h",
        "human_total_time_spent": "1h",
        "time_estimate": 7200,
        "total_time_spent": 3600,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TimeStats"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_20():
    example_data = {
        "human_time_estimate": None,
        "human_total_time_spent": None,
        "time_estimate": 0,
        "total_time_spent": 0,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TimeStats"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_merge_request_response_21():
    # Merge diff versions
    example_data = [
        {
            "id": 110,
            "head_commit_sha": "33e2ee8579fda5bc36accc9c6fbd0b4fefda9e30",
            "base_commit_sha": "eeb57dffe83deb686a60a71c16c32f71046868fd",
            "start_commit_sha": "eeb57dffe83deb686a60a71c16c32f71046868fd",
            "created_at": "2016-07-26T14:44:48.926Z",
            "merge_request_id": 105,
            "state": "collected",
            "real_size": "1",
            "patch_id_sha": "d504412d5b6e6739647e752aff8e468dde093f2f",
        },
        {
            "id": 108,
            "head_commit_sha": "3eed087b29835c48015768f839d76e5ea8f07a24",
            "base_commit_sha": "eeb57dffe83deb686a60a71c16c32f71046868fd",
            "start_commit_sha": "eeb57dffe83deb686a60a71c16c32f71046868fd",
            "created_at": "2016-07-25T14:21:33.028Z",
            "merge_request_id": 105,
            "state": "collected",
            "real_size": "1",
            "patch_id_sha": "72c30d1f0115fc1d2bb0b29b24dc2982cbcdfd32",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Diff"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_1():
    example_data = [
        {
            "state": "opened",
            "description": "Ratione dolores corrupti mollitia soluta quia.",
            "author": {
                "state": "active",
                "id": 18,
                "web_url": "https://gitlab.example.com/eileen.lowe",
                "name": "Alexandra Bashirian",
                "avatar_url": None,
                "username": "eileen.lowe",
            },
            "milestone": {
                "project_id": 1,
                "description": "Ducimus nam enim ex consequatur cumque ratione.",
                "state": "closed",
                "due_date": None,
                "iid": 2,
                "created_at": "2016-01-04T15:31:39.996Z",
                "title": "v4.0",
                "id": 17,
                "updated_at": "2016-01-04T15:31:39.996Z",
            },
            "project_id": 1,
            "assignees": [
                {
                    "state": "active",
                    "id": 1,
                    "name": "Administrator",
                    "web_url": "https://gitlab.example.com/root",
                    "avatar_url": None,
                    "username": "root",
                }
            ],
            "assignee": {
                "state": "active",
                "id": 1,
                "name": "Administrator",
                "web_url": "https://gitlab.example.com/root",
                "avatar_url": None,
                "username": "root",
            },
            "type": "ISSUE",
            "updated_at": "2016-01-04T15:31:51.081Z",
            "closed_at": None,
            "closed_by": None,
            "id": 76,
            "title": "Consequatur vero maxime deserunt laboriosam est voluptas dolorem.",
            "created_at": "2016-01-04T15:31:51.081Z",
            "moved_to_id": None,
            "iid": 6,
            "labels": ["foo", "bar"],
            "upvotes": 4,
            "downvotes": 0,
            "merge_requests_count": 0,
            "user_notes_count": 1,
            "due_date": "2016-07-22",
            "imported": False,
            "imported_from": "none",
            "web_url": "http://gitlab.example.com/my-group/my-project/issues/6",
            "references": {
                "short": "#6",
                "relative": "my-group/my-project#6",
                "full": "my-group/my-project#6",
            },
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "has_tasks": True,
            "task_status": "10 of 15 tasks completed",
            "confidential": False,
            "discussion_locked": False,
            "issue_type": "issue",
            "severity": "UNKNOWN",
            "_links": {
                "self": "http://gitlab.example.com/api/v4/projects/1/issues/76",
                "notes": "http://gitlab.example.com/api/v4/projects/1/issues/76/notes",
                "award_emoji": "http://gitlab.example.com/api/v4/projects/1/issues/76/award_emoji",
                "project": "http://gitlab.example.com/api/v4/projects/1",
                "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75",
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_2():
    example_data = [
        {
            "state": "opened",
            "description": "Ratione dolores corrupti mollitia soluta quia.",
            "weight": None,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_3():
    example_data = {
        "project_id": 4,
        "description": "Omnis vero earum sunt corporis dolor et placeat.",
        "epic_iid": 5,
        "epic": {
            "id": 42,
            "iid": 5,
            "title": "My epic epic",
            "url": "/groups/h5bp/-/epics/5",
            "group_id": 8,
        },
        "iteration": {
            "id": 90,
            "iid": 4,
            "sequence": 2,
            "group_id": 162,
            "title": None,
            "description": None,
            "state": 2,
            "created_at": "2022-03-14T05:21:11.929Z",
            "updated_at": "2022-03-14T05:21:11.929Z",
            "start_date": "2022-03-08",
            "due_date": "2022-03-14",
            "web_url": "https://gitlab.com/groups/my-group/-/iterations/90",
        },
        "state": "opened",
        "health_status": "on_track",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_4():
    example_data = [
        {
            "project_id": 4,
            "milestone": {
                "due_date": None,
                "project_id": 4,
                "state": "closed",
                "description": "Rerum est voluptatem provident consequuntur molestias similique ipsum dolor.",
                "iid": 3,
                "id": 11,
                "title": "v3.0",
                "created_at": "2016-01-04T15:31:39.788Z",
                "updated_at": "2016-01-04T15:31:39.788Z",
            },
            "author": {
                "state": "active",
                "web_url": "https://gitlab.example.com/root",
                "avatar_url": None,
                "username": "root",
                "id": 1,
                "name": "Administrator",
            },
            "description": "Omnis vero earum sunt corporis dolor et placeat.",
            "state": "closed",
            "iid": 1,
            "assignees": [
                {
                    "avatar_url": None,
                    "web_url": "https://gitlab.example.com/lennie",
                    "state": "active",
                    "username": "lennie",
                    "id": 9,
                    "name": "Dr. Luella Kovacek",
                }
            ],
            "assignee": {
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/lennie",
                "state": "active",
                "username": "lennie",
                "id": 9,
                "name": "Dr. Luella Kovacek",
            },
            "type": "ISSUE",
            "labels": ["foo", "bar"],
            "upvotes": 4,
            "downvotes": 0,
            "merge_requests_count": 0,
            "id": 41,
            "title": "Ut commodi ullam eos dolores perferendis nihil sunt.",
            "updated_at": "2016-01-04T15:31:46.176Z",
            "created_at": "2016-01-04T15:31:46.176Z",
            "closed_at": None,
            "closed_by": None,
            "user_notes_count": 1,
            "due_date": None,
            "imported": False,
            "imported_from": "none",
            "web_url": "http://gitlab.example.com/my-group/my-project/issues/1",
            "references": {
                "short": "#1",
                "relative": "my-project#1",
                "full": "my-group/my-project#1",
            },
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "has_tasks": True,
            "task_status": "10 of 15 tasks completed",
            "confidential": False,
            "discussion_locked": False,
            "issue_type": "issue",
            "severity": "UNKNOWN",
            "_links": {
                "self": "http://gitlab.example.com/api/v4/projects/4/issues/41",
                "notes": "http://gitlab.example.com/api/v4/projects/4/issues/41/notes",
                "award_emoji": "http://gitlab.example.com/api/v4/projects/4/issues/41/award_emoji",
                "project": "http://gitlab.example.com/api/v4/projects/4",
                "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75",
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "epic_iid": 5,
            "epic": {
                "id": 42,
                "iid": 5,
                "title": "My epic epic",
                "url": "/groups/h5bp/-/epics/5",
                "group_id": 8,
            },
            "health_status": "at_risk",
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_5():
    example_data = [
        {
            "project_id": 4,
            "milestone": {
                "due_date": None,
                "project_id": 4,
                "state": "closed",
                "description": "Rerum est voluptatem provident consequuntur molestias similique ipsum dolor.",
                "iid": 3,
                "id": 11,
                "title": "v3.0",
                "created_at": "2016-01-04T15:31:39.788Z",
                "updated_at": "2016-01-04T15:31:39.788Z",
            },
            "author": {
                "state": "active",
                "web_url": "https://gitlab.example.com/root",
                "avatar_url": None,
                "username": "root",
                "id": 1,
                "name": "Administrator",
            },
            "description": "Omnis vero earum sunt corporis dolor et placeat.",
            "state": "closed",
            "iid": 1,
            "assignees": [
                {
                    "avatar_url": None,
                    "web_url": "https://gitlab.example.com/lennie",
                    "state": "active",
                    "username": "lennie",
                    "id": 9,
                    "name": "Dr. Luella Kovacek",
                }
            ],
            "assignee": {
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/lennie",
                "state": "active",
                "username": "lennie",
                "id": 9,
                "name": "Dr. Luella Kovacek",
            },
            "type": "ISSUE",
            "labels": ["foo", "bar"],
            "upvotes": 4,
            "downvotes": 0,
            "merge_requests_count": 0,
            "id": 41,
            "title": "Ut commodi ullam eos dolores perferendis nihil sunt.",
            "updated_at": "2016-01-04T15:31:46.176Z",
            "created_at": "2016-01-04T15:31:46.176Z",
            "closed_at": "2016-01-05T15:31:46.176Z",
            "closed_by": {
                "state": "active",
                "web_url": "https://gitlab.example.com/root",
                "avatar_url": None,
                "username": "root",
                "id": 1,
                "name": "Administrator",
            },
            "user_notes_count": 1,
            "due_date": "2016-07-22",
            "imported": False,
            "imported_from": "none",
            "web_url": "http://gitlab.example.com/my-group/my-project/issues/1",
            "references": {
                "short": "#1",
                "relative": "#1",
                "full": "my-group/my-project#1",
            },
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "has_tasks": True,
            "task_status": "10 of 15 tasks completed",
            "confidential": False,
            "discussion_locked": False,
            "issue_type": "issue",
            "severity": "UNKNOWN",
            "_links": {
                "self": "http://gitlab.example.com/api/v4/projects/4/issues/41",
                "notes": "http://gitlab.example.com/api/v4/projects/4/issues/41/notes",
                "award_emoji": "http://gitlab.example.com/api/v4/projects/4/issues/41/award_emoji",
                "project": "http://gitlab.example.com/api/v4/projects/4",
                "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75",
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "epic_iid": 5,
            "epic": {
                "id": 42,
                "iid": 5,
                "title": "My epic epic",
                "url": "/groups/h5bp/-/epics/5",
                "group_id": 8,
            },
            "health_status": "at_risk",
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_6():
    example_data = {
        "id": 1,
        "milestone": {
            "due_date": None,
            "project_id": 4,
            "state": "closed",
            "description": "Rerum est voluptatem provident consequuntur molestias similique ipsum dolor.",
            "iid": 3,
            "id": 11,
            "title": "v3.0",
            "created_at": "2016-01-04T15:31:39.788Z",
            "updated_at": "2016-01-04T15:31:39.788Z",
            "closed_at": "2016-01-05T15:31:46.176Z",
        },
        "author": {
            "state": "active",
            "web_url": "https://gitlab.example.com/root",
            "avatar_url": None,
            "username": "root",
            "id": 1,
            "name": "Administrator",
        },
        "description": "Omnis vero earum sunt corporis dolor et placeat.",
        "state": "closed",
        "iid": 1,
        "assignees": [
            {
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/lennie",
                "state": "active",
                "username": "lennie",
                "id": 9,
                "name": "Dr. Luella Kovacek",
            }
        ],
        "assignee": {
            "avatar_url": None,
            "web_url": "https://gitlab.example.com/lennie",
            "state": "active",
            "username": "lennie",
            "id": 9,
            "name": "Dr. Luella Kovacek",
        },
        "type": "ISSUE",
        "labels": [],
        "upvotes": 4,
        "downvotes": 0,
        "merge_requests_count": 0,
        "title": "Ut commodi ullam eos dolores perferendis nihil sunt.",
        "updated_at": "2016-01-04T15:31:46.176Z",
        "created_at": "2016-01-04T15:31:46.176Z",
        "closed_at": None,
        "closed_by": None,
        "subscribed": False,
        "user_notes_count": 1,
        "due_date": None,
        "imported": False,
        "imported_from": "none",
        "web_url": "http://example.com/my-group/my-project/issues/1",
        "references": {
            "short": "#1",
            "relative": "#1",
            "full": "my-group/my-project#1",
        },
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "confidential": False,
        "discussion_locked": False,
        "issue_type": "issue",
        "severity": "UNKNOWN",
        "task_completion_status": {"count": 0, "completed_count": 0},
        "weight": None,
        "has_tasks": False,
        "_links": {
            "self": "http://gitlab.example:3000/api/v4/projects/1/issues/1",
            "notes": "http://gitlab.example:3000/api/v4/projects/1/issues/1/notes",
            "award_emoji": "http://gitlab.example:3000/api/v4/projects/1/issues/1/award_emoji",
            "project": "http://gitlab.example:3000/api/v4/projects/1",
            "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75",
        },
        "moved_to_id": None,
        "service_desk_reply_to": "service.desk@gitlab.com",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_7():
    example_data = {
        "project_id": 4,
        "id": 84,
        "created_at": "2016-01-07T12:44:33.959Z",
        "iid": 14,
        "title": "Issues with auth",
        "state": "opened",
        "assignees": [],
        "assignee": None,
        "type": "ISSUE",
        "labels": ["bug"],
        "upvotes": 4,
        "downvotes": 0,
        "merge_requests_count": 0,
        "author": {
            "name": "Alexandra Bashirian",
            "avatar_url": None,
            "state": "active",
            "web_url": "https://gitlab.example.com/eileen.lowe",
            "id": 18,
            "username": "eileen.lowe",
        },
        "description": None,
        "updated_at": "2016-01-07T12:44:33.959Z",
        "closed_at": None,
        "closed_by": None,
        "milestone": None,
        "subscribed": True,
        "user_notes_count": 0,
        "due_date": None,
        "web_url": "http://gitlab.example.com/my-group/my-project/issues/14",
        "references": {
            "short": "#14",
            "relative": "#14",
            "full": "my-group/my-project#14",
        },
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "confidential": False,
        "discussion_locked": False,
        "issue_type": "issue",
        "severity": "UNKNOWN",
        "_links": {
            "self": "http://gitlab.example.com/api/v4/projects/1/issues/2",
            "notes": "http://gitlab.example.com/api/v4/projects/1/issues/2/notes",
            "award_emoji": "http://gitlab.example.com/api/v4/projects/1/issues/2/award_emoji",
            "project": "http://gitlab.example.com/api/v4/projects/1",
            "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75",
        },
        "task_completion_status": {"count": 0, "completed_count": 0},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_8():
    example_data = {
        "id": 92,
        "iid": 11,
        "project_id": 5,
        "title": "Sit voluptas tempora quisquam aut doloribus et.",
        "description": "Repellat voluptas quibusdam voluptatem exercitationem.",
        "state": "opened",
        "created_at": "2016-04-05T21:41:45.652Z",
        "updated_at": "2016-04-07T12:20:17.596Z",
        "closed_at": None,
        "closed_by": None,
        "labels": [],
        "upvotes": 4,
        "downvotes": 0,
        "merge_requests_count": 0,
        "milestone": None,
        "assignees": [
            {
                "name": "Miss Monserrate Beier",
                "username": "axel.block",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/axel.block",
            }
        ],
        "assignee": {
            "name": "Miss Monserrate Beier",
            "username": "axel.block",
            "id": 12,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/axel.block",
        },
        "type": "ISSUE",
        "author": {
            "name": "Kris Steuber",
            "username": "solon.cremin",
            "id": 10,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/7a190fecbaa68212a4b68aeb6e3acd10?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/solon.cremin",
        },
        "due_date": None,
        "imported": False,
        "imported_from": "none",
        "web_url": "http://gitlab.example.com/my-group/my-project/issues/11",
        "references": {
            "short": "#11",
            "relative": "#11",
            "full": "my-group/my-project#11",
        },
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "confidential": False,
        "discussion_locked": False,
        "issue_type": "issue",
        "severity": "UNKNOWN",
        "_links": {
            "self": "http://gitlab.example.com/api/v4/projects/1/issues/2",
            "notes": "http://gitlab.example.com/api/v4/projects/1/issues/2/notes",
            "award_emoji": "http://gitlab.example.com/api/v4/projects/1/issues/2/award_emoji",
            "project": "http://gitlab.example.com/api/v4/projects/1",
            "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75",
        },
        "task_completion_status": {"count": 0, "completed_count": 0},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_9():
    example_data = {
        "id": 290,
        "iid": 1,
        "project_id": 143,
        "title": "foo",
        "description": "closed",
        "state": "opened",
        "created_at": "2021-09-14T22:24:11.696Z",
        "updated_at": "2021-09-14T22:24:11.696Z",
        "closed_at": None,
        "closed_by": None,
        "labels": [],
        "milestone": None,
        "assignees": [
            {
                "id": 179,
                "name": "John Doe2",
                "username": "john",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/10fc7f102be8de7657fb4d80898bbfe3?s=80\u0026d=identicon",
                "web_url": "https://gitlab.example.com/john",
            }
        ],
        "author": {
            "id": 179,
            "name": "John Doe2",
            "username": "john",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/10fc7f102be8de7657fb4d80898bbfe3?s=80\u0026d=identicon",
            "web_url": "https://gitlab.example.com/john",
        },
        "type": "ISSUE",
        "assignee": {
            "id": 179,
            "name": "John Doe2",
            "username": "john",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/10fc7f102be8de7657fb4d80898bbfe3?s=80\u0026d=identicon",
            "web_url": "https://gitlab.example.com/john",
        },
        "user_notes_count": 1,
        "merge_requests_count": 0,
        "upvotes": 0,
        "downvotes": 0,
        "due_date": None,
        "imported": False,
        "imported_from": "none",
        "confidential": False,
        "discussion_locked": None,
        "issue_type": "issue",
        "severity": "UNKNOWN",
        "web_url": "https://gitlab.example.com/namespace1/project2/-/issues/1",
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "task_completion_status": {"count": 0, "completed_count": 0},
        "blocking_issues_count": 0,
        "has_tasks": False,
        "_links": {
            "self": "https://gitlab.example.com/api/v4/projects/143/issues/1",
            "notes": "https://gitlab.example.com/api/v4/projects/143/issues/1/notes",
            "award_emoji": "https://gitlab.example.com/api/v4/projects/143/issues/1/award_emoji",
            "project": "https://gitlab.example.com/api/v4/projects/143",
            "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75",
        },
        "references": {
            "short": "#1",
            "relative": "#1",
            "full": "namespace1/project2#1",
        },
        "subscribed": True,
        "moved_to_id": None,
        "service_desk_reply_to": None,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_10():
    example_data = {
        "id": 92,
        "iid": 11,
        "project_id": 5,
        "title": "Sit voluptas tempora quisquam aut doloribus et.",
        "description": "Repellat voluptas quibusdam voluptatem exercitationem.",
        "state": "opened",
        "created_at": "2016-04-05T21:41:45.652Z",
        "updated_at": "2016-04-07T12:20:17.596Z",
        "closed_at": None,
        "closed_by": None,
        "labels": [],
        "upvotes": 4,
        "downvotes": 0,
        "merge_requests_count": 0,
        "milestone": None,
        "assignees": [
            {
                "name": "Miss Monserrate Beier",
                "username": "axel.block",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/axel.block",
            }
        ],
        "assignee": {
            "name": "Miss Monserrate Beier",
            "username": "axel.block",
            "id": 12,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/axel.block",
        },
        "type": "ISSUE",
        "author": {
            "name": "Kris Steuber",
            "username": "solon.cremin",
            "id": 10,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/7a190fecbaa68212a4b68aeb6e3acd10?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/solon.cremin",
        },
        "due_date": None,
        "web_url": "http://gitlab.example.com/my-group/my-project/issues/11",
        "references": {
            "short": "#11",
            "relative": "#11",
            "full": "my-group/my-project#11",
        },
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "confidential": False,
        "discussion_locked": False,
        "issue_type": "issue",
        "severity": "UNKNOWN",
        "_links": {
            "self": "http://gitlab.example.com/api/v4/projects/1/issues/2",
            "notes": "http://gitlab.example.com/api/v4/projects/1/issues/2/notes",
            "award_emoji": "http://gitlab.example.com/api/v4/projects/1/issues/2/award_emoji",
            "project": "http://gitlab.example.com/api/v4/projects/1",
            "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75",
        },
        "task_completion_status": {"count": 0, "completed_count": 0},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_11():
    example_data = {
        "id": 93,
        "iid": 12,
        "project_id": 5,
        "title": "Incidunt et rerum ea expedita iure quibusdam.",
        "description": "Et cumque architecto sed aut ipsam.",
        "state": "opened",
        "created_at": "2016-04-05T21:41:45.217Z",
        "updated_at": "2016-04-07T13:02:37.905Z",
        "labels": [],
        "upvotes": 4,
        "downvotes": 0,
        "merge_requests_count": 0,
        "milestone": None,
        "assignee": {
            "name": "Edwardo Grady",
            "username": "keyon",
            "id": 21,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/3e6f06a86cf27fa8b56f3f74f7615987?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/keyon",
        },
        "type": "ISSUE",
        "closed_at": None,
        "closed_by": None,
        "author": {
            "name": "Vivian Hermann",
            "username": "orville",
            "id": 11,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/5224fd70153710e92fb8bcf79ac29d67?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/orville",
        },
        "subscribed": False,
        "due_date": None,
        "web_url": "http://gitlab.example.com/my-group/my-project/issues/12",
        "references": {
            "short": "#12",
            "relative": "#12",
            "full": "my-group/my-project#12",
        },
        "confidential": False,
        "discussion_locked": False,
        "issue_type": "issue",
        "severity": "UNKNOWN",
        "task_completion_status": {"count": 0, "completed_count": 0},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Issue"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_12():
    example_data = {
        "id": 112,
        "project": {
            "id": 5,
            "name": "GitLab CI/CD",
            "name_with_namespace": "GitLab Org / GitLab CI/CD",
            "path": "gitlab-ci",
            "path_with_namespace": "gitlab-org/gitlab-ci",
        },
        "author": {
            "name": "Administrator",
            "username": "root",
            "id": 1,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/root",
        },
        "action_name": "marked",
        "target_type": "Issue",
        "target": {
            "id": 93,
            "iid": 10,
            "project_id": 5,
            "title": "Vel voluptas atque dicta mollitia adipisci qui at.",
            "description": "Tempora laboriosam sint magni sed voluptas similique.",
            "state": "closed",
            "created_at": "2016-06-17T07:47:39.486Z",
            "updated_at": "2016-07-01T11:09:13.998Z",
            "labels": [],
            "milestone": {
                "id": 26,
                "iid": 1,
                "project_id": 5,
                "title": "v0.0",
                "description": "Accusantium nostrum rerum quae quia quis nesciunt suscipit id.",
                "state": "closed",
                "created_at": "2016-06-17T07:47:33.832Z",
                "updated_at": "2016-06-17T07:47:33.832Z",
                "due_date": None,
            },
            "assignees": [
                {
                    "name": "Jarret O'Keefe",
                    "username": "francisca",
                    "id": 14,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/a7fa515d53450023c83d62986d0658a8?s=80&d=identicon",
                    "web_url": "https://gitlab.example.com/francisca",
                }
            ],
            "assignee": {
                "name": "Jarret O'Keefe",
                "username": "francisca",
                "id": 14,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/a7fa515d53450023c83d62986d0658a8?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/francisca",
            },
            "type": "ISSUE",
            "author": {
                "name": "Maxie Medhurst",
                "username": "craig_rutherford",
                "id": 12,
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/a0d477b3ea21970ce6ffcbb817b0b435?s=80&d=identicon",
                "web_url": "https://gitlab.example.com/craig_rutherford",
            },
            "subscribed": True,
            "user_notes_count": 7,
            "upvotes": 0,
            "downvotes": 0,
            "merge_requests_count": 0,
            "due_date": None,
            "web_url": "http://gitlab.example.com/my-group/my-project/issues/10",
            "references": {
                "short": "#10",
                "relative": "#10",
                "full": "my-group/my-project#10",
            },
            "confidential": False,
            "discussion_locked": False,
            "issue_type": "issue",
            "severity": "UNKNOWN",
            "task_completion_status": {"count": 0, "completed_count": 0},
        },
        "target_url": "https://gitlab.example.com/gitlab-org/gitlab-ci/issues/10",
        "body": "Vel voluptas atque dicta mollitia adipisci qui at.",
        "state": "pending",
        "created_at": "2016-07-01T11:09:13.992Z",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ToDo"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_13():
    example_data = {
        "id": 699,
        "type": None,
        "body": "Lets promote this to an epic",
        "attachment": None,
        "author": {
            "id": 1,
            "name": "Alexandra Bashirian",
            "username": "eileen.lowe",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/eileen.lowe",
        },
        "created_at": "2020-12-03T12:27:17.844Z",
        "updated_at": "2020-12-03T12:27:17.844Z",
        "system": False,
        "noteable_id": 461,
        "noteable_type": "Issue",
        "resolvable": False,
        "confidential": False,
        "noteable_iid": 33,
        "commands_changes": {"promote_to_epic": True},
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Comment"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_14():
    example_data = {
        "human_time_estimate": "3h 30m",
        "human_total_time_spent": None,
        "time_estimate": 12600,
        "total_time_spent": 0,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TimeStats"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_issues_response_15():
    example_data = {
        "human_time_estimate": None,
        "human_total_time_spent": None,
        "time_estimate": 0,
        "total_time_spent": 0,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TimeStats"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_1():
    example_data = [
        {
            "id": 47,
            "iid": 12,
            "project_id": 1,
            "status": "pending",
            "source": "push",
            "ref": "new-pipeline",
            "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
            "name": "Build pipeline",
            "web_url": "https://example.com/foo/bar/pipelines/47",
            "created_at": "2016-08-11T11:28:34.085Z",
            "updated_at": "2016-08-11T11:32:35.169Z",
        },
        {
            "id": 48,
            "iid": 13,
            "project_id": 1,
            "status": "pending",
            "source": "web",
            "ref": "new-pipeline",
            "sha": "eb94b618fb5865b26e80fdd8ae531b7a63ad851a",
            "name": "Build pipeline",
            "web_url": "https://example.com/foo/bar/pipelines/48",
            "created_at": "2016-08-12T10:06:04.561Z",
            "updated_at": "2016-08-12T10:09:56.223Z",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_2():
    example_data = {
        "id": 46,
        "iid": 11,
        "project_id": 1,
        "name": "Build pipeline",
        "status": "success",
        "ref": "main",
        "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "before_sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "tag": False,
        "yaml_errors": None,
        "user": {
            "name": "Administrator",
            "username": "root",
            "id": 1,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://localhost:3000/root",
        },
        "created_at": "2016-08-11T11:28:34.085Z",
        "updated_at": "2016-08-11T11:32:35.169Z",
        "started_at": None,
        "finished_at": "2016-08-11T11:32:35.145Z",
        "committed_at": None,
        "duration": 123.65,
        "queued_duration": 0.010,
        "coverage": "30.0",
        "web_url": "https://example.com/foo/bar/pipelines/46",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_3():
    example_data = [
        {"key": "RUN_NIGHTLY_BUILD", "variable_type": "env_var", "value": "true"},
        {"key": "foo", "value": "bar"},
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "PipelineVariable"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_4():
    example_data = {
        "total_time": 5,
        "total_count": 1,
        "success_count": 1,
        "failed_count": 0,
        "skipped_count": 0,
        "error_count": 0,
        "test_suites": [
            {
                "name": "Secure",
                "total_time": 5,
                "total_count": 1,
                "success_count": 1,
                "failed_count": 0,
                "skipped_count": 0,
                "error_count": 0,
                "test_cases": [
                    {
                        "status": "success",
                        "name": "Security Reports can create an auto-remediation MR",
                        "classname": "vulnerability_management_spec",
                        "execution_time": 5,
                        "system_output": None,
                        "stack_trace": None,
                    }
                ],
            }
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TestReport"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_5():
    example_data = {
        "total": {
            "time": 1904,
            "count": 3363,
            "success": 3351,
            "failed": 0,
            "skipped": 12,
            "error": 0,
            "suite_error": None,
        },
        "test_suites": [
            {
                "name": "test",
                "total_time": 1904,
                "total_count": 3363,
                "success_count": 3351,
                "failed_count": 0,
                "skipped_count": 12,
                "error_count": 0,
                "build_ids": [66004],
                "suite_error": None,
            }
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TestReport"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_6():
    example_data = {
        "total": {
            "time": 1904,
            "count": 3363,
            "success": 3351,
            "failed": 0,
            "skipped": 12,
            "error": 0,
            "suite_error": None,
        },
        "test_suites": [
            {
                "name": "test",
                "total_time": 1904,
                "total_count": 3363,
                "success_count": 3351,
                "failed_count": 0,
                "skipped_count": 12,
                "error_count": 0,
                "build_ids": [66004],
                "suite_error": None,
            }
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TestReport"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_7():
    example_data = {
        "id": 287,
        "iid": 144,
        "project_id": 21,
        "name": "Build pipeline",
        "sha": "50f0acb76a40e34a4ff304f7347dcc6587da8a14",
        "ref": "main",
        "status": "success",
        "source": "push",
        "created_at": "2022-09-21T01:05:07.200Z",
        "updated_at": "2022-09-21T01:05:50.185Z",
        "web_url": "http://127.0.0.1:3000/test-group/test-project/-/pipelines/287",
        "before_sha": "8a24fb3c5877a6d0b611ca41fc86edc174593e2b",
        "tag": False,
        "yaml_errors": None,
        "user": {
            "id": 1,
            "username": "root",
            "name": "Administrator",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://127.0.0.1:3000/root",
        },
        "started_at": "2022-09-21T01:05:14.197Z",
        "finished_at": "2022-09-21T01:05:50.175Z",
        "committed_at": None,
        "duration": 34,
        "queued_duration": 6,
        "coverage": None,
        "detailed_status": {
            "icon": "status_success",
            "text": "passed",
            "label": "passed",
            "group": "success",
            "tooltip": "passed",
            "has_details": False,
            "details_path": "/test-group/test-project/-/pipelines/287",
            "illustration": None,
            "favicon": "/assets/ci_favicons/favicon_status_success-8451333011eee8ce9f2ab25dc487fe24a8758c694827a582f17f42b0a90446a2.png",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_8():
    example_data = {
        "id": 61,
        "iid": 21,
        "project_id": 1,
        "sha": "384c444e840a515b23f21915ee5766b87068a70d",
        "ref": "main",
        "status": "pending",
        "before_sha": "0000000000000000000000000000000000000000",
        "tag": False,
        "yaml_errors": None,
        "user": {
            "name": "Administrator",
            "username": "root",
            "id": 1,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://localhost:3000/root",
        },
        "created_at": "2016-11-04T09:36:13.747Z",
        "updated_at": "2016-11-04T09:36:13.977Z",
        "started_at": None,
        "finished_at": None,
        "committed_at": None,
        "duration": None,
        "queued_duration": 0.010,
        "coverage": None,
        "web_url": "https://example.com/foo/bar/pipelines/61",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_9():
    example_data = {
        "id": 46,
        "iid": 11,
        "project_id": 1,
        "status": "pending",
        "ref": "main",
        "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "before_sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "tag": False,
        "yaml_errors": None,
        "user": {
            "name": "Administrator",
            "username": "root",
            "id": 1,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://localhost:3000/root",
        },
        "created_at": "2016-08-11T11:28:34.085Z",
        "updated_at": "2016-08-11T11:32:35.169Z",
        "started_at": None,
        "finished_at": "2016-08-11T11:32:35.145Z",
        "committed_at": None,
        "duration": None,
        "queued_duration": 0.010,
        "coverage": None,
        "web_url": "https://example.com/foo/bar/pipelines/46",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_10():
    example_data = {
        "id": 46,
        "iid": 11,
        "project_id": 1,
        "status": "canceled",
        "ref": "main",
        "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "before_sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "tag": False,
        "yaml_errors": None,
        "user": {
            "name": "Administrator",
            "username": "root",
            "id": 1,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://localhost:3000/root",
        },
        "created_at": "2016-08-11T11:28:34.085Z",
        "updated_at": "2016-08-11T11:32:35.169Z",
        "started_at": None,
        "finished_at": "2016-08-11T11:32:35.145Z",
        "committed_at": None,
        "duration": None,
        "queued_duration": 0.010,
        "coverage": None,
        "web_url": "https://example.com/foo/bar/pipelines/46",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_pipeline_response_11():
    example_data = {
        "id": 46,
        "iid": 11,
        "project_id": 1,
        "status": "running",
        "ref": "main",
        "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "before_sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "tag": False,
        "yaml_errors": None,
        "user": {
            "name": "Administrator",
            "username": "root",
            "id": 1,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://localhost:3000/root",
        },
        "created_at": "2016-08-11T11:28:34.085Z",
        "updated_at": "2016-08-11T11:32:35.169Z",
        "started_at": None,
        "finished_at": "2016-08-11T11:32:35.145Z",
        "committed_at": None,
        "duration": None,
        "queued_duration": 0.010,
        "coverage": None,
        "web_url": "https://example.com/foo/bar/pipelines/46",
        "name": "Some new pipeline name",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_1():
    example_data = [
        {
            "id": 1,
            "name": "Foobar Group",
            "path": "foo-bar",
            "description": "An interesting group",
            "visibility": "public",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "owner",
            "emails_disabled": None,
            "emails_enabled": None,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch": None,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 40}],
                "allow_force_push": False,
                "allowed_to_merge": [{"access_level": 40}],
            },
            "avatar_url": "http://localhost:3000/uploads/group/avatar/1/foo.jpg",
            "web_url": "http://localhost:3000/groups/foo-bar",
            "request_access_enabled": False,
            "repository_storage": "default",
            "full_name": "Foobar Group",
            "full_path": "foo-bar",
            "file_template_project_id": 1,
            "parent_id": None,
            "created_at": "2020-01-15T12:36:29.590Z",
            "ip_restriction_ranges": None,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_2():
    example_data = [
        {
            "id": 1,
            "name": "Foobar Group",
            "path": "foo-bar",
            "description": "An interesting group",
            "visibility": "public",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "owner",
            "emails_disabled": None,
            "emails_enabled": None,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch": None,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 40}],
                "allow_force_push": False,
                "allowed_to_merge": [{"access_level": 40}],
            },
            "avatar_url": "http://localhost:3000/uploads/group/avatar/1/foo.jpg",
            "web_url": "http://localhost:3000/groups/foo-bar",
            "request_access_enabled": False,
            "repository_storage": "default",
            "full_name": "Foobar Group",
            "full_path": "foo-bar",
            "file_template_project_id": 1,
            "parent_id": None,
            "created_at": "2020-01-15T12:36:29.590Z",
            "statistics": {
                "storage_size": 363,
                "repository_size": 33,
                "wiki_size": 100,
                "lfs_objects_size": 123,
                "job_artifacts_size": 57,
                "pipeline_artifacts_size": 0,
                "packages_size": 0,
                "snippets_size": 50,
                "uploads_size": 0,
            },
            "wiki_access_level": "private",
            "duo_features_enabled": True,
            "lock_duo_features_enabled": False,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_3():
    example_data = [
        {
            "id": 1,
            "name": "Foobar Group",
            "path": "foo-bar",
            "description": "An interesting group",
            "visibility": "public",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "owner",
            "emails_disabled": None,
            "emails_enabled": None,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch": None,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 40}],
                "allow_force_push": False,
                "allowed_to_merge": [{"access_level": 40}],
            },
            "avatar_url": "http://gitlab.example.com/uploads/group/avatar/1/foo.jpg",
            "web_url": "http://gitlab.example.com/groups/foo-bar",
            "request_access_enabled": False,
            "repository_storage": "default",
            "full_name": "Foobar Group",
            "full_path": "foo-bar",
            "file_template_project_id": 1,
            "parent_id": 123,
            "created_at": "2020-01-15T12:36:29.590Z",
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_4():
    example_data = [
        {
            "id": 2,
            "name": "Bar Group",
            "path": "bar",
            "description": "A subgroup of Foo Group",
            "visibility": "public",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "owner",
            "emails_disabled": None,
            "emails_enabled": None,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch": None,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 40}],
                "allow_force_push": False,
                "allowed_to_merge": [{"access_level": 40}],
            },
            "avatar_url": "http://gitlab.example.com/uploads/group/avatar/1/bar.jpg",
            "web_url": "http://gitlab.example.com/groups/foo/bar",
            "request_access_enabled": False,
            "full_name": "Bar Group",
            "full_path": "foo/bar",
            "file_template_project_id": 1,
            "parent_id": 123,
            "created_at": "2020-01-15T12:36:29.590Z",
        },
        {
            "id": 3,
            "name": "Baz Group",
            "path": "baz",
            "description": "A subgroup of Bar Group",
            "visibility": "public",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "owner",
            "emails_disabled": None,
            "emails_enabled": None,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch": None,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 40}],
                "allow_force_push": False,
                "allowed_to_merge": [{"access_level": 40}],
            },
            "avatar_url": "http://gitlab.example.com/uploads/group/avatar/1/baz.jpg",
            "web_url": "http://gitlab.example.com/groups/foo/bar/baz",
            "request_access_enabled": False,
            "full_name": "Baz Group",
            "full_path": "foo/bar/baz",
            "file_template_project_id": 1,
            "parent_id": 123,
            "created_at": "2020-01-15T12:36:29.590Z",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_5():
    # List groups
    example_data = [
        {
            "id": 9,
            "description": "foo",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "archived": False,
            "visibility": "internal",
            "ssh_url_to_repo": "git@gitlab.example.com/html5-boilerplate.git",
            "http_url_to_repo": "http://gitlab.example.com/h5bp/html5-boilerplate.git",
            "web_url": "http://gitlab.example.com/h5bp/html5-boilerplate",
            "name": "Html5 Boilerplate",
            "name_with_namespace": "Experimental / Html5 Boilerplate",
            "path": "html5-boilerplate",
            "path_with_namespace": "h5bp/html5-boilerplate",
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "created_at": "2016-04-05T21:40:50.169Z",
            "last_activity_at": "2016-04-06T16:52:08.432Z",
            "shared_runners_enabled": True,
            "creator_id": 1,
            "namespace": {
                "id": 5,
                "name": "Experimental",
                "path": "h5bp",
                "kind": "group",
            },
            "avatar_url": None,
            "star_count": 1,
            "forks_count": 0,
            "open_issues_count": 3,
            "public_jobs": True,
            "shared_with_groups": [],
            "request_access_enabled": False,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Project"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_6():
    # Groups shared projects
    example_data = [
        {
            "id": 8,
            "description": "Shared project for Html5 Boilerplate",
            "name": "Html5 Boilerplate",
            "name_with_namespace": "H5bp / Html5 Boilerplate",
            "path": "html5-boilerplate",
            "path_with_namespace": "h5bp/html5-boilerplate",
            "created_at": "2020-04-27T06:13:22.642Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "ssh://git@gitlab.com/h5bp/html5-boilerplate.git",
            "http_url_to_repo": "https://gitlab.com/h5bp/html5-boilerplate.git",
            "web_url": "https://gitlab.com/h5bp/html5-boilerplate",
            "readme_url": "https://gitlab.com/h5bp/html5-boilerplate/-/blob/main/README.md",
            "avatar_url": None,
            "star_count": 0,
            "forks_count": 4,
            "last_activity_at": "2020-04-27T06:13:22.642Z",
            "namespace": {
                "id": 28,
                "name": "H5bp",
                "path": "h5bp",
                "kind": "group",
                "full_path": "h5bp",
                "parent_id": None,
                "avatar_url": None,
                "web_url": "https://gitlab.com/groups/h5bp",
            },
            "_links": {
                "self": "https://gitlab.com/api/v4/projects/8",
                "issues": "https://gitlab.com/api/v4/projects/8/issues",
                "merge_requests": "https://gitlab.com/api/v4/projects/8/merge_requests",
                "repo_branches": "https://gitlab.com/api/v4/projects/8/repository/branches",
                "labels": "https://gitlab.com/api/v4/projects/8/labels",
                "events": "https://gitlab.com/api/v4/projects/8/events",
                "members": "https://gitlab.com/api/v4/projects/8/members",
            },
            "empty_repo": False,
            "archived": False,
            "visibility": "public",
            "resolve_outdated_diff_discussions": False,
            "container_registry_enabled": True,
            "container_expiration_policy": {
                "cadence": "7d",
                "enabled": True,
                "keep_n": None,
                "older_than": None,
                "name_regex": None,
                "name_regex_keep": None,
                "next_run_at": "2020-05-04T06:13:22.654Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "enabled",
            "security_and_compliance_access_level": "enabled",
            "emails_disabled": None,
            "emails_enabled": None,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 1,
            "import_status": "failed",
            "open_issues_count": 10,
            "ci_default_git_depth": 50,
            "ci_forward_deployment_enabled": True,
            "ci_forward_deployment_rollback_allowed": True,
            "ci_allow_fork_pipelines_to_run_in_parent_project": True,
            "public_jobs": True,
            "build_timeout": 3600,
            "auto_cancel_pending_pipelines": "enabled",
            "ci_config_path": None,
            "shared_with_groups": [
                {
                    "group_id": 24,
                    "group_name": "Commit451",
                    "group_full_path": "Commit451",
                    "group_access_level": 30,
                    "expires_at": None,
                }
            ],
            "only_allow_merge_if_pipeline_succeeds": False,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "suggestion_commit_message": None,
            "auto_devops_enabled": True,
            "auto_devops_deploy_strategy": "continuous",
            "autoclose_referenced_issues": True,
            "repository_storage": "default",
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Project"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_7():
    # Details of a group
    example_data = {
        "id": 4,
        "name": "Twitter",
        "path": "twitter",
        "description": "Aliquid qui quis dignissimos distinctio ut commodi voluptas est.",
        "visibility": "public",
        "avatar_url": None,
        "web_url": "https://gitlab.example.com/groups/twitter",
        "request_access_enabled": False,
        "repository_storage": "default",
        "full_name": "Twitter",
        "full_path": "twitter",
        "runners_token": "ba324ca7b1c77fc20bb9",
        "file_template_project_id": 1,
        "parent_id": None,
        "enabled_git_access_protocol": "all",
        "created_at": "2020-01-15T12:36:29.590Z",
        "shared_with_groups": [
            {
                "group_id": 28,
                "group_name": "H5bp",
                "group_full_path": "h5bp",
                "group_access_level": 20,
                "expires_at": None,
            }
        ],
        "prevent_sharing_groups_outside_hierarchy": False,
        "projects": [
            {
                "id": 7,
                "description": "Voluptas veniam qui et beatae voluptas doloremque explicabo facilis.",
                "default_branch": "main",
                "tag_list": [],
                "topics": [],
                "archived": False,
                "visibility": "public",
                "ssh_url_to_repo": "git@gitlab.example.com:twitter/typeahead-js.git",
                "http_url_to_repo": "https://gitlab.example.com/twitter/typeahead-js.git",
                "web_url": "https://gitlab.example.com/twitter/typeahead-js",
                "name": "Typeahead.Js",
                "name_with_namespace": "Twitter / Typeahead.Js",
                "path": "typeahead-js",
                "path_with_namespace": "twitter/typeahead-js",
                "issues_enabled": True,
                "merge_requests_enabled": True,
                "wiki_enabled": True,
                "jobs_enabled": True,
                "snippets_enabled": False,
                "container_registry_enabled": True,
                "created_at": "2016-06-17T07:47:25.578Z",
                "last_activity_at": "2016-06-17T07:47:25.881Z",
                "shared_runners_enabled": True,
                "creator_id": 1,
                "namespace": {
                    "id": 4,
                    "name": "Twitter",
                    "path": "twitter",
                    "kind": "group",
                },
                "avatar_url": None,
                "star_count": 0,
                "forks_count": 0,
                "open_issues_count": 3,
                "public_jobs": True,
                "shared_with_groups": [],
                "request_access_enabled": False,
            },
            {
                "id": 6,
                "description": "Aspernatur omnis repudiandae qui voluptatibus eaque.",
                "default_branch": "main",
                "tag_list": [],
                "topics": [],
                "archived": False,
                "visibility": "internal",
                "ssh_url_to_repo": "git@gitlab.example.com:twitter/flight.git",
                "http_url_to_repo": "https://gitlab.example.com/twitter/flight.git",
                "web_url": "https://gitlab.example.com/twitter/flight",
                "name": "Flight",
                "name_with_namespace": "Twitter / Flight",
                "path": "flight",
                "path_with_namespace": "twitter/flight",
                "issues_enabled": True,
                "merge_requests_enabled": True,
                "wiki_enabled": True,
                "jobs_enabled": True,
                "snippets_enabled": False,
                "container_registry_enabled": True,
                "created_at": "2016-06-17T07:47:24.661Z",
                "last_activity_at": "2016-06-17T07:47:24.838Z",
                "shared_runners_enabled": True,
                "creator_id": 1,
                "namespace": {
                    "id": 4,
                    "name": "Twitter",
                    "path": "twitter",
                    "kind": "group",
                },
                "avatar_url": None,
                "star_count": 0,
                "forks_count": 0,
                "open_issues_count": 8,
                "public_jobs": True,
                "shared_with_groups": [],
                "request_access_enabled": False,
            },
        ],
        "shared_projects": [
            {
                "id": 8,
                "description": "Velit eveniet provident fugiat saepe eligendi autem.",
                "default_branch": "main",
                "tag_list": [],
                "topics": [],
                "archived": False,
                "visibility": "private",
                "ssh_url_to_repo": "git@gitlab.example.com:h5bp/html5-boilerplate.git",
                "http_url_to_repo": "https://gitlab.example.com/h5bp/html5-boilerplate.git",
                "web_url": "https://gitlab.example.com/h5bp/html5-boilerplate",
                "name": "Html5 Boilerplate",
                "name_with_namespace": "H5bp / Html5 Boilerplate",
                "path": "html5-boilerplate",
                "path_with_namespace": "h5bp/html5-boilerplate",
                "issues_enabled": True,
                "merge_requests_enabled": True,
                "wiki_enabled": True,
                "jobs_enabled": True,
                "snippets_enabled": False,
                "container_registry_enabled": True,
                "created_at": "2016-06-17T07:47:27.089Z",
                "last_activity_at": "2016-06-17T07:47:27.310Z",
                "shared_runners_enabled": True,
                "creator_id": 1,
                "namespace": {"id": 5, "name": "H5bp", "path": "h5bp", "kind": "group"},
                "avatar_url": None,
                "star_count": 0,
                "forks_count": 0,
                "open_issues_count": 4,
                "public_jobs": True,
                "shared_with_groups": [
                    {
                        "group_id": 4,
                        "group_name": "Twitter",
                        "group_full_path": "twitter",
                        "group_access_level": 30,
                        "expires_at": None,
                    },
                    {
                        "group_id": 3,
                        "group_name": "Gitlab Org",
                        "group_full_path": "gitlab-org",
                        "group_access_level": 10,
                        "expires_at": "2018-08-14",
                    },
                ],
            }
        ],
        "ip_restriction_ranges": None,
        "math_rendering_limits_enabled": True,
        "lock_math_rendering_limits_enabled": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_8():
    # Details of a group
    example_data = {
        "id": 4,
        "description": "Aliquid qui quis dignissimos distinctio ut commodi voluptas est.",
        "shared_runners_minutes_limit": 133,
        "extra_shared_runners_minutes_limit": 133,
        "marked_for_deletion_on": "2020-04-03",
        "membership_lock": False,
        "wiki_access_level": "disabled",
        "duo_features_enabled": True,
        "lock_duo_features_enabled": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_9():
    # Details of a group
    example_data = {
        "id": 4,
        "name": "Twitter",
        "path": "twitter",
        "description": "Aliquid qui quis dignissimos distinctio ut commodi voluptas est.",
        "visibility": "public",
        "avatar_url": None,
        "web_url": "https://gitlab.example.com/groups/twitter",
        "request_access_enabled": False,
        "repository_storage": "default",
        "full_name": "Twitter",
        "full_path": "twitter",
        "file_template_project_id": 1,
        "parent_id": None,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_10():
    # Get groups to which a user can transfer a group
    example_data = [
        {
            "id": 27,
            "web_url": "https://gitlab.example.com/groups/gitlab",
            "name": "GitLab",
            "avatar_url": None,
            "full_name": "GitLab",
            "full_path": "GitLab",
        },
        {
            "id": 31,
            "web_url": "https://gitlab.example.com/groups/foobar",
            "name": "FooBar",
            "avatar_url": None,
            "full_name": "FooBar",
            "full_path": "FooBar",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_11():
    # Update group
    example_data = {
        "id": 5,
        "name": "Experimental",
        "path": "h5bp",
        "description": "foo",
        "visibility": "internal",
        "avatar_url": None,
        "web_url": "http://gitlab.example.com/groups/h5bp",
        "request_access_enabled": False,
        "repository_storage": "default",
        "full_name": "Foobar Group",
        "full_path": "h5bp",
        "file_template_project_id": 1,
        "parent_id": None,
        "enabled_git_access_protocol": "all",
        "created_at": "2020-01-15T12:36:29.590Z",
        "prevent_sharing_groups_outside_hierarchy": False,
        "projects": [
            {
                "id": 9,
                "description": "foo",
                "default_branch": "main",
                "tag_list": [],
                "topics": [],
                "public": False,
                "archived": False,
                "visibility": "internal",
                "ssh_url_to_repo": "git@gitlab.example.com/html5-boilerplate.git",
                "http_url_to_repo": "http://gitlab.example.com/h5bp/html5-boilerplate.git",
                "web_url": "http://gitlab.example.com/h5bp/html5-boilerplate",
                "name": "Html5 Boilerplate",
                "name_with_namespace": "Experimental / Html5 Boilerplate",
                "path": "html5-boilerplate",
                "path_with_namespace": "h5bp/html5-boilerplate",
                "issues_enabled": True,
                "merge_requests_enabled": True,
                "wiki_enabled": True,
                "jobs_enabled": True,
                "snippets_enabled": True,
                "created_at": "2016-04-05T21:40:50.169Z",
                "last_activity_at": "2016-04-06T16:52:08.432Z",
                "shared_runners_enabled": True,
                "creator_id": 1,
                "namespace": {
                    "id": 5,
                    "name": "Experimental",
                    "path": "h5bp",
                    "kind": "group",
                },
                "avatar_url": None,
                "star_count": 1,
                "forks_count": 0,
                "open_issues_count": 3,
                "public_jobs": True,
                "shared_with_groups": [],
                "request_access_enabled": False,
            }
        ],
        "ip_restriction_ranges": None,
        "math_rendering_limits_enabled": True,
        "lock_math_rendering_limits_enabled": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_12():
    # Search for a group
    example_data = [
        {
            "id": 1,
            "name": "Foobar Group",
            "path": "foo-bar",
            "description": "An interesting group",
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_13():
    # List provisioned users
    example_data = [
        {
            "id": 66,
            "username": "user22",
            "name": "John Doe22",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/xxx?s=80&d=identicon",
            "web_url": "http://my.gitlab.com/user22",
            "created_at": "2021-09-10T12:48:22.381Z",
            "bio": "",
            "location": None,
            "public_email": "",
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "website_url": "",
            "organization": None,
            "job_title": "",
            "pronouns": None,
            "bot": False,
            "work_information": None,
            "followers": 0,
            "following": 0,
            "local_time": None,
            "last_sign_in_at": None,
            "confirmed_at": "2021-09-10T12:48:22.330Z",
            "last_activity_on": None,
            "email": "user22@example.org",
            "theme_id": 1,
            "color_scheme_id": 1,
            "projects_limit": 100000,
            "current_sign_in_at": None,
            "identities": [],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": False,
            "external": False,
            "private_profile": False,
            "commit_email": "user22@example.org",
            "shared_runners_minutes_limit": None,
            "extra_shared_runners_minutes_limit": None,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_14():
    # List group users
    example_data = [
        {
            "id": 66,
            "username": "user22",
            "name": "John Doe22",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/xxx?s=80&d=identicon",
            "web_url": "http://my.gitlab.com/user22",
            "created_at": "2021-09-10T12:48:22.381Z",
            "bio": "",
            "location": None,
            "public_email": "",
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "website_url": "",
            "organization": None,
            "job_title": "",
            "pronouns": None,
            "bot": False,
            "work_information": None,
            "followers": 0,
            "following": 0,
            "local_time": None,
            "last_sign_in_at": None,
            "confirmed_at": "2021-09-10T12:48:22.330Z",
            "last_activity_on": None,
            "email": "user22@example.org",
            "theme_id": 1,
            "color_scheme_id": 1,
            "projects_limit": 100000,
            "current_sign_in_at": None,
            "identities": [],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": False,
            "external": False,
            "private_profile": False,
            "commit_email": "user22@example.org",
            "shared_runners_minutes_limit": None,
            "extra_shared_runners_minutes_limit": None,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_15():
    # Create Service Account User
    example_data = {
        "id": 57,
        "username": "service_account_group_345_6018816a18e515214e0c34c2b33523fc",
        "name": "Service account user",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_16():
    # Create Personal Access Token for Service Account User
    example_data = {
        "id": 6,
        "name": "service_accounts_token",
        "revoked": False,
        "created_at": "2023-06-13T07:47:13.900Z",
        "scopes": ["api"],
        "user_id": 71,
        "last_used_at": None,
        "active": True,
        "expires_at": "2024-06-12",
        "token": "<token_value>",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_17():
    # Rotate a Personal Access Token for Service Account User
    example_data = {
        "id": 7,
        "name": "service_accounts_token",
        "revoked": False,
        "created_at": "2023-06-13T07:54:49.962Z",
        "scopes": ["api"],
        "user_id": 71,
        "last_used_at": None,
        "active": True,
        "expires_at": "2023-06-20",
        "token": "<token_value>",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "DeployToken"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_18():
    # Get group hook
    example_data = {
        "id": 1,
        "url": "http://example.com/hook",
        "name": "Hook name",
        "description": "Hook description",
        "group_id": 3,
        "push_events": True,
        "push_events_branch_filter": "",
        "issues_events": True,
        "confidential_issues_events": True,
        "merge_requests_events": True,
        "tag_push_events": True,
        "note_events": True,
        "confidential_note_events": True,
        "job_events": True,
        "pipeline_events": True,
        "wiki_page_events": True,
        "deployment_events": True,
        "releases_events": True,
        "subgroup_events": True,
        "member_events": True,
        "enable_ssl_verification": True,
        "repository_update_events": False,
        "alert_status": "executable",
        "disabled_until": None,
        "url_variables": [],
        "created_at": "2012-10-12T17:04:47Z",
        "resource_access_token_events": True,
        "custom_webhook_template": '{"event":"{{object_kind}}"}',
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Webhook"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_19():
    # Push Rules
    example_data = {
        "id": 2,
        "created_at": "2020-08-17T19:09:19.580Z",
        "commit_committer_check": True,
        "commit_committer_name_check": True,
        "reject_unsigned_commits": False,
        "commit_message_regex": "[a-zA-Z]",
        "commit_message_negative_regex": "[x+]",
        "branch_name_regex": "[a-z]",
        "deny_delete_tag": True,
        "member_check": True,
        "prevent_secrets": True,
        "author_email_regex": "^[A-Za-z0-9.]+@gitlab.com$",
        "file_name_regex": "(exe)$",
        "max_file_size": 100,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Rule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_20():
    # Add SAML group link
    example_data = {"name": "saml-group-1", "access_level": 10, "member_role_id": 12}
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "AccessControl"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_21():
    # Get saml group link
    example_data = {"name": "saml-group-1", "access_level": 10, "member_role_id": 12}
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "AccessControl"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_22():
    example_data = [
        {
            "id": 68,
            "web_url": "http://gitlab.arpa/groups/homelab/miscellaneous",
            "name": "Miscellaneous",
            "path": "miscellaneous",
            "description": "",
            "visibility": "private",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "maintainer",
            "emails_disabled": False,
            "emails_enabled": True,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 30}],
                "allow_force_push": True,
                "allowed_to_merge": [{"access_level": 30}],
            },
            "avatar_url": None,
            "request_access_enabled": True,
            "full_name": "Homelab / Miscellaneous",
            "full_path": "homelab/miscellaneous",
            "created_at": "2023-11-13T05:10:53.281Z",
            "parent_id": 2,
            "organization_id": 1,
            "shared_runners_setting": "enabled",
        },
        {
            "id": 74,
            "web_url": "http://gitlab.arpa/groups/homelab/pipelines",
            "name": "Pipelines",
            "path": "pipelines",
            "description": "",
            "visibility": "private",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "maintainer",
            "emails_disabled": False,
            "emails_enabled": True,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 30}],
                "allow_force_push": True,
                "allowed_to_merge": [{"access_level": 30}],
            },
            "avatar_url": None,
            "request_access_enabled": True,
            "full_name": "Homelab / Pipelines",
            "full_path": "homelab/pipelines",
            "created_at": "2023-11-13T05:17:53.443Z",
            "parent_id": 2,
            "organization_id": 1,
            "shared_runners_setting": "enabled",
        },
        {
            "id": 72,
            "web_url": "http://gitlab.arpa/groups/homelab/powershell",
            "name": "PowerShell",
            "path": "powershell",
            "description": "",
            "visibility": "private",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "maintainer",
            "emails_disabled": False,
            "emails_enabled": True,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 30}],
                "allow_force_push": True,
                "allowed_to_merge": [{"access_level": 30}],
            },
            "avatar_url": None,
            "request_access_enabled": True,
            "full_name": "Homelab / PowerShell",
            "full_path": "homelab/powershell",
            "created_at": "2023-11-13T05:12:22.596Z",
            "parent_id": 2,
            "organization_id": 1,
            "shared_runners_setting": "enabled",
        },
        {
            "id": 109,
            "web_url": "http://gitlab.arpa/groups/homelab/rust",
            "name": "Rust",
            "path": "rust",
            "description": "",
            "visibility": "private",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "maintainer",
            "emails_disabled": False,
            "emails_enabled": True,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {},
            "avatar_url": None,
            "request_access_enabled": True,
            "full_name": "Homelab / Rust",
            "full_path": "homelab/rust",
            "created_at": "2024-03-30T14:16:18.308Z",
            "parent_id": 2,
            "organization_id": 1,
            "shared_runners_setting": "enabled",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Group"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_group_response_23():
    example_data = [
        {
            "id": 89,
            "description": "None",
            "name": "Immich",
            "name_with_namespace": "Homelab / Containers / Immich",
            "path": "immich",
            "path_with_namespace": "homelab/containers/immich",
            "created_at": "2024-05-26T15:35:04.767Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/immich.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/immich.git",
            "web_url": "http://gitlab.arpa/homelab/containers/immich",
            "readme_url": "http://gitlab.arpa/homelab/containers/immich/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": "None",
            "star_count": 0,
            "last_activity_at": "2024-05-26T15:35:04.767Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": "None",
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/89",
                "issues": "http://gitlab.arpa/api/v4/projects/89/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/89/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/89/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/89/labels",
                "events": "http://gitlab.arpa/api/v4/projects/89/events",
                "members": "http://gitlab.arpa/api/v4/projects/89/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/89/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": "None",
                "next_run_at": "2024-05-27T15:35:04.842Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": "None",
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-05-26T16:25:48.455Z",
            "ci_config_path": "None",
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": "None",
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": "None",
            "merge_commit_template": "None",
            "squash_commit_template": "None",
            "issue_branch_template": "None",
            "autoclose_referenced_issues": True,
        },
        {
            "id": 87,
            "description": "None",
            "name": "Ubuntu",
            "name_with_namespace": "Homelab / Containers / Ubuntu",
            "path": "ubuntu",
            "path_with_namespace": "homelab/containers/ubuntu",
            "created_at": "2024-03-16T15:07:06.719Z",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": "git@gitlab.arpa:homelab/containers/ubuntu.git",
            "http_url_to_repo": "http://gitlab.arpa/homelab/containers/ubuntu.git",
            "web_url": "http://gitlab.arpa/homelab/containers/ubuntu",
            "readme_url": "http://gitlab.arpa/homelab/containers/ubuntu/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": "None",
            "star_count": 0,
            "last_activity_at": "2024-03-16T15:07:06.719Z",
            "namespace": {
                "id": 6,
                "name": "Containers",
                "path": "containers",
                "kind": "group",
                "full_path": "homelab/containers",
                "parent_id": 2,
                "avatar_url": "None",
                "web_url": "http://gitlab.arpa/groups/homelab/containers",
            },
            "_links": {
                "self": "http://gitlab.arpa/api/v4/projects/87",
                "issues": "http://gitlab.arpa/api/v4/projects/87/issues",
                "merge_requests": "http://gitlab.arpa/api/v4/projects/87/merge_requests",
                "repo_branches": "http://gitlab.arpa/api/v4/projects/87/repository/branches",
                "labels": "http://gitlab.arpa/api/v4/projects/87/labels",
                "events": "http://gitlab.arpa/api/v4/projects/87/events",
                "members": "http://gitlab.arpa/api/v4/projects/87/members",
                "cluster_agents": "http://gitlab.arpa/api/v4/projects/87/cluster_agents",
            },
            "code_suggestions": True,
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "private",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": "None",
                "next_run_at": "2024-03-17T15:07:06.796Z",
            },
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": True,
            "service_desk_enabled": False,
            "service_desk_address": "None",
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "enabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": True,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_status": "none",
            "open_issues_count": 0,
            "description_html": "",
            "updated_at": "2024-03-16T15:09:52.871Z",
            "ci_config_path": "None",
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": "None",
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": "None",
            "merge_commit_template": "None",
            "squash_commit_template": "None",
            "issue_branch_template": "None",
            "autoclose_referenced_issues": True,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Project"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_1():
    # List project jobs
    example_data = [
        {
            "commit": {
                "author_email": "admin@example.com",
                "author_name": "Administrator",
                "created_at": "2015-12-24T16:51:14.000+01:00",
                "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "message": "Test the CI integration.",
                "short_id": "0ff3ae19",
                "title": "Test the CI integration.",
            },
            "coverage": None,
            "archived": False,
            "allow_failure": False,
            "created_at": "2015-12-24T15:51:21.802Z",
            "started_at": "2015-12-24T17:54:27.722Z",
            "finished_at": "2015-12-24T17:54:27.895Z",
            "erased_at": None,
            "duration": 0.173,
            "queued_duration": 0.010,
            "artifacts_file": {"filename": "artifacts.zip", "size": 1000},
            "artifacts": [
                {
                    "file_type": "archive",
                    "size": 1000,
                    "filename": "artifacts.zip",
                    "file_format": "zip",
                },
                {
                    "file_type": "metadata",
                    "size": 186,
                    "filename": "metadata.gz",
                    "file_format": "gzip",
                },
                {
                    "file_type": "trace",
                    "size": 1500,
                    "filename": "job.log",
                    "file_format": "raw",
                },
                {
                    "file_type": "junit",
                    "size": 750,
                    "filename": "junit.xml.gz",
                    "file_format": "gzip",
                },
            ],
            "artifacts_expire_at": "2016-01-23T17:54:27.895Z",
            "tag_list": ["docker runner", "ubuntu18"],
            "id": 7,
            "name": "teaspoon",
            "pipeline": {
                "id": 6,
                "project_id": 1,
                "ref": "main",
                "sha": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "status": "pending",
            },
            "ref": "main",
            "runner": {
                "id": 32,
                "description": "",
                "ip_address": None,
                "active": True,
                "paused": False,
                "is_shared": True,
                "runner_type": "instance_type",
                "name": None,
                "online": False,
                "status": "offline",
            },
            "runner_manager": {
                "id": 1,
                "system_id": "s_89e5e9956577",
                "version": "16.11.1",
                "revision": "535ced5f",
                "platform": "linux",
                "architecture": "amd64",
                "created_at": "2024-05-01T10:12:02.507Z",
                "contacted_at": "2024-05-07T06:30:09.355Z",
                "ip_address": "127.0.0.1",
                "status": "offline",
            },
            "stage": "test",
            "status": "failed",
            "failure_reason": "script_failure",
            "tag": False,
            "web_url": "https://example.com/foo/bar/-/jobs/7",
            "project": {"ci_job_token_scope_enabled": False},
            "user": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                "web_url": "http://gitlab.dev/root",
                "created_at": "2015-12-21T13:14:24.077Z",
                "bio": None,
                "location": None,
                "public_email": "",
                "skype": "",
                "linkedin": "",
                "twitter": "",
                "website_url": "",
                "organization": "",
            },
        },
        {
            "commit": {
                "author_email": "admin@example.com",
                "author_name": "Administrator",
                "created_at": "2015-12-24T16:51:14.000+01:00",
                "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "message": "Test the CI integration.",
                "short_id": "0ff3ae19",
                "title": "Test the CI integration.",
            },
            "coverage": None,
            "archived": False,
            "allow_failure": False,
            "created_at": "2015-12-24T15:51:21.727Z",
            "started_at": "2015-12-24T17:54:24.729Z",
            "finished_at": "2015-12-24T17:54:24.921Z",
            "erased_at": None,
            "duration": 0.192,
            "queued_duration": 0.023,
            "artifacts_expire_at": "2016-01-23T17:54:24.921Z",
            "tag_list": ["docker runner", "win10-2004"],
            "id": 6,
            "name": "rspec:other",
            "pipeline": {
                "id": 6,
                "project_id": 1,
                "ref": "main",
                "sha": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "status": "pending",
            },
            "ref": "main",
            "artifacts": [],
            "runner": None,
            "runner_manager": None,
            "stage": "test",
            "status": "failed",
            "failure_reason": "stuck_or_timeout_failure",
            "tag": False,
            "web_url": "https://example.com/foo/bar/-/jobs/6",
            "project": {"ci_job_token_scope_enabled": False},
            "user": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                "web_url": "http://gitlab.dev/root",
                "created_at": "2015-12-21T13:14:24.077Z",
                "bio": None,
                "location": None,
                "public_email": "",
                "skype": "",
                "linkedin": "",
                "twitter": "",
                "website_url": "",
                "organization": "",
            },
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_2():
    # List pipeline jobs
    example_data = [
        {
            "commit": {
                "author_email": "admin@example.com",
                "author_name": "Administrator",
                "created_at": "2015-12-24T16:51:14.000+01:00",
                "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "message": "Test the CI integration.",
                "short_id": "0ff3ae19",
                "title": "Test the CI integration.",
            },
            "coverage": None,
            "archived": False,
            "allow_failure": False,
            "created_at": "2015-12-24T15:51:21.727Z",
            "started_at": "2015-12-24T17:54:24.729Z",
            "finished_at": "2015-12-24T17:54:24.921Z",
            "erased_at": None,
            "duration": 0.192,
            "queued_duration": 0.023,
            "artifacts_expire_at": "2016-01-23T17:54:24.921Z",
            "tag_list": ["docker runner", "ubuntu18"],
            "id": 6,
            "name": "rspec:other",
            "pipeline": {
                "id": 6,
                "project_id": 1,
                "ref": "main",
                "sha": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "status": "pending",
            },
            "ref": "main",
            "artifacts": [],
            "runner": {
                "id": 32,
                "description": "",
                "ip_address": None,
                "active": True,
                "paused": False,
                "is_shared": True,
                "runner_type": "instance_type",
                "name": None,
                "online": False,
                "status": "offline",
            },
            "runner_manager": {
                "id": 1,
                "system_id": "s_89e5e9956577",
                "version": "16.11.1",
                "revision": "535ced5f",
                "platform": "linux",
                "architecture": "amd64",
                "created_at": "2024-05-01T10:12:02.507Z",
                "contacted_at": "2024-05-07T06:30:09.355Z",
                "ip_address": "127.0.0.1",
            },
            "stage": "test",
            "status": "failed",
            "failure_reason": "stuck_or_timeout_failure",
            "tag": False,
            "web_url": "https://example.com/foo/bar/-/jobs/6",
            "project": {"ci_job_token_scope_enabled": False},
            "user": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                "web_url": "http://gitlab.dev/root",
                "created_at": "2015-12-21T13:14:24.077Z",
                "bio": None,
                "location": None,
                "public_email": "",
                "skype": "",
                "linkedin": "",
                "twitter": "",
                "website_url": "",
                "organization": "",
            },
        },
        {
            "commit": {
                "author_email": "admin@example.com",
                "author_name": "Administrator",
                "created_at": "2015-12-24T16:51:14.000+01:00",
                "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "message": "Test the CI integration.",
                "short_id": "0ff3ae19",
                "title": "Test the CI integration.",
            },
            "coverage": None,
            "archived": False,
            "allow_failure": False,
            "created_at": "2015-12-24T15:51:21.802Z",
            "started_at": "2015-12-24T17:54:27.722Z",
            "finished_at": "2015-12-24T17:54:27.895Z",
            "erased_at": None,
            "duration": 0.173,
            "queued_duration": 0.023,
            "artifacts_file": {"filename": "artifacts.zip", "size": 1000},
            "artifacts": [
                {
                    "file_type": "archive",
                    "size": 1000,
                    "filename": "artifacts.zip",
                    "file_format": "zip",
                },
                {
                    "file_type": "metadata",
                    "size": 186,
                    "filename": "metadata.gz",
                    "file_format": "gzip",
                },
                {
                    "file_type": "trace",
                    "size": 1500,
                    "filename": "job.log",
                    "file_format": "raw",
                },
                {
                    "file_type": "junit",
                    "size": 750,
                    "filename": "junit.xml.gz",
                    "file_format": "gzip",
                },
            ],
            "artifacts_expire_at": "2016-01-23T17:54:27.895Z",
            "tag_list": ["docker runner", "ubuntu18"],
            "id": 7,
            "name": "teaspoon",
            "pipeline": {
                "id": 6,
                "project_id": 1,
                "ref": "main",
                "sha": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "status": "pending",
            },
            "ref": "main",
            "runner": None,
            "runner_manager": None,
            "stage": "test",
            "status": "failed",
            "failure_reason": "script_failure",
            "tag": False,
            "web_url": "https://example.com/foo/bar/-/jobs/7",
            "project": {"ci_job_token_scope_enabled": False},
            "user": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                "web_url": "http://gitlab.dev/root",
                "created_at": "2015-12-21T13:14:24.077Z",
                "bio": None,
                "location": None,
                "public_email": "",
                "skype": "",
                "linkedin": "",
                "twitter": "",
                "website_url": "",
                "organization": "",
            },
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_3():
    # List pipeline trigger jobs
    example_data = [
        {
            "commit": {
                "author_email": "admin@example.com",
                "author_name": "Administrator",
                "created_at": "2015-12-24T16:51:14.000+01:00",
                "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "message": "Test the CI integration.",
                "short_id": "0ff3ae19",
                "title": "Test the CI integration.",
            },
            "coverage": None,
            "archived": False,
            "allow_failure": False,
            "created_at": "2015-12-24T15:51:21.802Z",
            "started_at": "2015-12-24T17:54:27.722Z",
            "finished_at": "2015-12-24T17:58:27.895Z",
            "erased_at": None,
            "duration": 240,
            "queued_duration": 0.123,
            "id": 7,
            "name": "teaspoon",
            "pipeline": {
                "id": 6,
                "project_id": 1,
                "ref": "main",
                "sha": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
                "status": "pending",
                "created_at": "2015-12-24T15:50:16.123Z",
                "updated_at": "2015-12-24T18:00:44.432Z",
                "web_url": "https://example.com/foo/bar/pipelines/6",
            },
            "ref": "main",
            "stage": "test",
            "status": "pending",
            "tag": False,
            "web_url": "https://example.com/foo/bar/-/jobs/7",
            "project": {"ci_job_token_scope_enabled": False},
            "user": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                "web_url": "http://gitlab.dev/root",
                "created_at": "2015-12-21T13:14:24.077Z",
                "bio": None,
                "location": None,
                "public_email": "",
                "skype": "",
                "linkedin": "",
                "twitter": "",
                "website_url": "",
                "organization": "",
            },
            "downstream_pipeline": {
                "id": 5,
                "sha": "f62a4b2fb89754372a346f24659212eb8da13601",
                "ref": "main",
                "status": "pending",
                "created_at": "2015-12-24T17:54:27.722Z",
                "updated_at": "2015-12-24T17:58:27.896Z",
                "web_url": "https://example.com/diaspora/diaspora-client/pipelines/5",
            },
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_4():
    # Get job token’s job
    example_data = {
        "commit": {
            "author_email": "admin@example.com",
            "author_name": "Administrator",
            "created_at": "2015-12-24T16:51:14.000+01:00",
            "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "message": "Test the CI integration.",
            "short_id": "0ff3ae19",
            "title": "Test the CI integration.",
        },
        "coverage": None,
        "archived": False,
        "allow_failure": False,
        "created_at": "2015-12-24T15:51:21.880Z",
        "started_at": "2015-12-24T17:54:30.733Z",
        "finished_at": "2015-12-24T17:54:31.198Z",
        "erased_at": None,
        "duration": 0.465,
        "queued_duration": 0.123,
        "artifacts_expire_at": "2016-01-23T17:54:31.198Z",
        "id": 8,
        "name": "rubocop",
        "pipeline": {
            "id": 6,
            "project_id": 1,
            "ref": "main",
            "sha": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "status": "pending",
        },
        "ref": "main",
        "artifacts": [],
        "runner": None,
        "runner_manager": None,
        "stage": "test",
        "status": "failed",
        "failure_reason": "script_failure",
        "tag": False,
        "web_url": "https://example.com/foo/bar/-/jobs/8",
        "project": {"ci_job_token_scope_enabled": False},
        "user": {
            "id": 1,
            "name": "Administrator",
            "username": "root",
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://gitlab.dev/root",
            "created_at": "2015-12-21T13:14:24.077Z",
            "bio": None,
            "location": None,
            "public_email": "",
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "website_url": "",
            "organization": "",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_5():
    # Get GitLab agent by CI_JOB_TOKEN
    example_data = {
        "allowed_agents": [
            {
                "id": 1,
                "config_project": {
                    "id": 1,
                    "description": None,
                    "name": "project1",
                    "name_with_namespace": "John Doe2 / project1",
                    "path": "project1",
                    "path_with_namespace": "namespace1/project1",
                    "created_at": "2022-11-16T14:51:50.579Z",
                },
            }
        ],
        "job": {"id": 1},
        "pipeline": {"id": 2},
        "project": {"id": 1, "groups": [{"id": 1}, {"id": 2}, {"id": 3}]},
        "user": {
            "id": 2,
            "name": "John Doe3",
            "username": "user2",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/10fc7f102b",
            "web_url": "http://localhost/user2",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Agents"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_6():
    example_data = {
        "commit": {
            "author_email": "admin@example.com",
            "author_name": "Administrator",
            "created_at": "2015-12-24T16:51:14.000+01:00",
            "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "message": "Test the CI integration.",
            "short_id": "0ff3ae19",
            "title": "Test the CI integration.",
        },
        "coverage": None,
        "archived": False,
        "allow_failure": False,
        "created_at": "2015-12-24T15:51:21.880Z",
        "started_at": "2015-12-24T17:54:30.733Z",
        "finished_at": "2015-12-24T17:54:31.198Z",
        "erased_at": None,
        "duration": 0.465,
        "queued_duration": 0.010,
        "artifacts_expire_at": "2016-01-23T17:54:31.198Z",
        "tag_list": ["docker runner", "macos-10.15"],
        "id": 8,
        "name": "rubocop",
        "pipeline": {
            "id": 6,
            "project_id": 1,
            "ref": "main",
            "sha": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "status": "pending",
        },
        "ref": "main",
        "artifacts": [],
        "runner": None,
        "runner_manager": None,
        "stage": "test",
        "status": "failed",
        "tag": False,
        "web_url": "https://example.com/foo/bar/-/jobs/8",
        "project": {"ci_job_token_scope_enabled": False},
        "user": {
            "id": 1,
            "name": "Administrator",
            "username": "root",
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://gitlab.dev/root",
            "created_at": "2015-12-21T13:14:24.077Z",
            "bio": None,
            "location": None,
            "public_email": "",
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "website_url": "",
            "organization": "",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_7():
    # Cancel a job
    example_data = {
        "commit": {
            "author_email": "admin@example.com",
            "author_name": "Administrator",
            "created_at": "2015-12-24T16:51:14.000+01:00",
            "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "message": "Test the CI integration.",
            "short_id": "0ff3ae19",
            "title": "Test the CI integration.",
        },
        "coverage": None,
        "archived": False,
        "allow_failure": False,
        "created_at": "2016-01-11T10:13:33.506Z",
        "started_at": "2016-01-11T10:14:09.526Z",
        "finished_at": None,
        "erased_at": None,
        "duration": 8,
        "queued_duration": 0.010,
        "id": 1,
        "name": "rubocop",
        "ref": "main",
        "artifacts": [],
        "runner": None,
        "runner_manager": None,
        "stage": "test",
        "status": "canceled",
        "tag": False,
        "web_url": "https://example.com/foo/bar/-/jobs/1",
        "project": {"ci_job_token_scope_enabled": False},
        "user": None,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_8():
    # Retry a job
    example_data = {
        "commit": {
            "author_email": "admin@example.com",
            "author_name": "Administrator",
            "created_at": "2015-12-24T16:51:14.000+01:00",
            "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "message": "Test the CI integration.",
            "short_id": "0ff3ae19",
            "title": "Test the CI integration.",
        },
        "coverage": None,
        "archived": False,
        "allow_failure": False,
        "created_at": "2016-01-11T10:13:33.506Z",
        "started_at": None,
        "finished_at": None,
        "erased_at": None,
        "duration": None,
        "queued_duration": 0.010,
        "id": 1,
        "name": "rubocop",
        "ref": "main",
        "artifacts": [],
        "runner": None,
        "runner_manager": None,
        "stage": "test",
        "status": "pending",
        "tag": False,
        "web_url": "https://example.com/foo/bar/-/jobs/1",
        "project": {"ci_job_token_scope_enabled": False},
        "user": None,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_jobs_response_9():
    # Run a job
    example_data = {
        "commit": {
            "author_email": "admin@example.com",
            "author_name": "Administrator",
            "created_at": "2015-12-24T16:51:14.000+01:00",
            "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "message": "Test the CI integration.",
            "short_id": "0ff3ae19",
            "title": "Test the CI integration.",
        },
        "coverage": None,
        "archived": False,
        "allow_failure": False,
        "created_at": "2016-01-11T10:13:33.506Z",
        "started_at": None,
        "finished_at": None,
        "erased_at": None,
        "duration": None,
        "queued_duration": 0.010,
        "id": 1,
        "name": "rubocop",
        "ref": "main",
        "artifacts": [],
        "runner": None,
        "runner_manager": None,
        "stage": "test",
        "status": "pending",
        "tag": False,
        "web_url": "https://example.com/foo/bar/-/jobs/1",
        "project": {"ci_job_token_scope_enabled": False},
        "user": None,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_member_response_1():
    # List all members of a group or project
    example_data = [
        {
            "id": 1,
            "username": "raymond_smith",
            "name": "Raymond Smith",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
            "created_at": "2012-09-22T14:13:35Z",
            "created_by": {
                "id": 2,
                "username": "john_doe",
                "name": "John Doe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
                "web_url": "http://192.168.1.8:3000/root",
            },
            "expires_at": "2012-10-22T14:13:35Z",
            "access_level": 30,
            "group_saml_identity": None,
        },
        {
            "id": 2,
            "username": "john_doe",
            "name": "John Doe",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
            "created_at": "2012-09-22T14:13:35Z",
            "created_by": {
                "id": 1,
                "username": "raymond_smith",
                "name": "Raymond Smith",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
                "web_url": "http://192.168.1.8:3000/root",
            },
            "expires_at": "2012-10-22T14:13:35Z",
            "access_level": 30,
            "email": "john@example.com",
            "group_saml_identity": {
                "extern_uid": "ABC-1234567890",
                "provider": "group_saml",
                "saml_provider_id": 10,
            },
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_member_response_2():
    # List all members of a group or project including inherited and invited members
    example_data = [
        {
            "id": 1,
            "username": "raymond_smith",
            "name": "Raymond Smith",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
            "created_at": "2012-09-22T14:13:35Z",
            "created_by": {
                "id": 2,
                "username": "john_doe",
                "name": "John Doe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
                "web_url": "http://192.168.1.8:3000/root",
            },
            "expires_at": "2012-10-22T14:13:35Z",
            "access_level": 30,
            "group_saml_identity": None,
        },
        {
            "id": 2,
            "username": "john_doe",
            "name": "John Doe",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
            "created_at": "2012-09-22T14:13:35Z",
            "created_by": {
                "id": 1,
                "username": "raymond_smith",
                "name": "Raymond Smith",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
                "web_url": "http://192.168.1.8:3000/root",
            },
            "expires_at": "2012-10-22T14:13:35Z",
            "access_level": 30,
            "email": "john@example.com",
            "group_saml_identity": {
                "extern_uid": "ABC-1234567890",
                "provider": "group_saml",
                "saml_provider_id": 10,
            },
        },
        {
            "id": 3,
            "username": "foo_bar",
            "name": "Foo bar",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
            "created_at": "2012-10-22T14:13:35Z",
            "created_by": {
                "id": 2,
                "username": "john_doe",
                "name": "John Doe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
                "web_url": "http://192.168.1.8:3000/root",
            },
            "expires_at": "2012-11-22T14:13:35Z",
            "access_level": 30,
            "group_saml_identity": None,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_member_response_3():
    # Get a member of a group or project
    example_data = {
        "id": 1,
        "username": "raymond_smith",
        "name": "Raymond Smith",
        "state": "active",
        "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
        "web_url": "http://192.168.1.8:3000/root",
        "access_level": 30,
        "email": "john@example.com",
        "created_at": "2012-10-22T14:13:35Z",
        "created_by": {
            "id": 2,
            "username": "john_doe",
            "name": "John Doe",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
        },
        "expires_at": None,
        "group_saml_identity": None,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_member_response_4():
    # Get a member of a group or project, including inherited and invited members
    example_data = {
        "id": 1,
        "username": "raymond_smith",
        "name": "Raymond Smith",
        "state": "active",
        "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
        "web_url": "http://192.168.1.8:3000/root",
        "access_level": 30,
        "created_at": "2012-10-22T14:13:35Z",
        "created_by": {
            "id": 2,
            "username": "john_doe",
            "name": "John Doe",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
        },
        "email": "john@example.com",
        "expires_at": None,
        "group_saml_identity": None,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_member_response_5():
    #
    example_data = [
        {
            "id": 1,
            "username": "raymond_smith",
            "name": "Raymond Smith",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
            "last_activity_on": "2021-01-27",
            "membership_type": "group_member",
            "removable": True,
            "created_at": "2021-01-03T12:16:02.000Z",
            "last_login_at": "2022-10-09T01:33:06.000Z",
        },
        {
            "id": 2,
            "username": "john_doe",
            "name": "John Doe",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
            "email": "john@example.com",
            "last_activity_on": "2021-01-25",
            "membership_type": "group_member",
            "removable": True,
            "created_at": "2021-01-04T18:46:42.000Z",
            "last_login_at": "2022-09-29T22:18:46.000Z",
        },
        {
            "id": 3,
            "username": "foo_bar",
            "name": "Foo bar",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
            "last_activity_on": "2021-01-20",
            "membership_type": "group_invite",
            "removable": False,
            "created_at": "2021-01-09T07:12:31.000Z",
            "last_login_at": "2022-10-10T07:28:56.000Z",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_member_response_6():
    # List memberships for a billable member of a group
    example_data = [
        {
            "id": 168,
            "source_id": 131,
            "source_full_name": "Root Group / Sub Group One",
            "source_members_url": "https://gitlab.example.com/groups/root-group/sub-group-one/-/group_members",
            "created_at": "2021-03-31T17:28:44.812Z",
            "expires_at": "2022-03-21",
            "access_level": {"string_value": "Developer", "integer_value": 30},
        },
        {
            "id": 169,
            "source_id": 63,
            "source_full_name": "Root Group / Sub Group One / My Project",
            "source_members_url": "https://gitlab.example.com/root-group/sub-group-one/my-project/-/project_members",
            "created_at": "2021-03-31T17:29:14.934Z",
            "expires_at": None,
            "access_level": {"string_value": "Maintainer", "integer_value": 40},
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Membership"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_member_response_7():
    # Add a member to a group or project
    example_data = {
        "id": 1,
        "username": "raymond_smith",
        "name": "Raymond Smith",
        "state": "active",
        "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
        "web_url": "http://192.168.1.8:3000/root",
        "created_at": "2012-10-22T14:13:35Z",
        "created_by": {
            "id": 2,
            "username": "john_doe",
            "name": "John Doe",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
            "web_url": "http://192.168.1.8:3000/root",
        },
        "expires_at": "2012-10-22T14:13:35Z",
        "access_level": 30,
        "email": "john@example.com",
        "group_saml_identity": None,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_member_response_8():
    # List pending members of a group and its subgroups and projects
    example_data = [
        {
            "id": 168,
            "name": "Alex Garcia",
            "username": "alex_garcia",
            "email": "alex@example.com",
            "avatar_url": "http://example.com/uploads/user/avatar/1/cd8.jpeg",
            "web_url": "http://example.com/alex_garcia",
            "approved": False,
            "invited": False,
        },
        {
            "id": 169,
            "email": "sidney@example.com",
            "avatar_url": "http://gravatar.com/../e346561cd8.jpeg",
            "approved": False,
            "invited": True,
        },
        {
            "id": 170,
            "email": "zhang@example.com",
            "avatar_url": "http://gravatar.com/../e32131cd8.jpeg",
            "approved": True,
            "invited": True,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "User"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_1():
    # Get group-level approval rules
    example_data = [
        {
            "id": 2,
            "name": "rule1",
            "rule_type": "any_approver",
            "eligible_approvers": [],
            "approvals_required": 3,
            "users": [],
            "groups": [],
            "contains_hidden_groups": False,
            "protected_branches": [],
            "applies_to_all_protected_branches": True,
        },
        {
            "id": 3,
            "name": "rule2",
            "rule_type": "code_owner",
            "eligible_approvers": [],
            "approvals_required": 2,
            "users": [],
            "groups": [],
            "contains_hidden_groups": False,
            "protected_branches": [],
            "applies_to_all_protected_branches": True,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_2():
    # Create group-level approval rules
    example_data = {
        "id": 5,
        "name": "security",
        "rule_type": "any_approver",
        "eligible_approvers": [],
        "approvals_required": 2,
        "users": [],
        "groups": [],
        "contains_hidden_groups": False,
        "protected_branches": [
            {
                "id": 5,
                "name": "master",
                "push_access_levels": [
                    {
                        "id": 5,
                        "access_level": 40,
                        "access_level_description": "Maintainers",
                        "deploy_key_id": None,
                        "user_id": None,
                        "group_id": None,
                    }
                ],
                "merge_access_levels": [
                    {
                        "id": 5,
                        "access_level": 40,
                        "access_level_description": "Maintainers",
                        "user_id": None,
                        "group_id": None,
                    }
                ],
                "allow_force_push": False,
                "unprotect_access_levels": [],
                "code_owner_approval_required": False,
                "inherited": False,
            }
        ],
        "applies_to_all_protected_branches": True,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_3():
    # Update group-level approval rules
    example_data = {
        "id": 5,
        "name": "security2",
        "rule_type": "any_approver",
        "eligible_approvers": [],
        "approvals_required": 1,
        "users": [],
        "groups": [],
        "contains_hidden_groups": False,
        "protected_branches": [
            {
                "id": 5,
                "name": "master",
                "push_access_levels": [
                    {
                        "id": 5,
                        "access_level": 40,
                        "access_level_description": "Maintainers",
                        "deploy_key_id": None,
                        "user_id": None,
                        "group_id": None,
                    }
                ],
                "merge_access_levels": [
                    {
                        "id": 5,
                        "access_level": 40,
                        "access_level_description": "Maintainers",
                        "user_id": None,
                        "group_id": None,
                    }
                ],
                "allow_force_push": False,
                "unprotect_access_levels": [],
                "code_owner_approval_required": False,
                "inherited": False,
            }
        ],
        "applies_to_all_protected_branches": True,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_4():
    # Change configuration
    example_data = {
        "approvals_before_merge": 2,
        "reset_approvals_on_push": True,
        "selective_code_owner_removals": False,
        "disable_overriding_approvers_per_merge_request": False,
        "merge_requests_author_approval": False,
        "merge_requests_disable_committers_approval": False,
        "require_password_to_approve": True,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeApprovals"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_5():
    # Project-level MR approvals
    example_data = {
        "approvers": [],
        "approver_groups": [],
        "approvals_before_merge": 2,
        "reset_approvals_on_push": True,
        "selective_code_owner_removals": False,
        "disable_overriding_approvers_per_merge_request": False,
        "merge_requests_author_approval": True,
        "merge_requests_disable_committers_approval": False,
        "require_password_to_approve": True,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeApprovals"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_6():
    # Get project-level rules
    example_data = [
        {
            "id": 1,
            "name": "security",
            "rule_type": "regular",
            "eligible_approvers": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                },
                {
                    "id": 50,
                    "name": "Group Member 1",
                    "username": "group_member_1",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/group_member_1",
                },
            ],
            "approvals_required": 3,
            "users": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                }
            ],
            "groups": [
                {
                    "id": 5,
                    "name": "group1",
                    "path": "group1",
                    "description": "",
                    "visibility": "public",
                    "lfs_enabled": False,
                    "avatar_url": None,
                    "web_url": "http://localhost/groups/group1",
                    "request_access_enabled": False,
                    "full_name": "group1",
                    "full_path": "group1",
                    "parent_id": None,
                    "ldap_cn": None,
                    "ldap_access": None,
                }
            ],
            "applies_to_all_protected_branches": False,
            "protected_branches": [
                {
                    "id": 1,
                    "name": "main",
                    "push_access_levels": [
                        {
                            "access_level": 30,
                            "access_level_description": "Developers + Maintainers",
                        }
                    ],
                    "merge_access_levels": [
                        {
                            "access_level": 30,
                            "access_level_description": "Developers + Maintainers",
                        }
                    ],
                    "unprotect_access_levels": [
                        {"access_level": 40, "access_level_description": "Maintainers"}
                    ],
                    "code_owner_approval_required": "false",
                }
            ],
            "contains_hidden_groups": False,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_7():
    # Get a single project-level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 5,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 3,
        "users": [
            {
                "id": 5,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "applies_to_all_protected_branches": False,
        "protected_branches": [
            {
                "id": 1,
                "name": "main",
                "push_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "merge_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "unprotect_access_levels": [
                    {"access_level": 40, "access_level_description": "Maintainers"}
                ],
                "code_owner_approval_required": "false",
            }
        ],
        "contains_hidden_groups": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_8():
    # Create project-level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 1,
        "users": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "applies_to_all_protected_branches": False,
        "protected_branches": [
            {
                "id": 1,
                "name": "main",
                "push_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "merge_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "unprotect_access_levels": [
                    {"access_level": 40, "access_level_description": "Maintainers"}
                ],
                "code_owner_approval_required": "false",
            }
        ],
        "contains_hidden_groups": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_9():
    # Update Project level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 1,
        "users": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "applies_to_all_protected_branches": False,
        "protected_branches": [
            {
                "id": 1,
                "name": "main",
                "push_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "merge_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "unprotect_access_levels": [
                    {"access_level": 40, "access_level_description": "Maintainers"}
                ],
                "code_owner_approval_required": "false",
            }
        ],
        "contains_hidden_groups": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_10():
    # Merge request-level MR approvals
    example_data = {
        "id": 5,
        "iid": 5,
        "project_id": 1,
        "title": "Approvals API",
        "description": "Test",
        "state": "opened",
        "created_at": "2016-06-08T00:19:52.638Z",
        "updated_at": "2016-06-08T21:20:42.470Z",
        "merge_status": "cannot_be_merged",
        "approvals_required": 2,
        "approvals_left": 1,
        "approved_by": [
            {
                "user": {
                    "name": "Administrator",
                    "username": "root",
                    "id": 1,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                    "web_url": "http://localhost:3000/root",
                }
            }
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_11():
    # Get the approval state of merge requests
    example_data = {
        "approval_rules_overwritten": True,
        "rules": [
            {
                "id": 1,
                "name": "Ruby",
                "rule_type": "regular",
                "eligible_approvers": [
                    {
                        "id": 4,
                        "name": "John Doe",
                        "username": "jdoe",
                        "state": "active",
                        "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                        "web_url": "http://localhost/jdoe",
                    }
                ],
                "approvals_required": 2,
                "users": [
                    {
                        "id": 4,
                        "name": "John Doe",
                        "username": "jdoe",
                        "state": "active",
                        "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                        "web_url": "http://localhost/jdoe",
                    }
                ],
                "groups": [],
                "contains_hidden_groups": False,
                "approved_by": [
                    {
                        "id": 4,
                        "name": "John Doe",
                        "username": "jdoe",
                        "state": "active",
                        "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                        "web_url": "http://localhost/jdoe",
                    }
                ],
                "source_rule": None,
                "approved": True,
                "overridden": False,
            }
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_12():
    # Get merge request level rules
    example_data = [
        {
            "id": 1,
            "name": "security",
            "rule_type": "regular",
            "eligible_approvers": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                },
                {
                    "id": 50,
                    "name": "Group Member 1",
                    "username": "group_member_1",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/group_member_1",
                },
            ],
            "approvals_required": 3,
            "source_rule": None,
            "users": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                }
            ],
            "groups": [
                {
                    "id": 5,
                    "name": "group1",
                    "path": "group1",
                    "description": "",
                    "visibility": "public",
                    "lfs_enabled": False,
                    "avatar_url": None,
                    "web_url": "http://localhost/groups/group1",
                    "request_access_enabled": False,
                    "full_name": "group1",
                    "full_path": "group1",
                    "parent_id": None,
                    "ldap_cn": None,
                    "ldap_access": None,
                }
            ],
            "contains_hidden_groups": False,
            "overridden": False,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_13():
    # Get a single merge request level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 5,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 3,
        "source_rule": None,
        "users": [
            {
                "id": 5,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "contains_hidden_groups": False,
        "overridden": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_14():
    # Create merge request level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 1,
        "source_rule": None,
        "users": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "contains_hidden_groups": False,
        "overridden": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_approval_rule_response_15():
    # Approve merge request
    example_data = {
        "id": 5,
        "iid": 5,
        "project_id": 1,
        "title": "Approvals API",
        "description": "Test",
        "state": "opened",
        "created_at": "2016-06-08T00:19:52.638Z",
        "updated_at": "2016-06-09T21:32:14.105Z",
        "merge_status": "can_be_merged",
        "approvals_required": 2,
        "approvals_left": 0,
        "approved_by": [
            {
                "user": {
                    "name": "Administrator",
                    "username": "root",
                    "id": 1,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                    "web_url": "http://localhost:3000/root",
                }
            },
            {
                "user": {
                    "name": "Nico Cartwright",
                    "username": "ryley",
                    "id": 2,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/cf7ad14b34162a76d593e3affca2adca?s=80\u0026d=identicon",
                    "web_url": "http://localhost:3000/ryley",
                }
            },
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_1():
    # Get group-level approval rules
    example_data = [
        {
            "id": 2,
            "name": "rule1",
            "rule_type": "any_approver",
            "eligible_approvers": [],
            "approvals_required": 3,
            "users": [],
            "groups": [],
            "contains_hidden_groups": False,
            "protected_branches": [],
            "applies_to_all_protected_branches": True,
        },
        {
            "id": 3,
            "name": "rule2",
            "rule_type": "code_owner",
            "eligible_approvers": [],
            "approvals_required": 2,
            "users": [],
            "groups": [],
            "contains_hidden_groups": False,
            "protected_branches": [],
            "applies_to_all_protected_branches": True,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_2():
    # Create group-level approval rules
    example_data = {
        "id": 5,
        "name": "security",
        "rule_type": "any_approver",
        "eligible_approvers": [],
        "approvals_required": 2,
        "users": [],
        "groups": [],
        "contains_hidden_groups": False,
        "protected_branches": [
            {
                "id": 5,
                "name": "master",
                "push_access_levels": [
                    {
                        "id": 5,
                        "access_level": 40,
                        "access_level_description": "Maintainers",
                        "deploy_key_id": None,
                        "user_id": None,
                        "group_id": None,
                    }
                ],
                "merge_access_levels": [
                    {
                        "id": 5,
                        "access_level": 40,
                        "access_level_description": "Maintainers",
                        "user_id": None,
                        "group_id": None,
                    }
                ],
                "allow_force_push": False,
                "unprotect_access_levels": [],
                "code_owner_approval_required": False,
                "inherited": False,
            }
        ],
        "applies_to_all_protected_branches": True,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_3():
    # Update group-level approval rules
    example_data = {
        "id": 5,
        "name": "security2",
        "rule_type": "any_approver",
        "eligible_approvers": [],
        "approvals_required": 1,
        "users": [],
        "groups": [],
        "contains_hidden_groups": False,
        "protected_branches": [
            {
                "id": 5,
                "name": "master",
                "push_access_levels": [
                    {
                        "id": 5,
                        "access_level": 40,
                        "access_level_description": "Maintainers",
                        "deploy_key_id": None,
                        "user_id": None,
                        "group_id": None,
                    }
                ],
                "merge_access_levels": [
                    {
                        "id": 5,
                        "access_level": 40,
                        "access_level_description": "Maintainers",
                        "user_id": None,
                        "group_id": None,
                    }
                ],
                "allow_force_push": False,
                "unprotect_access_levels": [],
                "code_owner_approval_required": False,
                "inherited": False,
            }
        ],
        "applies_to_all_protected_branches": True,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_4():
    # Change configuration
    example_data = {
        "approvals_before_merge": 2,
        "reset_approvals_on_push": True,
        "selective_code_owner_removals": False,
        "disable_overriding_approvers_per_merge_request": False,
        "merge_requests_author_approval": False,
        "merge_requests_disable_committers_approval": False,
        "require_password_to_approve": True,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeApprovals"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_5():
    # Project-level MR approvals
    example_data = {
        "approvers": [],
        "approver_groups": [],
        "approvals_before_merge": 2,
        "reset_approvals_on_push": True,
        "selective_code_owner_removals": False,
        "disable_overriding_approvers_per_merge_request": False,
        "merge_requests_author_approval": True,
        "merge_requests_disable_committers_approval": False,
        "require_password_to_approve": True,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeApprovals"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_6():
    # Get project-level rules
    example_data = [
        {
            "id": 1,
            "name": "security",
            "rule_type": "regular",
            "eligible_approvers": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                },
                {
                    "id": 50,
                    "name": "Group Member 1",
                    "username": "group_member_1",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/group_member_1",
                },
            ],
            "approvals_required": 3,
            "users": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                }
            ],
            "groups": [
                {
                    "id": 5,
                    "name": "group1",
                    "path": "group1",
                    "description": "",
                    "visibility": "public",
                    "lfs_enabled": False,
                    "avatar_url": None,
                    "web_url": "http://localhost/groups/group1",
                    "request_access_enabled": False,
                    "full_name": "group1",
                    "full_path": "group1",
                    "parent_id": None,
                    "ldap_cn": None,
                    "ldap_access": None,
                }
            ],
            "applies_to_all_protected_branches": False,
            "protected_branches": [
                {
                    "id": 1,
                    "name": "main",
                    "push_access_levels": [
                        {
                            "access_level": 30,
                            "access_level_description": "Developers + Maintainers",
                        }
                    ],
                    "merge_access_levels": [
                        {
                            "access_level": 30,
                            "access_level_description": "Developers + Maintainers",
                        }
                    ],
                    "unprotect_access_levels": [
                        {"access_level": 40, "access_level_description": "Maintainers"}
                    ],
                    "code_owner_approval_required": "false",
                }
            ],
            "contains_hidden_groups": False,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_7():
    # Get a single project-level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 5,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 3,
        "users": [
            {
                "id": 5,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "applies_to_all_protected_branches": False,
        "protected_branches": [
            {
                "id": 1,
                "name": "main",
                "push_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "merge_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "unprotect_access_levels": [
                    {"access_level": 40, "access_level_description": "Maintainers"}
                ],
                "code_owner_approval_required": "false",
            }
        ],
        "contains_hidden_groups": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_8():
    # Create project-level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 1,
        "users": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "applies_to_all_protected_branches": False,
        "protected_branches": [
            {
                "id": 1,
                "name": "main",
                "push_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "merge_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "unprotect_access_levels": [
                    {"access_level": 40, "access_level_description": "Maintainers"}
                ],
                "code_owner_approval_required": "false",
            }
        ],
        "contains_hidden_groups": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_9():
    # Update Project level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 1,
        "users": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "applies_to_all_protected_branches": False,
        "protected_branches": [
            {
                "id": 1,
                "name": "main",
                "push_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "merge_access_levels": [
                    {
                        "access_level": 30,
                        "access_level_description": "Developers + Maintainers",
                    }
                ],
                "unprotect_access_levels": [
                    {"access_level": 40, "access_level_description": "Maintainers"}
                ],
                "code_owner_approval_required": "false",
            }
        ],
        "contains_hidden_groups": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_10():
    # Merge request-level MR approvals
    example_data = {
        "id": 5,
        "iid": 5,
        "project_id": 1,
        "title": "Approvals API",
        "description": "Test",
        "state": "opened",
        "created_at": "2016-06-08T00:19:52.638Z",
        "updated_at": "2016-06-08T21:20:42.470Z",
        "merge_status": "cannot_be_merged",
        "approvals_required": 2,
        "approvals_left": 1,
        "approved_by": [
            {
                "user": {
                    "name": "Administrator",
                    "username": "root",
                    "id": 1,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                    "web_url": "http://localhost:3000/root",
                }
            }
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_11():
    # Get the approval state of merge requests
    example_data = {
        "approval_rules_overwritten": True,
        "rules": [
            {
                "id": 1,
                "name": "Ruby",
                "rule_type": "regular",
                "eligible_approvers": [
                    {
                        "id": 4,
                        "name": "John Doe",
                        "username": "jdoe",
                        "state": "active",
                        "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                        "web_url": "http://localhost/jdoe",
                    }
                ],
                "approvals_required": 2,
                "users": [
                    {
                        "id": 4,
                        "name": "John Doe",
                        "username": "jdoe",
                        "state": "active",
                        "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                        "web_url": "http://localhost/jdoe",
                    }
                ],
                "groups": [],
                "contains_hidden_groups": False,
                "approved_by": [
                    {
                        "id": 4,
                        "name": "John Doe",
                        "username": "jdoe",
                        "state": "active",
                        "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                        "web_url": "http://localhost/jdoe",
                    }
                ],
                "source_rule": None,
                "approved": True,
                "overridden": False,
            }
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_12():
    # Get merge request level rules
    example_data = [
        {
            "id": 1,
            "name": "security",
            "rule_type": "regular",
            "eligible_approvers": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                },
                {
                    "id": 50,
                    "name": "Group Member 1",
                    "username": "group_member_1",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/group_member_1",
                },
            ],
            "approvals_required": 3,
            "source_rule": None,
            "users": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                }
            ],
            "groups": [
                {
                    "id": 5,
                    "name": "group1",
                    "path": "group1",
                    "description": "",
                    "visibility": "public",
                    "lfs_enabled": False,
                    "avatar_url": None,
                    "web_url": "http://localhost/groups/group1",
                    "request_access_enabled": False,
                    "full_name": "group1",
                    "full_path": "group1",
                    "parent_id": None,
                    "ldap_cn": None,
                    "ldap_access": None,
                }
            ],
            "contains_hidden_groups": False,
            "overridden": False,
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_13():
    # Get a single merge request level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 5,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 3,
        "source_rule": None,
        "users": [
            {
                "id": 5,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "contains_hidden_groups": False,
        "overridden": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_14():
    # Create merge request level rule
    example_data = {
        "id": 1,
        "name": "security",
        "rule_type": "regular",
        "eligible_approvers": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            },
            {
                "id": 50,
                "name": "Group Member 1",
                "username": "group_member_1",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/group_member_1",
            },
        ],
        "approvals_required": 1,
        "source_rule": None,
        "users": [
            {
                "id": 2,
                "name": "John Doe",
                "username": "jdoe",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                "web_url": "http://localhost/jdoe",
            }
        ],
        "groups": [
            {
                "id": 5,
                "name": "group1",
                "path": "group1",
                "description": "",
                "visibility": "public",
                "lfs_enabled": False,
                "avatar_url": None,
                "web_url": "http://localhost/groups/group1",
                "request_access_enabled": False,
                "full_name": "group1",
                "full_path": "group1",
                "parent_id": None,
                "ldap_cn": None,
                "ldap_access": None,
            }
        ],
        "contains_hidden_groups": False,
        "overridden": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "ApprovalRule"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_protected_branch_response_15():
    # Approve merge request
    example_data = {
        "id": 5,
        "iid": 5,
        "project_id": 1,
        "title": "Approvals API",
        "description": "Test",
        "state": "opened",
        "created_at": "2016-06-08T00:19:52.638Z",
        "updated_at": "2016-06-09T21:32:14.105Z",
        "merge_status": "can_be_merged",
        "approvals_required": 2,
        "approvals_left": 0,
        "approved_by": [
            {
                "user": {
                    "name": "Administrator",
                    "username": "root",
                    "id": 1,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                    "web_url": "http://localhost:3000/root",
                }
            },
            {
                "user": {
                    "name": "Nico Cartwright",
                    "username": "ryley",
                    "id": 2,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/cf7ad14b34162a76d593e3affca2adca?s=80\u0026d=identicon",
                    "web_url": "http://localhost:3000/ryley",
                }
            },
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_package_response_1():
    # List packages
    example_data = [
        {
            "id": 1,
            "name": "com/mycompany/my-app",
            "version": "1.0-SNAPSHOT",
            "package_type": "maven",
            "created_at": "2019-11-27T03:37:38.711Z",
        },
        {
            "id": 2,
            "name": "@foo/bar",
            "version": "1.0.3",
            "package_type": "npm",
            "created_at": "2019-11-27T03:37:38.711Z",
        },
        {
            "id": 3,
            "name": "Hello/0.1@mycompany/stable",
            "conan_package_name": "Hello",
            "version": "0.1",
            "package_type": "conan",
            "_links": {
                "web_path": "/foo/bar/-/packages/3",
                "delete_api_path": "https://gitlab.example.com/api/v4/projects/1/packages/3",
            },
            "created_at": "2029-12-16T20:33:34.316Z",
            "tags": [],
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Package"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_package_response_2():

    # Package for a group
    example_data = [
        {
            "id": 1,
            "name": "com/mycompany/my-app",
            "version": "1.0-SNAPSHOT",
            "package_type": "maven",
            "_links": {
                "web_path": "/namespace1/project1/-/packages/1",
                "delete_api_path": "/namespace1/project1/-/packages/1",
            },
            "created_at": "2019-11-27T03:37:38.711Z",
            "pipelines": [
                {
                    "id": 123,
                    "status": "pending",
                    "ref": "new-pipeline",
                    "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
                    "web_url": "https://example.com/foo/bar/pipelines/47",
                    "created_at": "2016-08-11T11:28:34.085Z",
                    "updated_at": "2016-08-11T11:32:35.169Z",
                    "user": {
                        "name": "Administrator",
                        "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                    },
                }
            ],
        },
        {
            "id": 2,
            "name": "@foo/bar",
            "version": "1.0.3",
            "package_type": "npm",
            "_links": {
                "web_path": "/namespace1/project1/-/packages/1",
                "delete_api_path": "/namespace1/project1/-/packages/1",
            },
            "created_at": "2019-11-27T03:37:38.711Z",
            "pipelines": [
                {
                    "id": 123,
                    "status": "pending",
                    "ref": "new-pipeline",
                    "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
                    "web_url": "https://example.com/foo/bar/pipelines/47",
                    "created_at": "2016-08-11T11:28:34.085Z",
                    "updated_at": "2016-08-11T11:32:35.169Z",
                    "user": {
                        "name": "Administrator",
                        "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                    },
                }
            ],
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Package"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_package_response_3():

    # Get a project package
    example_data = {
        "id": 1,
        "name": "com/mycompany/my-app",
        "version": "1.0-SNAPSHOT",
        "package_type": "maven",
        "_links": {
            "web_path": "/namespace1/project1/-/packages/1",
            "delete_api_path": "/namespace1/project1/-/packages/1",
        },
        "created_at": "2019-11-27T03:37:38.711Z",
        "last_downloaded_at": "2022-09-07T07:51:50.504Z",
        "pipelines": [
            {
                "id": 123,
                "status": "pending",
                "ref": "new-pipeline",
                "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
                "web_url": "https://example.com/foo/bar/pipelines/47",
                "created_at": "2016-08-11T11:28:34.085Z",
                "updated_at": "2016-08-11T11:32:35.169Z",
                "user": {
                    "name": "Administrator",
                    "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                },
            }
        ],
        "versions": [
            {
                "id": 2,
                "version": "2.0-SNAPSHOT",
                "created_at": "2020-04-28T04:42:11.573Z",
                "pipelines": [
                    {
                        "id": 234,
                        "status": "pending",
                        "ref": "new-pipeline",
                        "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
                        "web_url": "https://example.com/foo/bar/pipelines/58",
                        "created_at": "2016-08-11T11:28:34.085Z",
                        "updated_at": "2016-08-11T11:32:35.169Z",
                        "user": {
                            "name": "Administrator",
                            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                        },
                    }
                ],
            }
        ],
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Package"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_package_response_4():

    # List package files
    example_data = [
        {
            "id": 25,
            "package_id": 4,
            "created_at": "2018-11-07T15:25:52.199Z",
            "file_name": "my-app-1.5-20181107.152550-1.jar",
            "size": 2421,
            "file_md5": "58e6a45a629910c6ff99145a688971ac",
            "file_sha1": "ebd193463d3915d7e22219f52740056dfd26cbfe",
            "file_sha256": "a903393463d3915d7e22219f52740056dfd26cbfeff321b",
            "pipelines": [
                {
                    "id": 123,
                    "status": "pending",
                    "ref": "new-pipeline",
                    "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
                    "web_url": "https://example.com/foo/bar/pipelines/47",
                    "created_at": "2016-08-11T11:28:34.085Z",
                    "updated_at": "2016-08-11T11:32:35.169Z",
                    "user": {
                        "name": "Administrator",
                        "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                    },
                }
            ],
        },
        {
            "id": 26,
            "package_id": 4,
            "created_at": "2018-11-07T15:25:56.776Z",
            "file_name": "my-app-1.5-20181107.152550-1.pom",
            "size": 1122,
            "file_md5": "d90f11d851e17c5513586b4a7e98f1b2",
            "file_sha1": "9608d068fe88aff85781811a42f32d97feb440b5",
            "file_sha256": "2987d068fe88aff85781811a42f32d97feb4f092a399",
        },
        {
            "id": 27,
            "package_id": 4,
            "created_at": "2018-11-07T15:26:00.556Z",
            "file_name": "maven-metadata.xml",
            "size": 767,
            "file_md5": "6dfd0cce1203145a927fef5e3a1c650c",
            "file_sha1": "d25932de56052d320a8ac156f745ece73f6a8cd2",
            "file_sha256": "ac849d002e56052d320a8ac156f745ece73f6a8cd2f3e82",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Package"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_package_response_5():

    # List package pipelines
    example_data = [
        {
            "id": 1,
            "iid": 1,
            "project_id": 9,
            "sha": "2b6127f6bb6f475c4e81afcc2251e3f941e554f9",
            "ref": "mytag",
            "status": "failed",
            "source": "push",
            "created_at": "2023-02-01T12:19:21.895Z",
            "updated_at": "2023-02-01T14:00:05.922Z",
            "web_url": "http://gdk.test:3001/feature-testing/composer-repository/-/pipelines/1",
            "user": {
                "id": 1,
                "username": "root",
                "name": "Administrator",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                "web_url": "http://gdk.test:3001/root",
            },
        },
        {
            "id": 2,
            "iid": 2,
            "project_id": 9,
            "sha": "e564015ac6cb3d8617647802c875b27d392f72a6",
            "ref": "main",
            "status": "canceled",
            "source": "push",
            "created_at": "2023-02-01T12:23:23.694Z",
            "updated_at": "2023-02-01T12:26:28.635Z",
            "web_url": "http://gdk.test:3001/feature-testing/composer-repository/-/pipelines/2",
            "user": {
                "id": 1,
                "username": "root",
                "name": "Administrator",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                "web_url": "http://gdk.test:3001/root",
            },
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Pipeline"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_release_response_1():
    # List Releases
    example_data = [
        {
            "tag_name": "v0.2",
            "description": "## CHANGELOG\r\n\r\n- Escape label and milestone titles to prevent XSS in GLFM autocomplete. !2740\r\n- Prevent private snippets from being embeddable.\r\n- Add subresources removal to member destroy service.",
            "name": "Awesome app v0.2 beta",
            "created_at": "2019-01-03T01:56:19.539Z",
            "released_at": "2019-01-03T01:56:19.539Z",
            "author": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                "web_url": "https://gitlab.example.com/root",
            },
            "commit": {
                "id": "079e90101242458910cccd35eab0e211dfc359c0",
                "short_id": "079e9010",
                "title": "Update README.md",
                "created_at": "2019-01-03T01:55:38.000Z",
                "parent_ids": ["f8d3d94cbd347e924aa7b715845e439d00e80ca4"],
                "message": "Update README.md",
                "author_name": "Administrator",
                "author_email": "admin@example.com",
                "authored_date": "2019-01-03T01:55:38.000Z",
                "committer_name": "Administrator",
                "committer_email": "admin@example.com",
                "committed_date": "2019-01-03T01:55:38.000Z",
            },
            "milestones": [
                {
                    "id": 51,
                    "iid": 1,
                    "project_id": 24,
                    "title": "v1.0-rc",
                    "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                    "state": "closed",
                    "created_at": "2019-07-12T19:45:44.256Z",
                    "updated_at": "2019-07-12T19:45:44.256Z",
                    "due_date": "2019-08-16",
                    "start_date": "2019-07-30",
                    "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/1",
                    "issue_stats": {"total": 98, "closed": 76},
                },
                {
                    "id": 52,
                    "iid": 2,
                    "project_id": 24,
                    "title": "v1.0",
                    "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                    "state": "closed",
                    "created_at": "2019-07-16T14:00:12.256Z",
                    "updated_at": "2019-07-16T14:00:12.256Z",
                    "due_date": "2019-08-16",
                    "start_date": "2019-07-30",
                    "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/2",
                    "issue_stats": {"total": 24, "closed": 21},
                },
            ],
            "commit_path": "/root/awesome-app/commit/588440f66559714280628a4f9799f0c4eb880a4a",
            "tag_path": "/root/awesome-app/-/tags/v0.11.1",
            "assets": {
                "count": 6,
                "sources": [
                    {
                        "format": "zip",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.2/awesome-app-v0.2.zip",
                    },
                    {
                        "format": "tar.gz",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.2/awesome-app-v0.2.tar.gz",
                    },
                    {
                        "format": "tar.bz2",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.2/awesome-app-v0.2.tar.bz2",
                    },
                    {
                        "format": "tar",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.2/awesome-app-v0.2.tar",
                    },
                ],
                "links": [
                    {
                        "id": 2,
                        "name": "awesome-v0.2.msi",
                        "url": "http://192.168.10.15:3000/msi",
                        "link_type": "other",
                    },
                    {
                        "id": 1,
                        "name": "awesome-v0.2.dmg",
                        "url": "http://192.168.10.15:3000",
                        "link_type": "other",
                    },
                ],
                "evidence_file_path": "https://gitlab.example.com/root/awesome-app/-/releases/v0.2/evidence.json",
            },
            "evidences": [
                {
                    "sha": "760d6cdfb0879c3ffedec13af470e0f71cf52c6cde4d",
                    "filepath": "https://gitlab.example.com/root/awesome-app/-/releases/v0.2/evidence.json",
                    "collected_at": "2019-01-03T01:56:19.539Z",
                }
            ],
        },
        {
            "tag_name": "v0.1",
            "description": "## CHANGELOG\r\n\r\n-Remove limit of 100 when searching repository code. !8671\r\n- Show error message when attempting to reopen an MR and there is an open MR for the same branch. !16447 (Akos Gyimesi)\r\n- Fix a bug where internal email pattern wasn't respected. !22516",
            "name": "Awesome app v0.1 alpha",
            "created_at": "2019-01-03T01:55:18.203Z",
            "released_at": "2019-01-03T01:55:18.203Z",
            "author": {
                "id": 1,
                "name": "Administrator",
                "username": "root",
                "state": "active",
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
                "web_url": "https://gitlab.example.com/root",
            },
            "commit": {
                "id": "f8d3d94cbd347e924aa7b715845e439d00e80ca4",
                "short_id": "f8d3d94c",
                "title": "Initial commit",
                "created_at": "2019-01-03T01:53:28.000Z",
                "parent_ids": [],
                "message": "Initial commit",
                "author_name": "Administrator",
                "author_email": "admin@example.com",
                "authored_date": "2019-01-03T01:53:28.000Z",
                "committer_name": "Administrator",
                "committer_email": "admin@example.com",
                "committed_date": "2019-01-03T01:53:28.000Z",
            },
            "assets": {
                "count": 4,
                "sources": [
                    {
                        "format": "zip",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.zip",
                    },
                    {
                        "format": "tar.gz",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.gz",
                    },
                    {
                        "format": "tar.bz2",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.bz2",
                    },
                    {
                        "format": "tar",
                        "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar",
                    },
                ],
                "links": [],
                "evidence_file_path": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/evidence.json",
            },
            "evidences": [
                {
                    "sha": "c3ffedec13af470e760d6cdfb08790f71cf52c6cde4d",
                    "filepath": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/evidence.json",
                    "collected_at": "2019-01-03T01:55:18.203Z",
                }
            ],
            "_links": {
                "closed_issues_url": "https://gitlab.example.com/root/awesome-app/-/issues?release_tag=v0.1&scope=all&state=closed",
                "closed_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=closed",
                "edit_url": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/edit",
                "merged_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=merged",
                "opened_issues_url": "https://gitlab.example.com/root/awesome-app/-/issues?release_tag=v0.1&scope=all&state=opened",
                "opened_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=opened",
                "self": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1",
            },
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Release"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_release_response_2():
    # Get a Release by a tag name
    example_data = {
        "tag_name": "v0.1",
        "description": "## CHANGELOG\r\n\r\n- Remove limit of 100 when searching repository code. !8671\r\n- Show error message when attempting to reopen an MR and there is an open MR for the same branch. !16447 (Akos Gyimesi)\r\n- Fix a bug where internal email pattern wasn't respected. !22516",
        "name": "Awesome app v0.1 alpha",
        "created_at": "2019-01-03T01:55:18.203Z",
        "released_at": "2019-01-03T01:55:18.203Z",
        "author": {
            "id": 1,
            "name": "Administrator",
            "username": "root",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
            "web_url": "https://gitlab.example.com/root",
        },
        "commit": {
            "id": "f8d3d94cbd347e924aa7b715845e439d00e80ca4",
            "short_id": "f8d3d94c",
            "title": "Initial commit",
            "created_at": "2019-01-03T01:53:28.000Z",
            "parent_ids": [],
            "message": "Initial commit",
            "author_name": "Administrator",
            "author_email": "admin@example.com",
            "authored_date": "2019-01-03T01:53:28.000Z",
            "committer_name": "Administrator",
            "committer_email": "admin@example.com",
            "committed_date": "2019-01-03T01:53:28.000Z",
        },
        "milestones": [
            {
                "id": 51,
                "iid": 1,
                "project_id": 24,
                "title": "v1.0-rc",
                "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                "state": "closed",
                "created_at": "2019-07-12T19:45:44.256Z",
                "updated_at": "2019-07-12T19:45:44.256Z",
                "due_date": "2019-08-16",
                "start_date": "2019-07-30",
                "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/1",
                "issue_stats": {"total": 98, "closed": 76},
            },
            {
                "id": 52,
                "iid": 2,
                "project_id": 24,
                "title": "v1.0",
                "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                "state": "closed",
                "created_at": "2019-07-16T14:00:12.256Z",
                "updated_at": "2019-07-16T14:00:12.256Z",
                "due_date": "2019-08-16",
                "start_date": "2019-07-30",
                "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/2",
                "issue_stats": {"total": 24, "closed": 21},
            },
        ],
        "commit_path": "/root/awesome-app/commit/588440f66559714280628a4f9799f0c4eb880a4a",
        "tag_path": "/root/awesome-app/-/tags/v0.11.1",
        "assets": {
            "count": 5,
            "sources": [
                {
                    "format": "zip",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.zip",
                },
                {
                    "format": "tar.gz",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.gz",
                },
                {
                    "format": "tar.bz2",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.bz2",
                },
                {
                    "format": "tar",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar",
                },
            ],
            "links": [
                {
                    "id": 3,
                    "name": "hoge",
                    "url": "https://gitlab.example.com/root/awesome-app/-/tags/v0.11.1/binaries/linux-amd64",
                    "link_type": "other",
                }
            ],
        },
        "evidences": [
            {
                "sha": "760d6cdfb0879c3ffedec13af470e0f71cf52c6cde4d",
                "filepath": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/evidence.json",
                "collected_at": "2019-07-16T14:00:12.256Z",
            },
        ],
        "_links": {
            "closed_issues_url": "https://gitlab.example.com/root/awesome-app/-/issues?release_tag=v0.1&scope=all&state=closed",
            "closed_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=closed",
            "edit_url": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/edit",
            "merged_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=merged",
            "opened_issues_url": "https://gitlab.example.com/root/awesome-app/-/issues?release_tag=v0.1&scope=all&state=opened",
            "opened_merge_requests_url": "https://gitlab.example.com/root/awesome-app/-/merge_requests?release_tag=v0.1&scope=all&state=opened",
            "self": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Release"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_release_response_3():
    # Create a release
    example_data = {
        "tag_name": "v0.3",
        "description": "Super nice release",
        "name": "New release",
        "created_at": "2019-01-03T02:22:45.118Z",
        "released_at": "2019-01-03T02:22:45.118Z",
        "author": {
            "id": 1,
            "name": "Administrator",
            "username": "root",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
            "web_url": "https://gitlab.example.com/root",
        },
        "commit": {
            "id": "079e90101242458910cccd35eab0e211dfc359c0",
            "short_id": "079e9010",
            "title": "Update README.md",
            "created_at": "2019-01-03T01:55:38.000Z",
            "parent_ids": ["f8d3d94cbd347e924aa7b715845e439d00e80ca4"],
            "message": "Update README.md",
            "author_name": "Administrator",
            "author_email": "admin@example.com",
            "authored_date": "2019-01-03T01:55:38.000Z",
            "committer_name": "Administrator",
            "committer_email": "admin@example.com",
            "committed_date": "2019-01-03T01:55:38.000Z",
        },
        "milestones": [
            {
                "id": 51,
                "iid": 1,
                "project_id": 24,
                "title": "v1.0-rc",
                "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                "state": "closed",
                "created_at": "2019-07-12T19:45:44.256Z",
                "updated_at": "2019-07-12T19:45:44.256Z",
                "due_date": "2019-08-16",
                "start_date": "2019-07-30",
                "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/1",
                "issue_stats": {"total": 99, "closed": 76},
            },
            {
                "id": 52,
                "iid": 2,
                "project_id": 24,
                "title": "v1.0",
                "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                "state": "closed",
                "created_at": "2019-07-16T14:00:12.256Z",
                "updated_at": "2019-07-16T14:00:12.256Z",
                "due_date": "2019-08-16",
                "start_date": "2019-07-30",
                "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/2",
                "issue_stats": {"total": 24, "closed": 21},
            },
        ],
        "commit_path": "/root/awesome-app/commit/588440f66559714280628a4f9799f0c4eb880a4a",
        "tag_path": "/root/awesome-app/-/tags/v0.11.1",
        "evidence_sha": "760d6cdfb0879c3ffedec13af470e0f71cf52c6cde4d",
        "assets": {
            "count": 5,
            "sources": [
                {
                    "format": "zip",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.3/awesome-app-v0.3.zip",
                },
                {
                    "format": "tar.gz",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.3/awesome-app-v0.3.tar.gz",
                },
                {
                    "format": "tar.bz2",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.3/awesome-app-v0.3.tar.bz2",
                },
                {
                    "format": "tar",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.3/awesome-app-v0.3.tar",
                },
            ],
            "links": [
                {
                    "id": 3,
                    "name": "hoge",
                    "url": "https://gitlab.example.com/root/awesome-app/-/tags/v0.11.1/binaries/linux-amd64",
                    "link_type": "other",
                }
            ],
            "evidence_file_path": "https://gitlab.example.com/root/awesome-app/-/releases/v0.3/evidence.json",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Release"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_release_response_4():
    # Update a release
    example_data = {
        "tag_name": "v0.1",
        "description": "## CHANGELOG\r\n\r\n- Remove limit of 100 when searching repository code. !8671\r\n- Show error message when attempting to reopen an MR and there is an open MR for the same branch. !16447 (Akos Gyimesi)\r\n- Fix a bug where internal email pattern wasn't respected. !22516",
        "name": "new name",
        "created_at": "2019-01-03T01:55:18.203Z",
        "released_at": "2019-01-03T01:55:18.203Z",
        "author": {
            "id": 1,
            "name": "Administrator",
            "username": "root",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
            "web_url": "https://gitlab.example.com/root",
        },
        "commit": {
            "id": "f8d3d94cbd347e924aa7b715845e439d00e80ca4",
            "short_id": "f8d3d94c",
            "title": "Initial commit",
            "created_at": "2019-01-03T01:53:28.000Z",
            "parent_ids": [],
            "message": "Initial commit",
            "author_name": "Administrator",
            "author_email": "admin@example.com",
            "authored_date": "2019-01-03T01:53:28.000Z",
            "committer_name": "Administrator",
            "committer_email": "admin@example.com",
            "committed_date": "2019-01-03T01:53:28.000Z",
        },
        "milestones": [
            {
                "id": 53,
                "iid": 3,
                "project_id": 24,
                "title": "v1.2",
                "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
                "state": "active",
                "created_at": "2019-09-01T13:00:00.256Z",
                "updated_at": "2019-09-01T13:00:00.256Z",
                "due_date": "2019-09-20",
                "start_date": "2019-09-05",
                "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/3",
                "issue_stats": {"opened": 11, "closed": 78},
            }
        ],
        "commit_path": "/root/awesome-app/commit/588440f66559714280628a4f9799f0c4eb880a4a",
        "tag_path": "/root/awesome-app/-/tags/v0.11.1",
        "evidence_sha": "760d6cdfb0879c3ffedec13af470e0f71cf52c6cde4d",
        "assets": {
            "count": 4,
            "sources": [
                {
                    "format": "zip",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.zip",
                },
                {
                    "format": "tar.gz",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.gz",
                },
                {
                    "format": "tar.bz2",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.bz2",
                },
                {
                    "format": "tar",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar",
                },
            ],
            "links": [],
            "evidence_file_path": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/evidence.json",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Release"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_release_response_5():
    # Delete a Release
    example_data = {
        "tag_name": "v0.1",
        "description": "## CHANGELOG\r\n\r\n- Remove limit of 100 when searching repository code. !8671\r\n- Show error message when attempting to reopen an MR and there is an open MR for the same branch. !16447 (Akos Gyimesi)\r\n- Fix a bug where internal email pattern wasn't respected. !22516",
        "name": "new name",
        "created_at": "2019-01-03T01:55:18.203Z",
        "released_at": "2019-01-03T01:55:18.203Z",
        "author": {
            "id": 1,
            "name": "Administrator",
            "username": "root",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
            "web_url": "https://gitlab.example.com/root",
        },
        "commit": {
            "id": "f8d3d94cbd347e924aa7b715845e439d00e80ca4",
            "short_id": "f8d3d94c",
            "title": "Initial commit",
            "created_at": "2019-01-03T01:53:28.000Z",
            "parent_ids": [],
            "message": "Initial commit",
            "author_name": "Administrator",
            "author_email": "admin@example.com",
            "authored_date": "2019-01-03T01:53:28.000Z",
            "committer_name": "Administrator",
            "committer_email": "admin@example.com",
            "committed_date": "2019-01-03T01:53:28.000Z",
        },
        "commit_path": "/root/awesome-app/commit/588440f66559714280628a4f9799f0c4eb880a4a",
        "tag_path": "/root/awesome-app/-/tags/v0.11.1",
        "evidence_sha": "760d6cdfb0879c3ffedec13af470e0f71cf52c6cde4d",
        "assets": {
            "count": 4,
            "sources": [
                {
                    "format": "zip",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.zip",
                },
                {
                    "format": "tar.gz",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.gz",
                },
                {
                    "format": "tar.bz2",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar.bz2",
                },
                {
                    "format": "tar",
                    "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.1/awesome-app-v0.1.tar",
                },
            ],
            "links": [],
            "evidence_file_path": "https://gitlab.example.com/root/awesome-app/-/releases/v0.1/evidence.json",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Release"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_1():
    # List owned runners
    example_data = [
        {
            "active": True,
            "paused": False,
            "description": "test-1-20150125",
            "id": 6,
            "ip_address": "",
            "is_shared": False,
            "runner_type": "project_type",
            "name": None,
            "online": True,
            "status": "online",
        },
        {
            "active": True,
            "paused": False,
            "description": "test-2-20150125",
            "id": 8,
            "ip_address": "",
            "is_shared": False,
            "runner_type": "group_type",
            "name": None,
            "online": False,
            "status": "offline",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Runner"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_2():
    # List all runners
    example_data = [
        {
            "active": True,
            "paused": False,
            "description": "shared-runner-1",
            "id": 1,
            "ip_address": "",
            "is_shared": True,
            "runner_type": "instance_type",
            "name": None,
            "online": True,
            "status": "online",
        },
        {
            "active": True,
            "paused": False,
            "description": "shared-runner-2",
            "id": 3,
            "ip_address": "",
            "is_shared": True,
            "runner_type": "instance_type",
            "name": None,
            "online": False,
            "status": "offline",
        },
        {
            "active": True,
            "paused": False,
            "description": "test-1-20150125",
            "id": 6,
            "ip_address": "",
            "is_shared": False,
            "runner_type": "project_type",
            "name": None,
            "online": True,
            "status": "paused",
        },
        {
            "active": True,
            "paused": False,
            "description": "test-2-20150125",
            "id": 8,
            "ip_address": "",
            "is_shared": False,
            "runner_type": "group_type",
            "name": None,
            "online": False,
            "status": "offline",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Runner"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_3():
    # Get runner details
    example_data = {
        "active": True,
        "paused": False,
        "architecture": None,
        "description": "test-1-20150125",
        "id": 6,
        "ip_address": "",
        "is_shared": False,
        "runner_type": "project_type",
        "contacted_at": "2016-01-25T16:39:48.066Z",
        "maintenance_note": None,
        "name": None,
        "online": True,
        "status": "online",
        "platform": None,
        "projects": [
            {
                "id": 1,
                "name": "GitLab Community Edition",
                "name_with_namespace": "GitLab.org / GitLab Community Edition",
                "path": "gitlab-foss",
                "path_with_namespace": "gitlab-org/gitlab-foss",
            }
        ],
        "revision": None,
        "tag_list": ["ruby", "mysql"],
        "version": None,
        "access_level": "ref_protected",
        "maximum_timeout": 3600,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Runner"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_4():
    # List jobs processed by a runner
    example_data = [
        {
            "id": 2,
            "status": "running",
            "stage": "test",
            "name": "test",
            "ref": "main",
            "tag": False,
            "coverage": None,
            "created_at": "2017-11-16T08:50:29.000Z",
            "started_at": "2017-11-16T08:51:29.000Z",
            "finished_at": "2017-11-16T08:53:29.000Z",
            "duration": 120,
            "queued_duration": 2,
            "user": {
                "id": 1,
                "name": "John Doe2",
                "username": "user2",
                "state": "active",
                "avatar_url": "http://www.gravatar.com/avatar/c922747a93b40d1ea88262bf1aebee62?s=80&d=identicon",
                "web_url": "http://localhost/user2",
                "created_at": "2017-11-16T18:38:46.000Z",
                "bio": None,
                "location": None,
                "public_email": "",
                "skype": "",
                "linkedin": "",
                "twitter": "",
                "website_url": "",
                "organization": None,
            },
            "commit": {
                "id": "97de212e80737a608d939f648d959671fb0a0142",
                "short_id": "97de212e",
                "title": "Update configuration\r",
                "created_at": "2017-11-16T08:50:28.000Z",
                "parent_ids": [
                    "1b12f15a11fc6e62177bef08f47bc7b5ce50b141",
                    "498214de67004b1da3d820901307bed2a68a8ef6",
                ],
                "message": "See merge request !123",
                "author_name": "John Doe2",
                "author_email": "user2@example.org",
                "authored_date": "2017-11-16T08:50:27.000Z",
                "committer_name": "John Doe2",
                "committer_email": "user2@example.org",
                "committed_date": "2017-11-16T08:50:27.000Z",
            },
            "pipeline": {
                "id": 2,
                "sha": "97de212e80737a608d939f648d959671fb0a0142",
                "ref": "main",
                "status": "running",
            },
            "project": {
                "id": 1,
                "description": None,
                "name": "project1",
                "name_with_namespace": "John Doe2 / project1",
                "path": "project1",
                "path_with_namespace": "namespace1/project1",
                "created_at": "2017-11-16T18:38:46.620Z",
            },
        }
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Job"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_5():
    # List project’s runners
    example_data = [
        {
            "active": True,
            "paused": False,
            "description": "test-2-20150125",
            "id": 8,
            "ip_address": "",
            "is_shared": False,
            "runner_type": "project_type",
            "name": None,
            "online": False,
            "status": "offline",
        },
        {
            "active": True,
            "paused": False,
            "description": "development_runner",
            "id": 5,
            "ip_address": "",
            "is_shared": True,
            "runner_type": "instance_type",
            "name": None,
            "online": True,
            "status": "online",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "Runner"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_6():
    # Enable runner for project
    example_data = {
        "active": True,
        "description": "test-2016-02-01",
        "id": 9,
        "ip_address": "",
        "is_shared": False,
        "runner_type": "project_type",
        "name": None,
        "online": True,
        "status": "online",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Runner"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_7():
    # Create an instance runner
    example_data = {
        "id": 12345,
        "token": "6337ff461c94fd3fa32ba3b1ff4125",
        "token_expires_at": "2021-09-27T21:05:03.203Z",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Token"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_8():
    # Verify authentication for a registered runner
    example_data = {
        "id": 12345,
        "token": "glrt-6337ff461c94fd3fa32ba3b1ff4125",
        "token_expires_at": "2021-09-27T21:05:03.203Z",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Token"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_9():
    # Reset runner’s authentication token by using the runner ID
    example_data = {
        "token": "6337ff461c94fd3fa32ba3b1ff4125",
        "token_expires_at": "2021-09-27T21:05:03.203Z",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Token"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_response_10():
    # Reset runner’s authentication token by using the current token
    example_data = {
        "token": "6337ff461c94fd3fa32ba3b1ff4125",
        "token_expires_at": "2021-09-27T21:05:03.203Z",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Token"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_wiki_response_1():
    # List wiki pages
    example_data = [
        {
            "content": "Here is an instruction how to deploy this project.",
            "format": "markdown",
            "slug": "deploy",
            "title": "deploy",
            "encoding": "UTF-8",
        },
        {
            "content": "Our development process is described here.",
            "format": "markdown",
            "slug": "development",
            "title": "development",
            "encoding": "UTF-8",
        },
        {
            "content": "*  [Deploy](deploy)\n*  [Development](development)",
            "format": "markdown",
            "slug": "home",
            "title": "home",
            "encoding": "UTF-8",
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data[0].base_type == "WikiPage"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_wiki_response_2():
    # Get a wiki page
    example_data = {
        "content": "home page",
        "format": "markdown",
        "slug": "home",
        "title": "home",
        "encoding": "UTF-8",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "WikiPage"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_wiki_response_3():
    # Create a new wiki page
    example_data = {
        "content": "Hello world",
        "format": "markdown",
        "slug": "Hello",
        "title": "Hello",
        "encoding": "UTF-8",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "WikiPage"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_wiki_response_4():
    # Upload an attachment to the wiki repository
    example_data = {
        "file_name": "dk.png",
        "file_path": "uploads/6a061c4cf9f1c28cb22c384b4b8d4e3c/dk.png",
        "branch": "main",
        "link": {
            "url": "uploads/6a061c4cf9f1c28cb22c384b4b8d4e3c/dk.png",
            "markdown": "![dk](uploads/6a061c4cf9f1c28cb22c384b4b8d4e3c/dk.png)",
        },
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "WikiAttachment"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_wiki_response_5():
    # List wiki pages
    example_data = [
        {
            "content": "Here is an instruction how to deploy this project.",
            "format": "markdown",
            "slug": "deploy",
            "title": "deploy",
            "encoding": "UTF-8",
        },
        {
            "content": "Our development process is described here.",
            "format": "markdown",
            "slug": "development",
            "title": "development",
            "encoding": "UTF-8",
        },
        {
            "content": "*  [Deploy](deploy)\n*  [Development](development)",
            "format": "markdown",
            "slug": "home",
            "title": "home",
            "encoding": "UTF-8",
        },
    ]
    response = Response(
        data=example_data, status_code=200, headers={}, json_output=example_data
    )
    assert response.data[0].base_type == "WikiPage"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_contributor_response_1():
    example_data = [
        {
            "name": "Example User",
            "email": "example@example.com",
            "commits": 117,
            "additions": 0,
            "deletions": 0,
        },
        {
            "name": "Sample User",
            "email": "sample@example.com",
            "commits": 33,
            "additions": 0,
            "deletions": 0,
        },
    ]
    response = Response(
        data=example_data, status_code=200, headers={}, json_output=example_data
    )
    assert response.data[0].base_type == "Contributor"


if __name__ == "__main__":
    test_branch_model()
    test_commit_model()
    test_merge_request_model()
    test_merge_request_rule_model()
    test_pipeline_model()
    test_project_model()
    test_protected_branches_model()
    test_release_model()
    test_runner_model()
    test_user_model()
    test_wiki_model()
    test_project_response_1()
    test_project_response_2()
    test_project_response_3()
    test_user_response_1()
    test_user_response_2()
    test_branch_response_1()
    test_branch_response_2()
    test_branch_response_3()
    test_branch_response_4()
    test_commit_response_1()
    test_commit_response_2()
    test_commit_response_3()
    test_commit_response_4()
    test_commit_response_5()
    test_commit_response_6()
    test_commit_response_7()
    test_commit_response_8()
    test_commit_response_9()
    test_commit_response_10()
    test_commit_response_11()
    test_commit_response_12()
    test_commit_response_13()
    test_commit_response_14()
    test_commit_response_15()
    test_commit_response_16()
    test_commit_response_17()
    test_commit_response_18()
    test_commit_response_19()
    test_deploy_token_response_1()
    test_deploy_token_response_2()
    test_deploy_token_response_3()
    test_deploy_token_response_4()
    test_deploy_token_response_5()
    test_merge_request_response_1()
    test_merge_request_response_2()
    test_merge_request_response_3()
    test_merge_request_response_4()
    test_merge_request_response_5()
    test_merge_request_response_6()
    test_merge_request_response_7()
    test_merge_request_response_8()
    test_merge_request_response_9()
    test_merge_request_response_10()
    test_merge_request_response_11()
    test_merge_request_response_12()
    test_merge_request_response_13()
    test_merge_request_response_14()
    test_merge_request_response_15()
    test_merge_request_response_16()
    test_merge_request_response_17()
    test_merge_request_response_18()
    test_merge_request_response_19()
    test_merge_request_response_20()
    test_merge_request_response_21()
    test_issues_response_1()
    test_issues_response_2()
    test_issues_response_3()
    test_issues_response_4()
    test_issues_response_5()
    test_issues_response_6()
    test_issues_response_7()
    test_issues_response_8()
    test_issues_response_9()
    test_issues_response_10()
    test_issues_response_11()
    test_issues_response_12()
    test_issues_response_13()
    test_issues_response_14()
    test_issues_response_15()
    test_group_response_1()
    test_group_response_2()
    test_group_response_3()
    test_group_response_4()
    test_group_response_5()
    test_group_response_6()
    test_group_response_7()
    test_group_response_8()
    test_group_response_9()
    test_group_response_10()
    test_group_response_11()
    test_group_response_12()
    test_group_response_13()
    test_group_response_14()
    test_group_response_15()
    test_group_response_16()
    test_group_response_17()
    test_group_response_18()
    test_group_response_19()
    test_group_response_20()
    test_group_response_21()
    test_group_response_22()
    test_jobs_response_1()
    test_jobs_response_2()
    test_jobs_response_3()
    test_jobs_response_4()
    test_jobs_response_5()
    test_jobs_response_6()
    test_jobs_response_7()
    test_jobs_response_8()
    test_jobs_response_9()
    test_member_response_1()
    test_member_response_2()
    test_member_response_3()
    test_member_response_4()
    test_member_response_5()
    test_member_response_6()
    test_member_response_7()
    test_member_response_8()
    test_approval_rule_response_1()
    test_approval_rule_response_2()
    test_approval_rule_response_3()
    test_approval_rule_response_4()
    test_approval_rule_response_5()
    test_approval_rule_response_6()
    test_approval_rule_response_7()
    test_approval_rule_response_8()
    test_approval_rule_response_9()
    test_approval_rule_response_10()
    test_approval_rule_response_11()
    test_approval_rule_response_12()
    test_approval_rule_response_13()
    test_approval_rule_response_14()
    test_approval_rule_response_15()
    test_protected_branch_response_1()
    test_protected_branch_response_2()
    test_protected_branch_response_3()
    test_protected_branch_response_4()
    test_protected_branch_response_5()
    test_protected_branch_response_6()
    test_protected_branch_response_7()
    test_protected_branch_response_8()
    test_protected_branch_response_9()
    test_protected_branch_response_10()
    test_protected_branch_response_11()
    test_protected_branch_response_12()
    test_protected_branch_response_13()
    test_protected_branch_response_14()
    test_protected_branch_response_15()
    test_package_response_1()
    test_package_response_2()
    test_package_response_3()
    test_package_response_4()
    test_package_response_5()
    test_release_response_1()
    test_release_response_2()
    test_release_response_3()
    test_release_response_4()
    test_release_response_5()
    test_runner_response_1()
    test_runner_response_2()
    test_runner_response_3()
    test_runner_response_4()
    test_runner_response_5()
    test_runner_response_6()
    test_runner_response_7()
    test_runner_response_8()
    test_runner_response_9()
    test_runner_response_10()
    test_wiki_response_1()
    test_wiki_response_2()
    test_wiki_response_3()
    test_wiki_response_4()
    test_wiki_response_5()
    test_contributor_response_1()
