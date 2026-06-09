# gitlab-api

GitLab **API + MCP Server + A2A Agent** for the agent-utilities ecosystem — a typed,
action-routed connector for the GitLab REST and GraphQL APIs.

!!! info "Official documentation"
    This site is the canonical reference for `gitlab-api`, maintained alongside every
    release.

[![PyPI](https://img.shields.io/pypi/v/gitlab-api)](https://pypi.org/project/gitlab-api/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/gitlab-api)](https://github.com/Knuckles-Team/gitlab-api/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/gitlab-api)

## Overview

`gitlab-api` wraps the GitLab REST and GraphQL surface with typed, deterministic MCP
tools and an optional Pydantic-AI agent server. It provides:

- **`Api`** — a Python client (`gitlab_api.api_client.Api`) composed from per-domain
  mixins covering projects, repositories, merge requests, pipelines, environments,
  issues, users, and groups.
- **Action-routed MCP tools** — consolidated, togglable tool modules (branches,
  commits, merge requests, pipelines, releases, runners, and more) that minimize
  token overhead in LLM contexts.
- **An A2A agent server** — a Pydantic-AI graph agent (console script `gitlab-agent`)
  that calls the MCP tool surface and exposes an AG-UI web interface.

The connector remains inactive when credentials are absent: configure `GITLAB_URL`
and `GITLAB_TOKEN` to connect it to a GitLab instance.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `Api` client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy GitLab with Docker.
- :material-sitemap: **[Overview](overview.md)** — the action-routed tool surface and architecture.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:GL-*` registry.

</div>

## Quick start

```bash
pip install "gitlab-api[mcp]"
gitlab-mcp                        # stdio MCP server (default transport)
```

Connect it to a GitLab instance:

```bash
export GITLAB_URL=https://gitlab.example.com
export GITLAB_TOKEN=<your-gitlab-token>
gitlab-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the agent server, reverse
proxy, DNS).
