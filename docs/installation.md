# Installation

`gitlab-api` is a standard Python package and a prebuilt container image. Pick the
path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **GitLab instance** (GitLab.com or self-managed) and a personal /
  project access token — see [Backing Platform](platform.md) to deploy one locally.

## From PyPI (recommended)

```bash
pip install gitlab-api
```

### Optional extras

The base install is intentionally minimal. Install the extra for what you need:

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "gitlab-api[mcp]"` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "gitlab-api[agent]"` | Pydantic-AI agent + Logfire tracing |
| `gql` | `pip install "gitlab-api[gql]"` | `gql` client for the GitLab GraphQL API |
| `all` | `pip install "gitlab-api[all]"` | Everything above |

```bash
# Typical: run the MCP server with GraphQL support
pip install "gitlab-api[mcp,gql]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/gitlab-api.git
cd gitlab-api
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run gitlab-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint `gitlab-mcp`):

```bash
docker pull knucklessg1/gitlab-api:latest

docker run --rm -i \
  -e GITLAB_URL=https://gitlab.example.com \
  -e GITLAB_TOKEN=<your-gitlab-token> \
  knucklessg1/gitlab-api:latest        # stdio transport (default)
```

For an HTTP server with a published port and the agent server, see
[Deployment](deployment.md).

## Verify the install

```bash
gitlab-mcp --help
gitlab-agent --help
python -c "import gitlab_api; print(gitlab_api.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP / agent server behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
