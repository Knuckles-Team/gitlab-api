#!/usr/bin/python
# coding: utf-8
import logging

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

from sqlalchemy import Table, Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, backref, declarative_base, Mapped
from sqlalchemy import Integer, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Float,
    JSON,
)

BaseDBModel = declarative_base()


# Evidence Model
class EvidenceDBModel(BaseDBModel):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Evidence")
    sha = Column(String, nullable=True)
    filepath = Column(String, nullable=True)
    collected_at = Column(DateTime, nullable=True)


evidences_association = Table(
    "evidences_association",
    BaseDBModel.metadata,
    Column("evidences_collection_id", Integer, ForeignKey("evidences_collection.id")),
    Column("evidence_id", Integer, ForeignKey("evidences.id")),
)


class EvidencesDBModel(BaseDBModel):
    __tablename__ = "evidences_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Evidences")
    evidences = relationship(
        "EvidenceDBModel",
        secondary=evidences_association,
        backref=backref("evidences_collection", lazy="dynamic"),
    )


# IssueStats Model
class IssueStatsDBModel(BaseDBModel):
    __tablename__ = "issue_stats"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="IssueStats")
    total = Column(Integer, nullable=True)
    closed = Column(Integer, nullable=True)
    opened = Column(Integer, nullable=True)


# Milestone Model
class MilestoneDBModel(BaseDBModel):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Milestone")
    iid = Column(Integer, nullable=True)
    project_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_milestone_project_id"),
        nullable=True,
    )
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    due_date = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    web_url = Column(String, nullable=True)

    issue_stats_id = Column(
        Integer,
        ForeignKey(column="issue_stats.id", name="fk_milestone_issue_stats"),
        nullable=True,
    )
    issue_stats = relationship(
        argument="IssueStatsDBModel",
        foreign_keys=[issue_stats_id],
        backref=backref("milestones"),
    )

    release_id = Column(
        Integer,
        ForeignKey(column="releases.id", name="fk_milestone_release"),
        nullable=True,
    )
    releases = relationship(
        argument="ReleaseDBModel",
        foreign_keys=[release_id],
        backref=backref("milestone_associations"),
    )


milestone_association = Table(
    "milestone_association",
    BaseDBModel.metadata,
    Column("milestones_collection_id", Integer, ForeignKey("milestones_collection.id")),
    Column("milestone_id", Integer, ForeignKey("milestones.id")),
)


# Milestones Collection Model
class MilestonesDBModel(BaseDBModel):
    __tablename__ = "milestones_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Milestones")
    milestones = relationship(
        "MilestoneDBModel",
        secondary=milestone_association,
        backref=backref("milestones_collection", lazy="dynamic"),
    )


# DeployToken Model
class DeployTokenDBModel(BaseDBModel):
    __tablename__ = "deploy_tokens"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="DeployToken")
    name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    token = Column(String, nullable=True)
    revoked = Column(Boolean, nullable=True)
    expired = Column(Boolean, nullable=True)
    scopes = Column(ARRAY(String), nullable=True)
    active = Column(Boolean, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_deploy_token_user"),
        nullable=True,
    )
    user = relationship(
        argument="UserDBModel", foreign_keys=[user_id], backref=backref("deploy_tokens")
    )


deploy_tokens_association = Table(
    "deploy_tokens_association",
    BaseDBModel.metadata,
    Column(
        "deploy_tokens_collection_id",
        Integer,
        ForeignKey("deploy_tokens_collection.id"),
    ),
    Column("deploy_tokens_id", Integer, ForeignKey("deploy_tokens.id")),
)


# DeployTokens Collection Model
class DeployTokensDBModel(BaseDBModel):
    __tablename__ = "deploy_tokens_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="DeployTokens")
    deploy_tokens = relationship(
        "DeployTokenDBModel",
        secondary=deploy_tokens_association,
        backref=backref("deploy_tokens_collection", lazy="dynamic"),
    )


# Rule Model
class RuleDBModel(BaseDBModel):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Rule")
    created_at = Column(DateTime, nullable=True)
    commit_committer_check = Column(Boolean, default=False)
    commit_committer_name_check = Column(Boolean, default=False)
    reject_unsigned_commits = Column(Boolean, default=False)
    commit_message_regex = Column(String, nullable=True)
    commit_message_negative_regex = Column(String, nullable=True)
    branch_name_regex = Column(String, nullable=True)
    deny_delete_tag = Column(Boolean, default=False)
    member_check = Column(Boolean, default=False)
    prevent_secrets = Column(Boolean, default=False)
    author_email_regex = Column(String, nullable=True)
    file_name_regex = Column(String, nullable=True)
    max_file_size = Column(Integer, nullable=True)


# AccessControl Model
class AccessControlDBModel(BaseDBModel):
    __tablename__ = "access_controls"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="AccessControl")
    name = Column(String, nullable=True)
    access_level = Column(Integer, nullable=True)
    member_role_id = Column(Integer, nullable=True)


access_controls_association = Table(
    "access_controls_association",
    BaseDBModel.metadata,
    Column(
        "access_controls_collection_id",
        Integer,
        ForeignKey("access_controls_collection.id"),
    ),
    Column("access_controls_id", Integer, ForeignKey("access_controls.id")),
)


# AccessControls Collection Model
class AccessControlsDBModel(BaseDBModel):
    __tablename__ = "access_controls_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="AccessControls")
    access_controls = relationship(
        "AccessControlDBModel",
        secondary=access_controls_association,
        backref=backref("access_controls_collection", lazy="dynamic"),
    )


# Source Model
class SourcesDBModel(BaseDBModel):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Sources")
    format = Column(String, nullable=True)
    url = Column(String, nullable=True)

    assets_id = Column(
        Integer, ForeignKey(column="assets.id", name="fk_sources_assets"), nullable=True
    )
    assets = relationship(
        argument="AssetsDBModel",
        foreign_keys=[assets_id],
        backref=backref("sources_assets"),
    )


# Link Model
class LinkDBModel(BaseDBModel):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Link")
    name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    link_type = Column(String, nullable=True)

    assets_id = Column(
        Integer, ForeignKey(column="assets.id", name="fk_link_assets"), nullable=True
    )
    assets = relationship(
        argument="AssetsDBModel", foreign_keys=[assets_id], backref=backref("link")
    )


# Links Model
class LinksDBModel(BaseDBModel):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Links")
    self_link = Column(String, nullable=True)
    issues = Column(String, nullable=True)
    merge_requests = Column(String, nullable=True)
    repo_branches = Column(String, nullable=True)
    labels = Column(String, nullable=True)
    events = Column(String, nullable=True)
    members = Column(String, nullable=True)
    cluster_agents = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    award_emoji = Column(String, nullable=True)
    project = Column(String, nullable=True)
    closed_as_duplicate_of = Column(String, nullable=True)


links_association = Table(
    "links_association",
    BaseDBModel.metadata,
    Column("links_collection_id", Integer, ForeignKey("links_collection.id")),
    Column("link_id", Integer, ForeignKey("link.id")),
)


class LinksListDBModel(BaseDBModel):
    __tablename__ = "links_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="LinksList")
    links = relationship(
        "LinkDBModel",
        secondary=links_association,
        backref=backref("links_collection", lazy="dynamic"),
    )


# Assets Model
class AssetsDBModel(BaseDBModel):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Assets")
    count = Column(Integer, nullable=True)
    sources_id = Column(
        Integer,
        ForeignKey(column="sources.id", name="fk_assets_sources"),
        nullable=True,
    )
    sources = relationship(
        argument="SourcesDBModel", foreign_keys=[sources_id], backref=backref("sources")
    )
    links_id = Column(
        Integer, ForeignKey(column="links.id", name="fk_assets_links"), nullable=True
    )
    links = relationship(
        argument="LinksDBModel", foreign_keys=[links_id], backref=backref("links")
    )
    evidence_file_path = Column(String, nullable=True)


# ReleaseLinks Model
class ReleaseLinksDBModel(BaseDBModel):
    __tablename__ = "release_links"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ReleaseLinks")
    closed_issues_url = Column(String, nullable=True)
    closed_merge_requests_url = Column(String, nullable=True)
    edit_url = Column(String, nullable=True)
    merged_merge_requests_url = Column(String, nullable=True)
    opened_issues_url = Column(String, nullable=True)
    opened_merge_requests_url = Column(String, nullable=True)
    self_link = Column(String, nullable=True)
    releases_id = Column(
        Integer,
        ForeignKey(column="releases.id", name="fk_release_links_releases"),
        nullable=True,
    )
    release_link_releases = relationship(
        argument="ReleaseDBModel",
        foreign_keys=[releases_id],
        backref=backref("release_links"),
    )


# Token Model
class TokenDBModel(BaseDBModel):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Token")
    token = Column(String, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)


# ToDo Model
class ToDoDBModel(BaseDBModel):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ToDo")
    action_name = Column(String, nullable=True)
    target_type = Column(String, nullable=True)
    target_url = Column(String, nullable=True)
    body = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)

    project_id = Column(
        Integer, ForeignKey(column="projects.id", name="fk_todo_project"), nullable=True
    )
    project = relationship(
        argument="ProjectDBModel",
        foreign_keys=[project_id],
        backref=backref("todos_project"),
    )

    author_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_todo_author"), nullable=True
    )
    author = relationship(
        argument="UserDBModel",
        foreign_keys=[author_id],
        backref=backref("todos_author"),
    )

    target_id = Column(
        Integer, ForeignKey(column="issues.id", name="fk_todo_target"), nullable=True
    )
    target = relationship(
        argument="IssueDBModel",
        foreign_keys=[target_id],
        backref=backref("todos_target"),
    )


# WikiPage Model
class WikiPageDBModel(BaseDBModel):
    __tablename__ = "wiki_pages"
    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="WikiPage")
    content = Column(String, nullable=True)
    format = Column(String, nullable=True)
    slug = Column(String, nullable=True)
    title = Column(String, nullable=True)
    encoding = Column(String, nullable=True)


wiki_pages_association = Table(
    "wiki_pages_association",
    BaseDBModel.metadata,
    Column("wiki_pages_collection_id", Integer, ForeignKey("wiki_pages_collection.id")),
    Column("link_id", Integer, ForeignKey("wiki_pages.id")),
)


# WikiPages Collection Model
class WikiPagesDBModel(BaseDBModel):
    __tablename__ = "wiki_pages_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="WikiPages")
    wiki_pages = relationship(
        "WikiPageDBModel",
        secondary=wiki_pages_association,
        backref=backref("wiki_pages_collection", lazy="dynamic"),
    )


# WikiAttachmentLink Model
class WikiAttachmentLinkDBModel(BaseDBModel):
    __tablename__ = "wiki_attachment_links"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="WikiAttachmentLink")
    url = Column(String, nullable=True)
    markdown = Column(String, nullable=True)


# PipelineVariable Model
class PipelineVariableDBModel(BaseDBModel):
    __tablename__ = "pipeline_variables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="PipelineVariable")
    key = Column(String, nullable=True)
    variable_type = Column(String, nullable=True)
    value = Column(String, nullable=True)


