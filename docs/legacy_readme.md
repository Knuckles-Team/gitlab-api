# Gitlab Api
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/gitlab-api)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/gitlab-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/gitlab-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/gitlab-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/gitlab-api)
![PyPI - License](https://img.shields.io/pypi/l/gitlab-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/gitlab-api)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/gitlab-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/gitlab-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/gitlab-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/gitlab-api)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/gitlab-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/gitlab-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/gitlab-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/gitlab-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/gitlab-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/gitlab-api)

*Version: 25.24.1*

---

## Overview

**Gitlab Api** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with GitLab API + MCP Server + A2A Server.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the GitLab API + MCP Server + A2A Server API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](file:///home/apps/workspace/agent-packages/agents/gitlab-api/docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Misc** | `MISCTOOL` | `True` | Manage misc operations. |
| **Branches** | `BRANCHESTOOL` | `True` | Manage gitlab branches operations. Action-routed methods: `get`, `create`, `delete`. |
| **Protected Branches** | `PROTECTED_BRANCHESTOOL` | `True` | Manage gitlab protected branches operations. Action-routed methods: `get`, `protect`, `unprotect`. |
| **Commits** | `COMMITSTOOL` | `True` | Manage gitlab commits operations. Action-routed methods: `get`, `create`, `diff`, `revert`, `get_comments`, `create_comment`, `get_discussions`, `get_statuses`, `post_status`, `get_merge_requests`, `get_gpg_signature`. |
| **Deploy Tokens** | `DEPLOY_TOKENSTOOL` | `True` | Manage gitlab deploy tokens operations. Action-routed methods: `get`, `get_project`, `create_project`, `delete_project`, `get_group`, `create_group`, `delete_group`. |
| **Environments** | `ENVIRONMENTSTOOL` | `True` | Manage gitlab environments operations. Action-routed methods: `get`, `create`, `update`, `delete`, `stop`, `stop_stale`, `delete_stopped`, `get_protected`, `protect`, `update_protected`, `unprotect`. |
| **Groups** | `GROUPSTOOL` | `True` | Manage gitlab groups operations. Action-routed methods: `get`, `edit`, `get_subgroups`, `get_descendants`, `get_projects`, `get_merge_requests`. |
| **Jobs** | `JOBSTOOL` | `True` | Manage gitlab jobs operations. Action-routed methods: `get_project_jobs`, `get_log`, `cancel`, `retry`, `erase`, `run`, `get_pipeline_jobs`. |
| **Members** | `MEMBERSTOOL` | `True` | Manage gitlab members operations. Action-routed methods: `get_group`, `get_project`. |
| **Merge Requests** | `MERGE_REQUESTSTOOL` | `True` | Manage gitlab merge requests operations. Action-routed methods: `create`, `get`, `get_project`. |
| **Merge Rules** | `MERGE_RULESTOOL` | `True` | Manage gitlab merge rules operations. Action-routed methods: `get_project_level`, `create_project_level`, `update_project_level`, `delete_project_level`, `get_mr_approvals`, `get_mr_approval_state`, `get_mr_level`, `approve_mr`, `unapprove_mr`, `get_group_level`, `edit_group_level`, `edit_project_level`. |
| **Packages** | `PACKAGESTOOL` | `True` | Manage gitlab packages operations. Action-routed methods: `get`, `publish`, `download`. |
| **Pipelines** | `PIPELINESTOOL` | `True` | Manage gitlab pipelines operations. Action-routed methods: `get`, `run`. |
| **Pipeline Schedules** | `PIPELINE_SCHEDULESTOOL` | `True` | Manage gitlab pipeline schedules operations. Action-routed methods: `get_all`, `get`, `get_triggered`, `create`, `edit`, `take_ownership`, `delete`, `run`, `create_variable`, `delete_variable`. |
| **Projects** | `PROJECTSTOOL` | `True` | Manage gitlab projects operations. Action-routed methods: `get`, `get_nested_by_group`, `get_contributors`, `get_statistics`, `edit`, `share_with_group`, `unshare_with_group`. |
| **Releases** | `RELEASESTOOL` | `True` | Manage gitlab releases operations. Action-routed methods: `get`, `get_latest`, `get_latest_evidence`, `get_latest_asset`, `get_group_releases`, `download_asset`, `get_by_tag`, `create`, `create_evidence`, `update`, `delete`. |
| **Runners** | `RUNNERSTOOL` | `True` | Manage gitlab runners operations. Action-routed methods: `get_all`, `update_details`, `pause`, `get_jobs`, `get_project`, `enable_project`, `delete_project`, `get_group`, `register`, `delete`, `verify_auth`, `reset_gitlab_token`, `reset_project_token`, `reset_group_token`, `reset_token`. |
| **Tags** | `TAGSTOOL` | `True` | Manage gitlab tags operations. Action-routed methods: `get`, `create`, `delete`, `get_protected`, `get_protected_tag`, `protect`, `unprotect`. |
| **Custom Api** | `CUSTOM_APITOOL` | `True` | Manage api request operations. |
| **Graphql** | `GRAPHQLTOOL` | `True` | Execute raw GraphQL queries and mutations natively on GitLab. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](file:///home/apps/workspace/agent-packages/agents/gitlab-api/docs/mcp.md).

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "gitlab-api": {
      "command": "uvx",
      "args": [
        "--from",
        "gitlab-api",
        "gitlab-mcp"
      ],
      "env": {
        "GITLAB_URL": "your_gitlab_url_here",
        "GITLAB_TOKEN": "your_gitlab_token_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
To run the server as a long-running Streamable-HTTP service:

```json
{
  "mcpServers": {
    "gitlab-api": {
      "url": "http://localhost:8000/gitlab-api/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name gitlab-api-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e GITLAB_URL="your_value" \
  -e GITLAB_TOKEN="your_value" \
  knucklessg1/gitlab-api:latest
```

---

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export GITLAB_URL="your_value"
export GITLAB_TOKEN="your_value"

# Run the agent server
gitlab-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  gitlab-api-mcp:
    image: knucklessg1/gitlab-api:latest
    container_name: gitlab-api-mcp
    hostname: gitlab-api-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  gitlab-api-agent:
    image: knucklessg1/gitlab-api:latest
    container_name: gitlab-api-agent
    hostname: gitlab-api-agent
    restart: always
    depends_on:
      - gitlab-api-mcp
    env_file:
      - ../.env
    command: [ "gitlab-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9017
      - MCP_URL=http://gitlab-api-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9017:9017"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9017/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](file:///home/apps/workspace/agent-packages/agents/gitlab-api/docs/agent.md).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install gitlab-api[all]

# Using standard pip
python -m pip install gitlab-api[all]
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`
