#!/usr/bin/python
# coding: utf-8

import os
import argparse
import logging
import asyncio
import requests
import uvicorn
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from fastmcp import Client
from graphiti_core.nodes import EpisodeType
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.huggingface import HuggingFaceModel
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
from fasta2a import Skill
os.getenv("GRAPHITI_TELEMETRY_ENABLED", "false")
from graphiti_core import Graphiti
from graphiti_core.driver.kuzu_driver import KuzuDriver
from graphiti_core.driver.neo4j_driver import Neo4jDriver
from graphiti_core.driver.falkordb_driver import FalkorDriver
from openai import AsyncOpenAI
from graphiti_core.llm_client.azure_openai_client import AzureOpenAILLMClient
from graphiti_core.embedder.azure_openai import AzureOpenAIEmbedderClient
from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient
from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.llm_client.openai_generic_client import OpenAIGenericClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from gitlab_api.utils import to_integer

logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Output to console
)
logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)  # Enable pydantic-ai logs
logging.getLogger("graphiti_core").setLevel(logging.DEBUG)  # Enable Graphiti logs
logging.getLogger("fastmcp").setLevel(logging.DEBUG)  # Enable FastMCP logs
logging.getLogger("httpx").setLevel(logging.INFO)  # Quieter HTTP logs
logger = logging.getLogger(__name__)

DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen3:4b")
DEFAULT_OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://ollama.arpa/v1")
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", "http://localhost:8000/mcp")
DEFAULT_GRAPHITI_BACKEND = os.getenv("GRAPHITI_BACKEND", "kuzu")
DEFAULT_GRAPHITI_DB_PATH = os.getenv("GRAPHITI_DB_PATH", "graphiti.db")
DEFAULT_GRAPHITI_MCP_URL = os.getenv("GRAPHITI_MCP_URL", "http://localhost:8001/mcp")
DEFAULT_GRAPHITI_URI = os.getenv("DEFAULT_GRAPHITI_URI", "bolt://localhost:7687")
DEFAULT_GRAPHITI_USER = os.getenv("DEFAULT_GRAPHITI_USER", "neo4j")
DEFAULT_GRAPHITI_PASS = os.getenv("DEFAULT_GRAPHITI_PASS", "password")
DEFAULT_GRAPHITI_HOST = os.getenv("DEFAULT_GRAPHITI_HOST", "localhost")
DEFAULT_GRAPHITI_PORT = to_integer(string=os.getenv("DEFAULT_GRAPHITI_PORT", "6379"))

# Initial doc URLs for ingestion
INITIAL_DOC_URLS = [
    "https://github.com/Knuckles-Team/gitlab-api/blob/main/README.md",
    "https://docs.gitlab.com/api/branches",
    "https://docs.gitlab.com/api/commits",
    "https://docs.gitlab.com/api/deploy_tokens",
    "https://docs.gitlab.com/api/groups",
    "https://docs.gitlab.com/api/jobs",
    "https://docs.gitlab.com/api/members",
    "https://docs.gitlab.com/api/merge_requests",
    "https://docs.gitlab.com/api/merge_request_approvals",
    "https://docs.gitlab.com/api/merge_request_approval_settings",
    "https://docs.gitlab.com/api/namespaces",
    "https://docs.gitlab.com/api/packages",
    "https://docs.gitlab.com/api/pipelines",
    "https://docs.gitlab.com/api/pipeline_schedules",
    "https://docs.gitlab.com/api/projects",
    "https://docs.gitlab.com/api/protected_branches",
    "https://docs.gitlab.com/api/releases",
    "https://docs.gitlab.com/api/runners",
    "https://docs.gitlab.com/api/users",
    "https://docs.gitlab.com/api/wikis",
    "https://docs.gitlab.com/api/environments",
    "https://docs.gitlab.com/api/protected_environments",
    "https://docs.gitlab.com/api/tags",
    "https://docs.gitlab.com/api/protected_tags",
    "https://docs.gitlab.com/api/api_resources",
    "https://docs.gitlab.com/api/graphql/",
    "https://docs.gitlab.com/api/graphql/reference/",
    "https://docs.gitlab.com/api/graphql/getting_started/",
]

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