pipeline_variables_association = Table(
    "pipeline_variables_association",
    BaseDBModel.metadata,
    Column(
        "pipeline_variable_collection_id",
        Integer,
        ForeignKey("pipeline_variable_collection.id"),
    ),
    Column("pipeline_variable_id", Integer, ForeignKey("pipeline_variables.id")),
)


# PipelineVariables Collection Model
class PipelineVariablesDBModel(BaseDBModel):
    __tablename__ = "pipeline_variable_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="PipelineVariables")
    pipeline_variable = relationship(
        "PipelineVariableDBModel",
        secondary=pipeline_variables_association,
        backref=backref("pipeline_variable_collection", lazy="dynamic"),
    )


# WikiAttachment Model
class WikiAttachmentDBModel(BaseDBModel):
    __tablename__ = "wiki_attachments"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="WikiAttachment")
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    branch = Column(String, nullable=True)

    link_id = Column(
        Integer,
        ForeignKey(column="wiki_attachment_links.id", name="fk_wiki_attachment_links"),
        nullable=True,
    )
    link = relationship(
        argument="WikiAttachmentLinkDBModel",
        foreign_keys=[link_id],
        backref=backref("wiki_attachments"),
    )


# Agent Model
class AgentDBModel(BaseDBModel):
    __tablename__ = "agent"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Agent")

    config_project_id = Column(
        Integer,
        ForeignKey(column="project_configs.id", name="fk_agent_project_configs"),
        nullable=True,
    )
    config_project = relationship(
        argument="ProjectConfigDBModel",
        foreign_keys=[config_project_id],
        backref=backref("agent"),
    )


# Agents Model
class AgentsDBModel(BaseDBModel):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Agents")

    job_id = Column(
        Integer, ForeignKey(column="jobs.id", name="fk_agents_jobs"), nullable=True
    )
    job = relationship(
        argument="JobDBModel", foreign_keys=[job_id], backref=backref("agents")
    )

    pipeline_id = Column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_agents_pipelines"),
        nullable=True,
    )
    pipeline = relationship(
        argument="PipelineDBModel",
        foreign_keys=[pipeline_id],
        backref=backref("agents"),
    )

    project_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_agents_projects"),
        nullable=True,
    )
    project = relationship(
        argument="ProjectDBModel", foreign_keys=[project_id], backref=backref("agents")
    )

    user_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_agents_users"), nullable=True
    )
    user = relationship(
        argument="UserDBModel", foreign_keys=[user_id], backref=backref("agents")
    )


# Release Model
class ReleaseDBModel(BaseDBModel):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Release")
    tag_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    released_at = Column(DateTime, nullable=True)
    commit_path = Column(String, nullable=True)
    tag_path = Column(String, nullable=True)
    evidence_sha = Column(String, nullable=True)

    # Relationships (optional)

    author_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_release_author"), nullable=True
    )
    author = relationship(
        argument="UserDBModel", backref=backref("releases"), foreign_keys=[author_id]
    )

    commit_id = Column(
        String,
        ForeignKey(column="commits.id", name="fk_release_commits"),
        nullable=True,
    )
    commit = relationship(
        argument="CommitDBModel", backref=backref("releases"), foreign_keys=[commit_id]
    )
    milestones_id = Column(
        Integer,
        ForeignKey(column="milestones.id", name="fk_release_milestones"),
        nullable=True,
    )
    milestones = relationship(
        argument="MilestoneDBModel",
        foreign_keys=[milestones_id],
        backref=backref("release_associations"),
    )

    evidences_id = Column(
        Integer,
        ForeignKey(column="evidences.id", name="fk_release_evidences"),
        nullable=True,
    )
    evidences = relationship(
        argument="EvidenceDBModel",
        foreign_keys=[evidences_id],
        backref=backref("release_evidences"),
    )

    assets_id = Column(
        Integer, ForeignKey(column="assets.id", name="fk_release_assets"), nullable=True
    )
    assets = relationship(
        argument="AssetsDBModel", backref=backref("release"), foreign_keys=[assets_id]
    )

    links_id = Column(
        Integer,
        ForeignKey(column="release_links.id", name="fk_release_links"),
        nullable=True,
    )
    links = relationship(
        argument="ReleaseLinksDBModel",
        backref=backref("release"),
        foreign_keys=[links_id],
    )


releases_association = Table(
    "releases_association",
    BaseDBModel.metadata,
    Column("releases_collection_id", Integer, ForeignKey("releases_collection.id")),
    Column("releases_id", Integer, ForeignKey("releases.id")),
)


# Releases Collection Model
class ReleasesDBModel(BaseDBModel):
    __tablename__ = "releases_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Releases")
    releases = relationship(
        "ReleaseDBModel",
        secondary=releases_association,
        backref=backref("releases_collection", lazy="dynamic"),
    )


# AccessLevel Model
class AccessLevelDBModel(BaseDBModel):
    __tablename__ = "access_levels"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="AccessLevel")
    access_level = Column(Integer, nullable=True)
    access_level_description = Column(String, nullable=True)
    deploy_key_id = Column(Integer, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_access_level_users"),
        nullable=True,
    )
    user = relationship(
        argument="UserDBModel", foreign_keys=[user_id], backref=backref("access_levels")
    )

    group_id = Column(
        Integer,
        ForeignKey(column="groups.id", name="fk_access_level_groups"),
        nullable=True,
    )
    group = relationship(
        argument="GroupDBModel",
        foreign_keys=[group_id],
        backref=backref("access_levels"),
    )


access_levels_association = Table(
    "access_levels_association",
    BaseDBModel.metadata,
    Column(
        "access_levels_collection_id",
        Integer,
        ForeignKey("access_levels_collection.id"),
    ),
    Column("access_levels_id", Integer, ForeignKey("access_levels.id")),
)


# AccessLevels Collection Model
class AccessLevelsDBModel(BaseDBModel):
    __tablename__ = "access_levels_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="AccessLevels")
    access_levels = relationship(
        "AccessLevelDBModel",
        secondary=access_levels_association,
        backref=backref("access_levels_collection", lazy="dynamic"),
    )


# Branch Model
class BranchDBModel(BaseDBModel):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Branch")
    name = Column(String, nullable=True)
    merged = Column(Boolean, nullable=True)
    protected = Column(Boolean, nullable=True)
    default = Column(Boolean, nullable=True)
    developers_can_push = Column(Boolean, nullable=True)
    developers_can_merge = Column(Boolean, nullable=True)
    can_push = Column(Boolean, nullable=True)
    web_url = Column(String, nullable=True)
    allow_force_push = Column(Boolean, nullable=True)
    code_owner_approval_required = Column(Boolean, nullable=True)
    inherited = Column(Boolean, nullable=True)

    commit_id = Column(
        String,
        ForeignKey(column="commits.id", name="fk_branch_commits"),
        nullable=True,
    )
    commit = relationship(argument="CommitDBModel", backref=backref("branches_commit"))

    push_access_levels_id = Column(
        Integer,
        ForeignKey(column="access_levels.id", name="fk_branch_push_access_levels"),
        nullable=True,
    )
    push_access_levels = relationship(
        argument="AccessLevelDBModel",
        foreign_keys=[push_access_levels_id],
        backref=backref("branches_push_access_levels"),
    )

    merge_access_levels_id = Column(
        Integer,
        ForeignKey(column="access_levels.id", name="fk_branch_merge_access_levels"),
        nullable=True,
    )
    merge_access_levels = relationship(
        argument="AccessLevelDBModel",
        foreign_keys=[merge_access_levels_id],
        backref=backref("branches_merge_access_levels"),
    )

    unprotect_access_levels_id = Column(
        Integer,
        ForeignKey(column="access_levels.id", name="fk_branch_unprotect_access_levels"),
        nullable=True,
    )
    unprotect_access_levels = relationship(
        argument="AccessLevelDBModel",
        foreign_keys=[unprotect_access_levels_id],
        backref=backref("branches_unprotect_access_levels"),
    )


branches_association = Table(
    "branches_association",
    BaseDBModel.metadata,
    Column("branches_collection_id", Integer, ForeignKey("branches_collection.id")),
    Column("branches_id", Integer, ForeignKey("branches.id")),
)


# Branches Collection Model
class BranchesDBModel(BaseDBModel):
    __tablename__ = "branches_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Branches")
    branches = relationship(
        "BranchDBModel",
        secondary=branches_association,
        backref=backref("branches_collection", lazy="dynamic"),
    )


labels_association = Table(
    "labels_association",
    BaseDBModel.metadata,
    Column("label_id", Integer, ForeignKey("labels.id"), primary_key=True),
    Column(
        "labels_collection_id",
        Integer,
        ForeignKey("labels_collection.id"),
        primary_key=True,
    ),
)


# Label Model
class LabelDBModel(BaseDBModel):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    base_type = Column(String, default="Label")
    name = Column(String, nullable=True)
    color = Column(String, nullable=True)
    text_color = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_html = Column(Text, nullable=True)
    open_issues_count = Column(Integer, nullable=True)
    closed_issues_count = Column(Integer, nullable=True)
    open_merge_requests_count = Column(Integer, nullable=True)
    subscribed = Column(Boolean, nullable=True)
    priority = Column(Integer, nullable=True)
    is_project_label = Column(Boolean, nullable=True)


# Labels Model
class LabelsDBModel(BaseDBModel):
    __tablename__ = "labels_collection"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    base_type = Column(String, default="Labels")
    labels = relationship(
        "LabelDBModel",
        secondary=labels_association,
        backref=backref("labels_collections", lazy="dynamic"),
    )


class TopicDBModel(BaseDBModel):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Topic")
    name = Column(String, nullable=False)


topics_association = Table(
    "topics_association",
    BaseDBModel.metadata,
    Column("topics_collection_id", Integer, ForeignKey("topics_collection.id")),
    Column("topics_id", Integer, ForeignKey("topics.id")),
)


class TopicsDBModel(BaseDBModel):
    __tablename__ = "topics_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Topics")
    topics = relationship(
        "TopicDBModel",
        secondary=topics_association,
        backref=backref("topics_collection", lazy="dynamic"),
    )


class TagDBModel(BaseDBModel):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    base_type = Column(String, default="Tag")
    tag = Column(String, nullable=True)


