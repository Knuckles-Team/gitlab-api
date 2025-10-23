#!/usr/bin/python
# coding: utf-8
from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime, ForeignKey, Text, Table, Column
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import (
    relationship,
    declarative_base,
    Mapped,
)
from sqlalchemy import Integer, Boolean
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy import (
    Float,
)

BaseDBModel = declarative_base()


# Evidence Model
class EvidenceDBModel(BaseDBModel):
    __tablename__ = "evidences"

    def __eq__(self, other):
        if isinstance(other, EvidenceDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Evidence")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    sha: Mapped[str] = mapped_column(String, nullable=True)
    filepath: Mapped[str] = mapped_column(String, nullable=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    release_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="releases.id", name="fk_evidence_release"),
        nullable=True,
    )
    releases: Mapped["ReleaseDBModel"] = relationship(back_populates="evidences")


# IssueStats Model
class IssueStatsDBModel(BaseDBModel):
    __tablename__ = "issue_stats"

    def __eq__(self, other):
        if isinstance(other, IssueStatsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="IssueStats")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    total: Mapped[int] = mapped_column(Integer, nullable=True)
    closed: Mapped[int] = mapped_column(Integer, nullable=True)
    opened: Mapped[int] = mapped_column(Integer, nullable=True)
    milestones: Mapped[List["MilestoneDBModel"]] = relationship(
        back_populates="issue_stats"
    )


# Milestone Model
class MilestoneDBModel(BaseDBModel):
    __tablename__ = "milestones"

    def __eq__(self, other):
        if isinstance(other, MilestoneDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Milestone")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    iid: Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    due_date: Mapped[str] = mapped_column(String, nullable=True)
    start_date: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)

    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="projects.id", name="fk_milestone_project_id"),
        nullable=True,
    )
    project: Mapped["ProjectDBModel"] = relationship(back_populates="milestones")

    issue_stats_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="issue_stats.id", name="fk_milestone_issue_stats"),
        nullable=True,
    )
    issue_stats: Mapped["IssueStatsDBModel"] = relationship(back_populates="milestones")

    release_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="releases.id", name="fk_milestone_release"),
        nullable=True,
    )
    releases: Mapped["ReleaseDBModel"] = relationship(back_populates="milestones")
    issues: Mapped[List["IssueDBModel"]] = relationship(back_populates="milestone")


# DeployToken Model
class DeployTokenDBModel(BaseDBModel):
    __tablename__ = "deploy_tokens"

    def __eq__(self, other):
        if isinstance(other, DeployTokenDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="DeployToken")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    token: Mapped[str] = mapped_column(String, nullable=True)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=True)
    expired: Mapped[bool] = mapped_column(Boolean, nullable=True)
    scopes = mapped_column(ARRAY(String), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=True)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="users.id", name="fk_deploy_token_user"),
        nullable=True,
    )
    user: Mapped["UserDBModel"] = relationship(back_populates="deploy_tokens")


# Rule Model
class RuleDBModel(BaseDBModel):
    __tablename__ = "rules"

    def __eq__(self, other):
        if isinstance(other, RuleDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Rule")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    commit_committer_check: Mapped[bool] = mapped_column(Boolean, default=False)
    commit_committer_name_check: Mapped[bool] = mapped_column(Boolean, default=False)
    reject_unsigned_commits: Mapped[bool] = mapped_column(Boolean, default=False)
    commit_message_regex: Mapped[str] = mapped_column(String, nullable=True)
    commit_message_negative_regex: Mapped[str] = mapped_column(String, nullable=True)
    branch_name_regex: Mapped[str] = mapped_column(String, nullable=True)
    deny_delete_tag: Mapped[bool] = mapped_column(Boolean, default=False)
    member_check: Mapped[bool] = mapped_column(Boolean, default=False)
    prevent_secrets: Mapped[bool] = mapped_column(Boolean, default=False)
    author_email_regex: Mapped[str] = mapped_column(String, nullable=True)
    file_name_regex: Mapped[str] = mapped_column(String, nullable=True)
    max_file_size: Mapped[int] = mapped_column(Integer, nullable=True)


# AccessControl Model
class AccessControlDBModel(BaseDBModel):
    __tablename__ = "access_controls"

    def __eq__(self, other):
        if isinstance(other, AccessControlDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="AccessControl")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    access_level: Mapped[int] = mapped_column(Integer, nullable=True)
    member_role_id: Mapped[int] = mapped_column(Integer, nullable=True)


# Source Model
class SourceDBModel(BaseDBModel):
    __tablename__ = "sources"

    def __eq__(self, other):
        if isinstance(other, SourceDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Sources")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    format: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=True)

    assets_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="assets.id", name="fk_sources_assets"), nullable=True
    )
    assets: Mapped["AssetsDBModel"] = relationship(back_populates="sources")


# Links Model
class LinkDBModel(BaseDBModel):
    __tablename__ = "links"

    def __eq__(self, other):
        if isinstance(other, LinkDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Links")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    self_link: Mapped[str] = mapped_column(String, nullable=True)
    issues: Mapped[str] = mapped_column(String, nullable=True)
    merge_requests: Mapped[str] = mapped_column(String, nullable=True)
    repo_branches: Mapped[str] = mapped_column(String, nullable=True)
    labels: Mapped[str] = mapped_column(String, nullable=True)
    events: Mapped[str] = mapped_column(String, nullable=True)
    members: Mapped[str] = mapped_column(String, nullable=True)
    cluster_agents: Mapped[str] = mapped_column(String, nullable=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    award_emoji: Mapped[str] = mapped_column(String, nullable=True)
    project: Mapped[str] = mapped_column(String, nullable=True)
    closed_as_duplicate_of: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=True)
    direct_asset_url: Mapped[str] = mapped_column(String, nullable=True)
    link_type: Mapped[str] = mapped_column(String, nullable=True)
    assets_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="assets.id", name="fk_links_assets"), nullable=True
    )
    assets: Mapped["AssetsDBModel"] = relationship(back_populates="links")
    wiki_attachment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="wiki_attachments.id", name="fk_links_wiki_attachments"),
        nullable=True,
    )
    wiki_attachment: Mapped["WikiAttachmentDBModel"] = relationship(
        back_populates="link"
    )

    projects_links: Mapped["ProjectDBModel"] = relationship(
        back_populates="links", foreign_keys="[ProjectDBModel.links_id]"
    )
    projects_additional_links: Mapped["ProjectDBModel"] = relationship(
        back_populates="additional_links",
        foreign_keys="[ProjectDBModel.additional_links_id]",
    )


# Assets Model
class AssetsDBModel(BaseDBModel):
    __tablename__ = "assets"

    def __eq__(self, other):
        if isinstance(other, AssetsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Assets")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    count: Mapped[int] = mapped_column(Integer, nullable=True)
    sources: Mapped[List["SourceDBModel"]] = relationship(back_populates="assets")
    links: Mapped[List["LinkDBModel"]] = relationship(back_populates="assets")
    evidence_file_path: Mapped[str] = mapped_column(String, nullable=True)
    releases: Mapped[List["ReleaseDBModel"]] = relationship(back_populates="assets")


# ReleaseLinks Model
class ReleaseLinksDBModel(BaseDBModel):
    __tablename__ = "release_links"

    def __eq__(self, other):
        if isinstance(other, ReleaseLinksDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="ReleaseLinks")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    closed_issues_url: Mapped[str] = mapped_column(String, nullable=True)
    closed_merge_requests_url: Mapped[str] = mapped_column(String, nullable=True)
    edit_url: Mapped[str] = mapped_column(String, nullable=True)
    merged_merge_requests_url: Mapped[str] = mapped_column(String, nullable=True)
    opened_issues_url: Mapped[str] = mapped_column(String, nullable=True)
    opened_merge_requests_url: Mapped[str] = mapped_column(String, nullable=True)
    self_link: Mapped[str] = mapped_column(String, nullable=True)
    releases: Mapped["ReleaseDBModel"] = relationship(
        back_populates="links",
    )


# Token Model
class TokenDBModel(BaseDBModel):
    __tablename__ = "tokens"

    def __eq__(self, other):
        if isinstance(other, TokenDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Token")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    token: Mapped[str] = mapped_column(String, nullable=True)
    token_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


# To-Do Model
class ToDoDBModel(BaseDBModel):
    __tablename__ = "todos"

    def __eq__(self, other):
        if isinstance(other, ToDoDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="ToDo")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    action_name: Mapped[str] = mapped_column(String, nullable=True)
    target_type: Mapped[str] = mapped_column(String, nullable=True)
    target_url: Mapped[str] = mapped_column(String, nullable=True)
    body: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="projects.id", name="fk_todo_project_id"),
        nullable=True,
    )
    project: Mapped["ProjectDBModel"] = relationship(
        "ProjectDBModel", back_populates="todos"
    )

    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="groups.id", name="fk_todo_group"), nullable=True
    )
    group: Mapped["GroupDBModel"] = relationship(back_populates="todos")

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_todo_author"), nullable=True
    )
    author: Mapped["UserDBModel"] = relationship(back_populates="todos")

    target_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="issues.id", name="fk_todo_target"), nullable=True
    )
    target: Mapped["IssueDBModel"] = relationship(
        back_populates="todos", remote_side="[IssueDBModel.id]"
    )


# WikiPage Model
class WikiPageDBModel(BaseDBModel):
    __tablename__ = "wiki_pages"

    def __eq__(self, other):
        if isinstance(other, WikiPageDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="WikiPage")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    content: Mapped[str] = mapped_column(String, nullable=True)
    format: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    encoding: Mapped[str] = mapped_column(String, nullable=True)


# WikiAttachmentLink Model
class WikiAttachmentLinkDBModel(BaseDBModel):
    __tablename__ = "wiki_attachment_links"

    def __eq__(self, other):
        if isinstance(other, WikiAttachmentLinkDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="WikiAttachmentLink")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    url: Mapped[str] = mapped_column(String, nullable=True)
    markdown: Mapped[str] = mapped_column(String, nullable=True)


# PipelineVariable Model
class PipelineVariableDBModel(BaseDBModel):
    __tablename__ = "pipeline_variables"

    def __eq__(self, other):
        if isinstance(other, PipelineVariableDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="PipelineVariable")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    key: Mapped[str] = mapped_column(String, nullable=True)
    variable_type: Mapped[str] = mapped_column(String, nullable=True)
    value: Mapped[str] = mapped_column(String, nullable=True)
    pipeline_schedule_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="pipeline_schedules.id", name="fk_pipeline_schedule_variables"
        ),
        nullable=True,
    )
    pipeline_schedule: Mapped["PipelineScheduleDBModel"] = relationship(
        back_populates="variables"
    )


# WikiAttachment Model
class WikiAttachmentDBModel(BaseDBModel):
    __tablename__ = "wiki_attachments"

    def __eq__(self, other):
        if isinstance(other, WikiAttachmentDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="WikiAttachment")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    file_name: Mapped[str] = mapped_column(String, nullable=True)
    file_path: Mapped[str] = mapped_column(String, nullable=True)
    branch: Mapped[str] = mapped_column(String, nullable=True)

    link_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="wiki_attachment_links.id", name="fk_wiki_attachment_links"),
        nullable=True,
    )
    link: Mapped["LinkDBModel"] = relationship(back_populates="wiki_attachment")


# Agent Model
class AgentDBModel(BaseDBModel):
    __tablename__ = "agent"

    def __eq__(self, other):
        if isinstance(other, AgentDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Agent")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})

    config_project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="configurations.id", name="fk_agent_configurations"),
        nullable=True,
    )
    config_project: Mapped["ConfigurationDBModel"] = relationship(
        back_populates="agent"
    )


# Agents Model
class AgentsDBModel(BaseDBModel):
    __tablename__ = "agents"

    def __eq__(self, other):
        if isinstance(other, AgentsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="Agents")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})

    job_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("jobs.id", name="fk_agents_jobs"), nullable=True
    )
    job: Mapped["JobDBModel"] = relationship(
        "JobDBModel",
        back_populates="agents",
        primaryjoin="JobDBModel.id == foreign(AgentsDBModel.job_id)",
    )

    pipeline_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_agents_pipelines"),
        nullable=True,
    )
    pipeline: Mapped["PipelineDBModel"] = relationship(back_populates="agents")

    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="projects.id", name="fk_agents_projects"),
        nullable=True,
    )
    project: Mapped["ProjectDBModel"] = relationship(back_populates="agents")

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_agents_users"), nullable=True
    )
    user: Mapped["UserDBModel"] = relationship(back_populates="agents")


