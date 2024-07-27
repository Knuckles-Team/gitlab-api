#!/usr/bin/env python
# coding: utf-8
from gitlab_api.version import __version__, __author__, __credits__
from gitlab_api.gitlab_api import Api
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
from gitlab_api.gitlab_db_models import (
    BaseDBModel,
    DeployTokenDBModel,
    RuleDBModel,
    AccessControlDBModel,
    SourcesDBModel,
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
    ApprovedByDBModel,
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
    CreatedByDBModel,
    UserDBModel,
    NamespaceDBModel,
    ContainerExpirationPolicyDBModel,
    PermissionsDBModel,
    StatisticsDBModel,
    LinksDBModel,
    DiffDBModel,
    DetailedStatusDBModel,
)
from gitlab_api.utils import pydantic_to_sqlalchemy

"""
GitLab API

A Python Wrapper for GitLab API
"""

__version__ = __version__
__author__ = __author__
__credits__ = __credits__

__all__ = [
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
    "Rule",
    "AccessControl",
    "Source",
    "Link",
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
    "Branch",
    "ApprovalRule",
    "MergeRequest",
    "GroupAccess",
    "DefaultBranchProtectionDefaults",
    "Group",
    "Webhook",
    "AccessLevel",
    "ApprovedBy",
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
    "CreatedBy",
    "User",
    "Namespace",
    "ContainerExpirationPolicy",
    "Permissions",
    "Statistics",
    "Links",
    "Diff",
    "DetailedStatus",
    "BaseDBModel",
    "DeployTokenDBModel",
    "RuleDBModel",
    "AccessControlDBModel",
    "SourcesDBModel",
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
    "ApprovedByDBModel",
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
    "GroupSamlIdentityDBModel",
    "CreatedByDBModel",
    "UserDBModel",
    "TestCaseDBModel",
    "TestSuiteDBModel",
    "TestReportDBModel",
    "TestReportTotalDBModel",
    "NamespaceDBModel",
    "ContainerExpirationPolicyDBModel",
    "PermissionsDBModel",
    "StatisticsDBModel",
    "LinksDBModel",
    "DiffDBModel",
    "DetailedStatusDBModel",
]
