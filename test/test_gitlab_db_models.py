from datetime import datetime

import pytest
from gitlab_api import ComplianceFrameworksDBModel, CIIDTokenComponentsDBModel

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
    TopicDBModel,
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
    UserDBModel,
    NamespaceDBModel,
    ContainerExpirationPolicyDBModel,
    PermissionsDBModel,
    StatisticsDBModel,
    DiffDBModel,
    DetailedStatusDBModel,
    TagDBModel,
    ParentIDDBModel,
    BaseDBModel,
)


@pytest.mark.parametrize(
    "model, kwargs",
    [
        # Create the referenced records first
        (
            ProjectConfigDBModel,
            {
                "id": 2,  # Ensure this ID matches the foreign key
                "name": "project_config_1",
                "name_with_namespace": "namespace1/project_config_1",
                "path": "path1",
                "path_with_namespace": "namespace1/path1",
                "created_at": datetime.now(),
            },
        ),
        (
            JobDBModel,
            {
                "base_type": "Job",
                "id": 13983,
                "name": "prepare-release",
                "coverage": None,
                "erased_at": None,
                "commit": CommitDBModel(
                    **{
                        "base_type": "Commit",
                        "id": "7f4c58a36e74074173125b75985801e2210dc794",
                        "short_id": "7f4c58a3",
                        "created_at": datetime.now(),
                        "parent_ids": [
                            ParentIDDBModel(
                                **{
                                    "base_type": "ParentID",
                                    "parent_id": "0a03c4a5913963e10b680632508b9d0a655ce3e3",
                                }
                            )
                        ],
                        "title": "Added alpine image.",
                        "message": "New message",
                        "author_name": "KnucklesSG1",
                        "author_email": "knucklessg1@gmail.com",
                        "authored_date": datetime.now(),
                        "committer_name": "KnucklesSG1",
                        "committer_email": "knucklessg1@gmail.com",
                        "committed_date": datetime.now(),
                        "web_url": "http://gitlab.arpa/homelab/containers/alpine/-/commit/7f4c58a36e74074173125b75985801e2210dc794",
                    }
                ),
                "archived": False,
                "allow_failure": False,
                "created_at": datetime.now(),
                "started_at": datetime.now(),
                "finished_at": datetime.now(),
                "duration": 3.742688,
                "queued_duration": 1.018504,
                "artifacts_file": ArtifactsFileDBModel(
                    **{
                        "base_type": "ArtifactsFile",
                        "filename": "artifacts.zip",
                        "size": 243,
                    }
                ),
                "artifacts": [
                    ArtifactDBModel(
                        **{
                            "base_type": "Artifact",
                            "file_type": "dotenv",
                            "size": 161,
                            "filename": ".env.gz",
                            "file_format": "gzip",
                        }
                    ),
                    ArtifactDBModel(
                        **{
                            "base_type": "Artifact",
                            "file_type": "trace",
                            "size": 2582,
                            "filename": "job.log",
                        }
                    ),
                ],
                "artifacts_expire_at": datetime.now(),
                "tag_list": [TagDBModel(**{"base_type": "Tag", "tag": "Docker"})],
                "pipeline": PipelineDBModel(
                    **{
                        "base_type": "Pipeline",
                        "id": 6187,
                        "iid": 1,
                        "ref": "main",
                        "sha": "7f4c58a36e74074173125b75985801e2210dc794",
                        "status": "success",
                        "web_url": "http://gitlab.arpa/homelab/containers/alpine/-/pipelines/6187",
                        "project_id": 105,
                        "created_at": "2024-08-18T22:59:27.759Z",
                        "updated_at": "2024-08-18T23:00:06.470Z",
                        "source": "push",
                    }
                ),
                "ref": "main",
                "runner": RunnerDBModel(
                    **{
                        "base_type": "Runner",
                        "id": 1,
                        "description": "Docker-R510",
                        "active": True,
                        "paused": False,
                        "is_shared": False,
                        "runner_type": "group_type",
                        "online": True,
                        "status": "online",
                    }
                ),
                "runner_manager": RunnerManagerDBModel(
                    **{
                        "base_type": "RunnerManager",
                        "id": 40,
                        "system_id": "r_Rf0lgxIqDUYN",
                        "version": "17.2.0",
                        "revision": "6428c288",
                        "platform": "linux",
                        "architecture": "amd64",
                        "created_at": datetime.now(),
                        "contacted_at": datetime.now(),
                        "ip_address": "192.168.224.1",
                        "status": "online",
                    }
                ),
                "stage": "prepare-release",
                "status": "success",
                "tag": False,
                "web_url": "http://gitlab.arpa/homelab/containers/alpine/-/jobs/13983",
                "project": ProjectConfigDBModel(
                    **{
                        "base_type": "ProjectConfig",
                        "ci_job_token_scope_enabled": False,
                    }
                ),
                "user": UserDBModel(
                    **{
                        "base_type": "User",
                        "id": 5,
                        "username": "audel_rouhi",
                        "name": "Audel Rouhi",
                        "state": "active",
                        "locked": False,
                        "avatar_url": "https://www.gravatar.com/avatar/67028d2aea629022416fa7bcc7f7847d03c6a6b2365ef155473716cb0a0e7fc5?s=80&d=identicon",
                        "web_url": "http://gitlab.arpa/audel_rouhi",
                        "created_at": datetime.now(),
                        "bio": "",
                        "location": "",
                        "skype": "",
                        "linkedin": "",
                        "twitter": "",
                        "discord": "",
                        "website_url": "",
                        "organization": "",
                        "job_title": "",
                        "bot": False,
                        "followers": 0,
                        "following": 0,
                        "pronouns": None,
                        "work_information": None,
                        "local_time": "1:25 PM",
                    }
                ),
            },
        ),
        (
            MergeRequestDBModel,
            {"id": 1, "iid": 1, "title": "title_1", "state": "state_1"},
        ),
        (GroupDBModel, {"id": 1, "name": "group_1", "path": "group_path"}),
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
            {"file_type": "dotenv", "size": 161, "filename": ".env.gz"},
        ),
        (
            ArtifactsFileDBModel,
            {
                "base_type": "ArtifactsFile",
                "filename": "artifacts.zip",
                "size": 243,
            },
        ),
        (
            RunnerManagerDBModel,
            {"system_id": "r_Rf0lgxIqDUYN", "version": "17.2.0", "platform": "linux"},
        ),
        (
            ConfigurationDBModel,
            {"id": 1, "approvals_before_merge": 2, "reset_approvals_on_push": True},
        ),
        (IterationDBModel, {"title": "Iteration 1", "state": 1}),
        (IdentityDBModel, {"provider": "gitlab", "extern_uid": "user123"}),
        (NamespaceDBModel, {"id": 1, "name": "namespace_1", "path": "namespace_path"}),
        (ContainerExpirationPolicyDBModel, {"cadence": "1d", "enabled": True}),
        (AgentDBModel, {"id": 1, "config_project_id": 1}),
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
                "approvers_id": 5,
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
                "creator": UserDBModel(**{"id": 1, "username": "creator"}),
                "topics": [
                    TopicDBModel(**{"id": 1, "name": "Test Topic 1"}),
                    TopicDBModel(**{"id": 2, "name": "Test Topic 2"}),
                    TopicDBModel(**{"id": 3, "name": "Test Topic 3"}),
                ],
                "ci_id_token_sub_claim_components": [
                    CIIDTokenComponentsDBModel(**{"id": 1, "name": "Test Topic 1"}),
                    CIIDTokenComponentsDBModel(**{"id": 2, "name": "Test Topic 2"}),
                    CIIDTokenComponentsDBModel(**{"id": 3, "name": "Test Topic 3"}),
                ],
                "compliance_frameworks": [
                    ComplianceFrameworksDBModel(**{"id": 1, "name": "sox"}),
                ],
                "shared_with_groups": [
                    GroupDBModel(
                        **{
                            "base_type": "Group",
                            "id": 5,
                            "name": "group_1",
                            "path": "group_path",
                        }
                    )
                ],
                "groups": [
                    GroupDBModel(
                        **{
                            "base_type": "Group",
                            "id": 6,
                            "name": "group_2",
                            "path": "group_path2",
                        }
                    )
                ],
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
                # "project_id": 2,
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
        (AgentsDBModel, {"job_id": 13983, "pipeline_id": 6187}),
    ],
)
def test_model_creation(session, model, kwargs):
    instance = model(**kwargs)
    try:
        session.add(instance)
        session.commit()
    except:
        session.merge(instance)
        session.commit()

    retrieved = session.query(model).first()
    for key, value in kwargs.items():
        if isinstance(value, datetime):
            assert getattr(retrieved, key).replace(microsecond=0) == value.replace(
                microsecond=0
            )
        elif isinstance(value, list):
            # If the value is a list of models, compare specific attributes
            for retrieved_item, expected_item in zip(getattr(retrieved, key), value):
                if isinstance(expected_item, ArtifactsFileDBModel):
                    assert retrieved_item.filename == expected_item.filename
                    assert retrieved_item.size == expected_item.size
                elif isinstance(expected_item, TagDBModel):
                    assert retrieved_item.tag == expected_item.tag
                # Add similar blocks for other nested models if needed
        elif (
            isinstance(value, list)
            and len(value) > 0
            and isinstance(value[0], BaseDBModel)
        ):
            retrieved_ids = [getattr(g, "id") for g in getattr(retrieved, key)]
            expected_ids = [getattr(g, "id") for g in value]
            assert retrieved_ids == expected_ids
        elif isinstance(value, ArtifactsFileDBModel):
            # Compare specific attributes of ArtifactsFileDBModel
            retrieved_artifacts_file = getattr(retrieved, key)
            assert retrieved_artifacts_file.filename == value.filename
            assert retrieved_artifacts_file.size == value.size
        elif isinstance(value, CommitDBModel):
            # Compare specific attributes of CommitDBModel
            retrieved_commit = getattr(retrieved, key)
            assert retrieved_commit.id == value.id
            assert retrieved_commit.short_id == value.short_id
            # Add additional attribute comparisons as needed
        elif isinstance(value, UserDBModel):
            # Compare specific attributes of UserDBModel
            retrieved_user = getattr(retrieved, key)
            assert retrieved_user.id == value.id
            assert retrieved_user.username == value.username
        else:
            assert getattr(retrieved, key) == value