# Release Model
class ReleaseDBModel(BaseDBModel):
    __tablename__ = "releases"

    def __eq__(self, other):
        if isinstance(other, ReleaseDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Release")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    tag_name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    upcoming_release: Mapped[bool] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    released_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    commit_path: Mapped[str] = mapped_column(String, nullable=True)
    tag_path: Mapped[str] = mapped_column(String, nullable=True)
    evidence_sha: Mapped[str] = mapped_column(String, nullable=True)

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_release_author"), nullable=True
    )
    author: Mapped["UserDBModel"] = relationship(
        back_populates="releases", foreign_keys=[author_id]
    )

    commit_id: Mapped[int] = mapped_column(
        String,
        ForeignKey(column="commits.id", name="fk_release_commits"),
        nullable=True,
    )
    commit: Mapped["CommitDBModel"] = relationship(
        back_populates="releases", foreign_keys=[commit_id]
    )
    milestones: Mapped[List["MilestoneDBModel"]] = relationship(
        back_populates="releases"
    )
    evidences: Mapped[List["EvidenceDBModel"]] = relationship(back_populates="releases")
    assets_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="assets.id", name="fk_release_assets"), nullable=True
    )
    assets: Mapped[List["AssetsDBModel"]] = relationship(
        back_populates="releases", foreign_keys=[assets_id]
    )

    links_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="release_links.id", name="fk_release_links"),
        nullable=True,
    )
    links: Mapped["ReleaseLinksDBModel"] = relationship(
        back_populates="releases", foreign_keys=[links_id]
    )


# AccessLevel Model
class AccessLevelDBModel(BaseDBModel):
    __tablename__ = "access_levels"

    def __eq__(self, other):
        if isinstance(other, AccessLevelDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="AccessLevel")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    access_level: Mapped[int] = mapped_column(Integer, nullable=True)
    access_level_description: Mapped[str] = mapped_column(String, nullable=True)
    environment_id: Mapped[int] = mapped_column(
        ForeignKey("environments.id"), nullable=True
    )
    deploy_key_id: Mapped[int] = mapped_column(Integer, nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="users.id", name="fk_access_level_users"),
        nullable=True,
    )
    user: Mapped["UserDBModel"] = relationship(back_populates="access_levels")

    group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="groups.id", name="fk_access_level_groups"),
        nullable=True,
    )
    group: Mapped["GroupDBModel"] = relationship(
        back_populates="access_levels",
    )
    # Specify the foreign keys for each relationship
    branches_push_access: Mapped[List["BranchDBModel"]] = relationship(
        back_populates="push_access_levels",
        foreign_keys="[BranchDBModel.push_access_levels_id]",
    )

    branches_merge_access: Mapped[List["BranchDBModel"]] = relationship(
        back_populates="merge_access_levels",
        foreign_keys="[BranchDBModel.merge_access_levels_id]",
    )

    branches_unprotect_access: Mapped[List["BranchDBModel"]] = relationship(
        back_populates="unprotect_access_levels",
        foreign_keys="[BranchDBModel.unprotect_access_levels_id]",
    )
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=True)
    tag: Mapped["TagDBModel"] = relationship(back_populates="create_access_levels")


# Branch Model
class BranchDBModel(BaseDBModel):
    __tablename__ = "branches"

    def __eq__(self, other):
        if isinstance(other, BranchDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Branch")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    merged: Mapped[bool] = mapped_column(Boolean, nullable=True)
    protected: Mapped[bool] = mapped_column(Boolean, nullable=True)
    default: Mapped[bool] = mapped_column(Boolean, nullable=True)
    developers_can_push: Mapped[bool] = mapped_column(Boolean, nullable=True)
    developers_can_merge: Mapped[bool] = mapped_column(Boolean, nullable=True)
    can_push: Mapped[bool] = mapped_column(Boolean, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    allow_force_push: Mapped[bool] = mapped_column(Boolean, nullable=True)
    code_owner_approval_required: Mapped[bool] = mapped_column(Boolean, nullable=True)
    inherited: Mapped[bool] = mapped_column(Boolean, nullable=True)

    commit_id: Mapped[str] = mapped_column(
        String,
        ForeignKey(column="commits.id", name="fk_branch_commits"),
        nullable=True,
    )
    commit: Mapped["CommitDBModel"] = relationship(back_populates="branches")

    push_access_levels_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="access_levels.id", name="fk_branch_push_access_levels"),
        nullable=True,
    )
    push_access_levels: Mapped["AccessLevelDBModel"] = relationship(
        back_populates="branches_push_access",
        foreign_keys="[BranchDBModel.push_access_levels_id]",
    )

    merge_access_levels_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="access_levels.id", name="fk_branch_merge_access_levels"),
        nullable=True,
    )
    merge_access_levels: Mapped["AccessLevelDBModel"] = relationship(
        back_populates="branches_merge_access",
        foreign_keys="[BranchDBModel.merge_access_levels_id]",
    )

    unprotect_access_levels_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="access_levels.id", name="fk_branch_unprotect_access_levels"),
        nullable=True,
    )
    unprotect_access_levels: Mapped["AccessLevelDBModel"] = relationship(
        back_populates="branches_unprotect_access",
        foreign_keys="[BranchDBModel.unprotect_access_levels_id]",
    )
    approval_rules: Mapped[List["ApprovalRuleDBModel"]] = relationship(
        back_populates="protected_branches"
    )


merge_request_labels = Table(
    "merge_request_labels",
    BaseDBModel.metadata,
    Column(
        "merge_request_id", Integer, ForeignKey("merge_requests.id"), primary_key=True
    ),
    Column("label_id", Integer, ForeignKey("labels.id"), primary_key=True),
)


# Label Model
class LabelDBModel(BaseDBModel):
    __tablename__ = "labels"

    def __eq__(self, other):
        if isinstance(other, LabelDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    base_type: Mapped[str] = mapped_column(String, default="Label")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    color: Mapped[str] = mapped_column(String, nullable=True)
    text_color: Mapped[str] = mapped_column(String, nullable=True)
    description = mapped_column(Text, nullable=True)
    description_html = mapped_column(Text, nullable=True)
    open_issues_count: Mapped[int] = mapped_column(Integer, nullable=True)
    closed_issues_count: Mapped[int] = mapped_column(Integer, nullable=True)
    open_merge_requests_count: Mapped[int] = mapped_column(Integer, nullable=True)
    subscribed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=True)
    is_project_label: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        secondary=merge_request_labels,  # Link to the association table
        back_populates="labels",
    )


class ComplianceFrameworksDBModel(BaseDBModel):
    __tablename__ = "compliance_frameworks"

    def __eq__(self, other):
        if isinstance(other, ComplianceFrameworksDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="ComplianceFrameworks")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=True
    )
    project: Mapped["ProjectDBModel"] = relationship(
        back_populates="compliance_frameworks"
    )


class CIIDTokenComponentsDBModel(BaseDBModel):
    __tablename__ = "ci_id_token_sub_claim_components"

    def __eq__(self, other):
        if isinstance(other, CIIDTokenComponentsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="CIIDTokenComponents")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=True
    )
    project: Mapped["ProjectDBModel"] = relationship(
        back_populates="ci_id_token_sub_claim_components"
    )


class TopicDBModel(BaseDBModel):
    __tablename__ = "topics"

    def __eq__(self, other):
        if isinstance(other, TopicDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="Topic")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    total_projects_count: Mapped[int] = mapped_column(Integer, nullable=True)
    organization_id: Mapped[int] = mapped_column(Integer, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=True
    )
    project: Mapped["ProjectDBModel"] = relationship(back_populates="topics")


class DeployableDBModel(BaseDBModel):
    __tablename__ = "deployables"

    def __eq__(self, other):
        if isinstance(other, EnvironmentDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    stage: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    ref: Mapped[str] = mapped_column(String, nullable=True)
    tag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    coverage: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    duration: Mapped[float] = mapped_column(Float, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    commit_id: Mapped[str] = mapped_column(ForeignKey("commits.id"), nullable=True)
    pipeline_id: Mapped[int] = mapped_column(ForeignKey("pipelines.id"), nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    artifacts_expire_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=True)
    project: Mapped["ProjectDBModel"] = relationship(back_populates="deployables")
    pipeline: Mapped["PipelineDBModel"] = relationship(back_populates="deployables")
    user: Mapped["UserDBModel"] = relationship(back_populates="deployables")
    commit: Mapped["CommitDBModel"] = relationship(back_populates="deployables")
    artifacts: Mapped[List["ArtifactDBModel"]] = relationship(
        back_populates="deployable"
    )
    deployments: Mapped[List["LastDeploymentDBModel"]] = relationship(
        back_populates="deployable"
    )


class LastDeploymentDBModel(BaseDBModel):
    __tablename__ = "last_deployments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=True)
    iid: Mapped[int] = mapped_column(Integer, nullable=True)
    ref: Mapped[str] = mapped_column(String, nullable=True)
    sha: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    deployable_id: Mapped[int] = mapped_column(
        ForeignKey("deployables.id"), nullable=True
    )
    user: Mapped["UserDBModel"] = relationship(back_populates="deployments")
    deployable: Mapped["DeployableDBModel"] = relationship(back_populates="deployments")
    environment: Mapped["EnvironmentDBModel"] = relationship(
        back_populates="last_deployment", uselist=False  # One-to-one
    )


class ClusterAgentDBModel(BaseDBModel):
    __tablename__ = "cluster_agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    project_config_id: Mapped[int] = mapped_column(
        ForeignKey("project_configs.primary_id"), nullable=True
    )
    project_config: Mapped["ProjectConfigDBModel"] = relationship(
        back_populates="cluster_agents"
    )
    created_by_user: Mapped["UserDBModel"] = relationship(
        back_populates="cluster_agents_created"
    )
    environment: Mapped["EnvironmentDBModel"] = relationship(
        back_populates="cluster_agent"
    )


class EnvironmentDBModel(BaseDBModel):
    __tablename__ = "environments"

    def __eq__(self, other):
        if isinstance(other, EnvironmentDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    base_type: Mapped[str] = mapped_column(String, default="Environment")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    external_url: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    tier: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    enable_advanced_logs_querying: Mapped[bool] = mapped_column(Boolean, nullable=True)
    logs_api_path: Mapped[str] = mapped_column(String, nullable=True)
    auto_stop_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    kubernetes_namespace: Mapped[str] = mapped_column(String, nullable=True)
    flux_resource_path: Mapped[str] = mapped_column(String, nullable=True)
    auto_stop_setting: Mapped[str] = mapped_column(String, nullable=True)
    required_approval_count: Mapped[int] = mapped_column(Integer, nullable=True)
    deploy_access_levels: Mapped[List["AccessLevelDBModel"]] = relationship(
        "AccessLevelDBModel", backref="environment", cascade="all, delete-orphan"
    )
    last_deployment_id: Mapped[int] = mapped_column(
        ForeignKey("last_deployments.id"), nullable=True, unique=True
    )
    last_deployment: Mapped["LastDeploymentDBModel"] = relationship(
        back_populates="environment"
    )
    cluster_agent_id: Mapped[int] = mapped_column(
        ForeignKey("cluster_agents.id"), nullable=True
    )
    cluster_agent: Mapped["ClusterAgentDBModel"] = relationship(
        back_populates="environment"
    )


class TagDBModel(BaseDBModel):
    __tablename__ = "tags"

    def __eq__(self, other):
        if isinstance(other, TagDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    base_type: Mapped[str] = mapped_column(String, default="Tag")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    tag: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)

    merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        back_populates="tag_list"
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=True
    )
    project: Mapped["ProjectDBModel"] = relationship(back_populates="tag_list")

    packages: Mapped[List["PackageDBModel"]] = relationship(
        "PackageDBModel", back_populates="tags"
    )
    runners: Mapped[List["RunnerDBModel"]] = relationship(back_populates="tag_list")
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    job: Mapped["JobDBModel"] = relationship(back_populates="tag_list")
    create_access_levels: Mapped[List["AccessLevelDBModel"]] = relationship(
        back_populates="tag", cascade="all, delete-orphan"
    )


# ApprovalRule Model
class ApprovalRuleDBModel(BaseDBModel):
    __tablename__ = "approval_rules"

    def __eq__(self, other):
        if isinstance(other, ApprovalRuleDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="ApprovalRule")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    rule_type: Mapped[str] = mapped_column(String, nullable=True)
    approvals_required: Mapped[int] = mapped_column(Integer, nullable=True)
    contains_hidden_groups: Mapped[bool] = mapped_column(Boolean, nullable=True)
    applies_to_all_protected_branches: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    source_rule: Mapped[str] = mapped_column(String, nullable=True)
    approved: Mapped[bool] = mapped_column(Boolean, nullable=True)
    overridden: Mapped[bool] = mapped_column(Boolean, nullable=True)

    eligible_approvers_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="users.id", name="fk_eligible_approvers_rules"),
        nullable=True,
    )
    eligible_approvers: Mapped["UserDBModel"] = relationship(
        back_populates="approval_rules",
        foreign_keys="[ApprovalRuleDBModel.eligible_approvers_id]",
    )

    users_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="users.id", name="fk_users_rules"),
        nullable=True,
    )
    users: Mapped["UserDBModel"] = relationship(
        back_populates="approval_rules", foreign_keys="[ApprovalRuleDBModel.users_id]"
    )

    approved_by_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="users.id", name="fk_approval_rule_user_by_id"),
        nullable=True,
    )
    approved_by: Mapped["UserDBModel"] = relationship(
        back_populates="approval_rules",
        foreign_keys="[ApprovalRuleDBModel.approved_by_id]",
    )

    groups_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="groups.id", name="fk_groups_rules"),
        nullable=True,
    )
    groups: Mapped["GroupDBModel"] = relationship(back_populates="approval_rules")

    protected_branches_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="branches.id", name="fk_protected_branches_rules"),
        nullable=True,
    )
    protected_branches: Mapped["BranchDBModel"] = relationship(
        back_populates="approval_rules"
    )

    merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        back_populates="approval_rules"
    )


