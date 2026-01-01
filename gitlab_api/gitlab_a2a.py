#!/usr/bin/python
# coding: utf-8

import os
import argparse
import logging
import asyncio
import uvicorn
from typing import Optional, Dict, Any, List

from fastmcp import Client
from pydantic_ai import Agent, RunContext, FunctionToolset, ToolDefinition
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
    handlers=[logging.StreamHandler()]  # Output to console
)
logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)  # Enable pydantic-ai logs
logging.getLogger("fastmcp").setLevel(logging.DEBUG)  # Enable FastMCP logs
logging.getLogger("httpx").setLevel(logging.INFO)  # Quieter HTTP logs
logger = logging.getLogger(__name__)

skills_dir = files('gitlab_api') / 'skills'
with as_file(skills_dir) as path:
    skills_path = str(path)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(string=os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen3:4b")
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
    "custom_api",
]

AGENT_NAME = "GitLab"
AGENT_DESCRIPTION = (
    "An agent built with Agent Skills and GitLab MCP tools to maximize GitLab interactivity."
)


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

class DynamicGitLabMCPToolset(FunctionToolset):
    """Lightweight discovery layer for ALL GitLab MCP tools — no pre-filtering."""
    def __init__(self, client: Client[Any]):
        super().__init__()
        self.client = client
        self.add_function(self.list_gitlab_tools)
        self.add_function(self.get_gitlab_tool_schema)
        self.add_function(self.call_gitlab_tool)

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.__aexit__(exc_type, exc_value, traceback)

    @property
    def id(self) -> str:
        return "gitlab-dynamic-mcp"

    async def list_gitlab_tools(self, ctx: RunContext, tag_filter: str = None) -> List[Dict[str, Any]]:
        """List available GitLab tools. Optionally filter by tag (e.g. 'merge_requests')."""
        all_tools = await self.client.list_tools()
        result = []
        for tool in all_tools:
            tool_tags = tool.meta.get('_fastmcp', {}).get('tags', []) if tool.meta else []
            if not tag_filter or tag_filter in tool_tags:
                result.append({
                    "name": tool.name,
                    "description": tool.description[:180] + "..." if len(tool.description) > 180 else tool.description,
                    "tags": tool_tags
                })
        return result

    async def get_gitlab_tool_schema(self, ctx: RunContext, tool_name: str) -> Dict[str, Any]:
        """Get full parameter schema for any GitLab tool when you decide to use it."""
        tools = await self.client.list_tools()
        for tool in tools:
            if tool.name == tool_name:
                return tool.inputSchema
        raise ValueError(f"Tool '{tool_name}' not found.")

    async def call_gitlab_tool(self, ctx: RunContext, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute any GitLab MCP tool with the provided arguments."""
        return await self.client.call_tool(tool_name, arguments)


async def create_gitlab_agent(
        provider: str = DEFAULT_PROVIDER,
        model_id: str = DEFAULT_MODEL_ID,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        mcp_url: str = DEFAULT_MCP_URL,
        skills_directory: str = DEFAULT_SKILLS_DIRECTORY
) -> Agent:
    model = create_model(provider, model_id, base_url, api_key)

    client = Client[Any](transport=mcp_url)  # add auth if needed: auth=...

    dynamic_mcp_toolset = DynamicGitLabMCPToolset(client=client)

    # Progressive instructions via skills (one folder per tag)
    skills_toolset = SkillsToolset(directories=[skills_directory])

    system_prompt = (
        "You are a comprehensive GitLab expert agent.\n"
        "You have domain expertise available via skills:\n"
        "  - Use skills toolset to discover and load instructions for specific areas (merge_requests, pipelines, projects, branches, etc.)\n"
        "You have access to ALL GitLab API capabilities via dynamic tool discovery:\n"
        "  1. Call 'list_gitlab_tools' (with optional tag_filter) to discover available tools\n"
        "  2. Call 'get_gitlab_tool_schema' to learn parameters of any tool\n"
        "  3. Call 'call_gitlab_tool' to execute it\n\n"
        "Always start by loading domain knowledge through your skills, and then discovering relevant tools via tag.\n"
        "Make a list of all the tools and skills you will require to use. \n"
        "Next plan your entire workflow end to end first and explain your steps in the workflow as well as each tool usage.\n"
        "Always be warm and friendly with the user while striving for truth and accuracy.\n"
        "It is a fact that the user and you will sometimes be incorrect, but we strive for the truth together.\n"
        "Handle issues gracefully."
    )

    return Agent(
        model=model,
        system_prompt=system_prompt,
        name="GitLab_Master_Agent",
        toolsets=[dynamic_mcp_toolset, skills_toolset],
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
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host to bind the server to")
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port to bind the server to"
    )
    parser.add_argument(
        "--debug", type=bool, default=DEFAULT_DEBUG, help="Debug mode"
    )
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
    logging.getLogger("httpx").setLevel(logging.INFO) # Quiet down httpx
    logging.getLogger("neo4j").setLevel(logging.INFO)

    print(
        f"Starting {AGENT_NAME} with provider={args.provider}, model={args.model_id}, mcp={args.mcp_url}"
    )

    # Create the agent with CLI args
    cli_agent = asyncio.run(create_gitlab_agent(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
    ))

    if args.debug:
        import logfire
        logfire.configure()  # Auto-detects token; or pass write_token="YOUR_TOKEN"
        logfire.instrument_pydantic_ai()  # Enables tracing for all Pydantic AI operations
        logfire.instrument_httpx(capture_all=True)
    # Create A2A App
    cli_app = cli_agent.to_a2a(
        name=AGENT_NAME, description=AGENT_DESCRIPTION, version="25.13.8", skills=skills, debug=args.debug
    )
    logger.info("Starting A2A server with provider=%s, model=%s, mcp_url=%s", args.provider, args.model_id, args.mcp_url)
    uvicorn.run(
        cli_app,
        host=args.host,
        port=args.port,
        log_level="debug" if args.debug else "info",
    )


if __name__ == "__main__":
    agent_server()
