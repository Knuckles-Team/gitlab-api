# Usage — API / CLI / MCP

`gitlab-api` exposes the same capability three ways: as **MCP tools** an agent calls,
as a **Python API** (`Api`) the operator import, and as a **CLI**. The complete typed
tool surface is documented in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers one typed tool per GitLab operation,
for example `gitlab_get_projects`, `gitlab_create_merge_request`, `gitlab_get_pipelines`,
`gitlab_run_pipeline`, plus `gitlab_graphql`, `gitlab_graphql_ops_*` and the ingestion tools.
Destructive tools take `confirm=true`. Example agent prompts:

- *"List the open merge requests for project `group/app`"* -> `gitlab_get_project_merge_requests`
- *"Run a pipeline on main"* -> `gitlab_run_pipeline`

## As a Python API

`Api` (`gitlab_api.api_client.Api`) is composed from per-domain mixins covering
projects, repositories, merge requests, pipelines, environments, issues, users, and
groups. Build a client from the environment with `get_client()`:

```python
from gitlab_api.auth import get_client

api = get_client()  # reads GITLAB_URL / GITLAB_TOKEN from the environment / .env

# Reads
projects = api.get_projects()
merge_requests = api.get_project_merge_requests(project_id=42)
pipeline = api.get_pipeline(project_id=42, pipeline_id=1001)
```

Built it explicitly instead of relying on the environment:

```python
from gitlab_api.api_client import Api
from scion_sdk.core.transport_security import resolve_configured_tls_profile

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

gql_client = get_graphql_client()  # reads GITLAB_URL / GITLAB_TOKEN
```

## As a CLI

Both honor the same environment configuration documented in
[Deployment](deployment.md#configuration-environment) and remain inactive when
`GITLAB_TOKEN` is absent.
