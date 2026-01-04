#!/usr/bin/python
# coding: utf-8

import os
import argparse
import logging
import asyncio
import uvicorn
from typing import Optional, Any

from fastmcp import Client
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool
from pydantic_ai.toolsets import FilteredToolset
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
from pydantic_ai_skills import SkillsToolset
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.huggingface import HuggingFaceModel
from fasta2a import Skill
from gitlab_api.utils import to_integer, to_boolean
from importlib.resources import files, as_file

logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Output to console
)
logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)  # Enable pydantic-ai logs
logging.getLogger("fastmcp").setLevel(logging.DEBUG)  # Enable FastMCP logs
logging.getLogger("httpx").setLevel(logging.INFO)  # Quieter HTTP logs
logger = logging.getLogger(__name__)

skills_dir = files("gitlab_api") / "skills"
with as_file(skills_dir) as path:
    skills_path = str(path)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(string=os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "maternion/fara:7b")
DEFAULT_OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", "http://localhost:8000/mcp")
DEFAULT_SKILLS_DIRECTORY = os.getenv("SKILLS_DIRECTORY", skills_path)

# Detected tags from gitlab_mcp.py
TAGS = [
    "branches",
    "commits",
    "deploy_tokens",
    "environments",
    "groups",
    "jobs",
    "members",
    "merge_requests",
    "merge_rules",
    "packages",
    "pipeline_schedules",
    "pipelines",
    "projects",
    "protected_branches",
    "releases",
    "runners",
    "tags",
    # "custom_api",
]

AGENT_NAME = "GitLab"
AGENT_DESCRIPTION = "An agent built with Agent Skills and GitLab MCP tools to maximize GitLab interactivity."


def create_model(
    provider: str,
    model_id: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
):
    if provider == "openai":
        target_base_url = base_url or DEFAULT_OPENAI_BASE_URL
        target_api_key = api_key or DEFAULT_OPENAI_API_KEY
        if target_base_url:
            os.environ["OPENAI_BASE_URL"] = target_base_url
        if target_api_key:
            os.environ["OPENAI_API_KEY"] = target_api_key
        return OpenAIChatModel(model_id, provider="openai")

    elif provider == "anthropic":
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key
        return AnthropicModel(model_id)

    elif provider == "google":
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
            os.environ["GOOGLE_API_KEY"] = api_key
        return GoogleModel(model_id)

    elif provider == "huggingface":
        if api_key:
            os.environ["HF_TOKEN"] = api_key
        return HuggingFaceModel(model_id)

    else:
        raise ValueError(f"Unsupported provider: {provider}")


from pathlib import Path
from pydantic_ai.toolsets import FilteredToolset

async def create_sub_agent(
    model: Any,
    base_toolset: Any,
    tag: str,
    system_prompt: str,
    skills_directory: str,
) -> Agent:
    """
    Helper to create a specialized sub-agent for a specific GitLab tag.
    """
    # 1. Skills Toolset: Specific to this tag (if directory exists)
    tag_skills_dir = Path(skills_directory) / f"gitlab-{tag.replace('_', '-')}"
    agent_toolsets = []
    
    if tag_skills_dir.exists():
        logger.debug(f"Loading skills for {tag} from {tag_skills_dir}")
        skills = SkillsToolset(directories=[str(tag_skills_dir)])
        agent_toolsets.append(skills)
        logger.info(f"Loaded skills for {tag} from {tag_skills_dir} - Agent Toolsets: {agent_toolsets}")
    else:
        logger.warning(f"No specific skills directory found for {tag} at {tag_skills_dir}")

    # 2. MCP Tools: Filtered by tag from the base toolset
    # We define the filter function to check the 'tags' metadata
    def tool_filter(ctx, tool_def):
        # Safely access metadata
        metadata = getattr(tool_def, "metadata", {}) or {}
        tool_tags = metadata.get("tags", set())
        # Convert list to set if needed
        if isinstance(tool_tags, list):
            tool_tags = set(tool_tags)
        logger.info(f"Tool tags for {tool_def}: {tool_tags}")
        return tag in tool_tags

    filtered_tools = FilteredToolset(base_toolset, tool_filter)
    logger.info(f"Filtered tools for {tag}: {filtered_tools.get_tools(None)}")
    agent_toolsets.append(filtered_tools)
    logger.info(f"Agent toolsets for {tag}: {agent_toolsets}")

    # 3. Create Agent
    logger.info(f"Creating agent: GitLab_{tag.capitalize()}_Agent")
    return Agent(
        model=model,
        system_prompt=system_prompt,
        toolsets=agent_toolsets,
        name=f"GitLab_{tag.capitalize()}_Agent",
        deps_type=Any, # Allow passing context if needed
    )