class SettingDBModel(BaseDBModel):
    __tablename__ = "settings"

    def __eq__(self, other):
        if isinstance(other, ApprovalRuleDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Setting")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    value: Mapped[bool] = mapped_column(Boolean, nullable=True)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=True)
    inherited_from: Mapped[str] = mapped_column(String, nullable=True)
    merge_request_rule_setting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("merge_request_rule_settings.id"), nullable=True
    )


class MergeRequestRuleSettingsDBModel(BaseDBModel):
    __tablename__ = "merge_request_rule_settings"

    def __eq__(self, other):
        if isinstance(other, ApprovalRuleDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="ApprovalRule")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})

    allow_author_approval: Mapped["SettingDBModel"] = relationship(
        "SettingDBModel",
        primaryjoin="and_(MergeRequestRuleSettingsDBModel.id==SettingDBModel.merge_request_rule_setting_id, "
        "SettingDBModel.id==foreign(SettingDBModel.id))",
        uselist=False,
        cascade="all, delete-orphan",
    )
    allow_committer_approval: Mapped["SettingDBModel"] = relationship(
        "SettingDBModel",
        primaryjoin="and_(MergeRequestRuleSettingsDBModel.id==SettingDBModel.merge_request_rule_setting_id, "
        "SettingDBModel.id==foreign(SettingDBModel.id))",
        uselist=False,
        cascade="all, delete-orphan",
    )
    allow_overrides_to_approver_list_per_merge_request: Mapped["SettingDBModel"] = (
        relationship(
            "SettingDBModel",
            primaryjoin="and_(MergeRequestRuleSettingsDBModel.id==SettingDBModel.merge_request_rule_setting_id, "
            "SettingDBModel.id==foreign(SettingDBModel.id))",
            uselist=False,
            cascade="all, delete-orphan",
        )
    )
    retain_approvals_on_push: Mapped["SettingDBModel"] = relationship(
        "SettingDBModel",
        primaryjoin="and_(MergeRequestRuleSettingsDBModel.id==SettingDBModel.merge_request_rule_setting_id, "
        "SettingDBModel.id==foreign(SettingDBModel.id))",
        uselist=False,
        cascade="all, delete-orphan",
    )
    selective_code_owner_removals: Mapped["SettingDBModel"] = relationship(
        "SettingDBModel",
        primaryjoin="and_(MergeRequestRuleSettingsDBModel.id==SettingDBModel.merge_request_rule_setting_id, "
        "SettingDBModel.id==foreign(SettingDBModel.id))",
        uselist=False,
        cascade="all, delete-orphan",
    )
    require_password_to_approve: Mapped["SettingDBModel"] = relationship(
        "SettingDBModel",
        primaryjoin="and_(MergeRequestRuleSettingsDBModel.id==SettingDBModel.merge_request_rule_setting_id, "
        "SettingDBModel.id==foreign(SettingDBModel.id))",
        uselist=False,
        cascade="all, delete-orphan",
    )
    require_reauthentication_to_approve: Mapped["SettingDBModel"] = relationship(
        "SettingDBModel",
        primaryjoin="and_(MergeRequestRuleSettingsDBModel.id==SettingDBModel.merge_request_rule_setting_id, "
        "SettingDBModel.id==foreign(SettingDBModel.id))",
        uselist=False,
        cascade="all, delete-orphan",
    )


# Association table for MergeRequest assignees
merge_request_assignees = Table(
    "merge_request_assignees",
    BaseDBModel.metadata,
    Column(
        "merge_request_id", Integer, ForeignKey("merge_requests.id"), primary_key=True
    ),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)

# Association table for MergeRequest reviewers
merge_request_reviewers = Table(
    "merge_request_reviewers",
    BaseDBModel.metadata,
    Column(
        "merge_request_id", Integer, ForeignKey("merge_requests.id"), primary_key=True
    ),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class MergeRequestDBModel(BaseDBModel):
    __tablename__ = "merge_requests"

    def __eq__(self, other):
        if isinstance(other, MergeRequestDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="MergeRequest")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    iid: Mapped[int] = mapped_column(Integer, nullable=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    imported: Mapped[bool] = mapped_column(Boolean, nullable=True)
    imported_from: Mapped[str] = mapped_column(String, nullable=True)
    merged_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    merge_after: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    prepared_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    target_branch: Mapped[str] = mapped_column(String, nullable=True)
    source_branch: Mapped[str] = mapped_column(String, nullable=True)
    upvotes: Mapped[int] = mapped_column(Integer, nullable=True)
    downvotes: Mapped[int] = mapped_column(Integer, nullable=True)
    source_project_id: Mapped[int] = mapped_column(Integer, nullable=True)
    target_project_id: Mapped[int] = mapped_column(Integer, nullable=True)
    labels = mapped_column(ARRAY(String), nullable=True)
    draft: Mapped[bool] = mapped_column(Boolean, nullable=True)
    work_in_progress: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_when_pipeline_succeeds: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_status: Mapped[str] = mapped_column(String, nullable=True)
    detailed_merge_status: Mapped[str] = mapped_column(String, nullable=True)
    sha: Mapped[str] = mapped_column(String, nullable=True)
    merge_commit_sha: Mapped[str] = mapped_column(String, nullable=True)
    squash_commit_sha: Mapped[str] = mapped_column(String, nullable=True)
    user_notes_count: Mapped[int] = mapped_column(Integer, nullable=True)
    discussion_locked: Mapped[bool] = mapped_column(Boolean, nullable=True)
    should_remove_source_branch: Mapped[bool] = mapped_column(Boolean, nullable=True)
    force_remove_source_branch: Mapped[bool] = mapped_column(Boolean, nullable=True)
    allow_collaboration: Mapped[bool] = mapped_column(Boolean, nullable=True)
    allow_maintainer_to_push: Mapped[bool] = mapped_column(Boolean, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    squash: Mapped[bool] = mapped_column(Boolean, nullable=True)
    has_conflicts: Mapped[bool] = mapped_column(Boolean, nullable=True)
    blocking_discussions_resolved: Mapped[bool] = mapped_column(Boolean, nullable=True)
    approvals_before_merge: Mapped[int] = mapped_column(Integer, nullable=True)
    changes_count: Mapped[str] = mapped_column(String, nullable=True)
    subscribed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    overflow: Mapped[bool] = mapped_column(Boolean, nullable=True)
    # Relationships
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    author: Mapped["UserDBModel"] = relationship(
        back_populates="authored_merge_requests"
    )
    assignee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    assignee: Mapped["UserDBModel"] = relationship(
        back_populates="assigned_merge_requests"
    )
    assignees = relationship(
        "UserDBModel",
        secondary="merge_request_assignees",
        back_populates="assigned_merge_requests_list",
    )
    reviewers = relationship(
        "UserDBModel",
        secondary="merge_request_reviewers",
        back_populates="reviewed_merge_requests",
    )
    milestone_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("milestones.id"), nullable=True
    )
    milestone: Mapped["MilestoneDBModel"] = relationship(
        back_populates="merge_requests"
    )
    merged_by_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    merged_by: Mapped["UserDBModel"] = relationship(
        back_populates="merged_merge_requests"
    )
    merge_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    merge_user: Mapped["UserDBModel"] = relationship(
        back_populates="merge_user_merge_requests"
    )
    closed_by_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    closed_by: Mapped["UserDBModel"] = relationship(
        back_populates="closed_merge_requests"
    )
    references_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("references.id"), nullable=True
    )
    references: Mapped["ReferencesDBModel"] = relationship(
        back_populates="merge_requests"
    )
    time_stats_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("time_stats.id"), nullable=True
    )
    time_stats: Mapped["TimeStatsDBModel"] = relationship(
        back_populates="merge_requests"
    )
    task_completion_status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("task_completion_statuses.id"), nullable=True
    )
    task_completion_status: Mapped["TaskCompletionStatusDBModel"] = relationship(
        back_populates="merge_requests"
    )
    changes = relationship("DiffDBModel", back_populates="merge_requests")
    project: Mapped["ProjectDBModel"] = relationship(back_populates="merge_requests")


class RootStorageStatisticsDBModel(BaseDBModel):
    __tablename__ = "root_storage_statistics"

    def __eq__(self, other):
        if isinstance(other, RootStorageStatisticsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="RootStorageStatistics")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    storage_size: Mapped[int] = mapped_column(Integer, nullable=True)
    repository_size: Mapped[int] = mapped_column(Integer, nullable=True)
    wiki_size: Mapped[int] = mapped_column(Integer, nullable=True)
    lfs_objects_size: Mapped[int] = mapped_column(Integer, nullable=True)
    job_artifacts_size: Mapped[int] = mapped_column(Integer, nullable=True)
    pipeline_artifacts_size: Mapped[int] = mapped_column(Integer, nullable=True)
    packages_size: Mapped[int] = mapped_column(Integer, nullable=True)
    snippets_size: Mapped[int] = mapped_column(Integer, nullable=True)
    uploads_size: Mapped[int] = mapped_column(Integer, nullable=True)
    container_registry_size: Mapped[int] = mapped_column(Integer, nullable=True)
    build_artifacts_size: Mapped[int] = mapped_column(Integer, nullable=True)


# GroupAccess Model
class GroupAccessDBModel(BaseDBModel):
    __tablename__ = "group_accesses"

    def __eq__(self, other):
        if isinstance(other, GroupAccessDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="GroupAccess")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    access_level: Mapped[int] = mapped_column(Integer, nullable=True)
    push_branch_protection_defaults: Mapped[
        list["DefaultBranchProtectionDefaultsDBModel"]
    ] = relationship(
        "DefaultBranchProtectionDefaultsDBModel",
        back_populates="allowed_to_push",
        foreign_keys="[DefaultBranchProtectionDefaultsDBModel.allowed_to_push_id]",
    )
    merge_branch_protection_defaults: Mapped[
        list["DefaultBranchProtectionDefaultsDBModel"]
    ] = relationship(
        "DefaultBranchProtectionDefaultsDBModel",
        back_populates="allowed_to_merge",
        foreign_keys="[DefaultBranchProtectionDefaultsDBModel.allowed_to_merge_id]",
    )


# DefaultBranchProtectionDefaults Model
class DefaultBranchProtectionDefaultsDBModel(BaseDBModel):
    __tablename__ = "default_branch_protection_defaults"

    def __eq__(self, other):
        if isinstance(other, DefaultBranchProtectionDefaultsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(
        String, default="DefaultBranchProtectionDefaults"
    )
    allow_force_push: Mapped[bool] = mapped_column(Boolean, nullable=True)
    allowed_to_push_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="group_accesses.id", name="fk_default_rules_allow_push"),
        nullable=True,
    )
    allowed_to_push: Mapped["GroupAccessDBModel"] = relationship(
        back_populates="push_branch_protection_defaults",
        foreign_keys="[DefaultBranchProtectionDefaultsDBModel.allowed_to_push_id]",
    )

    allowed_to_merge_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="group_accesses.id", name="fk_default_rules_allow_merge"),
        nullable=True,
    )
    allowed_to_merge: Mapped["GroupAccessDBModel"] = relationship(
        back_populates="merge_branch_protection_defaults",
        foreign_keys="[DefaultBranchProtectionDefaultsDBModel.allowed_to_merge_id]",
    )
    groups: Mapped[List["GroupDBModel"]] = relationship(
        "GroupDBModel", back_populates="default_branch_protection_defaults"
    )


