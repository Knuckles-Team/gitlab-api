from datetime import datetime

import pytest

from gitlab_api.gitlab_db_models import (
    DeployTokenDBModel,
    RuleDBModel,
    AccessControlDBModel,
    SourceDBModel,
    LinkDBModel,
    AssetsDBModel,
    EvidenceDBModel,
    ReleaseLinksDBModel,
    TokenDBModel,
    ToDoDBModel,
    WikiPageDBModel,
    WikiAttachmentLinkDBModel,
    WikiAttachmentDBModel,
    AgentDBModel,
    AgentsDBModel,
    ReleaseDBModel,
    BranchDBModel,
    ApprovalRuleDBModel,
    MergeRequestDBModel,
    MergeApprovalsDBModel,
    TestCaseDBModel,
    TestSuiteDBModel,
    TestReportDBModel,
    TestReportTotalDBModel,
    GroupAccessDBModel,
    DefaultBranchProtectionDefaultsDBModel,
    GroupDBModel,
    WebhookDBModel,
    AccessLevelDBModel,
    ProjectDBModel,
    RunnerDBModel,
    EpicDBModel,
    IssueDBModel,
    JobDBModel,
    PipelineDBModel,
    PipelineVariableDBModel,
    PackageLinkDBModel,
    PackageVersionDBModel,
    PackageDBModel,
    ProjectConfigDBModel,
    ContributorDBModel,
    CommitStatsDBModel,
    CommitSignatureDBModel,
    CommentDBModel,
    CommitDBModel,
    MembershipDBModel,
    IssueStatsDBModel,
    MilestoneDBModel,
    TimeStatsDBModel,
    TaskCompletionStatusDBModel,
    ReferencesDBModel,
    ArtifactDBModel,
    ArtifactsFileDBModel,
    RunnerManagerDBModel,
    ConfigurationDBModel,
    IterationDBModel,
    IdentityDBModel,
    GroupSamlIdentityDBModel,
    UserDBModel,
    NamespaceDBModel,
    ContainerExpirationPolicyDBModel,
    PermissionsDBModel,
    StatisticsDBModel,
    DiffDBModel,
    DetailedStatusDBModel,
)


