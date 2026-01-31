#!/usr/bin/python
# coding: utf-8
import json
import os
import argparse
import logging
import uvicorn
from typing import Optional, Any, List
from contextlib import asynccontextmanager

from pydantic_ai import Agent, ModelSettings, RunContext
from pydantic_ai.mcp import load_mcp_servers, MCPServerStreamableHTTP, MCPServerSSE
from pydantic_ai_skills import SkillsToolset
from fasta2a import Skill
from gitlab_api.utils import (
    to_integer,
    to_boolean,
    get_mcp_config_path,
    get_skills_path,
    load_skills_from_directory,
    create_model,
    tool_in_tag,
)

from fastapi import FastAPI, Request
from starlette.responses import Response, StreamingResponse
from pydantic import ValidationError
from pydantic_ai.ui import SSE_CONTENT_TYPE
from pydantic_ai.ui.ag_ui import AGUIAdapter

__version__ = "25.14.16"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Output to console
)
logging.getLogger("pydantic_ai").setLevel(logging.INFO)
logging.getLogger("fastmcp").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(string=os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-4b-2507")
DEFAULT_OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL", "http://host.docker.internal:1234/v1"
)
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", None)
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())
DEFAULT_SKILLS_DIRECTORY = os.getenv("SKILLS_DIRECTORY", get_skills_path())
DEFAULT_ENABLE_WEB_UI = to_boolean(os.getenv("ENABLE_WEB_UI", "False"))

AGENT_NAME = "GitLab"
AGENT_DESCRIPTION = (
    "A multi-agent system for managing GitLab resources via delegated specialists."
)

# -------------------------------------------------------------------------
# 1. System Prompts
# -------------------------------------------------------------------------

SUPERVISOR_SYSTEM_PROMPT = os.environ.get(
    "SUPERVISOR_SYSTEM_PROMPT",
    default=(
        "You are the GitLab Supervisor Agent.\n"
        "Your goal is to assist the user by assigning tasks to specialized child agents through your available toolset.\n"
        "Analyze the user's request and determine which domain(s) it falls into (e.g., branches, commits, merge_requests, issues, etc.).\n"
        "Then, call the appropriate tool(s) to delegate the task.\n"
        "Synthesize the results from the child agents into a final helpful response.\n"
        "Always be warm, professional, and helpful."
        "Note: The final response should contain all the relevant information from the tool executions. Never leave out any relevant information or leave it to the user to find it. "
        "You are the final authority on the user's request and the final communicator to the user. Present information as logically and concisely as possible. "
        "Explore using organized output with headers, sections, lists, and tables to make the information easy to navigate. "
        "If there are gaps in the information, clearly state that information is missing. Do not make assumptions or invent placeholder information, only use the information which is available. "
        "Plainly say that you do not have that information. If you were given an error output, try to capture as many relevant details as possible from the error output and include it in your response as a bug formatted pull request."
    ),
)

BRANCHES_AGENT_PROMPT = os.environ.get(
    "BRANCHES_AGENT_PROMPT",
    default=(
        "You are the GitLab Branches Agent.\n"
        "Your goal is to manage branches.\n"
        "You can:\n"
        "- CRUD: `create_branch`, `delete_branch`\n"
        "- List: `get_branches`\n"
        "Always specify the project ID."
    ),
)

COMMITS_AGENT_PROMPT = os.environ.get(
    "COMMITS_AGENT_PROMPT",
    default=(
        "You are the GitLab Commits Agent.\n"
        "Your goal is to manage commits.\n"
        "You can:\n"
        "- CRUD: `create_commit`, `revert_commit`\n"
        "- Read: `get_commits`, `get_commit_diff`, `get_commit_gpg_signature`\n"
        "- Comments: `get_commit_comments`, `create_commit_comment`, `get_commit_discussions`\n"
        "- Status: `get_commit_statuses`, `post_build_status_to_commit`\n"
        "- MRs: `get_commit_merge_requests`"
    ),
)

CUSTOM_API_AGENT_PROMPT = os.environ.get(
    "CUSTOM_API_AGENT_PROMPT",
    default=(
        "You are the GitLab Custom API Agent.\n"
        "Your goal is to handle arbitrary API requests.\n"
        "Use `api_request` for endpoints not covered by other agents."
    ),
)