async def create_gitlab_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    skills_directory: str = DEFAULT_SKILLS_DIRECTORY,
) -> Agent:
    
    # Load all GitLab MCP tools (connection)
    # We create one base toolset to reuse connection/discovery
    base_toolset = FastMCPToolset(Client[Any](transport=mcp_url))
    logger.info(f"Connected to MCP at {mcp_url}")

    # Create the Model
    model = create_model(provider, model_id, base_url, api_key)

    # --- Create Explicit Sub-Agents ---
    
    # 1. Branches
    branch_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="branches",
        system_prompt="You are the GitLab Branch Specialist. manage branches, list them, search them. "
        "Use your skills and tools to handle all branch-related requests.",
        skills_directory=skills_directory, 
    )

    # 2. Commits
    commit_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="commits",
        system_prompt="You are the GitLab Commit Specialist. View details, diffs, blame, and commit history. "
        "Analyze code changes and commit messages.",
        skills_directory=skills_directory, 
    )

    # 3. Deploy Tokens
    deploy_tokens_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="deploy_tokens",
        system_prompt="You are the GitLab Deploy Token Specialist. Manage project and group deploy tokens.",
        skills_directory=skills_directory, 
    )

    # 4. Environments
    environments_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="environments",
        system_prompt="You are the GitLab Environment Specialist. Manage environments, stop them, delete them.",
        skills_directory=skills_directory, 
    )

    # 5. Groups
    groups_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="groups",
        system_prompt="You are the GitLab Group Specialist. Manage groups, subgroups, and group settings.",
        skills_directory=skills_directory, 
    )

    # 6. Jobs
    jobs_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="jobs",
        system_prompt="You are the GitLab Job Specialist. Inspect pipeline jobs, trace logs, and artifacts.",
        skills_directory=skills_directory, 
    )

    # 7. Members
    members_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="members",
        system_prompt="You are the GitLab Member Specialist. Manage project and group membership and permissions.",
        skills_directory=skills_directory, 
    )

    # 8. Merge Requests
    mr_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="merge_requests",
        system_prompt="You are the GitLab Merge Request Specialist. Create, update, list, and approve merge requests. "
        "Analyze MR diffs and comments.",
        skills_directory=skills_directory, 
    )

    # 9. Merge Rules
    merge_rules_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="merge_rules",
        system_prompt="You are the GitLab Merge Rules Specialist. configuration of merge request approval rules.",
        skills_directory=skills_directory, 
    )
    # 10. Packages
    packages_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="packages",
        system_prompt="You are the GitLab Package Specialist. Manage project and group packages.",
        skills_directory=skills_directory, 
    )

    # 11. Pipeline Schedules
    schedules_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="pipeline_schedules",
        system_prompt="You are the GitLab Pipeline Schedule Specialist. Manage scheduled pipelines.",
        skills_directory=skills_directory, 
    )

    # 12. Pipelines
    pipelines_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="pipelines",
        system_prompt="You are the GitLab Pipeline Specialist. Create, list, retry, and cancel pipelines. "
        "Debug pipeline failures.",
        skills_directory=skills_directory, 
    )

    # 13. Projects
    projects_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="projects",
        system_prompt="You are the GitLab Project Specialist. create, edit, and manage project settings and visibility.",
        skills_directory=skills_directory, 
    )

    # 14. Protected Branches
    protected_branches_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="protected_branches",
        system_prompt="You are the GitLab Protected Branch Specialist. Manage branch protection rules.",
        skills_directory=skills_directory, 
    )

    # 15. Releases
    releases_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="releases",
        system_prompt="You are the GitLab Release Specialist. Manage project releases and tags associated with them.",
        skills_directory=skills_directory, 
    )

    # 16. Runners
    runners_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="runners",
        system_prompt="You are the GitLab Runner Specialist. Manage and monitor CI/CD runners.",
        skills_directory=skills_directory, 
    )

    # 17. Tags
    tags_agent = await create_sub_agent(
        model=model, 
        base_toolset=base_toolset, 
        tag="tags",
        system_prompt="You are the GitLab Tag Specialist. Manage repository tags.",
        skills_directory=skills_directory, 
    )


    # Create delegation tools wrapper
    def create_delegation_tool(sub_agent: Agent, tag: str) -> Tool:
        async def delegate(ctx: RunContext, query: str) -> str:
            logger.info(f"Master Delegating to {sub_agent.name}: {query}")
            # We assume sub-agents don't need special deps for now, or match Master's deps
            # If sub-agents need deps, pass them here. 
            result = await sub_agent.run(query)
            return result.output
            
        delegate.__name__ = f"delegate_to_{tag}"
        delegate.__doc__ = f"Delegate to the {sub_agent.name}. Use this for tasks related to {tag}."
        return Tool(delegate)

    # --- Master Orchestrator ---

    logger.info("Initializing Master Orchestrator Agent")

    return Agent(
        model=model,
        system_prompt=(
            "You are the GitLab Master Orchestrator Agent.\n"
            "You do NOT execute GitLab API calls directly. Instead, you delegate tasks to your specialized sub-agents.\n"
            "Your responsibilities:\n"
            "1. Analyze the user's request.\n"
            "2. Identify the domain (e.g., branches, commits, MRs) and select the appropriate specialist agent.\n"
            "3. Delegating is your primary action. Do not try to answer questions that require tools yourself.\n"
            "4. If a complicated task requires multiple specialists (e.g. 'check out branch X and verify the last commit'), "
            "   orchestrate them sequentially: call the Branch Agent, then the Commit Agent.\n"
            "5. Always be warm, professional, and helpful.\n"
            "6. Explain your plan in detail before executing."
        ),
        name="GitLab_Master_Agent",
        # Pass all specialized agents as tools
        tools=[
            create_delegation_tool(branch_agent, "branches"),
            create_delegation_tool(commit_agent, "commits"),
            create_delegation_tool(deploy_tokens_agent, "deploy_tokens"),
            create_delegation_tool(environments_agent, "environments"),
            create_delegation_tool(groups_agent, "groups"),
            create_delegation_tool(jobs_agent, "jobs"),
            create_delegation_tool(members_agent, "members"),
            create_delegation_tool(mr_agent, "merge_requests"),
            create_delegation_tool(merge_rules_agent, "merge_rules"),
            create_delegation_tool(packages_agent, "packages"),
            create_delegation_tool(schedules_agent, "pipeline_schedules"),
            create_delegation_tool(pipelines_agent, "pipelines"),
            create_delegation_tool(projects_agent, "projects"),
            create_delegation_tool(protected_branches_agent, "protected_branches"),
            create_delegation_tool(releases_agent, "releases"),
            create_delegation_tool(runners_agent, "runners"),
            create_delegation_tool(tags_agent, "tags"),
        ],
        # Master agent also gets the general skills (documentation, etc.) if needed. 
        # For now, we only give it the sub-agents to force delegation.
        deps_type=Any,
    )