project_groups = Table(
    "project_groups",
    BaseDBModel.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

project_shared_with_groups = Table(
    "project_shared_with_groups",
    BaseDBModel.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("id", Integer, primary_key=True, autoincrement=True),
)

group_sharing = Table(
    "group_sharing",
    BaseDBModel.metadata,
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    Column("shared_group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)


# Group Model
class GroupDBModel(BaseDBModel):
    __tablename__ = "groups"

    def __eq__(self, other):
        if isinstance(other, GroupDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=True)
    base_type: Mapped[str] = mapped_column(String, default="Group")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    organization_id: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    group_name: Mapped[str] = mapped_column(String, nullable=True)
    group_full_path: Mapped[str] = mapped_column(String, nullable=True)
    path: Mapped[str] = mapped_column(String, nullable=True)
    group_access_level: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    visibility: Mapped[str] = mapped_column(String, nullable=True)
    shared_runners_setting: Mapped[str] = mapped_column(String, nullable=True)
    share_with_group_lock: Mapped[bool] = mapped_column(Boolean, nullable=True)
    require_two_factor_authentication: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    two_factor_grace_period: Mapped[int] = mapped_column(Integer, nullable=True)
    project_creation_level: Mapped[str] = mapped_column(String, nullable=True)
    auto_devops_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    subgroup_creation_level: Mapped[str] = mapped_column(String, nullable=True)
    emails_disabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    emails_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    mentions_disabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    lfs_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    default_branch: Mapped[str] = mapped_column(String, nullable=True)
    default_branch_protection: Mapped[int] = mapped_column(Integer, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    request_access_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    repository_storage: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    full_path: Mapped[str] = mapped_column(String, nullable=True)
    file_template_project_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    wiki_access_level: Mapped[str] = mapped_column(String, nullable=True)
    duo_features_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    lock_duo_features_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    runners_token: Mapped[str] = mapped_column(String, nullable=True)
    enabled_git_access_protocol: Mapped[str] = mapped_column(String, nullable=True)
    prevent_sharing_groups_outside_hierarchy: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    ip_restriction_ranges: Mapped[str] = mapped_column(String, nullable=True)
    math_rendering_limits_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    lock_math_rendering_limits_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    shared_runners_minutes_limit: Mapped[int] = mapped_column(Integer, nullable=True)
    extra_shared_runners_minutes_limit: Mapped[int] = mapped_column(
        Integer, nullable=True
    )
    marked_for_deletion_on: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    membership_lock: Mapped[bool] = mapped_column(Boolean, nullable=True)
    ldap_cn: Mapped[str] = mapped_column(String, nullable=True)
    ldap_access: Mapped[str] = mapped_column(String, nullable=True)
    prevent_forking_outside_group: Mapped[bool] = mapped_column(Boolean, nullable=True)
    allowed_email_domains_list: Mapped[str] = mapped_column(String, nullable=True)
    default_branch_protection_defaults_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="default_branch_protection_defaults.id",
            name="fk_group_default_branch_protection_defaults",
        ),
        nullable=True,
    )
    default_branch_protection_defaults: Mapped[
        "DefaultBranchProtectionDefaultsDBModel"
    ] = relationship(
        back_populates="groups",
        foreign_keys="[GroupDBModel.default_branch_protection_defaults_id]",
    )
    statistics_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="statistics.id", name="fk_group_statistics"),
        nullable=True,
    )
    statistics: Mapped["StatisticsDBModel"] = relationship(back_populates="groups")
    projects = relationship(
        "ProjectDBModel", secondary=project_groups, back_populates="groups"
    )

    shared_projects = relationship(
        "ProjectDBModel",
        secondary=project_shared_with_groups,
        back_populates="shared_with_groups",
    )

    shared_with_groups = relationship(
        "GroupDBModel",
        secondary=group_sharing,
        primaryjoin="GroupDBModel.id == group_sharing.c.group_id",
        secondaryjoin="GroupDBModel.id == group_sharing.c.shared_group_id",
        backref="groups_sharing_with_me",  # Optional, for the reverse relationship
    )

    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="groups.id"), nullable=True
    )
    parent: Mapped["GroupDBModel"] = relationship(
        "GroupDBModel",
        back_populates="groups",
        remote_side=[id],  # specify that this is a self-referential relationship
    )

    groups: Mapped[List["GroupDBModel"]] = relationship(
        "GroupDBModel",
        back_populates="parent",
        foreign_keys=[parent_id],
        cascade="all, delete-orphan",
    )
    todos: Mapped[List["ToDoDBModel"]] = relationship(back_populates="group")
    access_levels: Mapped[List["AccessLevelDBModel"]] = relationship(
        back_populates="group"
    )
    approval_rules: Mapped[List["ApprovalRuleDBModel"]] = relationship(
        back_populates="groups"
    )
    webhooks: Mapped[List["WebhookDBModel"]] = relationship(back_populates="group")
    iterations: Mapped[List["IterationDBModel"]] = relationship(
        back_populates="group", foreign_keys="[IterationDBModel.group_id]"
    )
    merge_request_approver_groups: Mapped[List["MergeApprovalsDBModel"]] = relationship(
        "MergeApprovalsDBModel", back_populates="approver_groups"
    )
    epics: Mapped[List["EpicDBModel"]] = relationship(
        "EpicDBModel", back_populates="groups"
    )


# Webhook Model
class WebhookDBModel(BaseDBModel):
    __tablename__ = "webhooks"

    def __eq__(self, other):
        if isinstance(other, WebhookDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Webhook")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    url: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    push_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    push_events_branch_filter: Mapped[str] = mapped_column(String, nullable=True)
    issues_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    confidential_issues_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_requests_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    tag_push_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    note_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    confidential_note_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    job_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    pipeline_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    wiki_page_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    deployment_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    releases_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    subgroup_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    member_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    enable_ssl_verification: Mapped[bool] = mapped_column(Boolean, nullable=True)
    repository_update_events: Mapped[bool] = mapped_column(Boolean, default=False)
    alert_status: Mapped[str] = mapped_column(String, nullable=True)
    disabled_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    url_variables: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    resource_access_token_events: Mapped[bool] = mapped_column(Boolean, nullable=True)
    custom_webhook_template: Mapped[str] = mapped_column(String, nullable=True)

    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="groups.id", name="fk_webhook_group"), nullable=True
    )
    group: Mapped["GroupDBModel"] = relationship(back_populates="webhooks")


class UserDBModel(BaseDBModel):
    __tablename__ = "users"

    def __eq__(self, other):
        if isinstance(other, UserDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="User")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    user: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=True)
    bio: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    skype: Mapped[str] = mapped_column(String, nullable=True)
    linkedin: Mapped[str] = mapped_column(String, nullable=True)
    twitter: Mapped[str] = mapped_column(String, nullable=True)
    discord: Mapped[str] = mapped_column(String, nullable=True)
    website_url: Mapped[str] = mapped_column(String, nullable=True)
    organization: Mapped[str] = mapped_column(String, nullable=True)
    job_title: Mapped[str] = mapped_column(String, nullable=True)
    last_sign_in_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    theme_id: Mapped[int] = mapped_column(Integer, nullable=True)
    last_activity_on: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    color_scheme_id: Mapped[int] = mapped_column(Integer, nullable=True)
    projects_limit: Mapped[int] = mapped_column(Integer, nullable=True)
    current_sign_in_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    note: Mapped[str] = mapped_column(String, nullable=True)
    can_create_group: Mapped[bool] = mapped_column(Boolean, nullable=True)
    can_create_project: Mapped[bool] = mapped_column(Boolean, nullable=True)
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    external: Mapped[bool] = mapped_column(Boolean, nullable=True)
    private_profile: Mapped[bool] = mapped_column(Boolean, nullable=True)
    current_sign_in_ip: Mapped[str] = mapped_column(String, nullable=True)
    last_sign_in_ip: Mapped[str] = mapped_column(String, nullable=True)
    email_reset_offered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    access_level: Mapped[int] = mapped_column(Integer, nullable=True)
    approved: Mapped[bool] = mapped_column(Boolean, nullable=True)
    invited: Mapped[bool] = mapped_column(Boolean, nullable=True)
    public_email: Mapped[str] = mapped_column(String, nullable=True)
    pronouns: Mapped[str] = mapped_column(String, nullable=True)
    bot: Mapped[bool] = mapped_column(Boolean, nullable=True)
    work_information: Mapped[str] = mapped_column(String, nullable=True)
    followers: Mapped[int] = mapped_column(Integer, nullable=True)
    following: Mapped[int] = mapped_column(Integer, nullable=True)
    local_time: Mapped[str] = mapped_column(String, nullable=True)
    commit_email: Mapped[str] = mapped_column(String, nullable=True)
    shared_runners_minutes_limit: Mapped[int] = mapped_column(Integer, nullable=True)
    extra_shared_runners_minutes_limit: Mapped[int] = mapped_column(
        Integer, nullable=True
    )
    membership_type: Mapped[str] = mapped_column(String, nullable=True)
    removable: Mapped[bool] = mapped_column(Boolean, nullable=True)
    last_login_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    created_by_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )
    created_by: Mapped["UserDBModel"] = relationship(
        "UserDBModel", remote_side=[id], back_populates="created_users"
    )

    created_users: Mapped[List["UserDBModel"]] = relationship(
        "UserDBModel", back_populates="created_by"
    )
    group_saml_identity: Mapped[List["GroupSamlIdentityDBModel"]] = relationship(
        "GroupSamlIdentityDBModel", back_populates="user"
    )

    namespace_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="namespaces.id",
            name="fk_user_namespace_id",
        ),
        nullable=True,
    )
    namespace: Mapped["NamespaceDBModel"] = relationship(
        "NamespaceDBModel",
        back_populates="user",
        foreign_keys=[namespace_id],
        remote_side="[NamespaceDBModel.id]",  # Specify the remote side of the relationship
    )

    deploy_tokens: Mapped[List["DeployTokenDBModel"]] = relationship(
        back_populates="user"
    )

    todos: Mapped[List["ToDoDBModel"]] = relationship(back_populates="author")
    agents = relationship("AgentsDBModel", back_populates="user")
    releases: Mapped[List["ReleaseDBModel"]] = relationship(back_populates="author")
    access_levels: Mapped[List["AccessLevelDBModel"]] = relationship(
        back_populates="user"
    )
    approval_rules: Mapped[List["ApprovalRuleDBModel"]] = relationship(
        "ApprovalRuleDBModel",
        back_populates="eligible_approvers",
        foreign_keys="[ApprovalRuleDBModel.eligible_approvers_id]",
    )
    # Relationships with MergeRequestDBModel
    authored_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        back_populates="author",
        primaryjoin="foreign(MergeRequestDBModel.author_id) == UserDBModel.id",
    )

    assigned_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        back_populates="assignee",
        primaryjoin="foreign(MergeRequestDBModel.assignee_id) == UserDBModel.id",
    )

    assignee_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        secondary=merge_request_assignees,  # Use the association table
        back_populates="assignees",
    )

    reviewed_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        back_populates="reviewer",
        primaryjoin="foreign(MergeRequestDBModel.reviewer_id) == UserDBModel.id",
    )

    reviewers_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        secondary=merge_request_reviewers,  # Use the association table
        back_populates="reviewers",
    )

    merged_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        back_populates="merged_by",
        primaryjoin="foreign(MergeRequestDBModel.merged_by_id) == UserDBModel.id",
    )

    merge_user_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        back_populates="merge_user",
        primaryjoin="foreign(MergeRequestDBModel.merge_user_id) == UserDBModel.id",
    )

    approved_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        back_populates="approved_by",
        primaryjoin="foreign(MergeRequestDBModel.approved_by_id) == UserDBModel.id",
    )

    closed_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        back_populates="closed_by",
        primaryjoin="foreign(MergeRequestDBModel.closed_by_id) == UserDBModel.id",
    )

    project_owner: Mapped[List["ProjectDBModel"]] = relationship(
        "ProjectDBModel",
        back_populates="owner",
        primaryjoin="foreign(ProjectDBModel.owner_id) == UserDBModel.id",
    )

    project_creator: Mapped[List["ProjectDBModel"]] = relationship(
        "ProjectDBModel",
        back_populates="creator",
        primaryjoin="foreign(ProjectDBModel.creator_id) == UserDBModel.id",
    )
    pipeline_schedules: Mapped[list["PipelineScheduleDBModel"]] = relationship(
        "PipelineScheduleDBModel",
        back_populates="owner",
        primaryjoin="foreign(PipelineScheduleDBModel.owner_id) == UserDBModel.id",
    )
    jobs = relationship("JobDBModel", back_populates="user")
    pipelines: Mapped[List["PipelineDBModel"]] = relationship(back_populates="user")
    comments: Mapped[List["CommentDBModel"]] = relationship(back_populates="author")
    commits: Mapped[List["CommitDBModel"]] = relationship(back_populates="author")
    issues: Mapped[List["IssueDBModel"]] = relationship(
        back_populates="author", foreign_keys="[IssueDBModel.author_id]"
    )
    assigned_issues: Mapped[List["IssueDBModel"]] = relationship(
        back_populates="assignee", foreign_keys="[IssueDBModel.assignee_id]"
    )
    closed_issues: Mapped[List["IssueDBModel"]] = relationship(
        back_populates="closed_by", foreign_keys="[IssueDBModel.closed_by_id]"
    )
    identities: Mapped[List["IdentityDBModel"]] = relationship(
        back_populates="user", foreign_keys="[IdentityDBModel.user_id]"
    )
    merge_request_approvers: Mapped[List["MergeApprovalsDBModel"]] = relationship(
        "MergeApprovalsDBModel",
        primaryjoin="UserDBModel.id == foreign(MergeApprovalsDBModel.approvers_id)",
        back_populates="approvers",
    )
    deployments: Mapped[List["LastDeploymentDBModel"]] = relationship(
        back_populates="user"
    )
    deployables: Mapped[List["DeployableDBModel"]] = relationship(back_populates="user")
    cluster_agents_created: Mapped[List["ClusterAgentDBModel"]] = relationship(
        back_populates="created_by_user"
    )
    github: Mapped[str] = mapped_column(String, nullable=True)

    namespace_id: Mapped[int] = mapped_column(Integer, nullable=True)
    is_auditor: Mapped[bool] = mapped_column(Boolean, nullable=True)
    using_license_seat: Mapped[bool] = mapped_column(Boolean, nullable=True)
    provisioned_by_group_id: Mapped[int] = mapped_column(Integer, nullable=True)
    is_followed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    plan: Mapped[str] = mapped_column(String, nullable=True)
    trial: Mapped[bool] = mapped_column(Boolean, nullable=True)
    sign_in_count: Mapped[int] = mapped_column(Integer, nullable=True)
    scim_identities = mapped_column(ARRAY(JSON), nullable=True)
    # Relationships
    assigned_merge_requests_list: Mapped[List["MergeRequestDBModel"]] = relationship(
        secondary="merge_request_assignees", back_populates="assignees"
    )

    owned_projects: Mapped[List["ProjectDBModel"]] = relationship(
        back_populates="owner"
    )