tags_association = Table(
    "tags_association",
    BaseDBModel.metadata,
    Column("tags_collection_id", Integer, ForeignKey("tags_collection.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


job_tags_association = Table(
    "job_tags_association",
    BaseDBModel.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id")),
    Column("tags_collection_id", Integer, ForeignKey("tags_collection.id")),
)


class TagsDBModel(BaseDBModel):
    __tablename__ = "tags_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Tags")
    tags = relationship(
        "TagDBModel",
        secondary=tags_association,
        backref=backref("tags_collection", lazy="dynamic"),
    )
    tags_jobs = relationship(
        "JobDBModel",
        secondary=job_tags_association,
        # backref=backref("tags_job_list"),  # or another appropriate name if needed
    )


# ApprovalRule Model
class ApprovalRuleDBModel(BaseDBModel):
    __tablename__ = "approval_rules"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ApprovalRule")
    name = Column(String, nullable=True)
    rule_type = Column(String, nullable=True)
    approvals_required = Column(Integer, nullable=True)
    contains_hidden_groups = Column(Boolean, nullable=True)
    applies_to_all_protected_branches = Column(Boolean, nullable=True)
    source_rule = Column(String, nullable=True)
    approved = Column(Boolean, nullable=True)
    overridden = Column(Boolean, nullable=True)

    eligible_approvers_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_eligible_approvers_rules"),
        nullable=True,
    )
    eligible_approvers = relationship(
        argument="UserDBModel",
        foreign_keys=[eligible_approvers_id],
        backref=backref("approval_rules"),
    )

    users_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_users_rules"),
        nullable=True,
    )
    users = relationship(
        argument="UserDBModel",
        foreign_keys=[users_id],
        backref=backref("approval_rules_users"),
    )

    groups_id = Column(
        Integer,
        ForeignKey(column="groups.id", name="fk_groups_rules"),
        nullable=True,
    )
    groups = relationship(
        argument="GroupDBModel",
        foreign_keys=[groups_id],
        backref=backref("approval_rules_groups"),
    )

    protected_branches_id = Column(
        Integer,
        ForeignKey(column="branches.id", name="fk_protected_branches_rules"),
        nullable=True,
    )
    protected_branches = relationship(
        argument="BranchDBModel",
        foreign_keys=[protected_branches_id],
        backref=backref("approval_rules_branches"),
    )

    approved_by_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_approval_rule_user_by_id"),
        nullable=True,
    )
    approved_by = relationship(
        argument="UserDBModel",
        foreign_keys=[approved_by_id],
        backref=backref("approval_rules_approved_by"),
    )


approval_rules_association = Table(
    "approval_rules_association",
    BaseDBModel.metadata,
    Column(
        "approval_rules_collection_id",
        Integer,
        ForeignKey("approval_rules_collection.id"),
    ),
    Column("approval_rules_id", Integer, ForeignKey("approval_rules.id")),
)


class ApprovalRulesDBModel(BaseDBModel):
    __tablename__ = "approval_rules_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="ApprovalRules")
    approval_rules = relationship(
        "ApprovalRuleDBModel",
        secondary=approval_rules_association,
        backref=backref("approval_rules_collection", lazy="dynamic"),
    )


# MergeRequest Model
class MergeRequestDBModel(BaseDBModel):
    __tablename__ = "merge_requests"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="MergeRequest")
    iid = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    merged_at = Column(DateTime, nullable=True)
    latest_build_started_at = Column(DateTime, nullable=True)
    latest_build_finished_at = Column(DateTime, nullable=True)
    first_deployed_to_production_at = Column(DateTime, nullable=True)
    prepared_at = Column(DateTime, nullable=True)
    target_branch = Column(String, nullable=True)
    source_branch = Column(String, nullable=True)
    upvotes = Column(Integer, nullable=True)
    downvotes = Column(Integer, nullable=True)
    source_project_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_merge_request_source_project"),
        nullable=True,
    )
    target_project_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_merge_request_target_project"),
        nullable=True,
    )
    work_in_progress = Column(Boolean, nullable=True)
    merge_when_pipeline_succeeds = Column(Boolean, nullable=True)
    merge_status = Column(String, nullable=True)
    sha = Column(String, nullable=True)
    merge_commit_sha = Column(String, nullable=True)
    draft = Column(Boolean, nullable=True)
    squash_commit_sha = Column(String, nullable=True)
    squash_on_merge = Column(Boolean, nullable=True)
    user_notes_count = Column(Integer, nullable=True)
    discussion_locked = Column(Boolean, nullable=True)
    should_remove_source_branch = Column(Boolean, nullable=True)
    force_remove_source_branch = Column(Boolean, nullable=True)
    allow_collaboration = Column(Boolean, nullable=True)
    allow_maintainer_to_push = Column(Boolean, nullable=True)
    web_url = Column(String, nullable=True)
    reference = Column(String, nullable=True)
    squash = Column(Boolean, nullable=True)
    has_conflicts = Column(Boolean, nullable=True)
    blocking_discussions_resolved = Column(Boolean, nullable=True)
    changes_count = Column(String, nullable=True)
    rebase_in_progress = Column(Boolean, nullable=True)
    approvals_before_merge = Column(Integer, nullable=True)
    tag_list = Column(ARRAY(String), nullable=True)
    imported = Column(Boolean, nullable=True)
    imported_from = Column(String, nullable=True)
    detailed_merge_status = Column(String, nullable=True)
    subscribed = Column(Boolean, nullable=True)
    overflow = Column(Boolean, nullable=True)
    diverged_commits_count = Column(Integer, nullable=True)
    merge_error = Column(String, nullable=True)
    approvals_required = Column(Integer, nullable=True)
    approvals_left = Column(Integer, nullable=True)
    approval_rules_overwritten = Column(Boolean, nullable=True)

    author_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_merge_request_author"),
        nullable=True,
    )
    author = relationship(
        argument="UserDBModel",
        foreign_keys=[author_id],
        backref=backref("author_merge_requests"),
    )

    assignee_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_merge_request_assignee"),
        nullable=True,
    )
    assignee = relationship(
        argument="UserDBModel",
        foreign_keys=[assignee_id],
        backref=backref("merge_request_assignee"),
    )

    assignees_id = Column(
        Integer,
        ForeignKey(column="users_collection.id", name="fk_merge_request_assignees"),
        nullable=True,
    )
    assignees = relationship(
        argument="UsersDBModel",
        foreign_keys=[assignees_id],
        backref=backref("merge_request_assignees"),
    )

    milestone_id = Column(
        Integer,
        ForeignKey(column="milestones.id", name="fk_merge_request_milestone"),
        nullable=True,
    )
    milestone = relationship(
        argument="MilestoneDBModel",
        foreign_keys=[milestone_id],
        backref=backref("merge_requests"),
    )

    merged_by_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_merge_request_merged_by"),
        nullable=True,
    )
    merged_by = relationship(
        "UserDBModel",
        foreign_keys=[merged_by_id],
        backref=backref("merged_merge_requests"),
    )

    merge_user_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_merge_request_merge_user"),
        nullable=True,
    )
    merge_user = relationship(
        "UserDBModel",
        foreign_keys=[merge_user_id],
        backref=backref("merge_user_merge_requests"),
    )

    closed_by_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_merge_request_close_by"),
        nullable=True,
    )
    closed_by = relationship(
        argument="UserDBModel",
        foreign_keys=[closed_by_id],
        backref=backref("merges_requests_closed_by"),
    )

    pipeline_id = Column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_merge_request_pipeline"),
        nullable=True,
    )
    pipeline = relationship(
        argument="PipelineDBModel",
        foreign_keys=[pipeline_id],
        backref=backref("merge_requests_pipeline"),
    )

    head_pipeline_id = Column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_merge_request_head_pipeline"),
        nullable=True,
    )
    head_pipeline = relationship(
        argument="PipelineDBModel",
        foreign_keys=[head_pipeline_id],
        backref=backref("head_merge_requests"),
    )

    project_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_merge_request_project"),
        nullable=True,
    )
    project = relationship(
        argument="ProjectDBModel",
        foreign_keys=[project_id],
        backref=backref("project_merge_requests"),
    )

    labels_id = Column(
        Integer,
        ForeignKey(column="labels_collection.id", name="fk_merge_request_labels"),
        nullable=True,
    )
    labels = relationship(
        argument="LabelsDBModel",
        foreign_keys=[labels_id],
        backref=backref("merge_requests_labels"),
    )

    references_id = Column(
        Integer,
        ForeignKey(column="references.id", name="fk_merge_request_references"),
        nullable=True,
    )
    references = relationship(
        argument="ReferencesDBModel",
        foreign_keys=[references_id],
        backref=backref("merge_requests"),
    )

    time_stats_id = Column(
        Integer,
        ForeignKey(column="time_stats.id", name="fk_merge_request_time_stats"),
        nullable=True,
    )

    time_stats = relationship(
        argument="TimeStatsDBModel",
        foreign_keys=[time_stats_id],
        backref=backref("merge_requests"),
    )

    task_completion_status_id = Column(
        Integer,
        ForeignKey(
            column="task_completion_status.id",
            name="fk_merge_request_task_completion_status",
        ),
        nullable=True,
    )
    task_completion_status = relationship(
        argument="TaskCompletionStatusDBModel",
        foreign_keys=[task_completion_status_id],
        backref=backref("merge_requests"),
    )

    change_id = Column(
        Integer,
        ForeignKey(column="diffs.id", name="fk_merge_request_change"),
        nullable=True,
    )
    changes = relationship(
        argument="DiffDBModel",
        foreign_keys=[change_id],
        backref=backref("merge_requests"),
    )

    reviewer_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_merge_request_reviewer"),
        nullable=True,
    )
    reviewer = relationship(
        argument="UserDBModel",
        foreign_keys=[reviewer_id],
        backref=backref("merge_request_reviewer"),
    )

    reviewers_id = Column(
        Integer,
        ForeignKey(column="users_collection.id", name="fk_merge_request_reviewers"),
        nullable=True,
    )
    reviewers = relationship(
        argument="UsersDBModel",
        foreign_keys=[reviewers_id],
        backref=backref("merge_request_reviewers"),
    )

    approved_by_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_merge_request_user_approved_by"),
        nullable=True,
    )
    approved_by = relationship(
        argument="UserDBModel",
        foreign_keys=[approved_by_id],
        backref=backref("approved_users_merge_request"),
    )

    approval_rules_id = Column(
        Integer,
        ForeignKey(column="approval_rules.id", name="fk_merge_request_approval_rules"),
        nullable=True,
    )
    approval_rules = relationship(
        argument="ApprovalRuleDBModel",
        foreign_keys=[approval_rules_id],
        backref=backref("approval_rules_merge_request"),
    )


merge_requests_association = Table(
    "merge_requests_association",
    BaseDBModel.metadata,
    Column(
        "merge_requests_collection_id",
        Integer,
        ForeignKey("merge_requests_collection.id"),
    ),
    Column("merge_requests_id", Integer, ForeignKey("merge_requests.id")),
)


class MergeRequestsDBModel(BaseDBModel):
    __tablename__ = "merge_requests_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="MergeRequests")
    merge_requests = relationship(
        "MergeRequestDBModel",
        secondary=merge_requests_association,
        backref=backref("merge_requests_collection", lazy="dynamic"),
    )


# GroupAccess Model
class GroupAccessDBModel(BaseDBModel):
    __tablename__ = "group_accesses"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="GroupAccess")
    access_level = Column(Integer, nullable=True)


group_accesses_association = Table(
    "group_accesses_association",
    BaseDBModel.metadata,
    Column(
        "group_accesses_collection_id",
        Integer,
        ForeignKey("group_accesses_collection.id"),
    ),
    Column("group_accesses_id", Integer, ForeignKey("group_accesses.id")),
)


class GroupAccessesDBModel(BaseDBModel):
    __tablename__ = "group_accesses_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="GroupAccesses")
    group_accesses = relationship(
        "GroupAccessDBModel",
        secondary=group_accesses_association,
        backref=backref("group_accesses_collection", lazy="dynamic"),
    )