def agent_server():
    parser = argparse.ArgumentParser(description=f"Run the {AGENT_NAME} A2A Server")
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port to bind the server to"
    )
    parser.add_argument("--debug", type=bool, default=DEFAULT_DEBUG, help="Debug mode")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        choices=["openai", "anthropic", "google", "huggingface"],
        help="LLM Provider",
    )
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="LLM Model ID")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_OPENAI_BASE_URL,
        help="LLM Base URL (for OpenAI compatible providers)",
    )
    parser.add_argument("--api-key", default=DEFAULT_OPENAI_API_KEY, help="LLM API Key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP Server URL")
    args = parser.parse_args()

    # Configure Logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.INFO)  # Quiet down httpx
    logging.getLogger("neo4j").setLevel(logging.INFO)

    print(
        f"Starting {AGENT_NAME} with provider={args.provider}, model={args.model_id}, mcp={args.mcp_url}"
    )

    # Create the agent with CLI args
    cli_agent = asyncio.run(
        create_gitlab_agent(
            provider=args.provider,
            model_id=args.model_id,
            base_url=args.base_url,
            api_key=args.api_key,
            mcp_url=args.mcp_url,
        )
    )

    if args.debug:
        import logfire

        logfire.configure()  # Auto-detects token; or pass write_token="YOUR_TOKEN"
        logfire.instrument_pydantic_ai()  # Enables tracing for all Pydantic AI operations
        logfire.instrument_httpx(capture_all=True)

    # Define Skills for Agent Card (High-level capabilities)
    skills = []
    for mcp_tag in TAGS:
        skills.append(
            Skill(
                id=f"gitlab_{mcp_tag}",
                name=f"GitLab {mcp_tag.replace('_', ' ').title()}",
                description=f"Manage and query GitLab {mcp_tag.replace('_', ' ')}.",
                tags=[mcp_tag, "gitlab"],
                input_modes=["text"],
                output_modes=["text"],
            )
        )
    # Create A2A App
    cli_app = cli_agent.to_a2a(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        version="25.13.8",
        skills=skills,
        debug=args.debug,
    )
    logger.info(
        "Starting A2A server with provider=%s, model=%s, mcp_url=%s",
        args.provider,
        args.model_id,
        args.mcp_url,
    )
    uvicorn.run(
        cli_app,
        host=args.host,
        port=args.port,
        log_level="debug" if args.debug else "info",
    )


if __name__ == "__main__":
    agent_server()