# Namespace Model
class NamespaceDBModel(BaseDBModel):
    __tablename__ = "namespaces"

    def __eq__(self, other):
        if isinstance(other, NamespaceDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Namespace")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    path: Mapped[str] = mapped_column(String, nullable=True)
    kind: Mapped[str] = mapped_column(String, nullable=True)
    full_path: Mapped[str] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    members_count_with_descendants: Mapped[int] = mapped_column(Integer, nullable=True)
    root_repository_size: Mapped[int] = mapped_column(Integer, nullable=True)
    projects_count: Mapped[int] = mapped_column(Integer, nullable=True)
    billable_members_count: Mapped[int] = mapped_column(Integer, nullable=True)
    plan: Mapped[str] = mapped_column(String, nullable=True)
    trial_ends_on: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    trial: Mapped[bool] = mapped_column(Boolean, nullable=True)

    parent_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    projects: Mapped[List["ProjectDBModel"]] = relationship(
        "ProjectDBModel",
        back_populates="namespace",
        primaryjoin="foreign(ProjectDBModel.namespace_id) == NamespaceDBModel.id",
    )

    user: Mapped["UserDBModel"] = relationship(
        back_populates="namespace",
    )


class ProjectDBModel(BaseDBModel):
    __tablename__ = "projects"

    def __eq__(self, other):
        if isinstance(other, ProjectDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Project")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    description: Mapped[str] = mapped_column(Text, nullable=True)
    description_html: Mapped[str] = mapped_column(Text, nullable=True)
    default_branch: Mapped[str] = mapped_column(String, nullable=True)
    visibility: Mapped[str] = mapped_column(String, nullable=True)
    ssh_url_to_repo: Mapped[str] = mapped_column(String, nullable=True)
    http_url_to_repo: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    readme_url: Mapped[str] = mapped_column(String, nullable=True)
    tag_list = mapped_column(ARRAY(String), nullable=True)
    topics = mapped_column(ARRAY(String), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    name_with_namespace: Mapped[str] = mapped_column(String, nullable=True)
    path: Mapped[str] = mapped_column(String, nullable=True)
    path_with_namespace: Mapped[str] = mapped_column(String, nullable=True)
    repository_object_format: Mapped[str] = mapped_column(String, nullable=True)
    issues_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    open_issues_count: Mapped[int] = mapped_column(Integer, nullable=True)
    merge_requests_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    jobs_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    wiki_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    snippets_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    can_create_merge_request_in: Mapped[bool] = mapped_column(Boolean, nullable=True)
    resolve_outdated_diff_discussions: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    container_registry_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    container_registry_access_level: Mapped[str] = mapped_column(String, nullable=True)
    security_and_compliance_access_level: Mapped[str] = mapped_column(
        String, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_activity_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    creator_id: Mapped[int] = mapped_column(Integer, nullable=True)
    import_url: Mapped[str] = mapped_column(String, nullable=True)
    import_type: Mapped[str] = mapped_column(String, nullable=True)
    import_status: Mapped[str] = mapped_column(String, nullable=True)
    import_error: Mapped[str] = mapped_column(String, nullable=True)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    license_url: Mapped[str] = mapped_column(String, nullable=True)
    shared_runners_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    group_runners_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    forks_count: Mapped[int] = mapped_column(Integer, nullable=True)
    star_count: Mapped[int] = mapped_column(Integer, nullable=True)
    runners_token: Mapped[str] = mapped_column(String, nullable=True)
    ci_default_git_depth: Mapped[int] = mapped_column(Integer, nullable=True)
    ci_forward_deployment_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    ci_forward_deployment_rollback_allowed: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    ci_allow_fork_pipelines_to_run_in_parent_project: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    ci_id_token_sub_claim_components = mapped_column(ARRAY(String), nullable=True)
    ci_separated_caches: Mapped[bool] = mapped_column(Boolean, nullable=True)
    ci_restrict_pipeline_cancellation_role: Mapped[str] = mapped_column(
        String, nullable=True
    )
    ci_pipeline_variables_minimum_override_role: Mapped[str] = mapped_column(
        String, nullable=True
    )
    ci_push_repository_for_job_token_allowed: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    public_jobs: Mapped[bool] = mapped_column(Boolean, nullable=True)
    repository_storage: Mapped[str] = mapped_column(String, nullable=True)
    only_allow_merge_if_pipeline_succeeds: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    allow_merge_on_skipped_pipeline: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    allow_pipeline_trigger_approve_deployment: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    restrict_user_defined_variables: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    only_allow_merge_if_all_discussions_are_resolved: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    remove_source_branch_after_merge: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    printing_merge_request_link_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    request_access_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_method: Mapped[str] = mapped_column(String, nullable=True)
    squash_option: Mapped[str] = mapped_column(String, nullable=True)
    auto_devops_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    auto_devops_deploy_strategy: Mapped[str] = mapped_column(String, nullable=True)
    approvals_before_merge: Mapped[int] = mapped_column(Integer, nullable=True)
    mirror: Mapped[bool] = mapped_column(Boolean, nullable=True)
    mirror_user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    mirror_trigger_builds: Mapped[bool] = mapped_column(Boolean, nullable=True)
    only_mirror_protected_branches: Mapped[bool] = mapped_column(Boolean, nullable=True)
    mirror_overwrites_diverged_branches: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    external_authorization_classification_label: Mapped[str] = mapped_column(
        String, nullable=True
    )
    packages_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    service_desk_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    service_desk_address: Mapped[str] = mapped_column(String, nullable=True)
    autoclose_referenced_issues: Mapped[bool] = mapped_column(Boolean, nullable=True)
    enforce_auth_checks_on_uploads: Mapped[bool] = mapped_column(Boolean, nullable=True)
    suggestion_commit_message: Mapped[str] = mapped_column(String, nullable=True)
    merge_commit_template: Mapped[str] = mapped_column(String, nullable=True)
    squash_commit_template: Mapped[str] = mapped_column(String, nullable=True)
    issue_branch_template: Mapped[str] = mapped_column(String, nullable=True)
    marked_for_deletion_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    marked_for_deletion_on: Mapped[str] = mapped_column(String, nullable=True)
    compliance_frameworks = mapped_column(ARRAY(String), nullable=True)
    warn_about_potentially_unwanted_characters: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    secret_push_protection_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    container_registry_image_prefix: Mapped[str] = mapped_column(String, nullable=True)
    empty_repo: Mapped[bool] = mapped_column(Boolean, nullable=True)
    issues_access_level: Mapped[str] = mapped_column(String, nullable=True)
    repository_access_level: Mapped[str] = mapped_column(String, nullable=True)
    merge_requests_access_level: Mapped[str] = mapped_column(String, nullable=True)
    forking_access_level: Mapped[str] = mapped_column(String, nullable=True)
    wiki_access_level: Mapped[str] = mapped_column(String, nullable=True)
    builds_access_level: Mapped[str] = mapped_column(String, nullable=True)
    snippets_access_level: Mapped[str] = mapped_column(String, nullable=True)
    pages_access_level: Mapped[str] = mapped_column(String, nullable=True)
    analytics_access_level: Mapped[str] = mapped_column(String, nullable=True)
    emails_disabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    emails_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    lfs_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    build_timeout: Mapped[int] = mapped_column(Integer, nullable=True)
    auto_cancel_pending_pipelines: Mapped[str] = mapped_column(String, nullable=True)
    ci_config_path: Mapped[str] = mapped_column(String, nullable=True)
    ci_job_token_scope_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    keep_latest_artifact: Mapped[bool] = mapped_column(Boolean, nullable=True)
    runner_token_expiration_interval: Mapped[str] = mapped_column(String, nullable=True)
    requirements_access_level: Mapped[str] = mapped_column(String, nullable=True)
    security_and_compliance_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    only_allow_merge_if_all_status_checks_passed: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    mr_default_target_self: Mapped[bool] = mapped_column(Boolean, nullable=True)
    package_registry_access_level: Mapped[str] = mapped_column(String, nullable=True)
    shared_with_groups = mapped_column(ARRAY(JSON), nullable=True)
    # Relationships
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    owner: Mapped["UserDBModel"] = relationship(back_populates="owned_projects")
    namespace_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("namespaces.id"), nullable=True
    )
    namespace: Mapped["NamespaceDBModel"] = relationship(back_populates="projects")
    permissions_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("permissions.id"), nullable=True
    )
    permissions: Mapped["PermissionsDBModel"] = relationship(back_populates="projects")
    statistics_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("statistics.id"), nullable=True
    )
    statistics: Mapped["StatisticsDBModel"] = relationship(back_populates="projects")
    license_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("licenses.id"), nullable=True
    )
    license: Mapped["LicenseDBModel"] = relationship(back_populates="projects")
    container_expiration_policy_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("container_expiration_policies.id"), nullable=True
    )
    container_expiration_policy: Mapped["ContainerExpirationPolicyDBModel"] = (
        relationship(back_populates="project")
    )
    links_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("links.id"), nullable=True
    )
    links: Mapped["LinkDBModel"] = relationship(back_populates="projects_links")
    forked_from_project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=True
    )
    forked_from_project: Mapped["ProjectDBModel"] = relationship(remote_side=[id])
    milestones: Mapped[List["MilestoneDBModel"]] = relationship(
        back_populates="project"
    )
    todos: Mapped[List["ToDoDBModel"]] = relationship(back_populates="project")
    merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        back_populates="project"
    )
    jobs: Mapped[List["JobDBModel"]] = relationship(back_populates="project")
    releases_access_level: Mapped[str] = mapped_column(String, nullable=True)
    environments_access_level: Mapped[str] = mapped_column(String, nullable=True)
    feature_flags_access_level: Mapped[str] = mapped_column(String, nullable=True)
    infrastructure_access_level: Mapped[str] = mapped_column(String, nullable=True)
    monitor_access_level: Mapped[str] = mapped_column(String, nullable=True)
    machine_learning_model_experiments_access_level = mapped_column(
        String, nullable=True
    )
    machine_learning_model_registry_access_level: Mapped[str] = mapped_column(
        String, nullable=True
    )
    forks = relationship(
        "ProjectDBModel",
        back_populates="forked_from_project",
        foreign_keys="ProjectDBModel.forked_from_project_id",
    )
    code_suggestions: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_pipelines_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_trains_skip_train_allowed: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    issues_template: Mapped[str] = mapped_column(String, nullable=True)
    merge_requests_template: Mapped[str] = mapped_column(String, nullable=True)
    packages_relocation_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    requirements_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    build_git_strategy: Mapped[str] = mapped_column(String, nullable=True)
    build_coverage_regex: Mapped[str] = mapped_column(String, nullable=True)
    shared_runners_minutes_limit: Mapped[int] = mapped_column(Integer, nullable=True)
    extra_shared_runners_minutes_limit: Mapped[int] = mapped_column(
        Integer, nullable=True
    )
    merge_trains_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    has_open_issues: Mapped[bool] = mapped_column(Boolean, nullable=True)

    operations_access_level: Mapped[str] = mapped_column(String, nullable=True)
    ci_dockerfile: Mapped[str] = mapped_column(String, nullable=True)
    public: Mapped[bool] = mapped_column(Boolean, nullable=True)

    creator: Mapped["UserDBModel"] = relationship(
        "UserDBModel",
        back_populates="project_creator",
        primaryjoin="foreign(ProjectDBModel.creator_id) == UserDBModel.id",
    )

    additional_links_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="links.id"), nullable=True
    )
    additional_links: Mapped["LinkDBModel"] = relationship(
        back_populates="projects_additional_links", foreign_keys=[additional_links_id]
    )

    groups = relationship(
        "GroupDBModel", secondary=project_groups, back_populates="projects"
    )

    agents = relationship("AgentsDBModel", back_populates="project")
    source_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        foreign_keys="[MergeRequestDBModel.source_project_id]",
        back_populates="source_project",
        primaryjoin="foreign(MergeRequestDBModel.source_project_id) == ProjectDBModel.id",
    )

    target_merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        foreign_keys="[MergeRequestDBModel.target_project_id]",
        back_populates="target_project",
        primaryjoin="foreign(MergeRequestDBModel.target_project_id) == ProjectDBModel.id",
    )
    runners: Mapped[List["RunnerDBModel"]] = relationship(back_populates="projects")
    issues: Mapped["IssueDBModel"] = relationship(back_populates="project")
    deployables: Mapped[List["DeployableDBModel"]] = relationship(
        back_populates="project"
    )


