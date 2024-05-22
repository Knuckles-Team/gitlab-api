import os
import sys

import pytest
from conftest import reason

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    import gitlab_api
    from gitlab_api.gitlab_models import (
        BranchModel,
        CommitModel,
        DeployTokenModel,
        GroupModel,
        JobModel,
        MembersModel,
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
    assert branch.api_parameters == "?branch=test_branch&ref=main"


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
    assert pipeline.api_parameters == "?per_page=100&ref=test"


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
    assert project.api_parameters == "?group_id=1234"


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
    assert release.api_parameters == "?simple=true"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_runner_model():
    project_id = 5679
    runner = RunnerModel(project_id=project_id, active=True, status="Online")
    assert project_id == runner.project_id
    assert runner.api_parameters == "?status=online"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_user_model():
    username = "test_user"
    user = UserModel(username=username, active=True)
    assert user.username == username
    assert user.active == True
    assert user.api_parameters == "?username=test_user&active=true"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_wiki_model():
    project_id = 5679
    wiki = WikiModel(project_id=project_id, with_content=True)
    assert project_id == wiki.project_id
    assert wiki.api_parameters == "?with_content=true"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_project_response():
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
    assert response.data.base_type == "Projects"

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
def test_user_response():
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
    assert response.data.base_type == "Users"
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
def test_branch_response():
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
    assert response.data.base_type == "Branches"

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

    example_data = {
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
    assert response.data.base_type == "Branches"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_commit_response():
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
    assert response.data.base_type == "Commits"

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

    example_data = {"count": 632}

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"

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

    example_data = {
        "message": "Sorry, we cannot revert this commit automatically. This commit may already have been reverted, or a more recent commit may have updated some of its content.",
        "error_code": "conflict",
    }

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"

    example_data = {"dry_run": "success"}

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Commit"

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
    assert response.data.base_type == "Diffs"

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
    assert response.data.base_type == "Comments"

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
    assert response.data.base_type == "Commits"

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
    assert response.data.base_type == "Commits"

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
    assert response.data.base_type == "MergeRequests"

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

    example_data = {"message": "404 GPG Signature Not Found"}

    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "CommitSignature"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_deploy_token_response():
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
    assert response.data.base_type == "DeployTokens"

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
    assert response.data.base_type == "DeployTokens"

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
    assert response.data.base_type == "DeployTokens"

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
def test_merge_request_response():
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
    assert response.data.base_type == "MergeRequests"

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
    assert response.data.base_type == "MergeRequests"

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
    assert response.data.base_type == "MergeRequests"

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
    assert response.data.base_type == "Users"

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
    assert response.data.base_type == "MergeRequests"

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
    assert response.data.base_type == "Commits"

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
        "description": "Qui voluptatibus placeat ipsa alias quasi. Deleniti rem ut sint. Optio velit qui distinctio.",
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
                "diff": "@@ -1 +1 @@\ -1.9.7\ +1.9.8",
                "new_file": False,
                "renamed_file": False,
                "deleted_file": False,
            }
        ],
        "overflow": False,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"

    # Diff
    example_data = [
        {
            "old_path": "README",
            "new_path": "README",
            "a_mode": "100644",
            "b_mode": "100644",
            "diff": "@@ -1 +1 @@\ -Title\ +README",
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
            "diff": "@@\ -1.9.7\ +1.9.8",
            "new_file": False,
            "renamed_file": False,
            "deleted_file": False,
            "generated_file": False,
        },
    ]
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "Diffs"

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
    assert response.data.base_type == "Pipelines"

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

    example_data = {"rebase_in_progress": True}
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"

    example_data = {"rebase_in_progress": True, "merge_error": None}
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"

    example_data = {"rebase_in_progress": False, "merge_error": None}
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"

    example_data = {
        "rebase_in_progress": False,
        "merge_error": "Rebase failed. Please rebase locally",
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "MergeRequest"

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
    assert response.data.base_type == "Issues"

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
    assert response.data.base_type == "Issues"

    # Time tracking for Merge Request
    example_data = {
        "human_time_estimate": "2h",
        "human_total_time_spent": "1h",
        "time_estimate": 7200,
        "total_time_spent": 3600,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TimeStats"

    example_data = {
        "human_time_estimate": None,
        "human_total_time_spent": None,
        "time_estimate": 0,
        "total_time_spent": 0,
    }
    response = Response(data=example_data, status_code=200, json_output=example_data)
    assert response.data.base_type == "TimeStats"

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
    assert response.data.base_type == "Diffs"


# @pytest.mark.skipif(
#     sys.platform in ["darwin"] or skip,
#     reason=reason,
# )
# def test_issues_response():
#     example_data = [
#         {
#             "state": "opened",
#             "description": "Ratione dolores corrupti mollitia soluta quia.",
#             "author": {
#                 "state": "active",
#                 "id": 18,
#                 "web_url": "https://gitlab.example.com/eileen.lowe",
#                 "name": "Alexandra Bashirian",
#                 "avatar_url": None,
#                 "username": "eileen.lowe"
#             },
#             "milestone": {
#                 "project_id": 1,
#                 "description": "Ducimus nam enim ex consequatur cumque ratione.",
#                 "state": "closed",
#                 "due_date": None,
#                 "iid": 2,
#                 "created_at": "2016-01-04T15:31:39.996Z",
#                 "title": "v4.0",
#                 "id": 17,
#                 "updated_at": "2016-01-04T15:31:39.996Z"
#             },
#             "project_id": 1,
#             "assignees": [{
#                 "state": "active",
#                 "id": 1,
#                 "name": "Administrator",
#                 "web_url": "https://gitlab.example.com/root",
#                 "avatar_url": None,
#                 "username": "root"
#             }],
#             "assignee": {
#                 "state": "active",
#                 "id": 1,
#                 "name": "Administrator",
#                 "web_url": "https://gitlab.example.com/root",
#                 "avatar_url": None,
#                 "username": "root"
#             },
#             "type": "ISSUE",
#             "updated_at": "2016-01-04T15:31:51.081Z",
#             "closed_at": None,
#             "closed_by": None,
#             "id": 76,
#             "title": "Consequatur vero maxime deserunt laboriosam est voluptas dolorem.",
#             "created_at": "2016-01-04T15:31:51.081Z",
#             "moved_to_id": None,
#             "iid": 6,
#             "labels": ["foo", "bar"],
#             "upvotes": 4,
#             "downvotes": 0,
#             "merge_requests_count": 0,
#             "user_notes_count": 1,
#             "due_date": "2016-07-22",
#             "imported": False,
#             "imported_from": "none",
#             "web_url": "http://gitlab.example.com/my-group/my-project/issues/6",
#             "references": {
#                 "short": "#6",
#                 "relative": "my-group/my-project#6",
#                 "full": "my-group/my-project#6"
#             },
#             "time_stats": {
#                 "time_estimate": 0,
#                 "total_time_spent": 0,
#                 "human_time_estimate": None,
#                 "human_total_time_spent": None
#             },
#             "has_tasks": True,
#             "task_status": "10 of 15 tasks completed",
#             "confidential": False,
#             "discussion_locked": False,
#             "issue_type": "issue",
#             "severity": "UNKNOWN",
#             "_links": {
#                 "self": "http://gitlab.example.com/api/v4/projects/1/issues/76",
#                 "notes": "http://gitlab.example.com/api/v4/projects/1/issues/76/notes",
#                 "award_emoji": "http://gitlab.example.com/api/v4/projects/1/issues/76/award_emoji",
#                 "project": "http://gitlab.example.com/api/v4/projects/1",
#                 "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
#             },
#             "task_completion_status": {
#                 "count": 0,
#                 "completed_count": 0
#             }
#         }
#     ]
#
#     example_data = [
#         {
#             "state": "opened",
#             "description": "Ratione dolores corrupti mollitia soluta quia.",
#             "weight": None,
#
#         }
#     ]
#
#     example_data = {
#         "project_id": 4,
#         "description": "Omnis vero earum sunt corporis dolor et placeat.",
#         "epic_iid": 5,
#         "epic": {
#             "id": 42,
#             "iid": 5,
#             "title": "My epic epic",
#             "url": "/groups/h5bp/-/epics/5",
#             "group_id": 8
#         },
#
#     }
#
#     example_data = {
#         "iteration": {
#             "id": 90,
#             "iid": 4,
#             "sequence": 2,
#             "group_id": 162,
#             "title": None,
#             "description": None,
#             "state": 2,
#             "created_at": "2022-03-14T05:21:11.929Z",
#             "updated_at": "2022-03-14T05:21:11.929Z",
#             "start_date": "2022-03-08",
#             "due_date": "2022-03-14",
#             "web_url": "https://gitlab.com/groups/my-group/-/iterations/90"
#         }
#
#     }
#
#     example_data = [
#         {
#             "state": "opened",
#             "description": "Ratione dolores corrupti mollitia soluta quia.",
#             "health_status": "on_track",
#
#         }
#     ]
#
#     example_data = [
#         {
#             "project_id": 4,
#             "milestone": {
#                 "due_date": None,
#                 "project_id": 4,
#                 "state": "closed",
#                 "description": "Rerum est voluptatem provident consequuntur molestias similique ipsum dolor.",
#                 "iid": 3,
#                 "id": 11,
#                 "title": "v3.0",
#                 "created_at": "2016-01-04T15:31:39.788Z",
#                 "updated_at": "2016-01-04T15:31:39.788Z"
#             },
#             "author": {
#                 "state": "active",
#                 "web_url": "https://gitlab.example.com/root",
#                 "avatar_url": None,
#                 "username": "root",
#                 "id": 1,
#                 "name": "Administrator"
#             },
#             "description": "Omnis vero earum sunt corporis dolor et placeat.",
#             "state": "closed",
#             "iid": 1,
#             "assignees": [{
#                 "avatar_url": None,
#                 "web_url": "https://gitlab.example.com/lennie",
#                 "state": "active",
#                 "username": "lennie",
#                 "id": 9,
#                 "name": "Dr. Luella Kovacek"
#             }],
#             "assignee": {
#                 "avatar_url": None,
#                 "web_url": "https://gitlab.example.com/lennie",
#                 "state": "active",
#                 "username": "lennie",
#                 "id": 9,
#                 "name": "Dr. Luella Kovacek"
#             },
#             "type": "ISSUE",
#             "labels": ["foo", "bar"],
#             "upvotes": 4,
#             "downvotes": 0,
#             "merge_requests_count": 0,
#             "id": 41,
#             "title": "Ut commodi ullam eos dolores perferendis nihil sunt.",
#             "updated_at": "2016-01-04T15:31:46.176Z",
#             "created_at": "2016-01-04T15:31:46.176Z",
#             "closed_at": None,
#             "closed_by": None,
#             "user_notes_count": 1,
#             "due_date": None,
#             "imported": False,
#             "imported_from": "none",
#             "web_url": "http://gitlab.example.com/my-group/my-project/issues/1",
#             "references": {
#                 "short": "#1",
#                 "relative": "my-project#1",
#                 "full": "my-group/my-project#1"
#             },
#             "time_stats": {
#                 "time_estimate": 0,
#                 "total_time_spent": 0,
#                 "human_time_estimate": None,
#                 "human_total_time_spent": None
#             },
#             "has_tasks": True,
#             "task_status": "10 of 15 tasks completed",
#             "confidential": False,
#             "discussion_locked": False,
#             "issue_type": "issue",
#             "severity": "UNKNOWN",
#             "_links": {
#                 "self": "http://gitlab.example.com/api/v4/projects/4/issues/41",
#                 "notes": "http://gitlab.example.com/api/v4/projects/4/issues/41/notes",
#                 "award_emoji": "http://gitlab.example.com/api/v4/projects/4/issues/41/award_emoji",
#                 "project": "http://gitlab.example.com/api/v4/projects/4",
#                 "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
#             },
#             "task_completion_status": {
#                 "count": 0,
#                 "completed_count": 0
#             },
#             "weight": None,
#             "epic_iid": 5,
#             "epic": {
#                 "id": 42,
#                 "iid": 5,
#                 "title": "My epic epic",
#                 "url": "/groups/h5bp/-/epics/5",
#                 "group_id": 8
#             },
#             "health_status": "at_risk",
#         }
#     ]
#
#     example_data = [
#         {
#             "project_id": 4,
#             "milestone": {
#                 "due_date": None,
#                 "project_id": 4,
#                 "state": "closed",
#                 "description": "Rerum est voluptatem provident consequuntur molestias similique ipsum dolor.",
#                 "iid": 3,
#                 "id": 11,
#                 "title": "v3.0",
#                 "created_at": "2016-01-04T15:31:39.788Z",
#                 "updated_at": "2016-01-04T15:31:39.788Z"
#             },
#             "author": {
#                 "state": "active",
#                 "web_url": "https://gitlab.example.com/root",
#                 "avatar_url": None,
#                 "username": "root",
#                 "id": 1,
#                 "name": "Administrator"
#             },
#             "description": "Omnis vero earum sunt corporis dolor et placeat.",
#             "state": "closed",
#             "iid": 1,
#             "assignees": [{
#                 "avatar_url": None,
#                 "web_url": "https://gitlab.example.com/lennie",
#                 "state": "active",
#                 "username": "lennie",
#                 "id": 9,
#                 "name": "Dr. Luella Kovacek"
#             }],
#             "assignee": {
#                 "avatar_url": None,
#                 "web_url": "https://gitlab.example.com/lennie",
#                 "state": "active",
#                 "username": "lennie",
#                 "id": 9,
#                 "name": "Dr. Luella Kovacek"
#             },
#             "type": "ISSUE",
#             "labels": ["foo", "bar"],
#             "upvotes": 4,
#             "downvotes": 0,
#             "merge_requests_count": 0,
#             "id": 41,
#             "title": "Ut commodi ullam eos dolores perferendis nihil sunt.",
#             "updated_at": "2016-01-04T15:31:46.176Z",
#             "created_at": "2016-01-04T15:31:46.176Z",
#             "closed_at": "2016-01-05T15:31:46.176Z",
#             "closed_by": {
#                 "state": "active",
#                 "web_url": "https://gitlab.example.com/root",
#                 "avatar_url": None,
#                 "username": "root",
#                 "id": 1,
#                 "name": "Administrator"
#             },
#             "user_notes_count": 1,
#             "due_date": "2016-07-22",
#             "imported": False,
#             "imported_from": "none",
#             "web_url": "http://gitlab.example.com/my-group/my-project/issues/1",
#             "references": {
#                 "short": "#1",
#                 "relative": "#1",
#                 "full": "my-group/my-project#1"
#             },
#             "time_stats": {
#                 "time_estimate": 0,
#                 "total_time_spent": 0,
#                 "human_time_estimate": None,
#                 "human_total_time_spent": None
#             },
#             "has_tasks": True,
#             "task_status": "10 of 15 tasks completed",
#             "confidential": False,
#             "discussion_locked": False,
#             "issue_type": "issue",
#             "severity": "UNKNOWN",
#             "_links": {
#                 "self": "http://gitlab.example.com/api/v4/projects/4/issues/41",
#                 "notes": "http://gitlab.example.com/api/v4/projects/4/issues/41/notes",
#                 "award_emoji": "http://gitlab.example.com/api/v4/projects/4/issues/41/award_emoji",
#                 "project": "http://gitlab.example.com/api/v4/projects/4",
#                 "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
#             },
#             "task_completion_status": {
#                 "count": 0,
#                 "completed_count": 0
#             },
#             "weight": None,
#             "epic_iid": 5,
#             "epic": {
#                 "id": 42,
#                 "iid": 5,
#                 "title": "My epic epic",
#                 "url": "/groups/h5bp/-/epics/5",
#                 "group_id": 8
#             },
#             "health_status": "at_risk",
#         }
#     ]
#
#     example_data = {
#         "id": 1,
#         "milestone": {
#             "due_date": None,
#             "project_id": 4,
#             "state": "closed",
#             "description": "Rerum est voluptatem provident consequuntur molestias similique ipsum dolor.",
#             "iid": 3,
#             "id": 11,
#             "title": "v3.0",
#             "created_at": "2016-01-04T15:31:39.788Z",
#             "updated_at": "2016-01-04T15:31:39.788Z",
#             "closed_at": "2016-01-05T15:31:46.176Z"
#         },
#         "author": {
#             "state": "active",
#             "web_url": "https://gitlab.example.com/root",
#             "avatar_url": None,
#             "username": "root",
#             "id": 1,
#             "name": "Administrator"
#         },
#         "description": "Omnis vero earum sunt corporis dolor et placeat.",
#         "state": "closed",
#         "iid": 1,
#         "assignees": [
#             {
#                 "avatar_url": None,
#                 "web_url": "https://gitlab.example.com/lennie",
#                 "state": "active",
#                 "username": "lennie",
#                 "id": 9,
#                 "name": "Dr. Luella Kovacek"
#             }
#         ],
#         "assignee": {
#             "avatar_url": None,
#             "web_url": "https://gitlab.example.com/lennie",
#             "state": "active",
#             "username": "lennie",
#             "id": 9,
#             "name": "Dr. Luella Kovacek"
#         },
#         "type": "ISSUE",
#         "labels": [],
#         "upvotes": 4,
#         "downvotes": 0,
#         "merge_requests_count": 0,
#         "title": "Ut commodi ullam eos dolores perferendis nihil sunt.",
#         "updated_at": "2016-01-04T15:31:46.176Z",
#         "created_at": "2016-01-04T15:31:46.176Z",
#         "closed_at": None,
#         "closed_by": None,
#         "subscribed": False,
#         "user_notes_count": 1,
#         "due_date": None,
#         "imported": False,
#         "imported_from": "none",
#         "web_url": "http://example.com/my-group/my-project/issues/1",
#         "references": {
#             "short": "#1",
#             "relative": "#1",
#             "full": "my-group/my-project#1"
#         },
#         "time_stats": {
#             "time_estimate": 0,
#             "total_time_spent": 0,
#             "human_time_estimate": None,
#             "human_total_time_spent": None
#         },
#         "confidential": False,
#         "discussion_locked": False,
#         "issue_type": "issue",
#         "severity": "UNKNOWN",
#         "task_completion_status": {
#             "count": 0,
#             "completed_count": 0
#         },
#         "weight": None,
#         "has_tasks": False,
#         "_links": {
#             "self": "http://gitlab.example:3000/api/v4/projects/1/issues/1",
#             "notes": "http://gitlab.example:3000/api/v4/projects/1/issues/1/notes",
#             "award_emoji": "http://gitlab.example:3000/api/v4/projects/1/issues/1/award_emoji",
#             "project": "http://gitlab.example:3000/api/v4/projects/1",
#             "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
#         },
#         "moved_to_id": None,
#         "service_desk_reply_to": "service.desk@gitlab.com"
#     }
#
#     example_data = {
#         "project_id": 4,
#         "id": 84,
#         "created_at": "2016-01-07T12:44:33.959Z",
#         "iid": 14,
#         "title": "Issues with auth",
#         "state": "opened",
#         "assignees": [],
#         "assignee": None,
#         "type": "ISSUE",
#         "labels": [
#             "bug"
#         ],
#         "upvotes": 4,
#         "downvotes": 0,
#         "merge_requests_count": 0,
#         "author": {
#             "name": "Alexandra Bashirian",
#             "avatar_url": None,
#             "state": "active",
#             "web_url": "https://gitlab.example.com/eileen.lowe",
#             "id": 18,
#             "username": "eileen.lowe"
#         },
#         "description": None,
#         "updated_at": "2016-01-07T12:44:33.959Z",
#         "closed_at": None,
#         "closed_by": None,
#         "milestone": None,
#         "subscribed": True,
#         "user_notes_count": 0,
#         "due_date": None,
#         "web_url": "http://gitlab.example.com/my-group/my-project/issues/14",
#         "references": {
#             "short": "#14",
#             "relative": "#14",
#             "full": "my-group/my-project#14"
#         },
#         "time_stats": {
#             "time_estimate": 0,
#             "total_time_spent": 0,
#             "human_time_estimate": None,
#             "human_total_time_spent": None
#         },
#         "confidential": False,
#         "discussion_locked": False,
#         "issue_type": "issue",
#         "severity": "UNKNOWN",
#         "_links": {
#             "self": "http://gitlab.example.com/api/v4/projects/1/issues/2",
#             "notes": "http://gitlab.example.com/api/v4/projects/1/issues/2/notes",
#             "award_emoji": "http://gitlab.example.com/api/v4/projects/1/issues/2/award_emoji",
#             "project": "http://gitlab.example.com/api/v4/projects/1",
#             "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
#         },
#         "task_completion_status": {
#             "count": 0,
#             "completed_count": 0
#         }
#     }
#
#     example_data = {
#         "id": 92,
#         "iid": 11,
#         "project_id": 5,
#         "title": "Sit voluptas tempora quisquam aut doloribus et.",
#         "description": "Repellat voluptas quibusdam voluptatem exercitationem.",
#         "state": "opened",
#         "created_at": "2016-04-05T21:41:45.652Z",
#         "updated_at": "2016-04-07T12:20:17.596Z",
#         "closed_at": None,
#         "closed_by": None,
#         "labels": [],
#         "upvotes": 4,
#         "downvotes": 0,
#         "merge_requests_count": 0,
#         "milestone": None,
#         "assignees": [{
#             "name": "Miss Monserrate Beier",
#             "username": "axel.block",
#             "id": 12,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/axel.block"
#         }],
#         "assignee": {
#             "name": "Miss Monserrate Beier",
#             "username": "axel.block",
#             "id": 12,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/axel.block"
#         },
#         "type": "ISSUE",
#         "author": {
#             "name": "Kris Steuber",
#             "username": "solon.cremin",
#             "id": 10,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/7a190fecbaa68212a4b68aeb6e3acd10?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/solon.cremin"
#         },
#         "due_date": None,
#         "imported": False,
#         "imported_from": "none",
#         "web_url": "http://gitlab.example.com/my-group/my-project/issues/11",
#         "references": {
#             "short": "#11",
#             "relative": "#11",
#             "full": "my-group/my-project#11"
#         },
#         "time_stats": {
#             "time_estimate": 0,
#             "total_time_spent": 0,
#             "human_time_estimate": None,
#             "human_total_time_spent": None
#         },
#         "confidential": False,
#         "discussion_locked": False,
#         "issue_type": "issue",
#         "severity": "UNKNOWN",
#         "_links": {
#             "self": "http://gitlab.example.com/api/v4/projects/1/issues/2",
#             "notes": "http://gitlab.example.com/api/v4/projects/1/issues/2/notes",
#             "award_emoji": "http://gitlab.example.com/api/v4/projects/1/issues/2/award_emoji",
#             "project": "http://gitlab.example.com/api/v4/projects/1",
#             "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
#         },
#         "task_completion_status": {
#             "count": 0,
#             "completed_count": 0
#         }
#     }
#
#     example_data = {
#         "id": 290,
#         "iid": 1,
#         "project_id": 143,
#         "title": "foo",
#         "description": "closed",
#         "state": "opened",
#         "created_at": "2021-09-14T22:24:11.696Z",
#         "updated_at": "2021-09-14T22:24:11.696Z",
#         "closed_at": None,
#         "closed_by": None,
#         "labels": [
#
#         ],
#         "milestone": None,
#         "assignees": [
#             {
#                 "id": 179,
#                 "name": "John Doe2",
#                 "username": "john",
#                 "state": "active",
#                 "avatar_url": "https://www.gravatar.com/avatar/10fc7f102be8de7657fb4d80898bbfe3?s=80\u0026d=identicon",
#                 "web_url": "https://gitlab.example.com/john"
#             }
#         ],
#         "author": {
#             "id": 179,
#             "name": "John Doe2",
#             "username": "john",
#             "state": "active",
#             "avatar_url": "https://www.gravatar.com/avatar/10fc7f102be8de7657fb4d80898bbfe3?s=80\u0026d=identicon",
#             "web_url": "https://gitlab.example.com/john"
#         },
#         "type": "ISSUE",
#         "assignee": {
#             "id": 179,
#             "name": "John Doe2",
#             "username": "john",
#             "state": "active",
#             "avatar_url": "https://www.gravatar.com/avatar/10fc7f102be8de7657fb4d80898bbfe3?s=80\u0026d=identicon",
#             "web_url": "https://gitlab.example.com/john"
#         },
#         "user_notes_count": 1,
#         "merge_requests_count": 0,
#         "upvotes": 0,
#         "downvotes": 0,
#         "due_date": None,
#         "imported": False,
#         "imported_from": "none",
#         "confidential": False,
#         "discussion_locked": None,
#         "issue_type": "issue",
#         "severity": "UNKNOWN",
#         "web_url": "https://gitlab.example.com/namespace1/project2/-/issues/1",
#         "time_stats": {
#             "time_estimate": 0,
#             "total_time_spent": 0,
#             "human_time_estimate": None,
#             "human_total_time_spent": None
#         },
#         "task_completion_status": {
#             "count": 0,
#             "completed_count": 0
#         },
#         "blocking_issues_count": 0,
#         "has_tasks": False,
#         "_links": {
#             "self": "https://gitlab.example.com/api/v4/projects/143/issues/1",
#             "notes": "https://gitlab.example.com/api/v4/projects/143/issues/1/notes",
#             "award_emoji": "https://gitlab.example.com/api/v4/projects/143/issues/1/award_emoji",
#             "project": "https://gitlab.example.com/api/v4/projects/143",
#             "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
#         },
#         "references": {
#             "short": "#1",
#             "relative": "#1",
#             "full": "namespace1/project2#1"
#         },
#         "subscribed": True,
#         "moved_to_id": None,
#         "service_desk_reply_to": None
#     }
#
#     example_data = {
#         "id": 92,
#         "iid": 11,
#         "project_id": 5,
#         "title": "Sit voluptas tempora quisquam aut doloribus et.",
#         "description": "Repellat voluptas quibusdam voluptatem exercitationem.",
#         "state": "opened",
#         "created_at": "2016-04-05T21:41:45.652Z",
#         "updated_at": "2016-04-07T12:20:17.596Z",
#         "closed_at": None,
#         "closed_by": None,
#         "labels": [],
#         "upvotes": 4,
#         "downvotes": 0,
#         "merge_requests_count": 0,
#         "milestone": None,
#         "assignees": [{
#             "name": "Miss Monserrate Beier",
#             "username": "axel.block",
#             "id": 12,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/axel.block"
#         }],
#         "assignee": {
#             "name": "Miss Monserrate Beier",
#             "username": "axel.block",
#             "id": 12,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/axel.block"
#         },
#         "type": "ISSUE",
#         "author": {
#             "name": "Kris Steuber",
#             "username": "solon.cremin",
#             "id": 10,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/7a190fecbaa68212a4b68aeb6e3acd10?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/solon.cremin"
#         },
#         "due_date": None,
#         "web_url": "http://gitlab.example.com/my-group/my-project/issues/11",
#         "references": {
#             "short": "#11",
#             "relative": "#11",
#             "full": "my-group/my-project#11"
#         },
#         "time_stats": {
#             "time_estimate": 0,
#             "total_time_spent": 0,
#             "human_time_estimate": None,
#             "human_total_time_spent": None
#         },
#         "confidential": False,
#         "discussion_locked": False,
#         "issue_type": "issue",
#         "severity": "UNKNOWN",
#         "_links": {
#             "self": "http://gitlab.example.com/api/v4/projects/1/issues/2",
#             "notes": "http://gitlab.example.com/api/v4/projects/1/issues/2/notes",
#             "award_emoji": "http://gitlab.example.com/api/v4/projects/1/issues/2/award_emoji",
#             "project": "http://gitlab.example.com/api/v4/projects/1",
#             "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
#         },
#         "task_completion_status": {
#             "count": 0,
#             "completed_count": 0
#         }
#     }
#
#     example_data = {
#         "id": 93,
#         "iid": 12,
#         "project_id": 5,
#         "title": "Incidunt et rerum ea expedita iure quibusdam.",
#         "description": "Et cumque architecto sed aut ipsam.",
#         "state": "opened",
#         "created_at": "2016-04-05T21:41:45.217Z",
#         "updated_at": "2016-04-07T13:02:37.905Z",
#         "labels": [],
#         "upvotes": 4,
#         "downvotes": 0,
#         "merge_requests_count": 0,
#         "milestone": None,
#         "assignee": {
#             "name": "Edwardo Grady",
#             "username": "keyon",
#             "id": 21,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/3e6f06a86cf27fa8b56f3f74f7615987?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/keyon"
#         },
#         "type": "ISSUE",
#         "closed_at": None,
#         "closed_by": None,
#         "author": {
#             "name": "Vivian Hermann",
#             "username": "orville",
#             "id": 11,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/5224fd70153710e92fb8bcf79ac29d67?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/orville"
#         },
#         "subscribed": False,
#         "due_date": None,
#         "web_url": "http://gitlab.example.com/my-group/my-project/issues/12",
#         "references": {
#             "short": "#12",
#             "relative": "#12",
#             "full": "my-group/my-project#12"
#         },
#         "confidential": False,
#         "discussion_locked": False,
#         "issue_type": "issue",
#         "severity": "UNKNOWN",
#         "task_completion_status": {
#             "count": 0,
#             "completed_count": 0
#         }
#     }
#
#     example_data = {
#         "id": 112,
#         "project": {
#             "id": 5,
#             "name": "GitLab CI/CD",
#             "name_with_namespace": "GitLab Org / GitLab CI/CD",
#             "path": "gitlab-ci",
#             "path_with_namespace": "gitlab-org/gitlab-ci"
#         },
#         "author": {
#             "name": "Administrator",
#             "username": "root",
#             "id": 1,
#             "state": "active",
#             "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/root"
#         },
#         "action_name": "marked",
#         "target_type": "Issue",
#         "target": {
#             "id": 93,
#             "iid": 10,
#             "project_id": 5,
#             "title": "Vel voluptas atque dicta mollitia adipisci qui at.",
#             "description": "Tempora laboriosam sint magni sed voluptas similique.",
#             "state": "closed",
#             "created_at": "2016-06-17T07:47:39.486Z",
#             "updated_at": "2016-07-01T11:09:13.998Z",
#             "labels": [],
#             "milestone": {
#                 "id": 26,
#                 "iid": 1,
#                 "project_id": 5,
#                 "title": "v0.0",
#                 "description": "Accusantium nostrum rerum quae quia quis nesciunt suscipit id.",
#                 "state": "closed",
#                 "created_at": "2016-06-17T07:47:33.832Z",
#                 "updated_at": "2016-06-17T07:47:33.832Z",
#                 "due_date": None
#             },
#             "assignees": [{
#                 "name": "Jarret O'Keefe",
#                 "username": "francisca",
#                 "id": 14,
#                 "state": "active",
#                 "avatar_url": "http://www.gravatar.com/avatar/a7fa515d53450023c83d62986d0658a8?s=80&d=identicon",
#                 "web_url": "https://gitlab.example.com/francisca"
#             }],
#             "assignee": {
#                 "name": "Jarret O'Keefe",
#                 "username": "francisca",
#                 "id": 14,
#                 "state": "active",
#                 "avatar_url": "http://www.gravatar.com/avatar/a7fa515d53450023c83d62986d0658a8?s=80&d=identicon",
#                 "web_url": "https://gitlab.example.com/francisca"
#             },
#             "type": "ISSUE",
#             "author": {
#                 "name": "Maxie Medhurst",
#                 "username": "craig_rutherford",
#                 "id": 12,
#                 "state": "active",
#                 "avatar_url": "http://www.gravatar.com/avatar/a0d477b3ea21970ce6ffcbb817b0b435?s=80&d=identicon",
#                 "web_url": "https://gitlab.example.com/craig_rutherford"
#             },
#             "subscribed": True,
#             "user_notes_count": 7,
#             "upvotes": 0,
#             "downvotes": 0,
#             "merge_requests_count": 0,
#             "due_date": None,
#             "web_url": "http://gitlab.example.com/my-group/my-project/issues/10",
#             "references": {
#                 "short": "#10",
#                 "relative": "#10",
#                 "full": "my-group/my-project#10"
#             },
#             "confidential": False,
#             "discussion_locked": False,
#             "issue_type": "issue",
#             "severity": "UNKNOWN",
#             "task_completion_status": {
#                 "count": 0,
#                 "completed_count": 0
#             }
#         },
#         "target_url": "https://gitlab.example.com/gitlab-org/gitlab-ci/issues/10",
#         "body": "Vel voluptas atque dicta mollitia adipisci qui at.",
#         "state": "pending",
#         "created_at": "2016-07-01T11:09:13.992Z"
#     }
#
#     example_data = {
#         "id": 699,
#         "type": None,
#         "body": "Lets promote this to an epic",
#         "attachment": None,
#         "author": {
#             "id": 1,
#             "name": "Alexandra Bashirian",
#             "username": "eileen.lowe",
#             "state": "active",
#             "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
#             "web_url": "https://gitlab.example.com/eileen.lowe"
#         },
#         "created_at": "2020-12-03T12:27:17.844Z",
#         "updated_at": "2020-12-03T12:27:17.844Z",
#         "system": False,
#         "noteable_id": 461,
#         "noteable_type": "Issue",
#         "resolvable": False,
#         "confidential": False,
#         "noteable_iid": 33,
#         "commands_changes": {
#             "promote_to_epic": True
#         }
#     }
#
#     example_data = {
#         "human_time_estimate": "3h 30m",
#         "human_total_time_spent": None,
#         "time_estimate": 12600,
#         "total_time_spent": 0
#     }
#
#     example_data = {
#         "human_time_estimate": None,
#         "human_total_time_spent": None,
#         "time_estimate": 0,
#         "total_time_spent": 0
#     }


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
    test_project_response()
    test_user_response()
    test_branch_response()
    test_commit_response()
    test_deploy_token_response()
    test_merge_request_response()
    #test_issues_response()