DEPLOY_TOKENS_AGENT_PROMPT = os.environ.get(
    "DEPLOY_TOKENS_AGENT_PROMPT",
    default=(
        "You are the GitLab Deploy Tokens Agent.\n"
        "Your goal is to manage deploy tokens.\n"
        "You can:\n"
        "- CRUD: `create_deploy_token`, `delete_deploy_token`\n"
        "- List: `list_deploy_tokens`"
    ),
)

ENVIRONMENTS_AGENT_PROMPT = os.environ.get(
    "ENVIRONMENTS_AGENT_PROMPT",
    default=(
        "You are the GitLab Environments Agent.\n"
        "Your goal is to manage environments.\n"
        "You can:\n"
        "- CRUD: `create_environment`, `get_environment`, `update_environment`, `delete_environment`\n"
        "- List: `list_environments`"
    ),
)

GROUPS_AGENT_PROMPT = os.environ.get(
    "GROUPS_AGENT_PROMPT",
    default=(
        "You are the GitLab Groups Agent.\n"
        "Your goal is to manage groups.\n"
        "You can:\n"
        "- CRUD: `create_group`, `get_group`, `update_group`, `delete_group`\n"
        "- List: `list_groups`"
    ),
)

JOBS_AGENT_PROMPT = os.environ.get(
    "JOBS_AGENT_PROMPT",
    default=(
        "You are the GitLab Jobs Agent.\n"
        "Your goal is to manage CI/CD jobs.\n"
        "You can:\n"
        "- Actions: `cancel_job`, `retry_job`, `play_job`\n"
        "- Read: `list_jobs`, `get_job`"
    ),
)

MEMBERS_AGENT_PROMPT = os.environ.get(
    "MEMBERS_AGENT_PROMPT",
    default=(
        "You are the GitLab Members Agent.\n"
        "Your goal is to manage members.\n"
        "You can:\n"
        "- CRUD: `add_member`, `edit_member`, `remove_member`\n"
        "- List: `list_members`\n"
        "Works for both projects and groups."
    ),
)

MERGE_REQUESTS_AGENT_PROMPT = os.environ.get(
    "MERGE_REQUESTS_AGENT_PROMPT",
    default=(
        "You are the GitLab Merge Requests Agent.\n"
        "Your goal is to manage merge requests (MRs).\n"
        "You can:\n"
        "- CRUD: `create_merge_request`, `get_merge_request`, `update_merge_request`, `delete_merge_request`\n"
        "- List: `list_merge_requests`\n"
        "Use this to review and merge code."
    ),
)

MERGE_RULES_AGENT_PROMPT = os.environ.get(
    "MERGE_RULES_AGENT_PROMPT",
    default=(
        "You are the GitLab Merge Rules Agent.\n"
        "Your goal is to manage MR approval rules.\n"
        "You can:\n"
        "- CRUD: `create_merge_request_approval_rule`, `update_merge_request_approval_rule`, `delete_merge_request_approval_rule`\n"
        "- Read: `get_merge_request_approval_rules`"
    ),
)

PACKAGES_AGENT_PROMPT = os.environ.get(
    "PACKAGES_AGENT_PROMPT",
    default=(
        "You are the GitLab Packages Agent.\n"
        "Your goal is to manage the package registry.\n"
        "You can:\n"
        "- Read: `list_packages`, `get_package`\n"
        "- Delete: `delete_package`"
    ),
)

PIPELINE_SCHEDULES_AGENT_PROMPT = os.environ.get(
    "PIPELINE_SCHEDULES_AGENT_PROMPT",
    default=(
        "You are the GitLab Pipeline Schedules Agent.\n"
        "Your goal is to manage scheduled pipelines.\n"
        "You can:\n"
        "- CRUD: `create_pipeline_schedule`, `update_pipeline_schedule`, `delete_pipeline_schedule`\n"
        "- List: `list_pipeline_schedules`"
    ),
)

