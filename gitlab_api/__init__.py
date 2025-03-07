#!/usr/bin/env python
# coding: utf-8
from gitlab_api.version import __version__, __author__, __credits__
from gitlab_api.gitlab_api import Api
from gitlab_api.gitlab_input_models import (
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
)
from gitlab_api.gitlab_response_models import (
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
    Project,
    Runner,
    Job,
    Label,
    Tag,
    Topic,
    CIIDTokenComponents,
    ComplianceFrameworks,
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
    User,
    Namespace,
    ContainerExpirationPolicy,
    Statistics,
    Diff,
    DetailedStatus,
)
from gitlab_api.gitlab_db_models import (
    BaseDBModel,
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
    TagDBModel,
    TopicDBModel,
    CIIDTokenComponentsDBModel,
    ComplianceFrameworksDBModel,
    LabelDBModel,
    ProjectDBModel,
    RunnerDBModel,
    EpicDBModel,
    IssueDBModel,
    JobDBModel,
    ParentIDDBModel,
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
from gitlab_api.utils import (
    upsert,
    create_table,
    pydantic_to_sqlalchemy,
    pydantic_to_sqlalchemy_fallback,
    save_model,
    load_model,
    run_migrations,
)

"""
GitLab API

A Python Wrapper for GitLab API
"""

__version__ = __version__
__author__ = __author__
__credits__ = __credits__

__all__ = [
    "upsert",
    "create_table",
    "pydantic_to_sqlalchemy",
    "Api",
    "BranchModel",
    "CommitModel",
    "DeployTokenModel",
    "GroupModel",
    "JobModel",
    "MembersModel",
    "PackageModel",
    "PipelineModel",
    "ProjectModel",
    "ProtectedBranchModel",
    "MergeRequestModel",
    "MergeRequestRuleModel",
    "ReleaseModel",
    "RunnerModel",
    "UserModel",
    "WikiModel",
    "DeployToken",
    "Branch",
    "Rule",
    "AccessControl",
    "Source",
    "Link",
    "Tag",
    "Topic",
    "CIIDTokenComponents",
    "ComplianceFrameworks",
    "Label",
    "Assets",
    "Evidence",
    "ReleaseLinks",
    "Token",
    "ToDo",
    "WikiPage",
    "WikiAttachmentLink",
    "WikiAttachment",
    "Agent",
    "Agents",
    "Release",
    "ApprovalRule",
    "MergeRequest",
    "GroupAccess",
    "DefaultBranchProtectionDefaults",
    "Group",
    "Webhook",
    "AccessLevel",
    "Project",
    "Runner",
    "Job",
    "Pipeline",
    "PackageLink",
    "PackageVersion",
    "Package",
    "Contributor",
    "CommitStats",
    "CommitSignature",
    "Comment",
    "Commit",
    "Membership",
    "IssueStats",
    "Milestone",
    "TimeStats",
    "TaskCompletionStatus",
    "References",
    "Artifact",
    "ArtifactsFile",
    "RunnerManager",
    "Configuration",
    "Iteration",
    "Identity",
    "GroupSamlIdentity",
    "User",
    "Namespace",
    "ContainerExpirationPolicy",
    "Statistics",
    "Diff",
    "DetailedStatus",
    "BaseDBModel",
    "DeployTokenDBModel",
    "RuleDBModel",
    "AccessControlDBModel",
    "SourceDBModel",
    "LinkDBModel",
    "AssetsDBModel",
    "EvidenceDBModel",
    "ReleaseLinksDBModel",
    "TokenDBModel",
    "ToDoDBModel",
    "WikiPageDBModel",
    "WikiAttachmentLinkDBModel",
    "WikiAttachmentDBModel",
    "AgentDBModel",
    "AgentsDBModel",
    "ReleaseDBModel",
    "BranchDBModel",
    "ApprovalRuleDBModel",
    "MergeRequestDBModel",
    "MergeApprovalsDBModel",
    "GroupAccessDBModel",
    "DefaultBranchProtectionDefaultsDBModel",
    "GroupDBModel",
    "WebhookDBModel",
    "AccessLevelDBModel",
    "ProjectDBModel",
    "RunnerDBModel",
    "EpicDBModel",
    "IssueDBModel",
    "JobDBModel",
    "PipelineDBModel",
    "PipelineVariableDBModel",
    "PackageLinkDBModel",
    "PackageVersionDBModel",
    "PackageDBModel",
    "LabelDBModel",
    "ProjectConfigDBModel",
    "ContributorDBModel",
    "CommitStatsDBModel",
    "CommitSignatureDBModel",
    "CommentDBModel",
    "CommitDBModel",
    "MembershipDBModel",
    "IssueStatsDBModel",
    "MilestoneDBModel",
    "TimeStatsDBModel",
    "TaskCompletionStatusDBModel",
    "ReferencesDBModel",
    "ArtifactDBModel",
    "ArtifactsFileDBModel",
    "RunnerManagerDBModel",
    "ConfigurationDBModel",
    "IterationDBModel",
    "IdentityDBModel",
    "ParentIDDBModel",
    "GroupSamlIdentityDBModel",
    "UserDBModel",
    "TagDBModel",
    "TopicDBModel",
    "CIIDTokenComponentsDBModel",
    "ComplianceFrameworksDBModel",
    "TestCaseDBModel",
    "TestSuiteDBModel",
    "TestReportDBModel",
    "TestReportTotalDBModel",
    "NamespaceDBModel",
    "ContainerExpirationPolicyDBModel",
    "PermissionsDBModel",
    "StatisticsDBModel",
    "DiffDBModel",
    "DetailedStatusDBModel",
]