# Runner Model
class RunnerDBModel(BaseDBModel):
    __tablename__ = "runners"

    def __eq__(self, other):
        if isinstance(other, RunnerDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Runner")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    description: Mapped[str] = mapped_column(String, nullable=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=True)
    paused: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_shared: Mapped[bool] = mapped_column(Boolean, nullable=True)
    runner_type: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    online: Mapped[bool] = mapped_column(Boolean, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    contacted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    architecture: Mapped[str] = mapped_column(String, nullable=True)
    platform: Mapped[str] = mapped_column(String, nullable=True)
    revision: Mapped[str] = mapped_column(String, nullable=True)
    version: Mapped[str] = mapped_column(String, nullable=True)
    access_level: Mapped[str] = mapped_column(String, nullable=True)
    maximum_timeout: Mapped[int] = mapped_column(Integer, nullable=True)
    maintenance_note: Mapped[str] = mapped_column(String, nullable=True)

    tag_list_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="tags.id"), nullable=True
    )

    tag_list: Mapped[List["TagDBModel"]] = relationship(back_populates="runners")

    projects_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="projects.id", name="fk_runner_project"),
        nullable=True,
    )
    projects: Mapped[List["ProjectDBModel"]] = relationship(back_populates="runners")
    jobs: Mapped[List["JobDBModel"]] = relationship(back_populates="runner")


class JobDBModel(BaseDBModel):
    __tablename__ = "jobs"

    def __eq__(self, other):
        if isinstance(other, JobDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Job")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    coverage: Mapped[float] = mapped_column(Float, nullable=True)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=True)
    allow_failure: Mapped[bool] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    erased_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    duration: Mapped[float] = mapped_column(Float, nullable=True)
    queued_duration: Mapped[float] = mapped_column(Float, nullable=True)
    artifacts_expire_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    tag_list = mapped_column(ARRAY(String), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    ref: Mapped[str] = mapped_column(String, nullable=True)
    stage: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    failure_reason: Mapped[str] = mapped_column(String, nullable=True)
    tag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    download_url: Mapped[str] = mapped_column(String, nullable=True)
    # Relationships
    commit_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("commits.id"), nullable=True
    )
    commit: Mapped["CommitDBModel"] = relationship(back_populates="jobs")
    artifacts_file_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("artifacts_files.id"), nullable=True
    )
    artifacts_file: Mapped["ArtifactsFileDBModel"] = relationship(back_populates="jobs")
    artifacts = relationship("ArtifactDBModel", back_populates="jobs")
    pipeline_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("pipelines.id"), nullable=True
    )
    pipeline: Mapped["PipelineDBModel"] = relationship(back_populates="jobs")
    runner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("runners.id"), nullable=True
    )
    runner: Mapped["RunnerDBModel"] = relationship(back_populates="jobs")
    runner_manager_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("runner_managers.id"), nullable=True
    )
    runner_manager: Mapped["RunnerManagerDBModel"] = relationship(back_populates="jobs")
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=True
    )
    project: Mapped["ProjectDBModel"] = relationship(back_populates="jobs")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["UserDBModel"] = relationship(back_populates="jobs")
    downstream_pipeline_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("pipelines.id"), nullable=True
    )
    downstream_pipeline: Mapped["PipelineDBModel"] = relationship(
        back_populates="upstream_jobs"
    )
    agents = relationship("AgentsDBModel", back_populates="job")


class PipelineScheduleDBModel(BaseDBModel):
    __tablename__ = "pipeline_schedules"

    def __eq__(self, other):
        if isinstance(other, PipelineScheduleDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    ref: Mapped[str] = mapped_column(String, nullable=True)
    cron: Mapped[str] = mapped_column(String, nullable=True)
    cron_timezone: Mapped[str] = mapped_column(String, nullable=True)
    next_run_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    owner_id: Mapped[int] = mapped_column(Integer, nullable=True)

    owner: Mapped["UserDBModel"] = relationship(
        "UserDBModel",
        back_populates="pipeline_schedules",
        primaryjoin="foreign(PipelineScheduleDBModel.owner_id) == UserDBModel.id",
    )

    last_pipeline_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_commit_last_pipeline"),
        nullable=True,
    )
    last_pipeline: Mapped["PipelineDBModel"] = relationship(
        back_populates="scheduled_by"
    )

    variables: Mapped[List["PipelineVariableDBModel"]] = relationship(
        back_populates="pipeline_schedule", cascade="all, delete-orphan"
    )


# Pipeline Model
class PipelineDBModel(BaseDBModel):
    __tablename__ = "pipelines"

    def __eq__(self, other):
        if isinstance(other, PipelineDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Pipeline")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    iid: Mapped[int] = mapped_column(Integer, nullable=True)
    ref: Mapped[str] = mapped_column(String, nullable=True)
    sha: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    project_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    before_sha: Mapped[str] = mapped_column(String, nullable=True)
    tag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    yaml_errors: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    committed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    duration: Mapped[float] = mapped_column(Float, nullable=True)
    queued_duration: Mapped[float] = mapped_column(Float, nullable=True)
    coverage: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_pipeline_user"), nullable=True
    )
    user: Mapped["UserDBModel"] = relationship(back_populates="pipelines")

    detailed_status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="detailed_status.id", name="fk_pipeline_detailed_status"),
        nullable=True,
    )
    detailed_status: Mapped["DetailedStatusDBModel"] = relationship(
        back_populates="pipelines"
    )
    agents = relationship("AgentsDBModel", back_populates="pipeline")
    merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        primaryjoin="foreign(MergeRequestDBModel.pipeline_id) == PipelineDBModel.id",
        back_populates="pipeline",
    )
    jobs: Mapped[List["JobDBModel"]] = relationship(
        "JobDBModel",
        back_populates="pipeline",
        primaryjoin="PipelineDBModel.id == JobDBModel.pipeline_id",
    )
    package_versions: Mapped[List["PackageVersionDBModel"]] = relationship(
        "PackageVersionDBModel",
        foreign_keys="[PackageVersionDBModel.pipeline_id]",
        back_populates="pipeline",
    )
    packages: Mapped[List["PackageDBModel"]] = relationship(
        back_populates="pipelines",
        foreign_keys="[PackageDBModel.pipelines_id]",  # Specify the foreign key here
    )

    commit: Mapped["CommitDBModel"] = relationship(back_populates="last_pipeline")
    deployables: Mapped[List["DeployableDBModel"]] = relationship(
        back_populates="pipeline"
    )
    scheduled_by: Mapped["PipelineScheduleDBModel"] = relationship(
        back_populates="last_pipeline", uselist=False
    )


# PackageLink Model
class PackageLinkDBModel(BaseDBModel):
    __tablename__ = "package_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="PackageLink")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    web_path: Mapped[str] = mapped_column(String, nullable=True)
    delete_api_path: Mapped[str] = mapped_column(String, nullable=True)
    packages: Mapped["PackageDBModel"] = relationship(
        "PackageDBModel",
        foreign_keys="[PackageDBModel.links_id]",
        back_populates="links",
    )


# PackageVersion Model
class PackageVersionDBModel(BaseDBModel):
    __tablename__ = "package_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="PackageVersion")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    version: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    pipeline_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_package_version_pipeline"),
        nullable=True,
    )
    pipeline: Mapped["PipelineDBModel"] = relationship(
        back_populates="package_versions"
    )
    package_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="packages.id", name="fk_package_version_package"),
        nullable=True,
    )
    package: Mapped["PackageDBModel"] = relationship(
        back_populates="package_versions",  # Correct relationship direction
        foreign_keys=[package_id],
    )


# Package Model
class PackageDBModel(BaseDBModel):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Package")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    version: Mapped[str] = mapped_column(String, nullable=True)
    package_type: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_downloaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    conan_package_name: Mapped[str] = mapped_column(String, nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=True)
    file_name: Mapped[str] = mapped_column(String, nullable=True)
    file_md5: Mapped[str] = mapped_column(String, nullable=True)
    file_sha1: Mapped[str] = mapped_column(String, nullable=True)
    file_sha256: Mapped[str] = mapped_column(String, nullable=True)

    tags_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="tags.id"), nullable=True
    )
    tags: Mapped[List["TagDBModel"]] = relationship(back_populates="packages")

    links_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="package_links.id", name="fk_package_links"),
        nullable=True,
    )
    links: Mapped["PackageLinkDBModel"] = relationship(
        back_populates="packages", foreign_keys=[links_id]
    )

    pipelines_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_package_pipeline"),
        nullable=True,
    )
    pipelines: Mapped[List["PipelineDBModel"]] = relationship(back_populates="packages")
    package_versions: Mapped[List["PackageVersionDBModel"]] = relationship(
        back_populates="package", foreign_keys="[PackageVersionDBModel.package_id]"
    )


# Contributor Model
class ContributorDBModel(BaseDBModel):
    __tablename__ = "contributors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Contributor")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    commits: Mapped[int] = mapped_column(Integer, nullable=True)
    additions: Mapped[int] = mapped_column(Integer, nullable=True)
    deletions: Mapped[int] = mapped_column(Integer, nullable=True)


# CommitStats Model
class CommitStatsDBModel(BaseDBModel):
    __tablename__ = "commit_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="CommitStats")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    additions: Mapped[int] = mapped_column(Integer, nullable=True)
    deletions: Mapped[int] = mapped_column(Integer, nullable=True)
    total: Mapped[int] = mapped_column(Integer, nullable=True)
    commit: Mapped["CommitDBModel"] = relationship(back_populates="stats")


# CommitSignature Model
class CommitSignatureDBModel(BaseDBModel):
    __tablename__ = "commit_signatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="CommitSignature")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    signature_type: Mapped[str] = mapped_column(String, nullable=True)
    verification_status: Mapped[str] = mapped_column(String, nullable=True)
    commit_source: Mapped[str] = mapped_column(String, nullable=True)
    gpg_key_id: Mapped[int] = mapped_column(Integer, nullable=True)
    gpg_key_primary_keyid: Mapped[str] = mapped_column(String, nullable=True)
    gpg_key_user_name: Mapped[str] = mapped_column(String, nullable=True)
    gpg_key_user_email: Mapped[str] = mapped_column(String, nullable=True)
    gpg_key_subkey_id: Mapped[str] = mapped_column(String, nullable=True)
    key: Mapped[dict] = mapped_column(JSON, nullable=True)
    x509_certificate: Mapped[dict] = mapped_column(JSON, nullable=True)
    message: Mapped[str] = mapped_column(String, nullable=True)
    commit_id: Mapped[str] = mapped_column(
        String,
        ForeignKey(column="commits.id", name="fk_commit_signature_commit"),
        nullable=True,
    )
    commit: Mapped["CommitDBModel"] = relationship(
        back_populates="commit_signatures", foreign_keys=[commit_id]
    )