PIPELINES_AGENT_PROMPT = os.environ.get(
    "PIPELINES_AGENT_PROMPT",
    default=(
        "You are the GitLab Pipelines Agent.\n"
        "Your goal is to manage CI/CD pipelines.\n"
        "You can:\n"
        "- Create: `create_pipeline`\n"
        "- Read: `list_pipelines`, `get_pipeline`\n"
        "- Delete: `delete_pipeline`"
    ),
)

PROJECTS_AGENT_PROMPT = os.environ.get(
    "PROJECTS_AGENT_PROMPT",
    default=(
        "You are the GitLab Projects Agent.\n"
        "Your goal is to manage projects.\n"
        "You can:\n"
        "- CRUD: `create_project`, `get_project`, `update_project`, `delete_project`\n"
        "- List: `list_projects`"
    ),
)

PROTECTED_BRANCHES_AGENT_PROMPT = os.environ.get(
    "PROTECTED_BRANCHES_AGENT_PROMPT",
    default=(
        "You are the GitLab Protected Branches Agent.\n"
        "Your goal is to manage branch protection.\n"
        "You can:\n"
        "- Protect: `protect_branch`\n"
        "- Unprotect: `unprotect_branch`\n"
        "- List: `list_protected_branches`"
    ),
)

RELEASES_AGENT_PROMPT = os.environ.get(
    "RELEASES_AGENT_PROMPT",
    default=(
        "You are the GitLab Releases Agent.\n"
        "Your goal is to manage releases.\n"
        "You can:\n"
        "- CRUD: `create_release`, `get_release`, `update_release`, `delete_release`\n"
        "- List: `list_releases`"
    ),
)

RUNNERS_AGENT_PROMPT = os.environ.get(
    "RUNNERS_AGENT_PROMPT",
    default=(
        "You are the GitLab Runners Agent.\n"
        "Your goal is to manage CI runners.\n"
        "You can:\n"
        "- Manage: `update_runner_details`, `pause_runner`, `delete_runner`\n"
        "- Register/Reset: `register_new_runner`, `reset_token`\n"
        "- List: `get_runners`"
    ),
)

TAGS_AGENT_PROMPT = os.environ.get(
    "TAGS_AGENT_PROMPT",
    default=(
        "You are the GitLab Tags Agent.\n"
        "Your goal is to manage tags.\n"
        "You can:\n"
        "- CRUD: `create_tag`, `delete_tag`\n"
        "- List: `get_tags`\n"
        "- Protection: `protect_tag`, `unprotect_tag`"
    ),
)

