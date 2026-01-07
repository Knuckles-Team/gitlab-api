#!/usr/bin/python
# coding: utf-8
import json
import os
import argparse
import logging
import asyncio
import uvicorn
from typing import Optional, Any, List
import traceback
from starlette.responses import JSONResponse

from fastmcp import Client
from pydantic_ai import Agent
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
from pydantic_ai_skills import SkillsToolset
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.huggingface import HuggingFaceModel
# from pydantic_ai.builtin_tools import CodeExecutionTool
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
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-8b")
DEFAULT_OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1")
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


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    #skills_directory: str = DEFAULT_SKILLS_DIRECTORY,
) -> Agent:
    # tools = [CodeExecutionTool()] 
    agent_toolsets = []

    base_toolset = FastMCPToolset(
        Client[Any](mcp_url, timeout=3600)
    )
    agent_toolsets.append(base_toolset)
    logger.info(f"Connected to MCP at {mcp_url}")

    # logger.info(f"Loaded Skills at {skills_directory}")
    # if os.path.exists(skills_directory):
    #     logger.debug(f"Loading skills {skills_directory}")
    #     skills = SkillsToolset(directories=[str(skills_directory)])
    #     agent_toolsets.append(skills)

    # Create the Model
    model = create_model(provider, model_id, base_url, api_key)

    logger.info("Initializing Agent")

    return Agent(
        model=model,
        system_prompt=(
            "You are the GitLab Agent.\n"
            "You have access to all GitLab skills and toolsets to interact with the API.\n"
            "Your responsibilities:\n"
            "1. Analyze the user's request.\n"
            "2. Identify the domain (e.g., branches, commits, MRs) and select the appropriate skills.\n"
            "3. Use the skills to reference the tools you will need to search for using the tool_search skill.\n"
            "4. If a complicated task requires multiple skills (e.g. 'check out branch X and verify the last commit'), "
            "   orchestrate them sequentially: call the Branch skill, then the Commit skill.\n"
            "5. Always be warm, professional, and helpful.\n"
            "6. Explain your plan in detail before executing."
        ),
        name="GitLab_Agent",
        # tools=tools, # Removed invalid tool
        toolsets=agent_toolsets,
        deps_type=Any,
    )


async def chat(agent: Agent, prompt: str, skills):
    # Add skills system prompt (includes skill descriptions and usage)
    @agent.system_prompt
    async def add_skills_prompt() -> str:
        return skills.get_skills_system_prompt()

    result = await agent.run(prompt)
    print(f"Response:\n\n{result.output}")


async def node_chat(agent: Agent, prompt: str) -> List:
    nodes = []
    async with agent.iter(prompt) as agent_run:
        async for node in agent_run:
            nodes.append(node)
            print(node)
    return nodes


async def stream_chat(agent: Agent, query: str) -> None:
    # Option A: Easiest & most common - just stream the final text output
    async with agent.run_stream(query) as result:
        async for text_chunk in result.stream_text(
            delta=True
        ):  # ← streams partial text deltas
            print(text_chunk, end="", flush=True)
        print("\nDone!")  # optional


def create_a2a_server(
    provider, model_id, base_url, api_key, mcp_url, debug, host, port
):
    print(
        f"Starting {AGENT_NAME} with provider={provider}, model={model_id}, mcp={mcp_url}"
    )
    agent = create_agent(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        mcp_url=mcp_url,
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
    # Create A2A App
    app = agent.to_a2a(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        version="25.13.8",
        skills=skills,
        debug=debug,
    )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global Exception: {exc}\n{traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": str(exc), "traceback": traceback.format_exc()})

    logger.info(
        "Starting A2A server with provider=%s, model=%s, mcp_url=%s",
        provider,
        model_id,
        mcp_url,
    )

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="debug" if debug else "info",
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
    logging.getLogger("httpx").setLevel(logging.INFO)

    # Create the agent with CLI args
    create_a2a_server(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
        debug=args.debug,
        host=args.host,
        port=args.port,
    )


if __name__ == "__main__":
    agent_server()