# DefaultBranchProtectionDefaults Model
class DefaultBranchProtectionDefaultsDBModel(BaseDBModel):
    __tablename__ = "default_branch_protection_defaults"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="DefaultBranchProtectionDefaults")
    allow_force_push = Column(Boolean, nullable=True)
    allowed_to_push_id = Column(
        Integer,
        ForeignKey(column="group_accesses.id", name="fk_default_rules_allow_push"),
        nullable=True,
    )
    allowed_to_push = relationship(
        argument="GroupAccessDBModel",
        foreign_keys=[allowed_to_push_id],
        backref=backref("push_defaults"),
    )
    allowed_to_merge_id = Column(
        Integer,
        ForeignKey(column="group_accesses.id", name="fk_default_rules_allow_merge"),
        nullable=True,
    )
    allowed_to_merge = relationship(
        argument="GroupAccessDBModel",
        foreign_keys=[allowed_to_merge_id],
        backref=backref("merge_defaults"),
    )


# Group Model
class GroupDBModel(BaseDBModel):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=True)
    base_type = Column(String, default="Group")
    organization_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    group_name = Column(String, nullable=True)
    group_full_path = Column(String, nullable=True)
    path = Column(String, nullable=True)
    group_access_level = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    visibility = Column(String, nullable=True)
    shared_runners_setting = Column(String, nullable=True)
    share_with_group_lock = Column(Boolean, nullable=True)
    require_two_factor_authentication = Column(Boolean, nullable=True)
    two_factor_grace_period = Column(Integer, nullable=True)
    project_creation_level = Column(String, nullable=True)
    auto_devops_enabled = Column(Boolean, nullable=True)
    subgroup_creation_level = Column(String, nullable=True)
    emails_disabled = Column(Boolean, nullable=True)
    emails_enabled = Column(Boolean, nullable=True)
    mentions_disabled = Column(Boolean, nullable=True)
    lfs_enabled = Column(Boolean, nullable=True)
    default_branch = Column(String, nullable=True)
    default_branch_protection = Column(Integer, nullable=True)
    avatar_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    request_access_enabled = Column(Boolean, nullable=True)
    repository_storage = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    full_path = Column(String, nullable=True)
    file_template_project_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    wiki_access_level = Column(String, nullable=True)
    duo_features_enabled = Column(Boolean, nullable=True)
    lock_duo_features_enabled = Column(Boolean, nullable=True)
    runners_token = Column(String, nullable=True)
    enabled_git_access_protocol = Column(String, nullable=True)
    prevent_sharing_groups_outside_hierarchy = Column(Boolean, nullable=True)
    ip_restriction_ranges = Column(String, nullable=True)
    math_rendering_limits_enabled = Column(Boolean, nullable=True)
    lock_math_rendering_limits_enabled = Column(Boolean, nullable=True)
    shared_runners_minutes_limit = Column(Integer, nullable=True)
    extra_shared_runners_minutes_limit = Column(Integer, nullable=True)
    marked_for_deletion_on = Column(DateTime, nullable=True)
    membership_lock = Column(Boolean, nullable=True)
    ldap_cn = Column(String, nullable=True)
    ldap_access = Column(String, nullable=True)
    prevent_forking_outside_group = Column(Boolean, nullable=True)

    default_branch_protection_defaults_id = Column(
        Integer,
        ForeignKey(
            column="default_branch_protection_defaults.id",
            name="fk_group_default_branch_protection_defaults",
        ),
        nullable=True,
    )
    default_branch_protection_defaults = relationship(
        argument="DefaultBranchProtectionDefaultsDBModel",
        foreign_keys=[default_branch_protection_defaults_id],
        backref=backref("groups"),
    )
    statistics_id = Column(
        Integer,
        ForeignKey(column="statistics.id", name="fk_group_statistics"),
        nullable=True,
    )
    statistics = relationship(
        argument="StatisticsDBModel",
        foreign_keys=[statistics_id],
        backref=backref("groups"),
    )
    projects_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_group_projects"),
        nullable=True,
    )
    projects = relationship(
        argument="ProjectDBModel",
        foreign_keys=[projects_id],
        backref=backref("group_projects"),
    )
    shared_projects_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_group_shared_projects"),
        nullable=True,
    )
    shared_projects = relationship(
        argument="ProjectDBModel",
        foreign_keys=[shared_projects_id],
        backref=backref("shared_group_projects"),
    )

    parent_id = Column(
        Integer, ForeignKey(column="groups.id", name="fk_"), nullable=True
    )
    parent = relationship(
        argument="GroupDBModel", foreign_keys=[parent_id], remote_side=[id]
    )


groups_association = Table(
    "groups_association",
    BaseDBModel.metadata,
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    Column(
        "groups_collection_id",
        Integer,
        ForeignKey("groups_collection.id"),
        primary_key=True,
    ),
)


class GroupsDBModel(BaseDBModel):
    __tablename__ = "groups_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Groups")
    groups = relationship(
        "GroupDBModel",
        secondary=groups_association,
        backref=backref("groups_collection", lazy="dynamic"),
    )


# Webhook Model
class WebhookDBModel(BaseDBModel):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Webhook")
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    push_events = Column(Boolean, nullable=False)
    push_events_branch_filter = Column(String, nullable=True)
    issues_events = Column(Boolean, nullable=False)
    confidential_issues_events = Column(Boolean, nullable=False)
    merge_requests_events = Column(Boolean, nullable=False)
    tag_push_events = Column(Boolean, nullable=False)
    note_events = Column(Boolean, nullable=False)
    confidential_note_events = Column(Boolean, nullable=False)
    job_events = Column(Boolean, nullable=False)
    pipeline_events = Column(Boolean, nullable=False)
    wiki_page_events = Column(Boolean, nullable=False)
    deployment_events = Column(Boolean, nullable=False)
    releases_events = Column(Boolean, nullable=False)
    subgroup_events = Column(Boolean, nullable=False)
    member_events = Column(Boolean, nullable=False)
    enable_ssl_verification = Column(Boolean, nullable=False)
    repository_update_events = Column(Boolean, default=False)
    alert_status = Column(String, nullable=True)
    disabled_until = Column(DateTime, nullable=True)
    url_variables = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    resource_access_token_events = Column(Boolean, nullable=False)
    custom_webhook_template = Column(String, nullable=True)

    group_id = Column(
        Integer, ForeignKey(column="groups.id", name="fk_webhook_group"), nullable=False
    )
    group = relationship(
        argument="GroupDBModel", foreign_keys=[group_id], backref=backref("webhooks")
    )


webhooks_association = Table(
    "webhooks_association",
    BaseDBModel.metadata,
    Column("webhooks_collection_id", Integer, ForeignKey("webhooks_collection.id")),
    Column("webhooks_id", Integer, ForeignKey("webhooks.id")),
)


class WebhooksDBModel(BaseDBModel):
    __tablename__ = "webhooks_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Webhooks")
    webhooks = relationship(
        "WebhookDBModel",
        secondary=webhooks_association,
        backref=backref("webhooks_collection", lazy="dynamic"),
    )


users_association = Table(
    "users_association",
    BaseDBModel.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column(
        "users_collection_id",
        Integer,
        ForeignKey("users_collection.id"),
        primary_key=True,
    ),
)


# User Model
class UserDBModel(BaseDBModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="User")
    user = Column(String, nullable=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
    name = Column(String, nullable=True)
    state = Column(String, nullable=True)
    locked = Column(Boolean, nullable=True)
    avatar_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    is_admin = Column(Boolean, nullable=True)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    skype = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    discord = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    last_sign_in_at = Column(DateTime, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)
    theme_id = Column(Integer, nullable=True)
    last_activity_on = Column(DateTime, nullable=True)
    color_scheme_id = Column(Integer, nullable=True)
    projects_limit = Column(Integer, nullable=True)
    current_sign_in_at = Column(DateTime, nullable=True)
    note = Column(String, nullable=True)
    can_create_group = Column(Boolean, nullable=True)
    can_create_project = Column(Boolean, nullable=True)
    two_factor_enabled = Column(Boolean, nullable=True)
    external = Column(Boolean, nullable=True)
    private_profile = Column(Boolean, nullable=True)
    current_sign_in_ip = Column(String, nullable=True)
    last_sign_in_ip = Column(String, nullable=True)
    email_reset_offered_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    access_level = Column(Integer, nullable=True)
    approved = Column(Boolean, nullable=True)
    invited = Column(Boolean, nullable=True)
    public_email = Column(String, nullable=True)
    pronouns = Column(String, nullable=True)
    bot = Column(Boolean, nullable=True)
    work_information = Column(String, nullable=True)
    followers = Column(Integer, nullable=True)
    following = Column(Integer, nullable=True)
    local_time = Column(String, nullable=True)
    commit_email = Column(String, nullable=True)
    shared_runners_minutes_limit = Column(Integer, nullable=True)
    extra_shared_runners_minutes_limit = Column(Integer, nullable=True)
    membership_type = Column(String, nullable=True)
    removable = Column(Boolean, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

    created_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )
    created_by = relationship(
        "UserDBModel",
        remote_side=[id],
        backref=backref("users", remote_side=[created_by_id]),
    )

    group_saml_identity_id = Column(
        Integer,
        ForeignKey(
            column="group_saml_identities.id", name="fk_user_group_saml_identity_id"
        ),
        nullable=True,
    )
    group_saml_identity = relationship(
        argument="GroupSamlIdentityDBModel",
        foreign_keys=[group_saml_identity_id],
        backref=backref("users"),
    )

    namespace_id = Column(
        Integer,
        ForeignKey(column="namespaces.id", name="fk_user_namespace_id"),
        nullable=True,
    )
    namespace = relationship(
        argument="NamespaceDBModel",
        foreign_keys=[namespace_id],
        backref=backref("users"),
    )


# Users Model
class UsersDBModel(BaseDBModel):
    __tablename__ = "users_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Users")
    users = relationship(
        "UserDBModel",
        secondary=users_association,
        backref=backref("users_collections", lazy="dynamic"),
    )


# Namespace Model
class NamespaceDBModel(BaseDBModel):
    __tablename__ = "namespaces"

    id = Column(
        Integer,
        ForeignKey(column="namespaces.id", name="fk_namespace_id"),
        primary_key=True,
    )
    base_type = Column(String, default="Namespace")
    name = Column(String, nullable=True)
    path = Column(String, nullable=True)
    kind = Column(String, nullable=True)
    full_path = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    billable_members_count = Column(Integer, nullable=True)
    plan = Column(String, nullable=True)
    trial_ends_on = Column(DateTime, nullable=True)
    trial = Column(Boolean, nullable=True)

    parent_id = Column(
        Integer,
        nullable=True,
    )

    project = relationship("ProjectDBModel", back_populates="namespace")

    user_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_namespace_user"), nullable=True
    )
    user: Mapped["User"] = relationship(
        argument="UserDBModel", foreign_keys=[user_id], backref=backref("namespaces")
    )


namespaces_association = Table(
    "namespaces_association",
    BaseDBModel.metadata,
    Column("namespaces_id", Integer, ForeignKey("namespaces.id"), primary_key=True),
    Column(
        "namespaces_collection_id",
        Integer,
        ForeignKey("namespaces_collection.id"),
        primary_key=True,
    ),
)