# Comment Model
class CommentDBModel(BaseDBModel):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Comment")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    type: Mapped[str] = mapped_column(String, nullable=True)
    body: Mapped[str] = mapped_column(String, nullable=True)
    note: Mapped[str] = mapped_column(String, nullable=True)
    attachment: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    system: Mapped[bool] = mapped_column(Boolean, nullable=True)
    noteable_id: Mapped[int] = mapped_column(Integer, nullable=True)
    noteable_type: Mapped[str] = mapped_column(String, nullable=True)
    resolvable: Mapped[bool] = mapped_column(Boolean, nullable=True)
    confidential: Mapped[bool] = mapped_column(Boolean, nullable=True)
    noteable_iid: Mapped[int] = mapped_column(Integer, nullable=True)
    commands_changes: Mapped[dict] = mapped_column(JSON, nullable=True)
    line_type: Mapped[str] = mapped_column(String, nullable=True)
    path: Mapped[str] = mapped_column(String, nullable=True)
    line: Mapped[int] = mapped_column(Integer, nullable=True)

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_comment_author"), nullable=True
    )
    author: Mapped["UserDBModel"] = relationship(back_populates="comments")

    commit_id: Mapped[str] = mapped_column(
        String,
        ForeignKey(column="commits.id", name="fk_commit_notes"),
        nullable=True,
    )
    commit: Mapped["CommitDBModel"] = relationship(
        back_populates="notes", foreign_keys=[commit_id]
    )


class LicenseDBModel(BaseDBModel):
    __tablename__ = "licenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="License")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    nickname: Mapped[str] = mapped_column(String, nullable=True)
    html_url: Mapped[str] = mapped_column(String, nullable=True)
    source_url: Mapped[str] = mapped_column(String, nullable=True)

    project: Mapped[List["ProjectDBModel"]] = relationship(
        "ProjectDBModel",
        back_populates="license",
        primaryjoin="foreign(ProjectDBModel.license_id) == LicenseDBModel.id",
    )


class ParentIDDBModel(BaseDBModel):
    __tablename__ = "parent_ids"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="ParentID")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    parent_id: Mapped[str] = mapped_column(String, nullable=False)
    commit_id: Mapped[str] = mapped_column(ForeignKey("commits.id"), nullable=True)
    commit: Mapped["CommitDBModel"] = relationship(back_populates="parent_ids")


# Commit Model
class CommitDBModel(BaseDBModel):
    __tablename__ = "commits"

    def __eq__(self, other):
        if isinstance(other, CommitDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Commit")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    short_id: Mapped[str] = mapped_column(String, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    message: Mapped[str] = mapped_column(String, nullable=True)
    author_name: Mapped[str] = mapped_column(String, nullable=True)
    author_email: Mapped[str] = mapped_column(String, nullable=True)
    authored_date = mapped_column(DateTime, nullable=True)
    committer_name: Mapped[str] = mapped_column(String, nullable=True)
    committer_email: Mapped[str] = mapped_column(String, nullable=True)
    committed_date = mapped_column(DateTime, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    trailers: Mapped[dict] = mapped_column(JSON, nullable=True)
    extended_trailers: Mapped[dict] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    sha: Mapped[str] = mapped_column(String, nullable=True)
    count: Mapped[int] = mapped_column(Integer, nullable=True)
    dry_run: Mapped[str] = mapped_column(String, nullable=True)
    individual_note: Mapped[bool] = mapped_column(Boolean, nullable=True)
    allow_failure: Mapped[bool] = mapped_column(Boolean, nullable=True)
    target_url: Mapped[str] = mapped_column(String, nullable=True)
    ref: Mapped[str] = mapped_column(String, nullable=True)
    error_code: Mapped[str] = mapped_column(String, nullable=True)
    coverage: Mapped[float] = mapped_column(Float, nullable=True)

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_commit_author"), nullable=True
    )
    author: Mapped["UserDBModel"] = relationship(back_populates="commits")

    stats_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="commit_stats.id", name="fk_commit_stats"),
        nullable=True,
    )
    stats: Mapped["CommitStatsDBModel"] = relationship(back_populates="commit")

    last_pipeline_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_commit_last_pipeline"),
        nullable=True,
    )
    last_pipeline: Mapped["PipelineDBModel"] = relationship(back_populates="commit")
    commit_signatures: Mapped[List["CommitSignatureDBModel"]] = relationship(
        back_populates="commit", remote_side="[CommitSignatureDBModel.commit_id]"
    )

    notes: Mapped["CommentDBModel"] = relationship(
        back_populates="commit", remote_side="[CommentDBModel.commit_id]"
    )
    parent_ids: Mapped[List["ParentIDDBModel"]] = relationship(back_populates="commit")
    releases: Mapped[List["ReleaseDBModel"]] = relationship(back_populates="commit")
    branches: Mapped[List["BranchDBModel"]] = relationship(back_populates="commit")

    jobs: Mapped[List["JobDBModel"]] = relationship(
        "JobDBModel", back_populates="commit"
    )
    deployables: Mapped[List["DeployableDBModel"]] = relationship(
        back_populates="commit"
    )


# Membership Model
class MembershipDBModel(BaseDBModel):
    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Membership")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    source_id: Mapped[int] = mapped_column(Integer, nullable=True)
    source_full_name: Mapped[str] = mapped_column(String, nullable=True)
    source_members_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    access_level: Mapped[dict] = mapped_column(JSON, nullable=True)


# Issue Model
class IssueDBModel(BaseDBModel):
    __tablename__ = "issues"

    def __eq__(self, other):
        if isinstance(other, IssueDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Issue")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    state: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    changes_count: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    moved_to_id: Mapped[int] = mapped_column(Integer, nullable=True)
    iid: Mapped[int] = mapped_column(Integer, nullable=True)
    labels = mapped_column(ARRAY(String), nullable=True)
    upvotes: Mapped[int] = mapped_column(Integer, nullable=True)
    downvotes: Mapped[int] = mapped_column(Integer, nullable=True)
    merge_requests_count: Mapped[int] = mapped_column(Integer, nullable=True)
    user_notes_count: Mapped[int] = mapped_column(Integer, nullable=True)
    due_date: Mapped[str] = mapped_column(String, nullable=True)
    imported: Mapped[bool] = mapped_column(Boolean, nullable=True)
    imported_from: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)
    has_tasks: Mapped[bool] = mapped_column(Boolean, nullable=True)
    task_status: Mapped[str] = mapped_column(String, nullable=True)
    confidential: Mapped[bool] = mapped_column(Boolean, nullable=True)
    discussion_locked: Mapped[bool] = mapped_column(Boolean, nullable=True)
    issue_type: Mapped[str] = mapped_column(String, nullable=True)
    severity: Mapped[str] = mapped_column(String, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=True)
    epic_iid: Mapped[int] = mapped_column(Integer, nullable=True)
    health_status: Mapped[str] = mapped_column(String, nullable=True)
    subscribed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    service_desk_reply_to: Mapped[str] = mapped_column(String, nullable=True)
    blocking_issues_count: Mapped[int] = mapped_column(Integer, nullable=True)

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="projects.id", name="fk_project"), nullable=True
    )
    project: Mapped["ProjectDBModel"] = relationship(back_populates="issues")

    milestone_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="milestones.id", name="fk_issue_milestone"),
        nullable=True,
    )
    milestone: Mapped["MilestoneDBModel"] = relationship(
        back_populates="issues", foreign_keys=[milestone_id]
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id"), nullable=True, name="fk_issue_author"
    )
    author: Mapped["UserDBModel"] = relationship(
        back_populates="issues", foreign_keys=[author_id]
    )

    assignee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_issue_assignee"), nullable=True
    )
    assignee: Mapped["UserDBModel"] = relationship(
        back_populates="issues", foreign_keys=[assignee_id]
    )

    closed_by_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_issue_closed_by"), nullable=True
    )
    closed_by: Mapped["UserDBModel"] = relationship(
        back_populates="issues", foreign_keys=[closed_by_id]
    )
    iteration_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="iterations.id", name="fk_issue_iteration"),
        nullable=True,
    )
    iteration: Mapped["IterationDBModel"] = relationship(
        back_populates="issues", foreign_keys="[IssueDBModel.iteration_id]"
    )
    epic_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="epics.id", name="fk_issue_epic"), nullable=True
    )
    epic: Mapped["EpicDBModel"] = relationship(back_populates="issues")

    todos: Mapped[List["ToDoDBModel"]] = relationship(
        back_populates="target", foreign_keys="[ToDoDBModel.target_id]"
    )


# TimeStats Model
class TimeStatsDBModel(BaseDBModel):
    __tablename__ = "time_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="TimeStats")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    time_estimate: Mapped[int] = mapped_column(Integer, nullable=True)
    total_time_spent: Mapped[int] = mapped_column(Integer, nullable=True)
    human_time_estimate: Mapped[str] = mapped_column(String, nullable=True)
    human_total_time_spent: Mapped[str] = mapped_column(String, nullable=True)
    merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        back_populates="time_stats"
    )


# TaskCompletionStatus Model
class TaskCompletionStatusDBModel(BaseDBModel):
    __tablename__ = "task_completion_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="TaskCompletionStatus")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    count: Mapped[int] = mapped_column(Integer, nullable=True)
    completed_count: Mapped[int] = mapped_column(Integer, nullable=True)
    merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        back_populates="task_completion_status"
    )


# References Model
class ReferencesDBModel(BaseDBModel):
    __tablename__ = "references"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="References")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    short: Mapped[str] = mapped_column(String, nullable=True)
    relative: Mapped[str] = mapped_column(String, nullable=True)
    full: Mapped[str] = mapped_column(String, nullable=True)
    merge_request_references: Mapped[List["MergeRequestDBModel"]] = relationship(
        back_populates="references", foreign_keys="[MergeRequestDBModel.references_id]"
    )


# Artifact Model
class ArtifactDBModel(BaseDBModel):
    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="Artifact")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    file_type: Mapped[str] = mapped_column(String, nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=True)
    filename: Mapped[str] = mapped_column(String, nullable=True)
    file_format: Mapped[str] = mapped_column(String, nullable=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    job: Mapped["JobDBModel"] = relationship(back_populates="artifacts")
    deployable_id: Mapped[int] = mapped_column(
        ForeignKey("deployables.id"), nullable=True
    )
    deployable: Mapped["DeployableDBModel"] = relationship(back_populates="artifacts")


# ArtifactsFile Model
class ArtifactsFileDBModel(BaseDBModel):
    __tablename__ = "artifacts_files"

    def __eq__(self, other):
        if isinstance(other, ArtifactsFileDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="ArtifactsFile")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    filename: Mapped[str] = mapped_column(String, nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=True)
    jobs: Mapped[List["JobDBModel"]] = relationship(back_populates="artifacts_file")


# RunnerManager Model
class RunnerManagerDBModel(BaseDBModel):
    __tablename__ = "runner_managers"

    def __eq__(self, other):
        if isinstance(other, RunnerManagerDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="RunnerManager")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    system_id: Mapped[str] = mapped_column(String, nullable=True)
    version: Mapped[str] = mapped_column(String, nullable=True)
    revision: Mapped[str] = mapped_column(String, nullable=True)
    platform: Mapped[str] = mapped_column(String, nullable=True)
    architecture: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    contacted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    jobs: Mapped[List["JobDBModel"]] = relationship(back_populates="runner_manager")


# Configuration Model
class ConfigurationDBModel(BaseDBModel):
    __tablename__ = "configurations"

    def __eq__(self, other):
        if isinstance(other, ConfigurationDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Configuration")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    approvals_before_merge: Mapped[int] = mapped_column(Integer, nullable=True)
    reset_approvals_on_push: Mapped[bool] = mapped_column(Boolean, nullable=True)
    selective_code_owner_removals: Mapped[bool] = mapped_column(Boolean, nullable=True)
    disable_overriding_approvers_per_merge_request = mapped_column(
        Boolean, nullable=True
    )
    merge_requests_author_approval: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_requests_disable_committers_approval: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    require_password_to_approve: Mapped[bool] = mapped_column(Boolean, nullable=True)
    agent: Mapped["AgentDBModel"] = relationship(back_populates="config_project")


# Iteration Model
class IterationDBModel(BaseDBModel):
    __tablename__ = "iterations"

    def __eq__(self, other):
        if isinstance(other, IterationDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Iteration")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    iid: Mapped[int] = mapped_column(Integer, nullable=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    start_date: Mapped[str] = mapped_column(String, nullable=True)
    due_date: Mapped[str] = mapped_column(String, nullable=True)
    web_url: Mapped[str] = mapped_column(String, nullable=True)

    group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="groups.id", name="fk_iteration_group"),
        nullable=True,
    )
    group: Mapped["GroupDBModel"] = relationship(back_populates="iterations")

    issues: Mapped[List["IssueDBModel"]] = relationship(
        back_populates="iteration",
        foreign_keys="[IssueDBModel.iteration_id]",  # Explicitly specify the foreign key
    )


# Identity Model
class IdentityDBModel(BaseDBModel):
    __tablename__ = "identities"

    def __eq__(self, other):
        if isinstance(other, IdentityDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Identity")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    provider: Mapped[str] = mapped_column(String, nullable=True)
    extern_uid: Mapped[str] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="users.id", name="fk_identity_user"), nullable=True
    )
    user: Mapped["UserDBModel"] = relationship(back_populates="identities")


