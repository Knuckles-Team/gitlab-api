"""GitLab graph configuration — tag prompts and env var mappings.

This is the only file needed to enable graph mode for this agent.
Provides TAG_PROMPTS and TAG_ENV_VARS for create_graph_agent_server().
"""

TAG_PROMPTS: dict[str, str] = {
    "branches": (
        "You are a GitLab Branches specialist. Help users manage and interact with Branches functionality using the available tools."
    ),
    "commits": (
        "You are a GitLab Commits specialist. Help users manage and interact with Commits functionality using the available tools."
    ),
    "custom-api": (
        "You are a GitLab Custom Api specialist. Help users manage and interact with Custom Api functionality using the available tools."
    ),
    "deploy_tokens": (
        "You are a GitLab Deploy Tokens specialist. Help users manage and interact with Deploy Tokens functionality using the available tools."
    ),
    "environments": (
        "You are a GitLab Environments specialist. Help users manage and interact with Environments functionality using the available tools."
    ),
    "groups": (
        "You are a GitLab Groups specialist. Help users manage and interact with Groups functionality using the available tools."
    ),
    "jobs": (
        "You are a GitLab Jobs specialist. Help users manage and interact with Jobs functionality using the available tools."
    ),
    "members": (
        "You are a GitLab Members specialist. Help users manage and interact with Members functionality using the available tools."
    ),
    "merge-requests": (
        "You are a GitLab Merge Requests specialist. Help users manage and interact with Merge Requests functionality using the available tools."
    ),
    "merge_rules": (
        "You are a GitLab Merge Rules specialist. Help users manage and interact with Merge Rules functionality using the available tools."
    ),
    "packages": (
        "You are a GitLab Packages specialist. Help users manage and interact with Packages functionality using the available tools."
    ),
    "pipeline_schedules": (
        "You are a GitLab Pipeline Schedules specialist. Help users manage and interact with Pipeline Schedules functionality using the available tools."
    ),
    "pipelines": (
        "You are a GitLab Pipelines specialist. Help users manage and interact with Pipelines functionality using the available tools."
    ),
    "projects": (
        "You are a GitLab Projects specialist. Help users manage and interact with Projects functionality using the available tools."
    ),
    "protected_branches": (
        "You are a GitLab Protected Branches specialist. Help users manage and interact with Protected Branches functionality using the available tools."
    ),
    "releases": (
        "You are a GitLab Releases specialist. Help users manage and interact with Releases functionality using the available tools."
    ),
    "runners": (
        "You are a GitLab Runners specialist. Help users manage and interact with Runners functionality using the available tools."
    ),
    "tags": (
        "You are a GitLab Tags specialist. Help users manage and interact with Tags functionality using the available tools."
    ),
}


TAG_ENV_VARS: dict[str, str] = {
    "branches": "BRANCHESTOOL",
    "commits": "COMMITSTOOL",
    "custom-api": "CUSTOM_APITOOL",
    "deploy_tokens": "DEPLOY_TOKENSTOOL",
    "environments": "ENVIRONMENTSTOOL",
    "groups": "GROUPSTOOL",
    "jobs": "JOBSTOOL",
    "members": "MEMBERSTOOL",
    "merge-requests": "MERGE_REQUESTSTOOL",
    "merge_rules": "MERGE_RULESTOOL",
    "packages": "PACKAGESTOOL",
    "pipeline_schedules": "PIPELINE_SCHEDULESTOOL",
    "pipelines": "PIPELINESTOOL",
    "projects": "PROJECTSTOOL",
    "protected_branches": "PROTECTED_BRANCHESTOOL",
    "releases": "RELEASESTOOL",
    "runners": "RUNNERSTOOL",
    "tags": "TAGSTOOL",
}
