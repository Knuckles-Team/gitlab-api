import pytest

from gitlab_api.gitlab_db_models import (
    DeployToken,
    Rule,
    AccessControl,
    Source,
    Link,
    Assets,
    Evidence,
    ReleaseLinks,
    Token,
    ToDo,
    WikiPage,
    WikiAttachmentLink,
    WikiAttachment,
    Agent,
    Agents,
    Release,
    Branch,
    ApprovalRule,
    MergeRequest,
    GroupAccess,
    DefaultBranchProtectionDefaults,
    Group,
    Webhook,
    AccessLevel,
    ApprovedByUser,
    Project,
    Runner,
    Job,
    Pipeline,
    PackageLink,
    PackageVersion,
    Package,
    Contributor,
    CommitStats,
    CommitSignature,
    Comment,
    Commit,
    Membership,
    IssueStats,
    Milestone,
    TimeStats,
    TaskCompletionStatus,
    References,
    Artifact,
    ArtifactsFile,
    RunnerManager,
    Configuration,
    Iteration,
    Identity,
    GroupSamlIdentity,
    CreatedBy,
    User,
    Namespace,
    ContainerExpirationPolicy,
    Permissions,
    Statistics,
    Links,
    Diff,
    DetailedStatus,
)

DATABASE_URL = "postgresql+psycopg://scott:tiger@localhost/test"


@pytest.mark.parametrize(
    "model, kwargs",
    [
        (DeployToken, {"name": "deploy_token_1", "username": "username_1"}),
        (Rule, {"commit_committer_check": True, "commit_committer_name_check": False}),
        (AccessControl, {"name": "access_control_1", "access_level": 10}),
        (Source, {"format": "format_1", "url": "http://example.com"}),
        (Link, {"name": "link_1", "url": "http://example.com"}),
        (Assets, {"count": 10}),
        (Evidence, {"sha": "abc123", "filepath": "/path/to/file"}),
        (ReleaseLinks, {"closed_issues_url": "http://example.com/issues"}),
        (Token, {"token": "token_1", "token_expires_at": "2023-01-01T00:00:00Z"}),
        (ToDo, {"action_name": "action_1", "state": "state_1"}),
        (WikiPage, {"content": "content_1", "format": "format_1"}),
        (WikiAttachmentLink, {"url": "http://example.com"}),
        (WikiAttachment, {"file_name": "file_1", "file_path": "/path/to/file"}),
        (Agent, {"config_project_id": 1}),
        (Agents, {"job_id": 1, "pipeline_id": 1}),
        (Release, {"tag_name": "tag_1", "description": "description_1"}),
        (Branch, {"name": "branch_1", "merged": True}),
        (ApprovalRule, {"name": "rule_1", "approvals_required": 2}),
        (MergeRequest, {"iid": 1, "title": "title_1", "state": "state_1"}),
        (GroupAccess, {"access_level": 30}),
        (DefaultBranchProtectionDefaults, {"allow_force_push": True}),
        (Group, {"name": "group_1", "path": "group_path"}),
        (Webhook, {"url": "http://example.com", "name": "webhook_1", "group_id": 1}),
        (AccessLevel, {"access_level": 40}),
        (ApprovedByUser, {"user_id": 1}),
        (Project, {"name": "project_1", "description": "description_1"}),
        (Runner, {"description": "runner_1", "ip_address": "127.0.0.1"}),
        (Job, {"name": "job_1", "status": "status_1"}),
        (Pipeline, {"iid": 1, "status": "status_1"}),
        (PackageLink, {"web_path": "/path/to/package"}),
        (PackageVersion, {"version": "1.0.0"}),
        (Package, {"name": "package_1", "version": "1.0.0"}),
        (Contributor, {"name": "contributor_1", "email": "contributor@example.com"}),
        (CommitStats, {"additions": 10, "deletions": 5}),
        (CommitSignature, {"signature_type": "gpg", "verification_status": "verified"}),
        (Comment, {"body": "comment_1", "note": "note_1"}),
        (Commit, {"id": "abc123", "message": "commit message"}),
        (Membership, {"source_id": 1, "access_level": {}}),
        (IssueStats, {"total": 10, "closed": 5}),
        (Milestone, {"title": "milestone_1", "state": "active"}),
        (TimeStats, {"time_estimate": 100, "total_time_spent": 50}),
        (TaskCompletionStatus, {"count": 10, "completed_count": 7}),
        (
            References,
            {"short": "short_ref", "relative": "relative_ref", "full": "full_ref"},
        ),
        (Artifact, {"file_type": "zip", "size": 1024, "filename": "artifact.zip"}),
        (ArtifactsFile, {"filename": "artifacts.zip", "size": 2048}),
        (
            RunnerManager,
            {"system_id": "sys123", "version": "v1.0", "platform": "linux"},
        ),
        (Configuration, {"approvals_before_merge": 2, "reset_approvals_on_push": True}),
        (Iteration, {"title": "Iteration 1", "state": 1}),
        (Identity, {"provider": "gitlab", "extern_uid": "user123"}),
        (GroupSamlIdentity, {"extern_uid": "saml123", "provider": "saml"}),
        (CreatedBy, {"username": "creator_user", "name": "Creator Name"}),
        (User, {"username": "user_1", "email": "user@example.com"}),
        (Namespace, {"name": "namespace_1", "path": "namespace_path"}),
        (ContainerExpirationPolicy, {"cadence": "1d", "enabled": True}),
        (
            Permissions,
            {
                "project_access": {"access_level": 30},
                "group_access": {"access_level": 40},
            },
        ),
        (Statistics, {"commit_count": 100, "storage_size": 2048}),
        (
            Links,
            {
                "self_link": "http://example.com/project",
                "issues": "http://example.com/issues",
            },
        ),
        (Diff, {"merge_request_id": 1, "diff": "diff content"}),
        (
            DetailedStatus,
            {"icon": "icon.png", "text": "status text", "label": "status label"},
        ),
    ],
)
def test_model_creation(session, model, kwargs):
    instance = model(**kwargs)
    session.add(instance)
    session.commit()

    retrieved = session.query(model).first()
    for key, value in kwargs.items():
        assert getattr(retrieved, key) == value