# -------------------------------------------------------------------------
# 2. Agent Creation Logic
# -------------------------------------------------------------------------


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
) -> Agent:
    """
    Creates the Supervisor Agent with sub-agents registered as tools.
    """
    logger.info("Initializing Multi-Agent System for GitLab...")

    model = create_model(provider, model_id, base_url, api_key)
    settings = ModelSettings(timeout=3600.0)

    # Load master toolsets
    master_toolsets = []
    if mcp_config:
        mcp_toolset = load_mcp_servers(mcp_config)
        master_toolsets.extend(mcp_toolset)
        logger.info(f"Connected to MCP Config JSON: {mcp_toolset}")
    elif mcp_url:
        if "sse" in mcp_url.lower():
            server = MCPServerSSE(mcp_url)
        else:
            server = MCPServerStreamableHTTP(mcp_url)
        master_toolsets.append(server)
        logger.info(f"Connected to MCP Server: {mcp_url}")

    if skills_directory and os.path.exists(skills_directory):
        master_toolsets.append(SkillsToolset(directories=[str(skills_directory)]))

    # Define Tag -> Prompt map
    agent_defs = {
        "branches": (BRANCHES_AGENT_PROMPT, "GitLab_Branches_Agent"),
        "commits": (COMMITS_AGENT_PROMPT, "GitLab_Commits_Agent"),
        "custom_api": (CUSTOM_API_AGENT_PROMPT, "GitLab_Custom_Api_Agent"),
        "deploy_tokens": (DEPLOY_TOKENS_AGENT_PROMPT, "GitLab_Deploy_Tokens_Agent"),
        "environments": (ENVIRONMENTS_AGENT_PROMPT, "GitLab_Environments_Agent"),
        "groups": (GROUPS_AGENT_PROMPT, "GitLab_Groups_Agent"),
        "jobs": (JOBS_AGENT_PROMPT, "GitLab_Jobs_Agent"),
        "members": (MEMBERS_AGENT_PROMPT, "GitLab_Members_Agent"),
        "merge_requests": (MERGE_REQUESTS_AGENT_PROMPT, "GitLab_Merge_Requests_Agent"),
        "merge_rules": (MERGE_RULES_AGENT_PROMPT, "GitLab_Merge_Rules_Agent"),
        "packages": (PACKAGES_AGENT_PROMPT, "GitLab_Packages_Agent"),
        "pipeline_schedules": (
            PIPELINE_SCHEDULES_AGENT_PROMPT,
            "GitLab_Pipeline_Schedules_Agent",
        ),
        "pipelines": (PIPELINES_AGENT_PROMPT, "GitLab_Pipelines_Agent"),
        "projects": (PROJECTS_AGENT_PROMPT, "GitLab_Projects_Agent"),
        "protected_branches": (
            PROTECTED_BRANCHES_AGENT_PROMPT,
            "GitLab_Protected_Branches_Agent",
        ),
        "releases": (RELEASES_AGENT_PROMPT, "GitLab_Releases_Agent"),
        "runners": (RUNNERS_AGENT_PROMPT, "GitLab_Runners_Agent"),
        "tags": (TAGS_AGENT_PROMPT, "GitLab_Tags_Agent"),
    }

    child_agents = {}

    for tag, (system_prompt, agent_name) in agent_defs.items():
        tag_toolsets = []
        for ts in master_toolsets:

            def filter_func(ctx, tool_def, t=tag):
                return tool_in_tag(tool_def, t)

            if hasattr(ts, "filtered"):
                filtered_ts = ts.filtered(filter_func)
                tag_toolsets.append(filtered_ts)
            else:
                pass

        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            name=agent_name,
            toolsets=tag_toolsets,
            tool_timeout=32400.0,
            model_settings=settings,
        )
        child_agents[tag] = agent

    # Create Supervisor
    supervisor = Agent(
        model=model,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        model_settings=settings,
        name=AGENT_NAME,
        deps_type=Any,
    )

    # Define delegation tools

    @supervisor.tool
    async def assign_task_to_branches_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to branches to the Branches Agent."""
        return (
            await child_agents["branches"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_commits_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to commits to the Commits Agent."""
        return (
            await child_agents["commits"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_custom_api_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to custom_api to the Custom Api Agent."""
        return (
            await child_agents["custom_api"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_deploy_tokens_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to deploy_tokens to the Deploy Tokens Agent."""
        return (
            await child_agents["deploy_tokens"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_environments_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to environments to the Environments Agent."""
        return (
            await child_agents["environments"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_groups_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to groups to the Groups Agent."""
        return (
            await child_agents["groups"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_jobs_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to jobs to the Jobs Agent."""
        return (
            await child_agents["jobs"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_members_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to members to the Members Agent."""
        return (
            await child_agents["members"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_merge_requests_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to merge_requests to the Merge Requests Agent."""
        return (
            await child_agents["merge_requests"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_merge_rules_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to merge_rules to the Merge Rules Agent."""
        return (
            await child_agents["merge_rules"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_packages_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to packages to the Packages Agent."""
        return (
            await child_agents["packages"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_pipeline_schedules_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to pipeline_schedules to the Pipeline Schedules Agent."""
        return (
            await child_agents["pipeline_schedules"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_pipelines_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to pipelines to the Pipelines Agent."""
        return (
            await child_agents["pipelines"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_projects_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to projects to the Projects Agent."""
        return (
            await child_agents["projects"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_protected_branches_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to protected_branches to the Protected Branches Agent."""
        return (
            await child_agents["protected_branches"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_releases_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to releases to the Releases Agent."""
        return (
            await child_agents["releases"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_runners_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to runners to the Runners Agent."""
        return (
            await child_agents["runners"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_tags_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to tags (git tags) to the Tags Agent."""
        return (
            await child_agents["tags"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    return supervisor


async def chat(agent: Agent, prompt: str):
    result = await agent.run(prompt)
    print(f"Response:\n\n{result.output}")


async def node_chat(agent: Agent, prompt: str) -> List:
    nodes = []
    async with agent.iter(prompt) as agent_run:
        async for node in agent_run:
            nodes.append(node)
            print(node)
    return nodes


async def stream_chat(agent: Agent, prompt: str) -> None:
    async with agent.run_stream(prompt) as result:
        async for text_chunk in result.stream_text(delta=True):
            print(text_chunk, end="", flush=True)
        print("\nDone!")


def create_agent_server(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
    debug: Optional[bool] = DEFAULT_DEBUG,
    host: Optional[str] = DEFAULT_HOST,
    port: Optional[int] = DEFAULT_PORT,
    enable_web_ui: bool = DEFAULT_ENABLE_WEB_UI,
):
    print(
        f"Starting {AGENT_NAME} with provider={provider}, model={model_id}, mcp={mcp_url} | {mcp_config}"
    )
    agent = create_agent(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        mcp_url=mcp_url,
        mcp_config=mcp_config,
        skills_directory=skills_directory,
    )

    if skills_directory and os.path.exists(skills_directory):
        skills = load_skills_from_directory(skills_directory)
        logger.info(f"Loaded {len(skills)} skills from {skills_directory}")
    else:
        skills = [
            Skill(
                id="gitlab_agent",
                name="GitLab Agent",
                description="This GitLab skill grants access to all GitLab tools provided by the GitLab MCP Server",
                tags=["gitlab"],
                input_modes=["text"],
                output_modes=["text"],
            )
        ]

    a2a_app = agent.to_a2a(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        version=__version__,
        skills=skills,
        debug=debug,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if hasattr(a2a_app, "router"):
            async with a2a_app.router.lifespan_context(a2a_app):
                yield
        else:
            yield

    app = FastAPI(
        title=f"{AGENT_NAME} - A2A + AG-UI Server",
        description=AGENT_DESCRIPTION,
        debug=debug,
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health_check():
        return {"status": "OK"}

    app.mount("/a2a", a2a_app)

    @app.post("/ag-ui")
    async def ag_ui_endpoint(request: Request) -> Response:
        accept = request.headers.get("accept", SSE_CONTENT_TYPE)
        try:
            run_input = AGUIAdapter.build_run_input(await request.body())
        except ValidationError as e:
            return Response(
                content=json.dumps(e.json()),
                media_type="application/json",
                status_code=422,
            )

        adapter = AGUIAdapter(agent=agent, run_input=run_input, accept=accept)
        event_stream = adapter.run_stream()
        sse_stream = adapter.encode_stream(event_stream)

        return StreamingResponse(
            sse_stream,
            media_type=accept,
        )

    if enable_web_ui:
        web_ui = agent.to_web(instructions=SUPERVISOR_SYSTEM_PROMPT)
        app.mount("/", web_ui)
        logger.info(
            "Starting server on %s:%s (A2A at /a2a, AG-UI at /ag-ui, Web UI: %s)",
            host,
            port,
            "Enabled at /" if enable_web_ui else "Disabled",
        )

    uvicorn.run(
        app,
        host=host,
        port=port,
        timeout_keep_alive=1800,
        timeout_graceful_shutdown=60,
        log_level="debug" if debug else "info",
    )


def agent_server():
    print(f"gitlab_agent v{__version__}")
    parser = argparse.ArgumentParser(
        description=f"Run the {AGENT_NAME} A2A + AG-UI Server"
    )
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
    parser.add_argument(
        "--mcp-config", default=DEFAULT_MCP_CONFIG, help="MCP Server Config"
    )
    parser.add_argument(
        "--web",
        action="store_true",
        default=DEFAULT_ENABLE_WEB_UI,
        help="Enable Pydantic AI Web UI",
    )
    args = parser.parse_args()

    if args.debug:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
            force=True,
        )
        logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)
        logging.getLogger("fastmcp").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    create_agent_server(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
        mcp_config=args.mcp_config,
        debug=args.debug,
        host=args.host,
        port=args.port,
        enable_web_ui=args.web,
    )


if __name__ == "__main__":
    agent_server()