class NamespacesDBModel(BaseDBModel):
    __tablename__ = "namespaces_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Namespaces")
    namespaces = relationship(
        "NamespacesDBModel",
        secondary=namespaces_association,
        backref=backref("namespaces_collection", lazy="dynamic"),
    )


# Project Association tables
project_owners = Table(
    "project_owners",
    BaseDBModel.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)

project_statistics = Table(
    "project_statistics",
    BaseDBModel.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("statistics_id", Integer, ForeignKey("statistics.id")),
)

project_links = Table(
    "project_links",
    BaseDBModel.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("link_id", Integer, ForeignKey("links.id")),
)

project_additional_links = Table(
    "project_additional_links",
    BaseDBModel.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("additional_link_id", Integer, ForeignKey("links.id")),
)

project_permissions = Table(
    "project_permissions",
    BaseDBModel.metadata,
    Column(
        "project_id",
        Integer,
    ),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)

project_shared_with_groups = Table(
    "project_shared_with_groups",
    BaseDBModel.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("groups_id", Integer, ForeignKey("groups_collection.id")),
)


# Project Model
class ProjectDBModel(BaseDBModel):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Project")
    description = Column(String, nullable=True)
    description_html = Column(String, nullable=True)
    name = Column(String, nullable=True)
    name_with_namespace = Column(String, nullable=True)
    path = Column(String, nullable=True)
    path_with_namespace = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    default_branch = Column(String, nullable=True)
    tag_list = Column(JSON, nullable=True)
    topics = Column(JSON, nullable=True)
    ssh_url_to_repo = Column(String, nullable=True)
    http_url_to_repo = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    readme_url = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    forks_count = Column(Integer, nullable=True)
    star_count = Column(Integer, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)
    container_registry_image_prefix = Column(String, nullable=True)
    packages_enabled = Column(Boolean, nullable=True)
    empty_repo = Column(Boolean, nullable=True)
    archived = Column(Boolean, nullable=True)
    visibility = Column(String, nullable=True)
    resolve_outdated_diff_discussions = Column(Boolean, nullable=True)
    releases_access_level = Column(String, nullable=True)
    environments_access_level = Column(String, nullable=True)
    feature_flags_access_level = Column(String, nullable=True)
    infrastructure_access_level = Column(String, nullable=True)
    monitor_access_level = Column(String, nullable=True)
    machine_learning_model_experiments_access_level = Column(String, nullable=True)
    machine_learning_model_registry_access_level = Column(String, nullable=True)
    issues_enabled = Column(Boolean, nullable=True)
    merge_requests_enabled = Column(Boolean, nullable=True)
    wiki_enabled = Column(Boolean, nullable=True)
    jobs_enabled = Column(Boolean, nullable=True)
    snippets_enabled = Column(Boolean, nullable=True)
    container_registry_enabled = Column(Boolean, nullable=True)
    container_registry_access_level = Column(String, nullable=True)
    security_and_compliance_access_level = Column(String, nullable=True)
    import_url = Column(String, nullable=True)
    import_type = Column(String, nullable=True)
    import_status = Column(String, nullable=True)
    import_error = Column(String, nullable=True)
    shared_runners_enabled = Column(Boolean, nullable=True)
    group_runners_enabled = Column(Boolean, nullable=True)
    lfs_enabled = Column(Boolean, nullable=True)
    ci_default_git_depth = Column(Integer, nullable=True)
    ci_forward_deployment_enabled = Column(Boolean, nullable=True)
    ci_forward_deployment_rollback_allowed = Column(Boolean, nullable=True)
    ci_allow_fork_pipelines_to_run_in_parent_project = Column(Boolean, nullable=True)
    ci_separated_caches = Column(Boolean, nullable=True)
    ci_restrict_pipeline_cancellation_role = Column(String, nullable=True)
    forked_from_project = Column(JSON, nullable=True)
    mr_default_target_self = Column(Boolean, nullable=True)
    public_jobs = Column(Boolean, nullable=True)
    only_allow_merge_if_pipeline_succeeds = Column(Boolean, nullable=True)
    allow_merge_on_skipped_pipeline = Column(Boolean, nullable=True)
    restrict_user_defined_variables = Column(Boolean, nullable=True)
    code_suggestions = Column(Boolean, nullable=True)
    only_allow_merge_if_all_discussions_are_resolved = Column(Boolean, nullable=True)
    remove_source_branch_after_merge = Column(Boolean, nullable=True)
    request_access_enabled = Column(Boolean, nullable=True)
    merge_pipelines_enabled = Column(Boolean, nullable=True)
    merge_trains_skip_train_allowed = Column(Boolean, nullable=True)
    allow_pipeline_trigger_approve_deployment = Column(Boolean, nullable=True)
    repository_object_format = Column(String, nullable=True)
    merge_method = Column(String, nullable=True)
    squash_option = Column(String, nullable=True)
    enforce_auth_checks_on_uploads = Column(Boolean, nullable=True)
    suggestion_commit_message = Column(String, nullable=True)
    compliance_frameworks = Column(JSON, nullable=True)
    issues_template = Column(String, nullable=True)
    merge_requests_template = Column(String, nullable=True)
    packages_relocation_enabled = Column(Boolean, nullable=True)
    requirements_enabled = Column(Boolean, nullable=True)
    build_git_strategy = Column(String, nullable=True)
    build_timeout = Column(Integer, nullable=True)
    auto_cancel_pending_pipelines = Column(String, nullable=True)
    build_coverage_regex = Column(String, nullable=True)
    ci_config_path = Column(String, nullable=True)
    shared_runners_minutes_limit = Column(Integer, nullable=True)
    extra_shared_runners_minutes_limit = Column(Integer, nullable=True)
    printing_merge_request_link_enabled = Column(Boolean, nullable=True)
    merge_trains_enabled = Column(Boolean, nullable=True)
    has_open_issues = Column(Boolean, nullable=True)
    approvals_before_merge = Column(Integer, nullable=True)
    mirror = Column(Boolean, nullable=True)
    mirror_user_id = Column(Integer, nullable=True)
    mirror_trigger_builds = Column(Boolean, nullable=True)
    only_mirror_protected_branches = Column(Boolean, nullable=True)
    mirror_overwrites_diverged_branches = Column(Boolean, nullable=True)
    service_desk_enabled = Column(Boolean, nullable=True)
    can_create_merge_request_in = Column(Boolean, nullable=True)
    repository_access_level = Column(String, nullable=True)
    merge_requests_access_level = Column(String, nullable=True)
    issues_access_level = Column(String, nullable=True)
    forking_access_level = Column(String, nullable=True)
    wiki_access_level = Column(String, nullable=True)
    builds_access_level = Column(String, nullable=True)
    snippets_access_level = Column(String, nullable=True)
    pages_access_level = Column(String, nullable=True)
    analytics_access_level = Column(String, nullable=True)
    emails_disabled = Column(Boolean, nullable=True)
    emails_enabled = Column(Boolean, nullable=True)
    open_issues_count = Column(Integer, nullable=True)
    ci_job_token_scope_enabled = Column(Boolean, nullable=True)
    merge_commit_template = Column(String, nullable=True)
    squash_commit_template = Column(String, nullable=True)
    issue_branch_template = Column(String, nullable=True)
    auto_devops_enabled = Column(Boolean, nullable=True)
    auto_devops_deploy_strategy = Column(String, nullable=True)
    autoclose_referenced_issues = Column(Boolean, nullable=True)
    keep_latest_artifact = Column(Boolean, nullable=True)
    runner_token_expiration_interval = Column(Boolean, nullable=True)
    external_authorization_classification_label = Column(String, nullable=True)
    requirements_access_level = Column(String, nullable=True)
    security_and_compliance_enabled = Column(Boolean, nullable=True)
    warn_about_potentially_unwanted_characters = Column(Boolean, nullable=True)
    runners_token = Column(String, nullable=True)
    repository_storage = Column(String, nullable=True)
    service_desk_address = Column(String, nullable=True)
    marked_for_deletion_at = Column(DateTime, nullable=True)
    marked_for_deletion_on = Column(DateTime, nullable=True)
    operations_access_level = Column(String, nullable=True)
    ci_dockerfile = Column(String, nullable=True)
    public = Column(Boolean, nullable=True)

    owner = relationship(
        "UserDBModel", secondary=project_owners, backref="project_owner"
    )
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship(
        "UserDBModel", foreign_keys=[creator_id], backref="project_creators"
    )
    namespace_id = Column(Integer, ForeignKey("namespaces.id"))
    namespace = relationship("NamespaceDBModel", back_populates="project")

    container_expiration_policy_id = Column(
        Integer, ForeignKey("container_expiration_policies.id")
    )
    container_expiration_policy = relationship(
        "ContainerExpirationPolicyDBModel",
        foreign_keys=[container_expiration_policy_id],
        backref="project_container_expiration_policy",
    )
    statistics = relationship(
        "StatisticsDBModel", secondary=project_statistics, backref="project_statistics"
    )
    links_id = Column(Integer, ForeignKey("links.id"))
    links = relationship(
        "LinksDBModel", foreign_keys=[links_id], backref="project_links"
    )
    additional_links_id = Column(Integer, ForeignKey("links.id"))
    additional_links = relationship(
        "LinksDBModel",
        foreign_keys=[additional_links_id],
        backref="project_additional_links",
    )
    permissions_id = Column(Integer, ForeignKey("permissions.id"))
    permissions = relationship(
        "PermissionsDBModel",
        foreign_keys=[permissions_id],
        backref="project_permissions",
    )
    shared_with_groups = relationship(
        argument="GroupsDBModel",
        secondary=project_shared_with_groups,
        backref=backref("project_shared_with_groups"),
    )


projects_association = Table(
    "projects_association",
    BaseDBModel.metadata,
    Column("projects_collection_id", Integer, ForeignKey("projects_collection.id")),
    Column("projects_id", Integer, ForeignKey("projects.id")),
)


class ProjectsDBModel(BaseDBModel):
    __tablename__ = "projects_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Projects")
    projects = relationship(
        "ProjectDBModel",
        secondary=projects_association,
        backref=backref("projects_collection", lazy="dynamic"),
    )


# Runner Model
class RunnerDBModel(BaseDBModel):
    __tablename__ = "runners"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Runner")
    description = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
    paused = Column(Boolean, nullable=True)
    is_shared = Column(Boolean, nullable=True)
    runner_type = Column(String, nullable=True)
    name = Column(String, nullable=True)
    online = Column(Boolean, nullable=True)
    status = Column(String, nullable=True)
    contacted_at = Column(DateTime, nullable=True)
    architecture = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    revision = Column(String, nullable=True)
    version = Column(String, nullable=True)
    access_level = Column(String, nullable=True)
    maximum_timeout = Column(Integer, nullable=True)
    maintenance_note = Column(String, nullable=True)
    tag_list = Column(JSON, nullable=True)

    projects_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_runner_project"),
        nullable=True,
    )
    projects = relationship(
        argument="ProjectDBModel",
        foreign_keys=[projects_id],
        backref=backref("runners"),
    )


