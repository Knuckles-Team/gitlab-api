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

*Version: 25.46.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, the integrated A2A agent server, and guidance for provisioning the
> backing GitLab instance are maintained in the
> [official documentation](https://knuckles-team.github.io/gitlab-api/).

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

### Tool surface — `MCP_TOOL_MODE`

Set `MCP_TOOL_MODE` (in the shared `~/.config/agent-utilities/config.json` or env):
`condensed` (default — the action-routed tools below), `verbose` (one named 1:1 tool
per API method, e.g. `gitlab_get_branches(...)`, tagged `verbose`), or `both`. Filter
the verbose set with `--tools tag:verbose` / `MCP_ENABLED_TAGS=verbose`. See the
agent-utilities *MCP Tool Modes* guide.

### Available MCP Tools

_Auto-generated from the live MCP server — do not edit by hand._

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `api_request` | `CUSTOM_APITOOL` | Execute arbitrary GitLab REST API requests directly. |
| `gitlab_branches` | `BRANCHESTOOL` | Manage gitlab branches operations. |
| `gitlab_commits` | `COMMITSTOOL` | Manage gitlab commits operations. |
| `gitlab_deploy_tokens` | `DEPLOY_TOKENSTOOL` | Manage gitlab deploy tokens operations. |
| `gitlab_discover_graphql_schema` | `GRAPHQLTOOL` | Discover the dynamic GitLab GraphQL schema including types, fields, and custom attributes in real-time. |
| `gitlab_environments` | `ENVIRONMENTSTOOL` | Manage gitlab environments operations. |
| `gitlab_epics` | `EPICSTOOL` | Manage GitLab epics. |
| `gitlab_graphql` | `GRAPHQLTOOL` | Execute raw GraphQL queries and mutations natively on GitLab. |
| `gitlab_groups` | `GROUPSTOOL` | Manage gitlab groups operations. |
| `gitlab_instances` | `MISCTOOL` | List the configured GitLab tenants (CONCEPT:KG-2.9g). |
| `gitlab_issues` | `ISSUESTOOL` | Manage GitLab issues. |
| `gitlab_jobs` | `JOBSTOOL` | Manage gitlab jobs operations. |
| `gitlab_labels` | `LABELSTOOL` | Manage GitLab labels. |
| `gitlab_members` | `MEMBERSTOOL` | Manage gitlab members operations. |
| `gitlab_merge_requests` | `MERGE_REQUESTSTOOL` | Manage gitlab merge requests operations. |
| `gitlab_merge_rules` | `MERGE_RULESTOOL` | Manage gitlab merge rules operations. |
| `gitlab_milestones` | `MILESTONESTOOL` | Manage GitLab milestones. |
| `gitlab_notes` | `NOTESTOOL` | Manage GitLab notes/comments on issues, merge requests, commits, and epics. |
| `gitlab_packages` | `PACKAGESTOOL` | Manage gitlab packages operations. |
| `gitlab_pipeline_schedules` | `PIPELINE_SCHEDULESTOOL` | Manage gitlab pipeline schedules operations. |
| `gitlab_pipelines` | `PIPELINESTOOL` | Manage gitlab pipelines operations. |
| `gitlab_projects` | `PROJECTSTOOL` | Manage gitlab projects operations. |
| `gitlab_protected_branches` | `PROTECTED_BRANCHESTOOL` | Manage gitlab protected branches operations. |
| `gitlab_releases` | `RELEASESTOOL` | Manage gitlab releases operations. |
| `gitlab_runners` | `RUNNERSTOOL` | Manage gitlab runners operations. |
| `gitlab_snippets` | `SNIPPETSTOOL` | Manage GitLab snippets. |
| `gitlab_tags` | `TAGSTOOL` | Manage gitlab tags operations. |

_27 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

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

> **Install the slim `[mcp]` extra.** All examples below install
> `gitlab-api[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "gitlab-api": {
      "command": "uvx",
      "args": [
        "--from",
        "gitlab-api[mcp]",
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
        "gitlab-api[mcp]",
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
  knucklessg1/gitlab-api:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `gitlab-api[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `gitlab-api[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `gitlab-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`gitlab-api` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/gitlab-api/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://gitlab-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

---

## Environment Variables

Every variable the server reads.

### Connection & Credentials
The connector is single-host by default and **multi-tenant** when `gitlab_instances` is
configured (see [Multi-Tenancy](#multi-tenancy-multiple-gitlab-instances)). When no
instances are configured, it falls back to the single-host `GITLAB_*` values below.

| Variable | Description | Default |
|----------|-------------|---------|
| `GITLAB_URL` | Base GitLab instance URL | `https://gitlab.example.com` |
| `GITLAB_TOKEN` | GitLab personal/project access token (`glpat-…`) | — |
| `GITLAB_SSL_VERIFY` | TLS certificate verification | `True` |

> Multiple instances are declared once under `gitlab_instances` in the shared
> agent-utilities XDG config (`~/.config/agent-utilities/config.json`) — each entry has
> `name`, `url`, `token`, and `verify_ssl`. Target a tenant by **name** from the client
> factory; an unset instance resolves to the first configured one (else `GITLAB_URL` /
> `GITLAB_TOKEN`).

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |
| `DEBUG` | Verbose logging | `False` |
| `PYTHONUNBUFFERED` | Unbuffered stdout (recommended in containers) | `1` |

### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`).
The full list is in the [Available MCP Tools](#available-mcp-tools) table above
(e.g. `PROJECTSTOOL`, `MERGE_REQUESTSTOOL`, `PIPELINESTOOL`, `GRAPHQLTOOL`, `CUSTOM_APITOOL`).

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Agent CLI (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |

See [`.env.example`](.env.example) for a copy-paste starting point.

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
    image: knucklessg1/gitlab-api:mcp
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

## Multi-Tenancy (multiple GitLab instances)

The client is natively multi-tenant. The set of instances is declared once in the
shared **agent-utilities XDG config** (`~/.config/agent-utilities/config.json`) under
`gitlab_instances` — the **same** list the Knowledge-Graph GitLab indexer reads, so one
config drives both code/metadata indexing and every API/MCP call:

```json
{
  "gitlab_instances": [
    {"name": "internal", "url": "https://gitlab.arpa", "token": "glpat-xxxx", "verify_ssl": false},
    {"name": "public",   "url": "https://gitlab.com",  "token": "glpat-yyyy", "verify_ssl": true}
  ]
}
```

Target a tenant by **name** from the client factory; a bare URL still works, and an
unset instance resolves to the first configured one (else `GITLAB_URL`/`GITLAB_TOKEN`):

```python
from gitlab_api.auth import get_client
from gitlab_api.instances import list_configured_instances

internal = get_client(instance="internal")   # resolves url+token+verify from config
public   = get_client(instance="public")
default  = get_client()                        # first configured / GITLAB_URL fallback
names    = [i.name for i in list_configured_instances()]
```

The MCP server exposes a `gitlab_instances` tool (`action=list|get`) to discover the
configured tenants (tokens are never returned). When no instances are configured, the
connector falls back to the single-host `GITLAB_URL`/`GITLAB_TOKEN` it has always used.

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

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `gitlab-api[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `gitlab-api[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `gitlab-api[all]` | Everything (`mcp` + `agent` + `gql` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "gitlab-api[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "gitlab-api[agent]"

# Everything (development)
uv pip install "gitlab-api[all]"      # or: python -m pip install "gitlab-api[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/gitlab-api:mcp` | `--target mcp` | `gitlab-api[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `gitlab-mcp` |
| `knucklessg1/gitlab-api:latest` | `--target agent` (default) | `gitlab-api[agent]` — **full** agent runtime + epistemic-graph engine | `gitlab-agent` |

```bash
docker build --target mcp   -t knucklessg1/gitlab-api:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/gitlab-api:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/gitlab-api/) and is the
recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/gitlab-api/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/gitlab-api/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/gitlab-api/usage/) | the MCP tools, the `Api` client, the CLI |
| [Backing Platform](https://knuckles-team.github.io/gitlab-api/platform/) | deploy GitLab with Docker |
| [Overview](https://knuckles-team.github.io/gitlab-api/overview/) | the action-routed tool surface and architecture |
| [Concepts](https://knuckles-team.github.io/gitlab-api/concepts/) | concept registry (`CONCEPT:GL-*`) |

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


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `gitlab-api` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx gitlab-mcp` · or `uv tool install gitlab-api` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/gitlab-api:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
