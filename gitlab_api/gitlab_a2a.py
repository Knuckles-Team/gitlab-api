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


async def build_tools_by_tag_dict(
    base_toolset: FastMCPToolset, model: Any
) -> dict[str, list[Tool]]:
    """
    Returns a dictionary: {tag: [Tool, Tool, ...]}
    Works with FastMCPToolset and other compatible toolsets
    """
    # We need a dummy context — doesn't have to be real
    dummy_ctx = RunContext[None](usage=None, deps=None, model=model)

    # Get all available tools (this is async!)
    all_tools = await base_toolset.get_tools(dummy_ctx)

    tools_by_tag: dict[str, list[Tool]] = {}

    for tool in all_tools.values():  # .values() → list[Tool]
        # Where FastMCP usually puts the tags (can be slightly different depending on version)
        meta = tool.tool_def.metadata.get("meta", {})
        fastmcp_meta = meta.get("_fastmcp", {})
        tags = fastmcp_meta.get("tags", set())

        for tag in tags:
            if tag not in tools_by_tag:
                tools_by_tag[tag] = []
            tools_by_tag[tag].append(tool)

    return tools_by_tag


async def create_gitlab_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    skills_directory: str = DEFAULT_SKILLS_DIRECTORY,
) -> Agent:

    skills_toolset = SkillsToolset(directories=[skills_directory])

    # Base model configuration to reuse
    model = create_model(provider, model_id, base_url, api_key)

    base_toolset = FastMCPToolset(Client[Any](transport=mcp_url))

    tools_by_tag = await build_tools_by_tag_dict(base_toolset, model)

    # Create Sub-Agents and Delegation Tools
    delegation_tools = []
    sub_agents = {}

    for tag in TAGS:
        if tag not in tools_by_tag or not tools_by_tag[tag]:
            continue

        tag_tools = tools_by_tag[tag]

        # Create filtered toolset for this tag (cleaner than passing list directly)
        tag_toolset = base_toolset.filtered(
            lambda ctx, defn: any(t.tool_def.name == defn.name for t in tag_tools)
        )

        sub_agent = Agent(
            model=model,
            system_prompt=f"You are GitLab **{tag}** specialist...",
            toolsets=[skills_toolset, tag_toolset],
            name=f"GitLab_{tag.title()}Agent",
        )

        sub_agents[tag] = sub_agent

        # Create delegation tool (closure-safe)
        async def make_delegate(_tag: str):
            async def delegate(ctx: RunContext, query: str) -> str:
                agent = sub_agents.get(_tag)
                if not agent:
                    return f"No specialist for domain: {_tag}"
                result = await agent.run(query, usage=ctx.usage)
                return result.output

            delegate.__name__ = f"delegate_to_{_tag}"
            delegate.__doc__ = f"Delegate task to the GitLab {tag} specialist"
            return delegate

        delegation_tools.append(await make_delegate(tag))

    return Agent(
        model=model,
        system_prompt=(
            "You are the GitLab Master Orchestrator Agent.\n"
            "You do NOT execute GitLab API calls directly. Instead, you delegate tasks to specialized sub-agents.\n"
            "Your responsibilities:\n"
            "1. Analyze the user's request.\n"
            "2. Identify which domain (tag) the request belongs to (e.g., branches, merge_requests, pipelines).\n"
            "3. Use the appropriate 'delegate_to_{tag}' tool to pass the request to the specialist.\n"
            "4. Combine results if necessary, or pass the specialist's response back to the user.\n"
            "5. If you need to look up documentation or patterns, use your skills toolset.\n\n"
            "Available Domains:\n"
            + "\n".join([f"- {tag}" for tag in TAGS if tools_by_tag.get(tag)])
            + "\n\n"
            "Always be warm and friendly. If a request spans multiple domains, break it down and delegate sequentially."
        ),
        name="GitLab_Master_Agent",
        toolsets=[skills_toolset],  # Master also has skills
        tools=delegation_tools,  # Tools to delegate
    )


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