runners_association = Table(
    "runners_association",
    BaseDBModel.metadata,
    Column("runners_collection_id", Integer, ForeignKey("runners_collection.id")),
    Column("runners_id", Integer, ForeignKey("runners.id")),
)


class RunnersDBModel(BaseDBModel):
    __tablename__ = "runners_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Runners")
    runners = relationship(
        "RunnerDBModel",
        secondary=runners_association,
        backref=backref("runners_collection", lazy="dynamic"),
    )


# Job Model
class JobDBModel(BaseDBModel):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Job")
    coverage = Column(Float, nullable=True)
    archived = Column(Boolean, nullable=True)
    allow_failure = Column(Boolean, nullable=True)
    created_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    erased_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    queued_duration = Column(Float, nullable=True)
    artifacts_expire_at = Column(DateTime, nullable=True)
    name = Column(String, nullable=True)
    ref = Column(String, nullable=True)
    stage = Column(String, nullable=True)
    status = Column(String, nullable=True)
    failure_reason = Column(String, nullable=True)
    tag = Column(Boolean, nullable=True)
    web_url = Column(String, nullable=True)

    tags_list_id = Column(
        Integer,
        ForeignKey(column="tags_collection.id", name="fk_job_tags_list"),
        nullable=True,
    )

    tag_list = relationship(
        argument="TagsDBModel",
        foreign_keys=[tags_list_id],
        backref=backref("job_tag_list"),
    )

    commit_id = Column(
        String, ForeignKey(column="commits.id", name="fk_job_commit"), nullable=True
    )
    commit = relationship(
        argument="CommitDBModel",
        foreign_keys=[commit_id],
        backref=backref("jobs_commits"),
    )

    pipeline_id = Column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_job_pipeline"),
        nullable=True,
    )
    pipeline = relationship(
        argument="PipelineDBModel",
        foreign_keys=[pipeline_id],
        backref=backref("jobs_pipeline"),
    )

    runner_id = Column(
        Integer, ForeignKey(column="runners.id", name="fk_job_runner"), nullable=True
    )
    runner = relationship(argument="RunnerDBModel", backref=backref("jobs_runner"))

    runner_manager_id = Column(
        Integer,
        ForeignKey(column="runner_managers.id", name="fk_job_runner_manager"),
        nullable=True,
    )
    runner_manager = relationship(
        argument="RunnerManagerDBModel",
        foreign_keys=[runner_manager_id],
        backref=backref("jobs_runner_manager"),
    )

    project_id = Column(
        Integer, ForeignKey(column="projects.id", name="fk_job_project"), nullable=True
    )
    project = relationship(argument="ProjectDBModel", backref=backref("jobs_projects"))

    user_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_job_user"), nullable=True
    )
    user = relationship(
        argument="UserDBModel", foreign_keys=[user_id], backref=backref("jobs_users")
    )

    downstream_pipeline_id = Column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_job_downstream_pipeline"),
        nullable=True,
    )
    downstream_pipeline = relationship(
        argument="PipelineDBModel",
        foreign_keys=[downstream_pipeline_id],
        backref=backref("jobs_downstream"),
    )

    artifacts_file_id = Column(
        Integer,
        ForeignKey(column="artifacts_files.id", name="fk_job_artifacts_file"),
        nullable=True,
    )
    artifacts_file = relationship(
        argument="ArtifactsFileDBModel", backref=backref("jobs_artifact_file")
    )

    artifacts_id = Column(
        Integer,
        ForeignKey(column="artifacts_collection.id", name="fk_job_artifacts"),
        nullable=True,
    )
    artifacts = relationship(
        argument="ArtifactsDBModel", backref=backref("jobs_artifacts")
    )


jobs_association = Table(
    "jobs_association",
    BaseDBModel.metadata,
    Column("jobs_collection_id", Integer, ForeignKey("jobs_collection.id")),
    Column("jobs_id", Integer, ForeignKey("jobs.id")),
)


class JobsDBModel(BaseDBModel):
    __tablename__ = "jobs_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Jobs")
    jobs = relationship(
        "JobDBModel",
        secondary=jobs_association,
        backref=backref("jobs_collection", lazy="dynamic"),
    )


# Pipeline Model
class PipelineDBModel(BaseDBModel):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Pipeline")
    iid = Column(Integer, nullable=True)
    ref = Column(String, nullable=True)
    sha = Column(String, nullable=True)
    status = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    project_id = Column(
        Integer,
        ForeignKey(column="projects.id", name="fk_pipeline_project"),
        nullable=True,
    )
    before_sha = Column(String, nullable=True)
    tag = Column(Boolean, nullable=True)
    yaml_errors = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    committed_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    queued_duration = Column(Float, nullable=True)
    coverage = Column(String, nullable=True)
    name = Column(String, nullable=True)
    source = Column(String, nullable=True)

    user_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_pipeline_user"), nullable=True
    )
    user = relationship(
        argument="UserDBModel",
        foreign_keys=[user_id],
        backref=backref("pipelines_user"),
    )

    detailed_status_id = Column(
        Integer,
        ForeignKey(column="detailed_status.id", name="fk_pipeline_detailed_status"),
        nullable=True,
    )
    detailed_status = relationship(
        argument="DetailedStatusDBModel",
        foreign_keys=[detailed_status_id],
        backref=backref("pipelines_status"),
    )

    job_id = Column(
        Integer, ForeignKey(column="jobs.id", name="fk_pipeline_job"), nullable=True
    )
    jobs = relationship(
        argument="JobDBModel", foreign_keys=[job_id], backref=backref("pipeline_jobs")
    )


pipelines_association = Table(
    "pipelines_association",
    BaseDBModel.metadata,
    Column("pipelines_collection_id", Integer, ForeignKey("pipelines_collection.id")),
    Column("pipelines_id", Integer, ForeignKey("pipelines.id")),
)


class PipelinesDBModel(BaseDBModel):
    __tablename__ = "pipelines_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Pipelines")
    pipelines = relationship(
        "PipelineDBModel",
        secondary=pipelines_association,
        backref=backref("pipelines_collection", lazy="dynamic"),
    )


# PackageLink Model
class PackageLinkDBModel(BaseDBModel):
    __tablename__ = "package_links"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="PackageLink")
    web_path = Column(String, nullable=True)
    delete_api_path = Column(String, nullable=True)


# PackageVersion Model
class PackageVersionDBModel(BaseDBModel):
    __tablename__ = "package_versions"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="PackageVersion")
    version = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)

    pipeline_id = Column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_package_version_pipeline"),
        nullable=True,
    )
    pipelines = relationship(
        argument="PipelineDBModel",
        foreign_keys=[pipeline_id],
        backref=backref("pipeline_package_versions"),
    )
    package_id = Column(
        Integer,
        ForeignKey(column="packages.id", name="fk_package_version_package"),
        nullable=True,
    )
    packages = relationship(
        argument="PackageDBModel",
        foreign_keys=[package_id],
        backref=backref("package_versions_package"),
    )


# Package Model
class PackageDBModel(BaseDBModel):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Package")
    name = Column(String, nullable=True)
    version = Column(String, nullable=True)
    package_type = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    last_downloaded_at = Column(DateTime, nullable=True)
    conan_package_name = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    file_name = Column(String, nullable=True)
    file_md5 = Column(String, nullable=True)
    file_sha1 = Column(String, nullable=True)
    file_sha256 = Column(String, nullable=True)

    links_id = Column(
        Integer,
        ForeignKey(column="package_links.id", name="fk_package_links"),
        nullable=True,
    )
    links = relationship(
        argument="PackageLinkDBModel",
        foreign_keys=[links_id],
        backref=backref("packages_links"),
    )

    pipeline_id = Column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_package_pipeline"),
        nullable=True,
    )
    pipelines = relationship(
        argument="PipelineDBModel",
        foreign_keys=[pipeline_id],
        backref=backref("packages"),
    )
    versions_id = Column(
        Integer,
        ForeignKey(column="package_versions.id", name="fk_package_version"),
        nullable=True,
    )
    package_versions = relationship(
        argument="PackageVersionDBModel",
        foreign_keys=[versions_id],
        backref=backref("packages_versions"),
    )


packages_association = Table(
    "packages_association",
    BaseDBModel.metadata,
    Column("packages_collection_id", Integer, ForeignKey("packages_collection.id")),
    Column("packages_id", Integer, ForeignKey("packages.id")),
)


class PackagesDBModel(BaseDBModel):
    __tablename__ = "packages_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Packages")
    packages = relationship(
        "PackageDBModel",
        secondary=packages_association,
        backref=backref("packages_collection", lazy="dynamic"),
    )


# Contributor Model
class ContributorDBModel(BaseDBModel):
    __tablename__ = "contributors"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Contributor")
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    commits = Column(Integer, nullable=True)
    additions = Column(Integer, nullable=True)
    deletions = Column(Integer, nullable=True)


contributors_association = Table(
    "contributors_association",
    BaseDBModel.metadata,
    Column(
        "contributors_collection_id", Integer, ForeignKey("contributors_collection.id")
    ),
    Column("contributors_id", Integer, ForeignKey("contributors.id")),
)


class ContributorsDBModel(BaseDBModel):
    __tablename__ = "contributors_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Contributors")
    contributors = relationship(
        "ContributorDBModel",
        secondary=contributors_association,
        backref=backref("contributors_collection", lazy="dynamic"),
    )


# CommitStats Model
class CommitStatsDBModel(BaseDBModel):
    __tablename__ = "commit_stats"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="CommitStats")
    additions = Column(Integer, nullable=True)
    deletions = Column(Integer, nullable=True)
    total = Column(Integer, nullable=True)


# CommitSignature Model
class CommitSignatureDBModel(BaseDBModel):
    __tablename__ = "commit_signatures"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="CommitSignature")
    signature_type = Column(String, nullable=True)
    verification_status = Column(String, nullable=True)
    commit_source = Column(String, nullable=True)
    gpg_key_id = Column(Integer, nullable=True)
    gpg_key_primary_keyid = Column(String, nullable=True)
    gpg_key_user_name = Column(String, nullable=True)
    gpg_key_user_email = Column(String, nullable=True)
    gpg_key_subkey_id = Column(String, nullable=True)
    key = Column(JSON, nullable=True)
    x509_certificate = Column(JSON, nullable=True)
    message = Column(String, nullable=True)


# Comment Model
class CommentDBModel(BaseDBModel):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Comment")
    type = Column(String, nullable=True)
    body = Column(String, nullable=True)
    note = Column(String, nullable=True)
    attachment = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    system = Column(Boolean, nullable=True)
    noteable_id = Column(Integer, nullable=True)
    noteable_type = Column(String, nullable=True)
    resolvable = Column(Boolean, nullable=True)
    confidential = Column(Boolean, nullable=True)
    noteable_iid = Column(Integer, nullable=True)
    commands_changes = Column(JSON, nullable=True)
    line_type = Column(String, nullable=True)
    path = Column(String, nullable=True)
    line = Column(Integer, nullable=True)

    author_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_comment_author"), nullable=True
    )
    author = relationship(
        argument="UserDBModel", foreign_keys=[author_id], backref=backref("comments")
    )

    commits_id = Column(
        String,
        ForeignKey(column="commits.id", name="fk_comment_commit"),
        nullable=True,
    )
    commits = relationship(
        argument="CommitDBModel",
        foreign_keys=[commits_id],
        backref=backref("commit_comments"),
    )