AGENT_NAME = "GitLabOrchestrator"
AGENT_DESCRIPTION = (
    "A multi-agent system for managing GitLab tasks via delegated specialists."
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


async def initialize_graphiti_db(
    backend: str,
    db_path: str,
    uri: str,
    user: str,
    password: str,
    host: str,
    port: int,
    database: str,
    force_reinit: bool = False,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model_id: str = DEFAULT_MODEL_ID,
    provider: str = DEFAULT_PROVIDER,
    ) -> Graphiti:
    """
    Initializes and returns a GraphitiClient for any backend.
    Optionally seeds with initial docs if empty or forced.
    """
    # Configure LLM and Embedder (Assuming OpenAI/Ollama for now based on context)
    # Using OpenAIGenericClient as recommended for Ollama

    target_base_url = base_url or DEFAULT_OPENAI_BASE_URL
    target_api_key = api_key or DEFAULT_OPENAI_API_KEY

    cross_encoder = None  # Default to None if not set

    if provider == "google":
        llm_config = LLMConfig(
            api_key=target_api_key,
            model=model_id,
            small_model=model_id,
        )
        llm_client = GeminiClient(config=llm_config)
        embedder_config = GeminiEmbedderConfig(
            api_key=target_api_key,
            embedding_model="embedding-001",
        )
        embedder = GeminiEmbedder(config=embedder_config)
        cross_encoder = GeminiRerankerClient(
            config=LLMConfig(
                api_key=target_api_key,
                model="gemini-1.5-flash-latest",
            )
        )
    elif provider in ["openai", "azure"]:  # azure handled via base_url check
        is_ollama = "ollama" in target_api_key.lower() or "11434" in target_base_url
        is_azure = "azure" in target_base_url.lower()
        is_standard_openai = not is_ollama and not is_azure

        llm_config = LLMConfig(
            model=model_id,
            small_model=model_id,
            api_key=target_api_key,
            base_url=target_base_url if is_ollama else None,
        )

        async_openai_client = AsyncOpenAI(
            base_url=target_base_url,
            api_key=target_api_key,
        )

        if is_ollama:
            llm_client = OpenAIGenericClient(config=llm_config)
            embedder = OpenAIEmbedder(
                config=OpenAIEmbedderConfig(
                    api_key=target_api_key,
                    embedding_model="nomic-embed-text",
                    embedding_dim=768,
                    base_url=target_base_url,
                )
            )
        elif is_azure:
            llm_client = AzureOpenAILLMClient(
                azure_client=async_openai_client,
                config=llm_config
            )
            embedder = AzureOpenAIEmbedderClient(
                azure_client=async_openai_client,
                model="text-embedding-3-small"
            )
        else:  # standard openai
            llm_client = OpenAIClient(
                client=async_openai_client,
                config=llm_config
            )
            embedder = OpenAIEmbedder(
                config=OpenAIEmbedderConfig(
                    api_key="ollama",  # Placeholder API key
                    embedding_model="nomic-embed-text",
                    embedding_dim=768,
                    base_url="http://localhost:11434/v1",
                )
            )
            # embedder = OpenAIEmbedderClient(
            #     openai_client=async_openai_client,
            #     model="text-embedding-3-small"
            # )

        cross_encoder = OpenAIRerankerClient(client=llm_client, config=llm_config)

    else:
        raise ValueError(f"Unsupported provider for Graphiti: {provider}")

    if backend == "kuzu":
        driver = KuzuDriver(db=db_path)
        client = Graphiti(graph_driver=driver, llm_client=llm_client, embedder=embedder, cross_encoder=cross_encoder)
        db_exists = os.path.exists(db_path) and os.path.getsize(db_path) > 0
    elif backend == "neo4j":
        driver = Neo4jDriver(uri=uri, user=user, password=password, database=database)
        client = Graphiti(graph_driver=driver, llm_client=llm_client, embedder=embedder, cross_encoder=cross_encoder)
        db_exists = True # Assume remote exists
    elif backend == "falkordb":
        driver = FalkorDriver(
            host=host, port=port, username=user, password=password, database=database
        )
        client = Graphiti(graph_driver=driver, llm_client=llm_client, embedder=embedder, cross_encoder=cross_encoder)
        db_exists = True
    else:
        raise ValueError(f"Unsupported backend: {backend}")

    # Check if graph is empty (simple heuristic)
    try:
        results = await client.search("MATCH (n) RETURN count(n) AS count")
        node_count = results[0]["count"] if results else 0
        is_empty = node_count == 0
        logger.debug("Graphiti DB has %d nodes (empty=%s)", node_count, is_empty)
    except Exception as e:
        print(e)
        is_empty = True  # Assume empty on error

    should_init = force_reinit or (backend == "kuzu" and not db_exists) or is_empty

    if should_init:
        print(
            f"Initializing {backend.upper()} Graphiti DB with initial documentation..."
        )
        for url in INITIAL_DOC_URLS:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                content = response.text
                await client.add_episode(
                    name=url,
                    episode_body=content,
                    source=url,
                    source_description="Initial documentation ingestion",
                    reference_time=datetime.now(timezone.utc)
                )
                print(f"Ingested: {url}")
                logger.debug("Ingested doc: %s", url)
            except Exception as e:
                print(f"Failed to ingest {url}: {e}")
    else:
        print(f"Using existing {backend.upper()} Graphiti DB (skip init)")
    logger.debug("Initializing Graphiti with backend=%s, db_path=%s", backend, db_path)
    return client


def has_tag(tool_def, tag):
    annotations = tool_def.metadata.get('annotations', {})
    tags = annotations.get('tags', []) if isinstance(annotations, dict) else []
    return tag in tags


def create_child_agent(
    tag: str,
    mcp_url: str,
    provider: str,
    model_id: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    graphiti_backend: str = DEFAULT_GRAPHITI_BACKEND,
    graphiti_client: Optional[Graphiti] = None,  # Passed if Kuzu (embedded)
    graphiti_mcp_url: Optional[str] = None,  # For server backends
) -> Agent:
    """
    Creates a specialized child agent for a specific tag.
    """
    model = create_model(provider, model_id, base_url, api_key)

    # Create toolset and filter by tag
    toolset = FastMCPToolset(client=Client[Any](transport=mcp_url))

    # filtered returns a new toolset with only tools that match the predicate
    # The predicate receives (context, tool_definition)
    # We check if the 'tag' is present in tool_definition.tags
    filtered_toolset = toolset.filtered(
        lambda ctx, tool_def: has_tag(tool_def, tag)
    )

    system_prompt = (
        f"You are a specialized GitLab agent focused on '{tag}' tasks. "
        f"You have access to tools tagged with '{tag}'. "
        "Use them to fulfill the user's request efficiently. "
        "If a task is outside your scope, kindly indicate that."
    )

    additional_tools = []
    additional_toolsets = []

    if graphiti_backend == "kuzu":
        # Embedded Kuzu: Use custom tools wrapping GraphitiClient
        if graphiti_client is None:
            raise ValueError("GraphitiClient required for Kuzu backend")

        async def ingest_to_graph(
            ctx: RunContext, content: str, source: str = "user"
        ) -> str:
            try:
                await graphiti_client.add_episode(
                    name=f"Ingestion from {source}",
                    episode_body=content,
                    source=EpisodeType.text,
                    source_description=f"Ingested content from {source}",
                    reference_time=datetime.now(timezone.utc)
                )
                return "Ingested successfully into the knowledge graph."
            except Exception as e:
                return f"Error ingesting: {str(e)}"

        ingest_to_graph.__name__ = "ingest_to_graph"
        ingest_to_graph.__doc__ = "Ingest text content (e.g., docs, chat history) into the temporal knowledge graph as an episode."

        additional_tools.append(ingest_to_graph)

        async def query_graph(ctx: RunContext, query: str) -> str:
            try:
                results = graphiti_client.search(query)
                return str(results)  # Or format as needed
            except Exception as e:
                return f"Error querying graph: {str(e)}"

        query_graph.__name__ = "query_graph"
        query_graph.__doc__ = "Query the temporal knowledge graph for context (e.g., hybrid search on entities/relationships)."

        additional_tools.append(query_graph)
        system_prompt += (
            " Use ingest_to_graph and query_graph for knowledge graph interactions."
        )

    else:
        # Server backends (Neo4j/FalkorDB): Use MCP
        if graphiti_mcp_url is None:
            raise ValueError("Graphiti MCP URL required for server backends")
        graphiti_toolset = FastMCPToolset(client=Client[Any](transport=graphiti_mcp_url))
        additional_toolsets.append(graphiti_toolset)
        system_prompt += " Use Graphiti MCP tools for querying/ingesting into the temporal knowledge graph."
    logger.debug("Created child agent for tag '%s' with MCP tools and Graphiti", tag)
    return Agent(
        model=model,
        system_prompt=system_prompt,
        name=f"GitLab_{tag}_Specialist",
        toolsets=[filtered_toolset] + additional_toolsets,
        tools=additional_tools,
    )


async def create_orchestrator(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    graphiti_backend: str = DEFAULT_GRAPHITI_BACKEND,
    graphiti_db_path: str = DEFAULT_GRAPHITI_DB_PATH,
    graphiti_uri: str = DEFAULT_GRAPHITI_URI,
    graphiti_user: str = DEFAULT_GRAPHITI_USER,
    graphiti_pass: str = DEFAULT_GRAPHITI_PASS,
    graphiti_host: str = DEFAULT_GRAPHITI_HOST,
    graphiti_port: int = DEFAULT_GRAPHITI_PORT,
    graphiti_mcp_url: str = DEFAULT_GRAPHITI_MCP_URL,
    graphiti_force_reinit: bool = False,
) -> Agent:
    """
    Creates the parent Orchestrator agent with tools to delegate to children.
    """
    graphiti_client = await initialize_graphiti_db(
        backend=graphiti_backend,
        db_path=graphiti_db_path,
        uri=graphiti_uri,
        user=graphiti_user,
        password=graphiti_pass,
        host=graphiti_host,
        port=graphiti_port,
        database="graphiti",
        force_reinit=graphiti_force_reinit,
        base_url=base_url,
        api_key=api_key,
        model_id=model_id,
        provider=provider,
    )

    # 1. Create all child agents
    children: Dict[str, Agent] = {}
    for tag in TAGS:
        children[tag] = create_child_agent(
            tag=tag,
            mcp_url=mcp_url,
            provider=provider,
            model_id=model_id,
            base_url=base_url,
            api_key=api_key,
            graphiti_backend=graphiti_backend,
            graphiti_client=graphiti_client,
            graphiti_mcp_url=graphiti_mcp_url,
        )

    # 2. Create Model for Parent
    model = create_model(
        provider=provider, model_id=model_id, base_url=base_url, api_key=api_key
    )

    # 3. Create Delegation Tools
    # We create a list of callables that the parent can use as tools.
    delegation_tools = []

    for tag, child_agent in children.items():

        # Define the tool function.
        # CAUTION: Python closures capture variables by reference.
        # We must bind 'child_agent' and 'tag' to the function scope using default args.
        async def delegate_task(
            ctx: RunContext, task_description: str, _agent=child_agent, _tag=tag
        ) -> str:
            # We don't have a docstring here yet, we'll set it below.
            print(
                f"[Orchestrator] debug: Delegating task to {_tag} specialist: {task_description}"
            )
            logging.debug(f"[Orchestrator] Delegating to {_tag}: {task_description}")
            try:
                print(f"[Orchestrator] Running child agent {_tag}...")
                result = await _agent.run(task_description)
                print(f"[Orchestrator] Child agent {_tag} returned: {result.output[:100]}...")
                return result.output
            except Exception as e:
                logging.exception(f"Error executing task with {_tag} specialist")
                return f"Error executing task with {_tag} specialist: {str(e)}"

        # Set metadata for the tool
        delegate_task.__name__ = f"delegate_to_{tag}"
        delegate_task.__doc__ = (
            f"Delegate a task related to '{tag}' (e.g., {tag} management, queries) "
            f"to the dedicated {tag} specialist agent. "
            f"Provide a clear, self-contained description of the subtask."
        )

        delegation_tools.append(delegate_task)

    # 4. Create Parent Agent
    system_prompt = (
        "You are the GitLab Orchestrator Agent. "
        "Your goal is to assist the user by delegating tasks to specialized child agents. "
        "Analyze the user's request and determine which domain(s) it falls into "
        "(e.g., merge_requests, pipelines, projects). "
        "Then, call the appropriate delegation tool(s) with a specific task description. "
        "Synthesize the results from the child agents into a final helpful response. "
        "Do not attempt to perform GitLab actions directly; always delegate."
    )

    orchestrator = Agent(
        model=model,
        system_prompt=system_prompt,
        name=AGENT_NAME,
        tools=delegation_tools,  # Register the wrapper functions as tools
    )

    logger.debug("Orchestrator created with %d delegation tools", len(delegation_tools))

    return orchestrator


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
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument(
        "--port", type=int, default=9000, help="Port to bind the server to"
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
        default=None,
        help="LLM Base URL (for OpenAI compatible providers)",
    )
    parser.add_argument("--api-key", default=None, help="LLM API Key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP Server URL")
    # Graphiti args
    parser.add_argument(
        "--graphiti-backend",
        default=DEFAULT_GRAPHITI_BACKEND,
        choices=["kuzu", "neo4j", "falkordb"],
        help="Graphiti backend (kuzu for local file)",
    )
    parser.add_argument(
        "--graphiti-db-path",
        default=DEFAULT_GRAPHITI_DB_PATH,
        help="Path to Kuzu DB file",
    )
    parser.add_argument(
        "--graphiti-uri", default=DEFAULT_GRAPHITI_URI, help="Neo4j URI"
    )
    parser.add_argument(
        "--graphiti-user",
        default=DEFAULT_GRAPHITI_USER,
        help="Neo4j username",
    )
    parser.add_argument(
        "--graphiti-pass",
        default=DEFAULT_GRAPHITI_PASS,
        help="Neo4j password",
    )
    parser.add_argument(
        "--graphiti-host",
        default=DEFAULT_GRAPHITI_HOST,
        help="FalkorDB host",
    )
    parser.add_argument(
        "--graphiti-port",
        type=int,
        default=DEFAULT_GRAPHITI_PORT,
        help="FalkorDB port",
    )
    parser.add_argument(
        "--graphiti-mcp-url",
        default=DEFAULT_GRAPHITI_MCP_URL,
        help="Graphiti MCP URL for server backends",
    )
    parser.add_argument(
        "--graphiti-force-reinit",
        action="store_true",
        help="Force reinitialize Graphiti DB with initial docs",
    )
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
    cli_agent = asyncio.run(create_orchestrator(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
        graphiti_backend=args.graphiti_backend,
        graphiti_db_path=args.graphiti_db_path,
        graphiti_uri=args.graphiti_uri,
        graphiti_user=args.graphiti_user,
        graphiti_pass=args.graphiti_pass,
        graphiti_host=args.graphiti_host,
        graphiti_port=args.graphiti_port,
        graphiti_mcp_url=args.graphiti_mcp_url,
        graphiti_force_reinit=args.graphiti_force_reinit,
    ))

    # Create A2A App
    cli_app = cli_agent.to_a2a(
        name=AGENT_NAME, description=AGENT_DESCRIPTION, version="25.13.8", skills=skills
    )
    logger.info("Starting A2A server with provider=%s, model=%s, mcp_url=%s", args.provider, args.model_id, args.mcp_url)
    uvicorn.run(
        cli_app,
        host=args.host,
        port=args.port,
    )


if __name__ == "__main__":
    agent_server()