@pytest.mark.parametrize(
    "model, kwargs",
    [
        # Create the referenced records first
        (
            ProjectConfigDBModel,
            {
                "id": 1,  # Ensure this ID matches the foreign key
                "name": "project_config_1",
                "name_with_namespace": "namespace1/project_config_1",
                "path": "path1",
                "path_with_namespace": "namespace1/path1",
                "created_at": datetime.now(),
            },
        ),
        (JobDBModel, {"id": 1, "name": "job_1", "status": "status_1"}),
        (UserDBModel, {"id": 1, "username": "user_1", "email": "user@example.com"}),
        (
            MergeRequestDBModel,
            {"id": 1, "iid": 1, "title": "title_1", "state": "state_1"},
        ),
        (GroupDBModel, {"id": 1, "name": "group_1", "path": "group_path"}),
        (PipelineDBModel, {"id": 1, "iid": 1, "status": "status_1"}),
        # Create dependent records after the referenced records
        (DiffDBModel, {"id": 1, "diff": "diff content"}),
        (
            WebhookDBModel,
            {
                "url": "http://example.com",
                "name": "webhook_1",
                "group_id": 1,
                "description": "Webhook description",
                "push_events": True,
                "issues_events": True,
                "merge_requests_events": True,
                "confidential_issues_events": True,
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
                "repository_update_events": True,
                "resource_access_token_events": True,
                "created_at": datetime(year=2023, month=1, day=1, hour=0, minute=0),
            },
        ),
        (DeployTokenDBModel, {"name": "deploy_token_1", "username": "username_1"}),
        (
            RuleDBModel,
            {"commit_committer_check": True, "commit_committer_name_check": False},
        ),
        (AccessControlDBModel, {"name": "access_control_1", "access_level": 10}),
        (SourceDBModel, {"format": "format_1", "url": "http://example.com"}),
        (LinkDBModel, {"name": "link_1", "url": "http://example.com"}),
        (AssetsDBModel, {"count": 10}),
        (EvidenceDBModel, {"sha": "abc123", "filepath": "/path/to/file"}),
        (ReleaseLinksDBModel, {"closed_issues_url": "http://example.com/issues"}),
        (
            TokenDBModel,
            {
                "token": "token_1",
                "token_expires_at": datetime(
                    year=2023, month=1, day=1, hour=0, minute=0
                ),
            },
        ),
        (ToDoDBModel, {"action_name": "action_1", "state": "state_1"}),
        (WikiPageDBModel, {"content": "content_1", "format": "format_1"}),
        (WikiAttachmentLinkDBModel, {"url": "http://example.com"}),
        (WikiAttachmentDBModel, {"file_name": "file_1", "file_path": "/path/to/file"}),
        (ReleaseDBModel, {"tag_name": "tag_1", "description": "description_1"}),
        (BranchDBModel, {"name": "branch_1", "merged": True}),
        (ApprovalRuleDBModel, {"name": "rule_1", "approvals_required": 2}),
        (GroupAccessDBModel, {"access_level": 30}),
        (DefaultBranchProtectionDefaultsDBModel, {"allow_force_push": True}),
        (AccessLevelDBModel, {"access_level": 40}),
        (RunnerDBModel, {"description": "runner_1", "ip_address": "127.0.0.1"}),
        (PackageLinkDBModel, {"web_path": "/path/to/package"}),
        (PackageVersionDBModel, {"version": "1.0.0"}),
        (PackageDBModel, {"name": "package_1", "version": "1.0.0"}),
        (
            ContributorDBModel,
            {"name": "contributor_1", "email": "contributor@example.com"},
        ),
        (CommitStatsDBModel, {"additions": 10, "deletions": 5}),
        (
            CommitSignatureDBModel,
            {"signature_type": "gpg", "verification_status": "verified"},
        ),
        (CommentDBModel, {"body": "comment_1", "note": "note_1"}),
        (CommitDBModel, {"id": '123', "message": "commit message"}),
        (MembershipDBModel, {"source_id": 1, "access_level": {}}),
        (IssueStatsDBModel, {"total": 10, "closed": 5}),
        (MilestoneDBModel, {"title": "milestone_1", "state": "active"}),
        (TimeStatsDBModel, {"time_estimate": 100, "total_time_spent": 50}),
        (TaskCompletionStatusDBModel, {"count": 10, "completed_count": 7}),
        (
            ReferencesDBModel,
            {"short": "short_ref", "relative": "relative_ref", "full": "full_ref"},
        ),
        (
            ArtifactDBModel,
            {"file_type": "zip", "size": 1024, "filename": "artifact.zip"},
        ),
        (ArtifactsFileDBModel, {"filename": "artifacts.zip", "size": 2048}),
        (
            RunnerManagerDBModel,
            {"system_id": "sys123", "version": "v1.0", "platform": "linux"},
        ),
        (
            ConfigurationDBModel,
            {"id": 1, "approvals_before_merge": 2, "reset_approvals_on_push": True},
        ),
        (IterationDBModel, {"title": "Iteration 1", "state": 1}),
        (IdentityDBModel, {"provider": "gitlab", "extern_uid": "user123"}),
        (GroupSamlIdentityDBModel, {"user_id": 1, "extern_uid": "saml123", "provider": "saml"}),
        (NamespaceDBModel, {"id": 1, "name": "namespace_1", "path": "namespace_path"}),
        (ContainerExpirationPolicyDBModel, {"cadence": "1d", "enabled": True}),
        (AgentDBModel, {"id": 1, "config_project_id": 1}),
        (AgentsDBModel, {"job_id": 1, "pipeline_id": 1}),
        (
            PermissionsDBModel,
            {
                "project_access": {"access_level": 30},
                "group_access": {"access_level": 40},
            },
        ),
        (StatisticsDBModel, {"commit_count": 100, "storage_size": 2048}),
        (
            DetailedStatusDBModel,
            {"icon": "icon.png", "text": "status text", "label": "status label"},
        ),
        (
            MergeApprovalsDBModel,
            {
                "approvals_before_merge": 2,
                "reset_approvals_on_push": True,
                "approvers_id": 1,
            },
        ),
        (
            TestCaseDBModel,
            {
                "status": "success",
                "name": "test_case_1",
                "classname": "TestClass",
                "execution_time": 1.23,
            },
        ),
        (
            TestSuiteDBModel,
            {
                "name": "test_suite_1",
                "total_time": 12.34,
                "total_count": 10,
                "success_count": 9,
                "failed_count": 1,
                "skipped_count": 0,
                "error_count": 0,
            },
        ),
        (
            TestReportTotalDBModel,
            {
                "time": 100,
                "count": 10,
                "success": 8,
                "failed": 2,
                "skipped": 0,
                "error": 0,
            },
        ),
        (
            TestReportDBModel,
            {
                "total_time": 100,
                "total_count": 10,
                "success_count": 8,
                "failed_count": 2,
                "skipped_count": 0,
                "error_count": 0,
                "total_id": 1,
                "test_suites_id": 1,
            },
        ),
        (
            ProjectDBModel,
            {
                "id": 1,
                "description": "project description",
                "name": "project_1",
                "created_at": datetime.now(),
                "shared_with_groups": [GroupDBModel(**{"base_type": "Group", "id": 5, "name": "group_1", "path": "group_path"})],
                "groups": [GroupDBModel(**{"base_type": "Group","id": 6, "name": "group_2", "path": "group_path2"})]
            },
        ),
        (
            EpicDBModel,
            {"iid": 1, "title": "Epic 1", "group_id": 1},
        ),
        (
            IssueDBModel,
            {
                "state": "opened",
                "description": "issue description",
                #"project_id": 2,
                "title": "Issue 1",
                "created_at": datetime.now(),
                "author_id": 1,
                "milestone_id": 1,
            },
        ),
        (
            PipelineVariableDBModel,
            {"key": "VAR_KEY", "variable_type": "env_var", "value": "VAR_VALUE"},
        ),
    ],
)
def test_model_creation(session, model, kwargs):
    instance = model(**kwargs)
    session.merge(instance)
    session.commit()

    retrieved = session.query(model).first()
    for key, value in kwargs.items():
        if isinstance(value, datetime):
            assert getattr(retrieved, key).replace(microsecond=0) == value.replace(microsecond=0)
        elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], GroupDBModel):
            retrieved_ids = [getattr(g, 'id') for g in getattr(retrieved, key)]
            expected_ids = [getattr(g, 'id') for g in value]
            assert retrieved_ids == expected_ids
        else:
            assert getattr(retrieved, key) == value