comments_association = Table(
    "comments_association",
    BaseDBModel.metadata,
    Column("comments_collection_id", Integer, ForeignKey("comments_collection.id")),
    Column("comments_id", Integer, ForeignKey("comments.id")),
)


class CommentsDBModel(BaseDBModel):
    __tablename__ = "comments_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Comments")
    comments = relationship(
        "CommentDBModel",
        secondary=comments_association,
        backref=backref("comments_collection", lazy="dynamic"),
    )


parent_ids_association = Table(
    "parent_ids_association",
    BaseDBModel.metadata,
    Column("parent_ids_id", Integer, ForeignKey("parent_ids.id"), primary_key=True),
    Column(
        "parent_ids_collection",
        Integer,
        ForeignKey("parent_ids_collection.id"),
        primary_key=True,
    ),
)


class ParentIDDBModel(BaseDBModel):
    __tablename__ = "parent_ids"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="ParentID")
    parent_id = Column(String, nullable=False)


class ParentIDsDBModel(BaseDBModel):
    __tablename__ = "parent_ids_collection"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    base_type = Column(String, default="ParentIDs")
    parent_ids = relationship(
        "ParentIDDBModel",
        secondary=parent_ids_association,
        backref=backref("parent_ids_collection", lazy="dynamic"),
    )


# Commit Model
class CommitDBModel(BaseDBModel):
    __tablename__ = "commits"

    id = Column(String, primary_key=True)
    base_type = Column(String, default="Commit")
    short_id = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    message = Column(String, nullable=True)
    author_name = Column(String, nullable=True)
    author_email = Column(String, nullable=True)
    authored_date = Column(DateTime, nullable=True)
    committer_name = Column(String, nullable=True)
    committer_email = Column(String, nullable=True)
    committed_date = Column(DateTime, nullable=True)
    name = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    trailers = Column(JSON, nullable=True)
    extended_trailers = Column(JSON, nullable=True)
    status = Column(String, nullable=True)
    sha = Column(String, nullable=True)
    count = Column(Integer, nullable=True)
    dry_run = Column(String, nullable=True)
    individual_note = Column(Boolean, nullable=True)
    allow_failure = Column(Boolean, nullable=True)
    target_url = Column(String, nullable=True)
    ref = Column(String, nullable=True)
    error_code = Column(String, nullable=True)
    coverage = Column(Float, nullable=True)

    author_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_commit_author"), nullable=True
    )
    author = relationship(
        argument="UserDBModel",
        foreign_keys=[author_id],
        backref=backref("commits_author"),
    )

    stats_id = Column(
        Integer,
        ForeignKey(column="commit_stats.id", name="fk_commit_stats"),
        nullable=True,
    )
    stats = relationship(
        argument="CommitStatsDBModel",
        foreign_keys=[stats_id],
        backref=backref("commits_stats"),
    )

    last_pipeline_id = Column(
        Integer,
        ForeignKey(column="pipelines.id", name="fk_commit_last_pipeline"),
        nullable=True,
    )
    last_pipeline = relationship(
        argument="PipelineDBModel",
        foreign_keys=[last_pipeline_id],
        backref=backref("commits_last_pipeline"),
    )

    commit_signatures_id = Column(
        Integer,
        ForeignKey(column="commit_signatures.id", name="fk_commit_signatures"),
        nullable=True,
    )
    commit_signatures = relationship(
        argument="CommitSignatureDBModel",
        foreign_keys=[commit_signatures_id],
        backref=backref("commits_signatures"),
    )

    notes_id = Column(
        Integer, ForeignKey(column="comments.id", name="fk_commit_notes"), nullable=True
    )
    notes = relationship(
        argument="CommentDBModel",
        foreign_keys=[notes_id],
        backref=backref("commit_notes"),
    )
    parent_ids_id = Column(
        Integer,
        ForeignKey(column="parent_ids_collection.id", name="fk_commit_parent_ids"),
        nullable=True,
    )
    parent_ids = relationship(
        argument="ParentIDsDBModel",
        foreign_keys=[parent_ids_id],
        backref=backref("commit_parent_ids"),
    )


commits_association = Table(
    "commits_association",
    BaseDBModel.metadata,
    Column("commits_collection_id", String, ForeignKey("commits_collection.id")),
    Column("commits_id", String, ForeignKey("commits.id")),
)


class CommitsDBModel(BaseDBModel):
    __tablename__ = "commits_collection"

    id = Column(String, primary_key=True)
    base_type = Column(String, default="Commits")
    commits = relationship(
        "CommitDBModel",
        secondary=commits_association,
        backref=backref("commits_collection", lazy="dynamic"),
    )


# Membership Model
class MembershipDBModel(BaseDBModel):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Membership")
    source_id = Column(Integer, nullable=True)
    source_full_name = Column(String, nullable=True)
    source_members_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    access_level = Column(JSON, nullable=True)


memberships_association = Table(
    "memberships_association",
    BaseDBModel.metadata,
    Column(
        "memberships_collection_id", Integer, ForeignKey("memberships_collection.id")
    ),
    Column("memberships_id", Integer, ForeignKey("memberships.id")),
)


class MembershipsDBModel(BaseDBModel):
    __tablename__ = "memberships_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Memberships")
    memberships = relationship(
        "MembershipDBModel",
        secondary=memberships_association,
        backref=backref("memberships_collection", lazy="dynamic"),
    )


# Issue Model
class IssueDBModel(BaseDBModel):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Issue")
    state = Column(String, nullable=True)
    description = Column(String, nullable=True)
    project_id = Column(
        Integer, ForeignKey(column="projects.id", name="fk_project"), nullable=True
    )
    type = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    changes_count = Column(String, nullable=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    moved_to_id = Column(Integer, nullable=True)
    iid = Column(Integer, nullable=True)
    labels = Column(ARRAY(String), nullable=True)
    upvotes = Column(Integer, nullable=True)
    downvotes = Column(Integer, nullable=True)
    merge_requests_count = Column(Integer, nullable=True)
    user_notes_count = Column(Integer, nullable=True)
    due_date = Column(String, nullable=True)
    imported = Column(Boolean, nullable=True)
    imported_from = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    has_tasks = Column(Boolean, nullable=True)
    task_status = Column(String, nullable=True)
    confidential = Column(Boolean, nullable=True)
    discussion_locked = Column(Boolean, nullable=True)
    issue_type = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    epic_iid = Column(Integer, nullable=True)
    health_status = Column(String, nullable=True)
    subscribed = Column(Boolean, nullable=True)
    service_desk_reply_to = Column(String, nullable=True)
    blocking_issues_count = Column(Integer, nullable=True)

    author_id = Column(
        Integer, ForeignKey(column="users.id"), nullable=True, name="fk_issue_author"
    )
    author = relationship(
        argument="UserDBModel",
        foreign_keys=[author_id],
        backref=backref("authored_issues"),
    )

    milestone_id = Column(
        Integer,
        ForeignKey(column="milestones.id", name="fk_issue_milestone"),
        nullable=True,
    )
    milestone = relationship(
        argument="MilestoneDBModel",
        foreign_keys=[milestone_id],
        backref=backref("issues"),
    )

    assignee_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_issue_assignee"), nullable=True
    )
    assignee = relationship(
        argument="UserDBModel",
        foreign_keys=[assignee_id],
        backref=backref("assigned_issues"),
    )

    closed_by_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_issue_closed_by"), nullable=True
    )
    iteration_id = Column(
        Integer,
        ForeignKey(column="iterations.id", name="fk_issue_iteration"),
        nullable=True,
    )
    epic_id = Column(
        Integer, ForeignKey(column="epics.id", name="fk_issue_epic"), nullable=True
    )
    closed_by = relationship(
        argument="UserDBModel",
        foreign_keys=[closed_by_id],
        backref=backref("closed_issues"),
    )
    iteration = relationship(argument="IterationDBModel", backref=backref("issues"))
    epic = relationship(argument="EpicDBModel", backref=backref("issues"))


issues_association = Table(
    "issues_association",
    BaseDBModel.metadata,
    Column("issues_collection_id", Integer, ForeignKey("issues_collection.id")),
    Column("issues_id", Integer, ForeignKey("issues.id")),
)


class IssuesDBModel(BaseDBModel):
    __tablename__ = "issues_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Issues")
    issues = relationship(
        "IssueDBModel",
        secondary=issues_association,
        backref=backref("issues_collection", lazy="dynamic"),
    )


# TimeStats Model
class TimeStatsDBModel(BaseDBModel):
    __tablename__ = "time_stats"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="TimeStats")
    time_estimate = Column(Integer, nullable=True)
    total_time_spent = Column(Integer, nullable=True)
    human_time_estimate = Column(String, nullable=True)
    human_total_time_spent = Column(String, nullable=True)


# TaskCompletionStatus Model
class TaskCompletionStatusDBModel(BaseDBModel):
    __tablename__ = "task_completion_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="TaskCompletionStatus")
    count = Column(Integer, nullable=True)
    completed_count = Column(Integer, nullable=True)


# References Model
class ReferencesDBModel(BaseDBModel):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="References")
    short = Column(String, nullable=True)
    relative = Column(String, nullable=True)
    full = Column(String, nullable=True)


artifacts_association = Table(
    "artifacts_association",
    BaseDBModel.metadata,
    Column("artifacts_collection_id", Integer, ForeignKey("artifacts_collection.id")),
    Column("artifact_id", Integer, ForeignKey("artifacts.id")),
)


# Artifact Model
class ArtifactDBModel(BaseDBModel):
    __tablename__ = "artifacts"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Artifact")
    file_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    filename = Column(String, nullable=True)
    file_format = Column(String, nullable=True)


class ArtifactsDBModel(BaseDBModel):
    __tablename__ = "artifacts_collection"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    base_type = Column(String, default="Artifacts")
    artifacts = relationship(
        "ArtifactDBModel",
        secondary=artifacts_association,
        backref=backref("artifacts_collection", lazy="dynamic"),
    )


# ArtifactsFile Model
class ArtifactsFileDBModel(BaseDBModel):
    __tablename__ = "artifacts_files"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ArtifactsFile")
    filename = Column(String, nullable=True)
    size = Column(Integer, nullable=True)


# RunnerManager Model
class RunnerManagerDBModel(BaseDBModel):
    __tablename__ = "runner_managers"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="RunnerManager")
    system_id = Column(String, nullable=True)
    version = Column(String, nullable=True)
    revision = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    architecture = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    contacted_at = Column(DateTime, nullable=True)
    ip_address = Column(String, nullable=True)
    status = Column(String, nullable=True)


# Configuration Model
class ConfigurationDBModel(BaseDBModel):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Configuration")
    approvals_before_merge = Column(Integer, nullable=True)
    reset_approvals_on_push = Column(Boolean, nullable=True)
    selective_code_owner_removals = Column(Boolean, nullable=True)
    disable_overriding_approvers_per_merge_request = Column(Boolean, nullable=True)
    merge_requests_author_approval = Column(Boolean, nullable=True)
    merge_requests_disable_committers_approval = Column(Boolean, nullable=True)
    require_password_to_approve = Column(Boolean, nullable=True)


