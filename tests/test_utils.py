from datetime import datetime
import logging

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from gitlab_api.gitlab_models import (
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
    ProjectConfig,
    Agent,
    Release,
    Branch,
    ApprovalRule,
    MergeRequest,
    ApprovedBy,
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
    Issue,
    PipelineVariable,
    TestCase,
    Epic,
    TestSuite,
    TestReport,
    TestReportTotal,
    MergeApprovals,
)
from gitlab_api.utils import pydantic_to_sqlalchemy

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()


@pytest.fixture
def issue_stats_fixture():
    return IssueStats(base_type="IssueStats", total=10, closed=5, opened=5)


@pytest.fixture
def milestone_fixture():
    return Milestone(
        base_type="Milestone",
        id=1,
        iid=101,
        project_id=1,
        title="Milestone Title",
        description="Milestone Description",
        state="active",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        closed_at=datetime(2023, 1, 3, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        due_date="2023-02-01",
        start_date="2023-01-01",
        web_url="http://example.com",
        # issue_stats={"total":10, "closed":5, "opened":5},
        # issue_stats=IssueStats(total=10, closed=5, opened=5),
    )


@pytest.fixture
def time_stats_fixture():
    return TimeStats(
        base_type="TimeStats",
        time_estimate=3600,
        total_time_spent=1800,
        human_time_estimate="1h",
        human_total_time_spent="30m",
    )


@pytest.fixture
def task_completion_status_fixture():
    return TaskCompletionStatus(
        base_type="TaskCompletionStatus", count=10, completed_count=5
    )


@pytest.fixture
def references_fixture():
    return References(
        base_type="References",
        short="short_ref",
        relative="relative_ref",
        full="full_ref",
    )


@pytest.fixture
def artifact_fixture():
    return Artifact(
        base_type="Artifact",
        file_type="artifact",
        size=1024,
        filename="artifact.txt",
        file_format="txt",
    )


@pytest.fixture
def artifacts_file_fixture():
    return ArtifactsFile(base_type="ArtifactsFile", filename="artifacts.zip", size=2048)


@pytest.fixture
def runner_manager_fixture():
    return RunnerManager(
        base_type="RunnerManager",
        id=1,
        system_id="system_id",
        version="v1.0",
        revision="rev1",
        platform="linux",
        architecture="x86_64",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        contacted_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        ip_address="127.0.0.1",
        status="active",
    )


@pytest.fixture
def configuration_fixture():
    return Configuration(
        base_type="Configuration",
        approvals_before_merge=2,
        reset_approvals_on_push=True,
        selective_code_owner_removals=True,
        disable_overriding_approvers_per_merge_request=False,
        merge_requests_author_approval=True,
        merge_requests_disable_committers_approval=False,
        require_password_to_approve=False,
    )


@pytest.fixture
def iteration_fixture():
    return Iteration(
        base_type="Iteration",
        id=1,
        iid=101,
        sequence=1,
        group_id=1,
        title="Iteration Title",
        description="Iteration Description",
        state=1,
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        start_date="2023-01-01",
        due_date="2023-02-01",
        web_url="http://example.com",
    )


@pytest.fixture
def identity_fixture():
    return Identity(base_type="Identity", provider="provider", extern_uid="extern_uid")


@pytest.fixture
def group_saml_identity_fixture():
    return GroupSamlIdentity(
        base_type="GroupSamlIdentity",
        extern_uid="extern_uid",
        provider="provider",
        saml_provider_id=1,
    )


@pytest.fixture
def created_by_fixture():
    return CreatedBy(
        base_type="CreatedBy",
        id=1,
        username="creator",
        name="Creator Name",
        state="active",
        avatar_url="http://example.com/avatar",
        web_url="http://example.com",
    )


@pytest.fixture
def user_fixture():
    return User(
        base_type="User",
        id=1,
        username="user",
        user="user",
        email="user@example.com",
        name="User Name",
        state="active",
        locked=False,
        avatar_url="http://example.com/avatar",
        web_url="http://example.com",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        is_admin=False,
        bio="User bio",
        location="User location",
        skype="user_skype",
        linkedin="user_linkedin",
        twitter="user_twitter",
        discord="user_discord",
        website_url="http://example.com",
        organization="User organization",
        job_title="User job title",
        last_sign_in_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        confirmed_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        theme_id=1,
        last_activity_on=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        color_scheme_id=1,
        projects_limit=10,
        current_sign_in_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        note="User note",
        identities=[],
        can_create_group=True,
        can_create_project=True,
        two_factor_enabled=False,
        external=False,
        private_profile=False,
        current_sign_in_ip="127.0.0.1",
        last_sign_in_ip="127.0.0.1",
        namespace_id=1,
        created_by=1,
        email_reset_offered_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        expires_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        access_level=10,
        group_saml_identity=None,
        approved=False,
        invited=False,
        public_email="public@example.com",
        pronouns="they/them",
        bot=False,
        work_information="Work info",
        followers=10,
        following=10,
        local_time="10:00",
        commit_email="commit@example.com",
        shared_runners_minutes_limit=1000,
        extra_shared_runners_minutes_limit=100,
        membership_type="member",
        removable=True,
        last_login_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
    )


@pytest.fixture
def namespace_fixture():
    return Namespace(
        base_type="Namespace",
        id=1,
        name="Namespace Name",
        path="namespace_path",
        kind="group",
        full_path="full/namespace_path",
        parent_id=None,
        avatar_url="http://example.com/avatar",
        web_url="http://example.com",
    )


@pytest.fixture
def container_expiration_policy_fixture():
    return ContainerExpirationPolicy(
        base_type="ContainerExpirationPolicy",
        cadence="1d",
        enabled=True,
        keep_n=10,
        older_than="1w",
        name_regex=".*",
        name_regex_keep=".*",
        next_run_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
    )


@pytest.fixture
def permissions_fixture():
    return Permissions(
        base_type="Permissions",
        project_access={"access_level": 40, "notification_level": 3},
        group_access={"access_level": 50, "notification_level": 2},
    )


@pytest.fixture
def statistics_fixture():
    return Statistics(
        base_type="Statistics",
        commit_count=100,
        storage_size=2048,
        repository_size=1024,
        wiki_size=512,
        lfs_objects_size=256,
        job_artifacts_size=128,
        pipeline_artifacts_size=64,
        packages_size=32,
        snippets_size=16,
        uploads_size=8,
    )


@pytest.fixture
def links_fixture():
    return Links(
        base_type="Links",
        self="http://example.com/self",
        issues="http://example.com/issues",
        merge_requests="http://example.com/merge_requests",
        repo_branches="http://example.com/repo_branches",
        labels="http://example.com/labels",
        events="http://example.com/events",
        members="http://example.com/members",
        cluster_agents="http://example.com/cluster_agents",
        self_link="http://example.com/self_link",
        notes="http://example.com/notes",
        award_emoji="http://example.com/award_emoji",
        project="http://example.com/project",
        closed_as_duplicate_of="http://example.com/closed_as_duplicate_of",
    )


@pytest.fixture
def diff_fixture():
    return Diff(
        base_type="Diff",
        id=1,
        merge_request_id=1,
        head_commit_sha="abc123",
        base_commit_sha="def456",
        start_commit_sha="ghi789",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        state="active",
        real_size="large",
        patch_id_sha="jkl012",
        diff="diff content",
        new_path="new_path",
        old_path="old_path",
        a_mode="100644",
        b_mode="100755",
        new_file=True,
        renamed_file=False,
        deleted_file=False,
        generated_file=False,
    )


@pytest.fixture
def detailed_status_fixture():
    return DetailedStatus(
        base_type="DetailedStatus",
        icon="icon",
        text="text",
        label="label",
        group="group",
        tooltip="tooltip",
        has_details=True,
        details_path="http://example.com/details_path",
        illustration=None,
        favicon="http://example.com/favicon",
    )


@pytest.fixture
def pipeline_fixture():
    return Pipeline(
        base_type="Pipeline",
        id=1,
        iid=101,
        ref="refs/heads/main",
        sha="abc123",
        status="success",
        web_url="http://example.com",
        project_id=1,
        before_sha="def456",
        tag=False,
        yaml_errors=None,
        user=None,
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-02T00:00:00Z",
        started_at="2023-01-01T01:00:00Z",
        finished_at="2023-01-01T02:00:00Z",
        committed_at="2023-01-01T03:00:00Z",
        duration=3600,
        queued_duration=600,
        coverage="85.5%",
        name="pipeline_name",
        source="push",
        detailed_status=None,
    )


@pytest.fixture
def package_link_fixture():
    return PackageLink(
        base_type="PackageLink",
        web_path="http://example.com/web_path",
        delete_api_path="http://example.com/delete_api_path",
    )


@pytest.fixture
def package_version_fixture():
    return PackageVersion(
        base_type="PackageVersion",
        id=1,
        version="1.0.0",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        pipelines=None,
    )


@pytest.fixture
def package_fixture():
    return Package(
        base_type="Package",
        id=1,
        name="package_name",
        version="1.0.0",
        package_type="npm",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        last_downloaded_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        conan_package_name="conan_package",
        links=None,
        pipelines=None,
        tags=["tag1", "tag2"],
        versions=None,
        package_id=1,
        file_name="package_file",
        size=1024,
        file_md5="md5hash",
        file_sha1="sha1hash",
        file_sha256="sha256hash",
    )


@pytest.fixture
def contributor_fixture():
    return Contributor(
        base_type="CommitStats",
        name="Contributor Name",
        email="contributor@example.com",
        commits=10,
        additions=100,
        deletions=50,
    )


@pytest.fixture
def commit_stats_fixture():
    return CommitStats(base_type="CommitStats", additions=100, deletions=50, total=150)


@pytest.fixture
def commit_signature_fixture():
    return CommitSignature(
        base_type="CommitSignature",
        signature_type="PGP",
        verification_status="verified",
        commit_source="web",
        gpg_key_id=1,
        gpg_key_primary_keyid="primary_keyid",
        gpg_key_user_name="User Name",
        gpg_key_user_email="user@example.com",
        gpg_key_subkey_id="subkey_id",
        key={"type": "ssh", "key": "ssh-rsa AAAAB3Nza..."},
        x509_certificate={"issuer": "CA", "subject": "User"},
        message="Signature message",
    )


@pytest.fixture
def comment_fixture():
    return Comment(
        base_type="Comment",
        id=1,
        type="Note",
        body="Comment body",
        note="Note content",
        attachment=None,
        author=None,
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        system=False,
        noteable_id=1,
        noteable_type="Issue",
        resolvable=True,
        confidential=False,
        noteable_iid=101,
        commands_changes={},
        line_type="new",
        path="file/path",
        line=10,
    )


@pytest.fixture
def membership_fixture():
    return Membership(
        base_type="Membership",
        id=1,
        source_id=1,
        source_full_name="Source Full Name",
        source_members_url="http://example.com/members",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        expires_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        access_level={"access_level": 40, "notification_level": 3},
    )


@pytest.fixture
def approved_by_fixture():
    return ApprovedBy(base_type="ApprovedBy", user=None)


@pytest.fixture
def project_fixture():
    return Project(
        base_type="Project",
        id=1,
        description="Project description",
        description_html="Project description HTML",
        name="Project Name",
        name_with_namespace="Namespace / Project Name",
        path="project_path",
        path_with_namespace="namespace/project_path",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        default_branch="main",
        tag_list=["tag1", "tag2"],
        topics=["topic1", "topic2"],
        ssh_url_to_repo="git@example.com:namespace/project_path.git",
        http_url_to_repo="http://example.com/namespace/project_path",
        web_url="http://example.com",
        readme_url="http://example.com/readme",
        avatar_url="http://example.com/avatar",
        forks_count=10,
        star_count=20,
        last_activity_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        namespace=None,
        container_registry_image_prefix="registry.example.com/namespace/project_path",
        additional_links=None,
        packages_enabled=True,
        empty_repo=False,
        archived=False,
        visibility="public",
        resolve_outdated_diff_discussions=True,
        container_expiration_policy=None,
        releases_access_level="enabled",
        environments_access_level="enabled",
        feature_flags_access_level="enabled",
        infrastructure_access_level="enabled",
        monitor_access_level="enabled",
        machine_learning_model_experiments_access_level="enabled",
        machine_learning_model_registry_access_level="enabled",
        issues_enabled=True,
        merge_requests_enabled=True,
        wiki_enabled=True,
        jobs_enabled=True,
        snippets_enabled=True,
        container_registry_enabled=True,
        container_registry_access_level="enabled",
        security_and_compliance_access_level="enabled",
        creator_id=1,
        import_url="http://example.com/import",
        import_type="gitlab",
        import_status="finished",
        import_error=None,
        shared_runners_enabled=True,
        group_runners_enabled=True,
        lfs_enabled=True,
        ci_default_git_depth=50,
        ci_forward_deployment_enabled=True,
        ci_forward_deployment_rollback_allowed=True,
        ci_allow_fork_pipelines_to_run_in_parent_project=True,
        ci_separated_caches=True,
        ci_restrict_pipeline_cancellation_role="maintainer",
        forked_from_project=None,
        mr_default_target_self=True,
        public_jobs=True,
        shared_with_groups=[],
        only_allow_merge_if_pipeline_succeeds=True,
        allow_merge_on_skipped_pipeline=False,
        restrict_user_defined_variables=True,
        code_suggestions=True,
        only_allow_merge_if_all_discussions_are_resolved=True,
        remove_source_branch_after_merge=True,
        request_access_enabled=True,
        merge_pipelines_enabled=True,
        merge_trains_skip_train_allowed=True,
        allow_pipeline_trigger_approve_deployment=True,
        repository_object_format="hashed",
        merge_method="merge",
        squash_option="always",
        enforce_auth_checks_on_uploads=True,
        suggestion_commit_message="Suggestion commit message",
        compliance_frameworks=["framework1", "framework2"],
        issues_template="Issues template",
        merge_requests_template="Merge requests template",
        packages_relocation_enabled=True,
        requirements_enabled=True,
        build_git_strategy="fetch",
        build_timeout=3600,
        auto_cancel_pending_pipelines="enabled",
        build_coverage_regex=".*",
        ci_config_path=".gitlab-ci.yml",
        shared_runners_minutes_limit=1000,
        extra_shared_runners_minutes_limit=100,
        printing_merge_request_link_enabled=True,
        merge_trains_enabled=True,
        has_open_issues=True,
        approvals_before_merge=2,
        mirror=False,
        mirror_user_id=1,
        mirror_trigger_builds=True,
        only_mirror_protected_branches=True,
        mirror_overwrites_diverged_branches=True,
        permissions=None,
        statistics=None,
        links=None,
        service_desk_enabled=True,
        can_create_merge_request_in=True,
        repository_access_level="enabled",
        merge_requests_access_level="enabled",
        issues_access_level="enabled",
        forking_access_level="enabled",
        wiki_access_level="enabled",
        builds_access_level="enabled",
        snippets_access_level="enabled",
        pages_access_level="enabled",
        analytics_access_level="enabled",
        emails_disabled=False,
        emails_enabled=True,
        open_issues_count=5,
        ci_job_token_scope_enabled=True,
        merge_commit_template="Merge commit template",
        squash_commit_template="Squash commit template",
        issue_branch_template="Issue branch template",
        auto_devops_enabled=True,
        auto_devops_deploy_strategy="continuous",
        autoclose_referenced_issues=True,
        keep_latest_artifact=True,
        runner_token_expiration_interval=True,
        external_authorization_classification_label="classification",
        requirements_access_level="enabled",
        security_and_compliance_enabled=True,
        warn_about_potentially_unwanted_characters=True,
        owner=None,
        runners_token="runners_token",
        repository_storage="default",
        service_desk_address="service_desk@example.com",
        marked_for_deletion_at="2023-01-01T00:00:00Z",
        marked_for_deletion_on="2023-01-02T00:00:00Z",
        operations_access_level="enabled",
        ci_dockerfile="Dockerfile",
        groups=[],
        public=True,
    )


@pytest.fixture
def runner_fixture():
    return Runner(
        base_type="Runner",
        id=1,
        description="Runner description",
        ip_address="192.168.0.1",
        active=True,
        paused=False,
        is_shared=True,
        runner_type="instance_type",
        name="Runner name",
        online=True,
        status="online",
        contacted_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        architecture="x86_64",
        platform="linux",
        revision="1.0.0",
        version="14.0",
        access_level="not_protected",
        maximum_timeout=3600,
        maintenance_note="Maintenance note",
        projects=None,
        tag_list=["tag1", "tag2"],
    )


@pytest.fixture
def job_fixture():
    return Job(
        base_type="Job",
        commit=None,
        coverage=85.5,
        archived=False,
        allow_failure=True,
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        started_at=datetime(2023, 1, 1, 1, 0).strftime("%Y-%m-%d %H:%M:%S"),
        finished_at=datetime(2023, 1, 1, 2, 0).strftime("%Y-%m-%d %H:%M:%S"),
        erased_at=datetime(2023, 1, 1, 3, 0).strftime("%Y-%m-%d %H:%M:%S"),
        duration=3600,
        queued_duration=600,
        artifacts_file=None,
        artifacts=[],
        artifacts_expire_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        tag_list=["tag1", "tag2"],
        id=1,
        name="Job name",
        pipeline=None,
        ref="refs/heads/main",
        runner=None,
        runner_manager=None,
        stage="build",
        status="success",
        failure_reason=None,
        tag=True,
        web_url="http://example.com",
        project=None,
        user=None,
        downstream_pipeline=None,
    )


@pytest.fixture
def branch_fixture():
    return Branch(
        base_type="Branch",
        name="main",
        merged=False,
        protected=True,
        default=True,
        developers_can_push=False,
        developers_can_merge=True,
        can_push=True,
        web_url="http://example.com",
        commit=None,
        id=1,
        push_access_levels=[],
        merge_access_levels=[],
        unprotect_access_levels=[],
        allow_force_push=False,
        code_owner_approval_required=True,
        inherited=False,
    )


@pytest.fixture
def approval_rule_fixture():
    return ApprovalRule(
        base_type="ApprovalRule",
        id=1,
        name="Approval Rule",
        rule_type="regular",
        eligible_approvers=[],
        approvals_required=2,
        users=[],
        groups=[],
        contains_hidden_groups=False,
        protected_branches=[],
        applies_to_all_protected_branches=True,
        source_rule="source_rule",
        approved=False,
        overridden=False,
        approved_by=[],
    )


@pytest.fixture
def merge_request_fixture():
    return MergeRequest(
        base_type="MergeRequest",
        id=1,
        iid=101,
        project_id=1,
        title="Merge Request Title",
        description="Merge Request Description",
        state="opened",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        target_branch="main",
        source_branch="feature_branch",
        upvotes=10,
        downvotes=2,
        author=None,
        assignee=None,
        source_project_id=1,
        target_project_id=2,
        labels=["label1", "label2"],
        work_in_progress=False,
        milestone=None,
        merge_when_pipeline_succeeds=True,
        merge_status="can_be_merged",
        sha="abc123",
        merge_commit_sha="def456",
        draft=False,
        squash_commit_sha="ghi789",
        squash_on_merge=True,
        user_notes_count=5,
        discussion_locked=False,
        should_remove_source_branch=True,
        force_remove_source_branch=False,
        allow_collaboration=True,
        allow_maintainer_to_push=True,
        web_url="http://example.com",
        references=None,
        reference="!101",
        time_stats=None,
        squash=True,
        task_completion_status=None,
        has_conflicts=False,
        blocking_discussions_resolved=True,
        changes=None,
        merge_user=User(
            base_type="User",
            id=2202,
            username="test",
            user=None,
            email=None,
            state="active",
            last_login_at=None,
        ),
        merged_by=User(
            base_type="User",
            id=2202,
            username="test",
            user=None,
            email=None,
            state="active",
            last_login_at=None,
        ),
        merged_at=None,
        closed_by=None,
        closed_at=None,
        latest_build_started_at=None,
        latest_build_finished_at=None,
        first_deployed_to_production_at=None,
        pipeline=None,
        head_pipeline=None,
        diff_refs=None,
        # user={
        #     "base_type": "User",
        #     "id": 2202,
        #     "username": "test",
        #     "user": None,
        #     "email": None,
        #     "state": "active",
        #     "last_login_at": None,
        # },
        user=User(
            base_type="User",
            id=2202,
            username="test",
            user=None,
            email=None,
            state="active",
            last_login_at=None,
        ),
        changes_count="1",
        rebase_in_progress=False,
        approvals_before_merge=2,
        tag_list=["tag1", "tag2"],
        reviewer=[],
        review=None,
        imported=False,
        imported_from=None,
        prepared_at=None,
        assignees=[],
        reviewers=[],
        approvals=[],
        detailed_merge_status="mergeable",
        subscribed=True,
        overflow=False,
        diverged_commits_count=0,
        merge_error=None,
        approvals_required=2,
        approvals_left=1,
        approved_by=[],
        approval_rules_overwritten=False,
        rules=[],
    )


@pytest.fixture
def epic_fixture():
    return Epic(
        base_type="Epic",
        id=1,
        iid=101,
        title="Epic Title",
        url="http://example.com",
        group_id=1,
    )


@pytest.fixture
def issue_fixture():
    return Issue(
        base_type="Issue",
        state="opened",
        description="Issue description",
        author=None,
        milestone=None,
        project_id=1,
        assignees=[],
        assignee=None,
        type="issue",
        updated_at=datetime(2023, 1, 2, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        closed_at=None,
        closed_by=None,
        changes_count="1",
        id=1,
        title="Issue title",
        created_at=datetime(2023, 1, 1, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        moved_to_id=None,
        iid=101,
        labels=["label1", "label2"],
        upvotes=10,
        downvotes=2,
        merge_requests_count=1,
        user_notes_count=5,
        iteration=None,
        due_date="2023-01-10",
        imported=False,
        imported_from=None,
        web_url="http://example.com",
        references=None,
        time_stats=None,
        has_tasks=True,
        task_status="in_progress",
        confidential=False,
        discussion_locked=False,
        issue_type="issue",
        severity="medium",
        links=None,
        task_completion_status=None,
        weight=3,
        epic_iid=101,
        epic=None,
        health_status="on_track",
        subscribed=True,
        service_desk_reply_to="service_desk@example.com",
        blocking_issues_count=0,
    )


@pytest.fixture
def pipeline_variable_fixture():
    return PipelineVariable(
        base_type="PipelineVariable",
        key="VARIABLE_KEY",
        variable_type="env_var",
        value="value",
    )


@pytest.fixture
def test_case_fixture():
    return TestCase(
        base_type="TestCase",
        status="success",
        name="test_case",
        classname="TestCaseClass",
        execution_time=1.23,
        system_output="System output",
        stack_trace="Stack trace",
    )


@pytest.fixture
def test_suite_fixture():
    return TestSuite(
        base_type="TestSuite",
        name="TestSuite",
        total_time=123.45,
        total_count=10,
        success_count=9,
        failed_count=1,
        skipped_count=0,
        error_count=0,
        test_cases=[],
        build_ids=[],
        suite_error=None,
    )


@pytest.fixture
def test_report_total_fixture():
    return TestReportTotal(
        base_type="TestReportTotal",
        time=123,
        count=10,
        success=9,
        failed=1,
        skipped=0,
        error=0,
        suite_error=None,
    )


@pytest.fixture
def test_report_fixture():
    return TestReport(
        base_type="TestReport",
        name="TestReport",
        total_time=123,
        total_count=10,
        success_count=9,
        failed_count=1,
        skipped_count=0,
        error_count=0,
        suites=[],
        total=None,
    )


@pytest.fixture
def merge_approvals_fixture():
    return MergeApprovals(
        base_type="MergeApprovals",
        reset_approvals_on_push=True,
    )


@pytest.fixture
def deploy_token_fixture():
    return DeployToken(
        base_type="DeployToken",
        id=1,
        name="DeployToken",
        username="username",
        token="token",
        scopes=["read_repository"],
        expires_at="2023-12-31",
        revoked=False,
    )


@pytest.fixture
def rule_fixture():
    return Rule(
        base_type="Rule",
        commit_message_regex="Rule",
        file_name_regex="FilesRule",
        branch_name_regex="Rule",
    )


@pytest.fixture
def access_control_fixture():
    return AccessControl(
        base_type="AccessControl",
        access_level=40,
    )


@pytest.fixture
def source_fixture():
    return Source(
        base_type="Source",
        format="zip",
        url="Source.com",
    )


@pytest.fixture
def link_fixture():
    return Link(
        base_type="Link",
        id=1,
        name="Link",
        url="http://example.com",
        link_type="other",
    )


@pytest.fixture
def assets_fixture():
    return Assets(
        base_type="Assets",
        count=0,
        evidence_file_path="Markdown/content",
    )


@pytest.fixture
def evidence_fixture():
    return Evidence(
        base_type="Evidence",
        sha="sha256",
        collected_at="2023-01-01T00:00:00Z",
    )


@pytest.fixture
def release_links_fixture():
    return ReleaseLinks(
        base_type="ReleaseLinks",
        closed_issues_url="http://example.com",
        closed_merge_requests_url="http://example.com",
        edit_url="http://example.com",
        merged_merge_requests_url="http://example.com",
        opened_issues_url="http://example.com",
        opened_merge_requests_url="http://example.com",
    )


@pytest.fixture
def release_fixture():
    return Release(
        base_type="Release",
        description="Release description",
        name="Release Name",
        created_at="2023-01-01T00:00:00Z",
        released_at="2023-01-01T01:00:00Z",
    )


@pytest.fixture
def token_fixture():
    return Token(
        base_type="Token",
        id=1,
        token="token",
        token_expires_at="2023-01-01T00:00:00Z",
    )


@pytest.fixture
def todo_fixture():
    return ToDo(
        base_type="ToDo",
        action_name="action",
        target_type="issue",
        body="ToDo body",
        created_at="2023-01-01T00:00:00Z",
        state="pending",
        id=1,
    )


@pytest.fixture
def wiki_page_fixture():
    return WikiPage(
        base_type="WikiPage",
        title="Wiki Page Title",
        content="Wiki page content",
        format="markdown",
        slug="wiki-page-slug",
    )


@pytest.fixture
def wiki_attachment_link_fixture():
    return WikiAttachmentLink(
        base_type="WikiAttachmentLink",
        url="attachment.com",
        markdown="![attachment](http://example.com/attachment.txt)",
    )


@pytest.fixture
def wiki_attachment_fixture():
    return WikiAttachment(
        base_type="WikiAttachment",
        file_name="attachment.txt",
        file_path="text/plain",
        branch="attachment.txt",
    )


@pytest.fixture
def project_config_fixture():
    return ProjectConfig(
        base_type="ProjectConfig",
        id=1,
        description="config_key",
        name="config_value",
        name_with_namespace="config_key",
        path="config_key",
        path_with_namespace="config_key",
    )


@pytest.fixture
def agent_fixture():
    return Agent(
        base_type="Agent",
        id=1,
    )


# Test function to validate the conversion for each model
@pytest.mark.parametrize(
    "fixture",
    [
        "evidence_fixture",
        "issue_stats_fixture",
        "milestone_fixture",
        "deploy_token_fixture",
        "rule_fixture",
        "merge_approvals_fixture",
        "rule_fixture",
        "access_control_fixture",
        "source_fixture",
        "link_fixture",
        "assets_fixture",
        "release_links_fixture",
        "release_fixture",
        "token_fixture",
        "todo_fixture",
        "wiki_page_fixture",
        "wiki_attachment_link_fixture",
        "wiki_attachment_fixture",
        "project_config_fixture",
        "agent_fixture",
    ],
)
def test_parse_pydantic_schema(fixture, request):
    pydantic_model = request.getfixturevalue(fixture)
    try:
        sqlalchemy_model = pydantic_to_sqlalchemy(pydantic_model)
        pydantic_model_dict = {
            k: v for k, v in pydantic_model.model_dump().items() if v is not None
        }
        logger.debug(f"sqlalchemy_model for {fixture}:\n{sqlalchemy_model}\n")
        sqlalchemy_model_dict = {k: v for k, v in sqlalchemy_model.__dict__.items()}
        sqlalchemy_model_dict.pop("_sa_instance_state", None)
        logger.debug(f"sqlalchemy_model_dict for {fixture}:\n{sqlalchemy_model_dict}\n")

        assert sqlalchemy_model_dict == pydantic_model_dict
    except Exception as e:
        pytest.fail(f"Conversion failed for {fixture}: {e}")
