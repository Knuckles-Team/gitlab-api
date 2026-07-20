# Usage — API / CLI / MCP

`gitlab-api` exposes the same capability three ways: as **MCP tools** an agent calls,
as a **Python API** (`Api`) you import, and as a **CLI**. The complete action-routed
tool surface is documented in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers consolidated, action-routed tool
modules. Each module is independently togglable with a `*TOOL` environment flag:

| Group | Tool modules |
|---|---|
| Source | `branches`, `protected_branches`, `commits`, `tags`, `repositories` |
| Project & group | `projects`, `groups`, `members`, `environments`, `deploy_tokens` |
| CI/CD | `pipelines`, `pipeline_schedules`, `jobs`, `runners`, `releases`, `packages` |
| Collaboration | `merge_requests`, `merge_rules`, `issues`, `labels`, `milestones`, `notes`, `snippets` |
| Escape hatches | `custom_api` (arbitrary REST), `graphql` (GitLab GraphQL), `misc` |

Each module is action-routed: a single tool dispatches to named methods (for example
`branches` routes `create`, `delete`, `get`). Example agent prompts that map onto
these tools:

- *"List the open merge requests for project `group/app`"* → `merge_requests` (`get_project`)
- *"Run the pipeline on the `main` branch of project 42"* → `pipelines` (`run`)
- *"Create a `release/2.0` branch from `main`"* → `branches` (`create`)

## As a Python API

`Api` (`gitlab_api.api_client.Api`) is composed from per-domain mixins covering
projects, repositories, merge requests, pipelines, environments, issues, users, and
groups. Build a client from the environment with `get_client()`:

```python
from gitlab_api.auth import get_client

api = get_client()        # reads GITLAB_URL / GITLAB_TOKEN from the environment / .env

# Reads
projects = api.get_projects()
merge_requests = api.get_project_merge_requests(project_id=42)
pipeline = api.get_pipeline(project_id=42, pipeline_id=1001)
```

Construct it explicitly instead of relying on the environment:

```python
from gitlab_api.api_client import Api
from agent_utilities.core.transport_security import resolve_configured_tls_profile

api = Api(
    url="https://gitlab.example.com",
    token="<your-gitlab-token>",
    tls_profile=resolve_configured_tls_profile("GITLAB"),
)
groups = api.get_groups()
```

For the GitLab GraphQL API, build a `gql` client with `get_graphql_client()`:

```python
from gitlab_api.auth import get_graphql_client

gql_client = get_graphql_client()      # reads GITLAB_URL / GITLAB_TOKEN
```

## As a CLI

The MCP and agent servers are themselves command-line entry points:

```bash
# MCP server — stdio (default) or an HTTP transport
gitlab-mcp --transport streamable-http --host 0.0.0.0 --port 8000

# A2A agent server — Pydantic-AI graph agent + AG-UI web interface (port 9017)
MCP_URL=http://localhost:8000/mcp gitlab-agent
```

Both honor the same environment configuration documented in
[Deployment](deployment.md#configuration-environment) and remain inactive when
`GITLAB_TOKEN` is absent.