# GroupSamlIdentity Model
class GroupSamlIdentityDBModel(BaseDBModel):
    __tablename__ = "group_saml_identities"

    def __eq__(self, other):
        if isinstance(other, GroupSamlIdentityDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="GroupSamlIdentity")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    extern_uid: Mapped[str] = mapped_column(String, nullable=True)
    provider: Mapped[str] = mapped_column(String, nullable=True)
    saml_provider_id: Mapped[int] = mapped_column(Integer, nullable=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    # Define the many-to-one relationship
    user: Mapped["UserDBModel"] = relationship(
        "UserDBModel", back_populates="group_saml_identity"
    )


# ContainerExpirationPolicy Model
class ContainerExpirationPolicyDBModel(BaseDBModel):
    __tablename__ = "container_expiration_policies"

    def __eq__(self, other):
        if isinstance(other, ContainerExpirationPolicyDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="ContainerExpirationPolicy")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    cadence: Mapped[str] = mapped_column(String, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    keep_n: Mapped[int] = mapped_column(Integer, nullable=True)
    older_than: Mapped[str] = mapped_column(String, nullable=True)
    name_regex: Mapped[str] = mapped_column(String, nullable=True)
    name_regex_keep: Mapped[str] = mapped_column(String, nullable=True)
    next_run_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=True
    )

    project: Mapped["ProjectDBModel"] = relationship(
        "ProjectDBModel",
        back_populates="container_expiration_policy",
        foreign_keys=[project_id],  # Specify the foreign key here
    )


# Permissions Model
class PermissionsDBModel(BaseDBModel):
    __tablename__ = "permissions"

    def __eq__(self, other):
        if isinstance(other, PermissionsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Permissions")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    project_access: Mapped[dict] = mapped_column(JSON, nullable=True)
    group_access: Mapped[dict] = mapped_column(JSON, nullable=True)

    projects: Mapped["ProjectDBModel"] = relationship(back_populates="permissions")


# Statistics Model
class StatisticsDBModel(BaseDBModel):
    __tablename__ = "statistics"

    def __eq__(self, other):
        if isinstance(other, StatisticsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Statistics")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    commit_count: Mapped[int] = mapped_column(Integer, nullable=True)
    storage_size: Mapped[int] = mapped_column(Integer, nullable=True)
    repository_size: Mapped[int] = mapped_column(Integer, nullable=True)
    wiki_size: Mapped[int] = mapped_column(Integer, nullable=True)
    lfs_objects_size: Mapped[int] = mapped_column(Integer, nullable=True)
    job_artifacts_size: Mapped[int] = mapped_column(Integer, nullable=True)
    pipeline_artifacts_size: Mapped[int] = mapped_column(Integer, nullable=True)
    packages_size: Mapped[int] = mapped_column(Integer, nullable=True)
    snippets_size: Mapped[int] = mapped_column(Integer, nullable=True)
    uploads_size: Mapped[int] = mapped_column(Integer, nullable=True)
    groups: Mapped[List["GroupDBModel"]] = relationship(
        "GroupDBModel", back_populates="statistics"
    )

    projects: Mapped["ProjectDBModel"] = relationship(back_populates="statistics")


# Diff Model
class DiffDBModel(BaseDBModel):
    __tablename__ = "diffs"

    def __eq__(self, other):
        if isinstance(other, DiffDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Diff")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    head_commit_sha: Mapped[str] = mapped_column(String, nullable=True)
    base_commit_sha: Mapped[str] = mapped_column(String, nullable=True)
    start_commit_sha: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    real_size: Mapped[str] = mapped_column(String, nullable=True)
    patch_id_sha: Mapped[str] = mapped_column(String, nullable=True)
    diff: Mapped[str] = mapped_column(String, nullable=True)
    new_path: Mapped[str] = mapped_column(String, nullable=True)
    old_path: Mapped[str] = mapped_column(String, nullable=True)
    a_mode: Mapped[str] = mapped_column(String, nullable=True)
    b_mode: Mapped[str] = mapped_column(String, nullable=True)
    new_file: Mapped[bool] = mapped_column(Boolean, nullable=True)
    renamed_file: Mapped[bool] = mapped_column(Boolean, nullable=True)
    deleted_file: Mapped[bool] = mapped_column(Boolean, nullable=True)
    generated_file: Mapped[bool] = mapped_column(Boolean, nullable=True)

    merge_requests: Mapped[List["MergeRequestDBModel"]] = relationship(
        "MergeRequestDBModel",
        back_populates="changes",
        foreign_keys="[MergeRequestDBModel.change_id]",
    )


class MergeApprovalsDBModel(BaseDBModel):
    __tablename__ = "merge_approvals"

    def __eq__(self, other):
        if isinstance(other, MergeApprovalsDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="MergeApprovals")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    approvals_before_merge: Mapped[int] = mapped_column(Integer, nullable=True)
    reset_approvals_on_push: Mapped[bool] = mapped_column(Boolean, nullable=True)
    selective_code_owner_removals: Mapped[bool] = mapped_column(Boolean, nullable=True)
    disable_overriding_approvers_per_merge_request = mapped_column(
        Boolean, nullable=True
    )
    merge_requests_author_approval: Mapped[bool] = mapped_column(Boolean, nullable=True)
    merge_requests_disable_committers_approval: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )
    require_password_to_approve: Mapped[bool] = mapped_column(Boolean, nullable=True)

    approvers_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="users.id", name="fk_merge_approvals_approvers"),
        nullable=True,
    )
    approvers: Mapped[List["UserDBModel"]] = relationship(
        back_populates="merge_request_approvers"
    )

    approver_groups_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="groups.id", name="fk_merge_approvals_approver_groups"),
        nullable=True,
    )
    approver_groups: Mapped["GroupDBModel"] = relationship(
        back_populates="merge_request_approver_groups",
        foreign_keys=[approver_groups_id],
    )


# DetailedStatus Model
class DetailedStatusDBModel(BaseDBModel):
    __tablename__ = "detailed_status"

    def __eq__(self, other):
        if isinstance(other, DetailedStatusDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="DetailedStatus")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    icon: Mapped[str] = mapped_column(String, nullable=True)
    text: Mapped[str] = mapped_column(String, nullable=True)
    label: Mapped[str] = mapped_column(String, nullable=True)
    group: Mapped[str] = mapped_column(String, nullable=True)
    tooltip: Mapped[str] = mapped_column(String, nullable=True)
    has_details: Mapped[bool] = mapped_column(Boolean, nullable=True)
    details_path: Mapped[str] = mapped_column(String, nullable=True)
    illustration: Mapped[dict] = mapped_column(JSON, nullable=True)
    favicon: Mapped[str] = mapped_column(String, nullable=True)

    pipelines: Mapped[List["PipelineDBModel"]] = relationship(
        back_populates="detailed_status"
    )


# pytest: ignore these classes
class TestReportDBModel(BaseDBModel):
    __tablename__ = "test_reports"

    def __eq__(self, other):
        if isinstance(other, TestReportDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_type: Mapped[str] = mapped_column(String, default="TestReport")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    total_time: Mapped[int] = mapped_column(Integer, nullable=True)
    total_count: Mapped[int] = mapped_column(Integer, nullable=True)
    success_count: Mapped[int] = mapped_column(Integer, nullable=True)
    failed_count: Mapped[int] = mapped_column(Integer, nullable=True)
    skipped_count: Mapped[int] = mapped_column(Integer, nullable=True)
    error_count: Mapped[int] = mapped_column(Integer, nullable=True)

    total_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="test_report_totals.id", name="fk_test_report_total"),
        nullable=True,
    )
    total: Mapped["TestReportTotalDBModel"] = relationship(
        back_populates="test_reports"
    )

    test_suites_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("test_suites.id", name="fk_test_report_test_suite"),
        nullable=True,
    )
    test_suites: Mapped[List["TestSuiteDBModel"]] = relationship(
        back_populates="test_reports"
    )


class ProjectConfigDBModel(BaseDBModel):
    __tablename__ = "project_configs"

    def __eq__(self, other):
        if isinstance(other, ProjectConfigDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    primary_id = Column(Integer, primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(Integer, nullable=True, unique=True)
    base_type: Mapped[str] = mapped_column(String, default="ProjectConfig")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    description: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    name_with_namespace: Mapped[str] = mapped_column(String, nullable=True)
    path: Mapped[str] = mapped_column(String, nullable=True)
    path_with_namespace: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ci_job_token_scope_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    jobs = relationship("JobDBModel", back_populates="project")
    cluster_agents: Mapped[List["ClusterAgentDBModel"]] = relationship(
        back_populates="project_config"
    )


# Epic Model
class EpicDBModel(BaseDBModel):
    __tablename__ = "epics"

    def __eq__(self, other):
        if isinstance(other, EpicDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="Epic")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    iid: Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=True)

    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(column="groups.id", name="fk_epic_group"), nullable=True
    )
    groups: Mapped[List["GroupDBModel"]] = relationship(back_populates="epics")
    issues: Mapped[List["IssueDBModel"]] = relationship(
        back_populates="epic",
        foreign_keys="[IssueDBModel.epic_id]",  # Explicitly specify the foreign key
    )


# TestCase Model
class TestCaseDBModel(BaseDBModel):
    __tablename__ = "test_cases"

    def __eq__(self, other):
        if isinstance(other, TestCaseDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="TestCase")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    status: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    classname: Mapped[str] = mapped_column(String, nullable=True)
    execution_time: Mapped[float] = mapped_column(Float, nullable=True)
    system_output: Mapped[str] = mapped_column(String, nullable=True)
    stack_trace: Mapped[str] = mapped_column(String, nullable=True)
    test_suite_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("test_suites.id"), nullable=True
    )

    test_suites: Mapped["TestSuiteDBModel"] = relationship(
        "TestSuiteDBModel",
        back_populates="test_cases",
        foreign_keys=[test_suite_id],  # Specify the correct foreign key
    )


# TestSuite Model
class TestSuiteDBModel(BaseDBModel):
    __tablename__ = "test_suites"

    def __eq__(self, other):
        if isinstance(other, TestSuiteDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="TestSuite")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    name: Mapped[str] = mapped_column(String, nullable=True)
    total_time: Mapped[float] = mapped_column(Float, nullable=True)
    total_count: Mapped[int] = mapped_column(Integer, nullable=True)
    success_count: Mapped[int] = mapped_column(Integer, nullable=True)
    failed_count: Mapped[int] = mapped_column(Integer, nullable=True)
    skipped_count: Mapped[int] = mapped_column(Integer, nullable=True)
    error_count: Mapped[int] = mapped_column(Integer, nullable=True)
    suite_error: Mapped[str] = mapped_column(String, nullable=True)

    test_cases: Mapped[List["TestCaseDBModel"]] = relationship(
        "TestCaseDBModel",
        back_populates="test_suites",
        foreign_keys="[TestCaseDBModel.test_suite_id]",  # Specify the correct foreign key
    )
    test_reports: Mapped[List["TestReportDBModel"]] = relationship(
        back_populates="test_suites"
    )


# TestReportTotal Model
class TestReportTotalDBModel(BaseDBModel):
    __tablename__ = "test_report_totals"

    def __eq__(self, other):
        if isinstance(other, TestReportTotalDBModel):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_type: Mapped[str] = mapped_column(String, default="TestReportTotal")
    extras: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    time: Mapped[int] = mapped_column(Integer, nullable=True)
    count: Mapped[int] = mapped_column(Integer, nullable=True)
    success: Mapped[int] = mapped_column(Integer, nullable=True)
    failed: Mapped[int] = mapped_column(Integer, nullable=True)
    skipped: Mapped[int] = mapped_column(Integer, nullable=True)
    error: Mapped[int] = mapped_column(Integer, nullable=True)
    suite_error: Mapped[str] = mapped_column(String, nullable=True)
    test_reports: Mapped[List["TestReportDBModel"]] = relationship(
        back_populates="total"
    )