# Iteration Model
class IterationDBModel(BaseDBModel):
    __tablename__ = "iterations"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Iteration")
    iid = Column(Integer, nullable=True)
    sequence = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    start_date = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    web_url = Column(String, nullable=True)

    group_id = Column(
        Integer,
        ForeignKey(column="groups.id", name="fk_iteration_group"),
        nullable=True,
    )
    group = relationship(
        argument="GroupDBModel", foreign_keys=[group_id], backref=backref("iterations")
    )


# Identity Model
class IdentityDBModel(BaseDBModel):
    __tablename__ = "identities"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Identity")
    provider = Column(String, nullable=True)
    extern_uid = Column(String, nullable=True)

    user_id = Column(
        Integer, ForeignKey(column="users.id", name="fk_identity_user"), nullable=True
    )
    user = relationship(
        argument="UserDBModel", foreign_keys=[user_id], backref=backref("identities")
    )


identities_association = Table(
    "identities_association",
    BaseDBModel.metadata,
    Column("identities_id", Integer, ForeignKey("identities.id"), primary_key=True),
    Column(
        "identities_collection_id",
        Integer,
        ForeignKey("identities_collection.id"),
        primary_key=True,
    ),
)


class IdentitiesDBModel(BaseDBModel):
    __tablename__ = "identities_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Identities")
    identities = relationship(
        "IdentityDBModel",
        secondary=identities_association,
        backref=backref("identities_collection", lazy="dynamic"),
    )


# GroupSamlIdentity Model
class GroupSamlIdentityDBModel(BaseDBModel):
    __tablename__ = "group_saml_identities"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="GroupSamlIdentity")
    extern_uid = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    saml_provider_id = Column(Integer, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_group_saml_identity_user_id"),
        nullable=True,
    )
    user = relationship(
        argument="UserDBModel",
        foreign_keys=[user_id],
        backref=backref("group_saml_identities_user"),
    )


# ContainerExpirationPolicy Model
class ContainerExpirationPolicyDBModel(BaseDBModel):
    __tablename__ = "container_expiration_policies"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ContainerExpirationPolicy")
    cadence = Column(String, nullable=True)
    enabled = Column(Boolean, nullable=True)
    keep_n = Column(Integer, nullable=True)
    older_than = Column(String, nullable=True)
    name_regex = Column(String, nullable=True)
    name_regex_keep = Column(String, nullable=True)
    next_run_at = Column(DateTime, nullable=True)


# Permissions Model
class PermissionsDBModel(BaseDBModel):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Permissions")
    project_access = Column(JSON, nullable=True)
    group_access = Column(JSON, nullable=True)


# Statistics Model
class StatisticsDBModel(BaseDBModel):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Statistics")
    commit_count = Column(Integer, nullable=True)
    storage_size = Column(Integer, nullable=True)
    repository_size = Column(Integer, nullable=True)
    wiki_size = Column(Integer, nullable=True)
    lfs_objects_size = Column(Integer, nullable=True)
    job_artifacts_size = Column(Integer, nullable=True)
    pipeline_artifacts_size = Column(Integer, nullable=True)
    packages_size = Column(Integer, nullable=True)
    snippets_size = Column(Integer, nullable=True)
    uploads_size = Column(Integer, nullable=True)


# Diff Model
class DiffDBModel(BaseDBModel):
    __tablename__ = "diffs"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Diff")
    head_commit_sha = Column(String, nullable=True)
    base_commit_sha = Column(String, nullable=True)
    start_commit_sha = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    state = Column(String, nullable=True)
    real_size = Column(String, nullable=True)
    patch_id_sha = Column(String, nullable=True)
    diff = Column(String, nullable=True)
    new_path = Column(String, nullable=True)
    old_path = Column(String, nullable=True)
    a_mode = Column(String, nullable=True)
    b_mode = Column(String, nullable=True)
    new_file = Column(Boolean, nullable=True)
    renamed_file = Column(Boolean, nullable=True)
    deleted_file = Column(Boolean, nullable=True)
    generated_file = Column(Boolean, nullable=True)

    merge_request_id = Column(
        Integer,
        ForeignKey(column="merge_requests.id", name="fk_diff_merge_request"),
        nullable=True,
    )
    merge_request = relationship(
        argument="MergeRequestDBModel",
        foreign_keys=[merge_request_id],
        backref=backref("diffs"),
    )


diffs_association = Table(
    "diffs_association",
    BaseDBModel.metadata,
    Column("diffs_id", Integer, ForeignKey("diffs.id"), primary_key=True),
    Column(
        "diffs_collection_id",
        Integer,
        ForeignKey("diffs_collection.id"),
        primary_key=True,
    ),
)


class DiffsDBModel(BaseDBModel):
    __tablename__ = "diffs_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="Diffs")
    diffs = relationship(
        "DiffDBModel",
        secondary=diffs_association,
        backref=backref("diffs_collection", lazy="dynamic"),
    )


class MergeApprovalsDBModel(BaseDBModel):
    __tablename__ = "merge_approvals"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="MergeApprovals")
    approvals_before_merge = Column(Integer, nullable=True)
    reset_approvals_on_push = Column(Boolean, nullable=True)
    selective_code_owner_removals = Column(Boolean, nullable=True)
    disable_overriding_approvers_per_merge_request = Column(Boolean, nullable=True)
    merge_requests_author_approval = Column(Boolean, nullable=True)
    merge_requests_disable_committers_approval = Column(Boolean, nullable=True)
    require_password_to_approve = Column(Boolean, nullable=True)

    approvers_id = Column(
        Integer,
        ForeignKey(column="users.id", name="fk_merge_approvals_approvers"),
        nullable=True,
    )
    approvers = relationship(
        argument="UserDBModel",
        foreign_keys=[approvers_id],
        backref=backref("merge_approvals"),
    )

    approver_groups_id = Column(
        Integer,
        ForeignKey(column="groups.id", name="fk_merge_approvals_approver_groups"),
        nullable=True,
    )
    approver_groups = relationship(
        argument="GroupDBModel",
        foreign_keys=[approver_groups_id],
        backref=backref("merge_approvals"),
    )


# DetailedStatus Model
class DetailedStatusDBModel(BaseDBModel):
    __tablename__ = "detailed_status"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="DetailedStatus")
    icon = Column(String, nullable=True)
    text = Column(String, nullable=True)
    label = Column(String, nullable=True)
    group = Column(String, nullable=True)
    tooltip = Column(String, nullable=True)
    has_details = Column(Boolean, nullable=True)
    details_path = Column(String, nullable=True)
    illustration = Column(JSON, nullable=True)
    favicon = Column(String, nullable=True)


# pytest: ignore these classes
class TestReportDBModel(BaseDBModel):
    __tablename__ = "test_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="TestReport")
    total_time = Column(Integer, nullable=True)
    total_count = Column(Integer, nullable=True)
    success_count = Column(Integer, nullable=True)
    failed_count = Column(Integer, nullable=True)
    skipped_count = Column(Integer, nullable=True)
    error_count = Column(Integer, nullable=True)

    total_id = Column(
        Integer,
        ForeignKey(column="test_report_totals.id", name="fk_test_report_total"),
        nullable=True,
    )
    total = relationship(
        argument="TestReportTotalDBModel",
        foreign_keys=[total_id],
        backref=backref("test_reports"),
    )

    test_suites_id = Column(
        Integer,
        ForeignKey(column="test_suites.id", name="fk_test_report_test_suite"),
        nullable=True,
    )
    test_suites = relationship(
        argument="TestSuiteDBModel",
        foreign_keys=[test_suites_id],
        backref=backref("test_reports"),
    )


class ProjectConfigDBModel(BaseDBModel):
    __tablename__ = "project_configs"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ProjectConfig")
    description = Column(String, nullable=True)
    name = Column(String, nullable=False)
    name_with_namespace = Column(String, nullable=False)
    path = Column(String, nullable=False)
    path_with_namespace = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


# Epic Model
class EpicDBModel(BaseDBModel):
    __tablename__ = "epics"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Epic")
    iid = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)

    group_id = Column(
        Integer, ForeignKey(column="groups.id", name="fk_epic_group"), nullable=True
    )
    groups = relationship(
        argument="GroupDBModel", foreign_keys=[group_id], backref=backref("epics")
    )


# TestCase Model
class TestCaseDBModel(BaseDBModel):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="TestCase")
    status = Column(String, nullable=True)
    name = Column(String, nullable=True)
    classname = Column(String, nullable=True)
    execution_time = Column(Float, nullable=True)
    system_output = Column(String, nullable=True)
    stack_trace = Column(String, nullable=True)


test_cases_association = Table(
    "test_cases_association",
    BaseDBModel.metadata,
    Column("test_cases_id", Integer, ForeignKey("test_cases.id"), primary_key=True),
    Column(
        "test_cases_collection_id",
        Integer,
        ForeignKey("test_cases_collection.id"),
        primary_key=True,
    ),
)


class TestCasesDBModel(BaseDBModel):
    __tablename__ = "test_cases_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="TestCases")
    test_cases = relationship(
        "TestCaseDBModel",
        secondary=test_cases_association,
        backref=backref("test_cases_collection", lazy="dynamic"),
    )


# TestSuite Model
class TestSuiteDBModel(BaseDBModel):
    __tablename__ = "test_suites"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="TestSuite")
    name = Column(String, nullable=True)
    total_time = Column(Float, nullable=True)
    total_count = Column(Integer, nullable=True)
    success_count = Column(Integer, nullable=True)
    failed_count = Column(Integer, nullable=True)
    skipped_count = Column(Integer, nullable=True)
    error_count = Column(Integer, nullable=True)
    suite_error = Column(String, nullable=True)

    test_cases_id = Column(
        Integer,
        ForeignKey(column="test_cases.id", name="fk_test_suite_test_cases"),
        nullable=True,
    )
    test_cases = relationship(
        argument="TestCaseDBModel",
        foreign_keys=[test_cases_id],
        backref=backref("test_suites"),
    )


test_suites_association = Table(
    "test_suites_association",
    BaseDBModel.metadata,
    Column("test_suites_id", Integer, ForeignKey("test_suites.id"), primary_key=True),
    Column(
        "test_suites_collection_id",
        Integer,
        ForeignKey("test_suites_collection.id"),
        primary_key=True,
    ),
)


class TestSuitesDBModel(BaseDBModel):
    __tablename__ = "test_suites_collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="TestSuites")
    test_suites = relationship(
        "TestSuiteDBModel",
        secondary=test_suites_association,
        backref=backref("test_cases_collection", lazy="dynamic"),
    )


# TestReportTotal Model
class TestReportTotalDBModel(BaseDBModel):
    __tablename__ = "test_report_totals"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="TestReportTotal")
    time = Column(Integer, nullable=True)
    count = Column(Integer, nullable=True)
    success = Column(Integer, nullable=True)
    failed = Column(Integer, nullable=True)
    skipped = Column(Integer, nullable=True)
    error = Column(Integer, nullable=True)
    suite_error = Column(String, nullable=True)
