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

*Version: 25.36.2*

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

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Misc** | `MISC_TOOL` | `True` | Manage gitlab api misc operations. |
| **Branches** | `BRANCHES_TOOL` | `True` | Manage gitlab branches operations. Action-routed methods: `create`, `delete`, `get`. |
| **Protected Branches** | `PROTECTED_BRANCHES_TOOL` | `True` | Manage gitlab protected branches operations. Action-routed methods: `get`, `protect`, `unprotect`. |
| **Commits** | `COMMITS_TOOL` | `True` | Manage gitlab commits operations. Action-routed methods: `create`, `create_comment`, `diff`, `get`, `get_comments`, `get_discussions`, `get_gpg_signature`, `get_merge_requests`, `get_statuses`, `post_status`, `revert`. |
| **Deploy Tokens** | `DEPLOY_TOKENS_TOOL` | `True` | Manage gitlab deploy tokens operations. Action-routed methods: `create_group`, `create_project`, `delete_group`, `delete_project`, `get`, `get_group`, `get_project`. |
| **Environments** | `ENVIRONMENTS_TOOL` | `True` | Manage gitlab environments operations. Action-routed methods: `create`, `delete`, `delete_stopped`, `get`, `get_protected`, `protect`, `stop`, `stop_stale`, `unprotect`, `update`, `update_protected`. |
| **Groups** | `GROUPS_TOOL` | `True` | Manage gitlab groups operations. Action-routed methods: `edit`, `get`, `get_descendants`, `get_merge_requests`, `get_projects`, `get_subgroups`. |
| **Jobs** | `JOBS_TOOL` | `True` | Manage gitlab jobs operations. Action-routed methods: `cancel`, `erase`, `get_log`, `get_pipeline_jobs`, `get_project_jobs`, `retry`, `run`. |
| **Members** | `MEMBERS_TOOL` | `True` | Manage gitlab members operations. Action-routed methods: `get_group`, `get_project`. |
| **Merge Requests** | `MERGE_REQUESTS_TOOL` | `True` | Manage gitlab merge requests operations. Action-routed methods: `create`, `get`, `get_project`. |
| **Merge Rules** | `MERGE_RULES_TOOL` | `True` | Manage gitlab merge rules operations. Action-routed methods: `approve_mr`, `create_project_level`, `delete_project_level`, `edit_group_level`, `edit_project_level`, `get_group_level`, `get_mr_approval_state`, `get_mr_approvals`, `get_mr_level`, `get_project_level`, `unapprove_mr`, `update_project_level`. |
| **Packages** | `PACKAGES_TOOL` | `True` | Manage gitlab packages operations. Action-routed methods: `download`, `get`, `publish`. |
| **Pipelines** | `PIPELINES_TOOL` | `True` | Manage gitlab pipelines operations. Action-routed methods: `get`, `run`. |
| **Pipeline Schedules** | `PIPELINE_SCHEDULES_TOOL` | `True` | Manage gitlab pipeline schedules operations. Action-routed methods: `create`, `create_variable`, `delete`, `delete_variable`, `edit`, `get`, `get_all`, `get_triggered`, `run`, `take_ownership`. |
| **Projects** | `PROJECTS_TOOL` | `True` | Manage gitlab projects operations. Action-routed methods: `edit`, `get`, `get_contributors`, `get_nested_by_group`, `get_statistics`, `share_with_group`, `unshare_with_group`. |
| **Releases** | `RELEASES_TOOL` | `True` | Manage gitlab releases operations. Action-routed methods: `create`, `create_evidence`, `delete`, `download_asset`, `get`, `get_by_tag`, `get_group_releases`, `get_latest`, `get_latest_asset`, `get_latest_evidence`, `update`. |
| **Runners** | `RUNNERS_TOOL` | `True` | Manage gitlab runners operations. Action-routed methods: `delete`, `delete_project`, `enable_project`, `get_all`, `get_group`, `get_jobs`, `get_project`, `pause`, `register`, `reset_gitlab_token`, `reset_group_token`, `reset_project_token`, `reset_token`, `update_details`, `verify_auth`. |
| **Tags** | `TAGS_TOOL` | `True` | Manage gitlab tags operations. Action-routed methods: `create`, `delete`, `get`, `get_protected`, `get_protected_tag`, `protect`, `unprotect`. |
| **Labels** | `LABELS_TOOL` | `True` | Manage GitLab labels. Action-routed methods: `create`, `delete`, `get`, `update`. |
| **Milestones** | `MILESTONES_TOOL` | `True` | Manage GitLab milestones. Action-routed methods: `create`, `delete`, `get`, `update`. |
| **Snippets** | `SNIPPETS_TOOL` | `True` | Manage GitLab snippets. Action-routed methods: `create`, `delete`, `get`, `update`. |
| **Notes** | `NOTES_TOOL` | `True` | Manage GitLab notes/comments on issues, merge requests, commits, and epics. Action-routed methods: `create`, `delete`, `get`, `update`. |
| **Epics** | `EPICS_TOOL` | `True` | Manage GitLab epics. Action-routed methods: `create`, `delete`, `get`, `update`. |
| **Issues** | `ISSUES_TOOL` | `True` | Manage GitLab issues. Action-routed methods: `create`, `delete`, `get`, `update`. |
| **Custom Api** | `CUSTOM_API_TOOL` | `True` | Execute arbitrary GitLab REST API requests directly. |
| **Graphql** | `GRAPHQL_TOOL` | `True` | Execute raw GraphQL queries and mutations natively on GitLab. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](docs/mcp.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

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
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

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
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "GITLAB_URL": "your_gitlab_url_here",
        "GITLAB_TOKEN": "your_gitlab_token_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](docs/agent.md).

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
