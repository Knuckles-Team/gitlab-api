# GitLab API

![PyPI - Version](https://img.shields.io/pypi/v/gitlab-api)
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

*Version: 25.10.0*

Pythonic GitLab API Library

GitLab MCP Server for Agentic AI! Get started with Pip or Docker

Includes a large portion of useful API calls to GitLab and SQLAlchemy Models to handle loading API calls directly to a database!

This repository is actively maintained - Contributions are welcome!

Additional Features:
- All responses are returned as native Pydantic models
- Save Pydantic models to pickle files locally
- Easily convert Pydantic to SQLAlchemy models for quick database insertion

### API Calls:
- Branches
- Commits
- Deploy Tokens
- Groups
- Jobs
- Members
- Merge Request
- Merge Request Rules
- Merge Request Rule Settings
- Namespaces
- Packages
- Pipeline
- Pipeline Schedules
- Projects
- Protected Branches
- Releases
- Runners
- Users
- Wiki
- Environments
- Protected Environments
- Tags
- Protected Tags
- Custom Endpoint

If your API call isn't supported, you can always run the standard custom API endpoint function to get/post/put/delete and endpoint

### Experimental - GraphQL:
- Branches
- Groups
- Jobs
- Merge Request
- Pipeline
- Branches
- Users
- Wiki
- Projects

<details>
  <summary><b>Usage:</b></summary>

### Using as an MCP Server:

The GitLab MCP server can be configured via CLI arguments to support various transport methods (`stdio`, `http`, `sse`) and authentication options (`none`, `static`, `jwt`, `oauth-proxy`, `oidc-proxy`, `remote-oauth`). Eunomia authorization is also supported (`none`, `embedded`, `remote`).

#### CLI Configuration
Run the MCP server with custom options:

```bash
gitlab-mcp --transport http --host 0.0.0.0 --port 8002 \
  --auth-type jwt \
  --token-jwks-uri "https://example.com/.well-known/jwks.json" \
  --token-issuer "https://example.com" \
  --token-audience "gitlab-mcp" \
  --eunomia-type embedded \
  --eunomia-policy-file "policies.json"
```

Available CLI options:
- `--transport`: Transport method (`stdio`, `http`, `sse`) [default: `stdio`]
- `--host`: Host address for HTTP/SSE transport [default: `0.0.0.0`]
- `--port`: Port number for HTTP/SSE transport [default: `8002`]
- `--auth-type`: Authentication type (`none`, `static`, `jwt`, `oauth-proxy`, `oidc-proxy`, `remote-oauth`) [default: `none`]
- `--token-jwks-uri`: JWKS URI for JWT verification
- `--token-issuer`: Issuer for JWT verification
- `--token-audience`: Audience for JWT verification
- `--oauth-upstream-auth-endpoint`: Upstream authorization endpoint for OAuth proxy
- `--oauth-upstream-token-endpoint`: Upstream token endpoint for OAuth proxy
- `--oauth-upstream-client-id`: Upstream client ID for OAuth proxy
- `--oauth-upstream-client-secret`: Upstream client secret for OAuth proxy
- `--oauth-base-url`: Base URL for OAuth proxy
- `--oidc-config-url`: OIDC configuration URL
- `--oidc-client-id`: OIDC client ID
- `--oidc-client-secret`: OIDC client secret
- `--oidc-base-url`: Base URL for OIDC proxy
- `--remote-auth-servers`: Comma-separated list of authorization servers for remote OAuth
- `--remote-base-url`: Base URL for remote OAuth
- `--allowed-client-redirect-uris`: Comma-separated list of allowed client redirect URIs
- `--eunomia-type`: Eunomia authorization type (`none`, `embedded`, `remote`) [default: `none`]
- `--eunomia-policy-file`: Policy file for embedded Eunomia [default: `mcp_policies.json`]
- `--eunomia-remote-url`: URL for remote Eunomia server

#### AI Prompt Examples
**Prompt**: Get me the details of my GitLab project with ID 420.

**Response**:
```text
Here are the details for your GitLab project:

Project Name: Docker Registry
Project ID: 420
Namespace: Homelab
Visibility: Internal
Created: November 13, 1999
Default Branch: main
Last Activity: August 20, 2025
Web URL: http://gitlab.arpa/homelab/docker-registry

This project is configured with container registry capabilities
and supports CI/CD pipelines, merge requests, and issue tracking.
It is currently active with no open issues and follows
the default branch strategy for its workflow.
```

**Prompt**: Run the GitLab pipeline for this project ID 133 on the main branch.

**Response**:
```text
The pipeline has been successfully created for the project ID 133 on the main reference. Here are the details:

Pipeline ID: 20601
Reference: main
SHA: asidfaskdjvalksdjv
Status: Created
Web URL:

Created At: 2025-08-27T02:49:20.068Z
The pipeline is now queued and will start executing soon. Let me know if you'd like further details or actions!
```

**Prompt**: Create a branch called "test" from the main branch in this GitLab project with ID 133.

**Response**:
```text
The branch test has been successfully created from the main branch in the project with ID 133.

Branch Details:
Name: test
URL:

Commit:
Short ID: 1c3775ac
Message: "Add adguard."
Author: KnucklesSG1
Committed Date: August 25, 2025, at 05:03:01 (UTC-05:00)
This branch is not protected, and it is not set as the default branch.
The branch is currently unmerged and can be pushed to by authorized users.

Let me know if you'd like further actions (e.g., merging, pushing changes)!
```

**Prompt**: Create a merge request for project 133 from the test branch to the main branch with a title of "This is a merge request by Qwen3" and a description of "This is a description populated by Qwen3 LLM".

**Response**:
```text
The merge request has been successfully created with the following details:

Title: This is a merge request by Qwen3
Description: This is a description populated by Qwen3 LLM
Source Branch: test
Target Branch: main
Project: homelab/containers/services/project
Merge Request URL:

Status: Opened
Created At: 2025-08-27T03:15:51.520000Z
The merge request is currently in the "preparing" state and is ready for review. Let me know if you'd like further actions, such as assigning reviewers or approving the merge! 😊
```

### Use API Directly
```python
#!/usr/bin/python

import gitlab_api
from gitlab_api import pydantic_to_sqlalchemy, upsert, save_model, load_model
from gitlab_api.gitlab_db_models import BaseDBModel as Base
import urllib3
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

gitlab_token = os.environ["GITLAB_TOKEN"]
postgres_username = os.environ["POSTGRES_USERNAME"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_db_host = os.environ["POSTGRES_DB_HOST"]
postgres_port = os.environ["POSTGRES_PORT"]
postgres_db_name = os.environ["POSTGRES_DB_NAME"]

if __name__ == "__main__":
    print("Creating GitLab Client...")
    client = gitlab_api.Api(
        url="http://gitlab.arpa/api/v4/",
        token=gitlab_token,
        verify=False,
    )
    print("GitLab Client Created\n\n")

    print("\nFetching User Data...")
    user_response = client.get_users(active=True, humans=True)
    print(
        f"Users ({len(user_response.data)}) Fetched - "
        f"Status: {user_response.status_code}\n"
    )

    print("\nFetching Namespace Data...")
    namespace_response = client.get_namespaces()
    print(
        f"Namespaces ({len(namespace_response.data)}) Fetched - "
        f"Status: {namespace_response.status_code}\n"
    )

    print("\nFetching Project Data...")
    project_response = client.get_nested_projects_by_group(group_id=2, per_page=100)
    print(
        f"Projects ({len(project_response.data)}) Fetched - "
        f"Status: {project_response.status_code}\n"
    )

    print("\nFetching Merge Request Data...")
    merge_request_response = client.get_group_merge_requests(
        argument="state=all", group_id=2
    )
    print(
        f"\nMerge Requests ({len(merge_request_response.data)}) Fetched - "
        f"Status: {merge_request_response.status_code}\n"
    )

    # Pipeline Jobs table
    pipeline_job_response = None
    for project in project_response.data:
        job_response = client.get_project_jobs(project_id=project.id)
        if (
            not pipeline_job_response
            and hasattr(job_response, "data")
            and len(job_response.data) > 0
        ):
            pipeline_job_response = job_response
        elif (
            pipeline_job_response
            and hasattr(job_response, "data")
            and len(job_response.data) > 0
        ):
            pipeline_job_response.data.extend(job_response.data)
            print(
                f"Pipeline Jobs ({len(getattr(pipeline_job_response, 'data', []))}) "
                f"Fetched for Project ({project.id}) - "
                f"Status: {pipeline_job_response.status_code}\n"
            )

    print("Saving Pydantic Models...")
    user_file = save_model(model=user_response, file_name="user_model", file_path=".")
    namespace_file = save_model(
        model=namespace_response, file_name="namespace_model", file_path="."
    )
    project_file = save_model(
        model=project_response, file_name="project_model", file_path="."
    )
    merge_request_file = save_model(
        model=merge_request_response, file_name="merge_request_model", file_path="."
    )
    pipeline_job_file = save_model(
        model=pipeline_job_response, file_name="pipeline_job_model", file_path="."
    )
    print("Models Saved")

    print("Loading Pydantic Models...")
    user_response = load_model(file=user_file)
    namespace_response = load_model(file=namespace_file)
    project_response = load_model(file=project_file)
    merge_request_response = load_model(file=merge_request_file)
    pipeline_job_response = load_model(file=pipeline_job_file)
    print("Models Loaded")

    print("Converting Pydantic to SQLAlchemy model...")
    user_db_model = pydantic_to_sqlalchemy(schema=user_response)
    print(f"Database Models: {user_db_model}\n")

    print("Converting Pydantic to SQLAlchemy model...")
    namespace_db_model = pydantic_to_sqlalchemy(schema=namespace_response)
    print(f"Database Models: {namespace_db_model}\n")

    print("Converting Pydantic to SQLAlchemy model...")
    project_db_model = pydantic_to_sqlalchemy(schema=project_response)
    print(f"Database Models: {project_db_model}\n")

    print("Converting Pydantic to SQLAlchemy model...")
    merge_request_db_model = pydantic_to_sqlalchemy(schema=merge_request_response)
    print(f"Database Models: {merge_request_db_model}\n")

    print("Converting Pydantic to SQLAlchemy model...")
    pipeline_db_model = pydantic_to_sqlalchemy(schema=pipeline_job_response)
    print(f"Database Models: {pipeline_db_model}\n")

    print("Creating Engine")
    engine = create_engine(
        f"postgresql://{postgres_username}:{quote_plus(postgres_password)}@"
        f"{postgres_db_host}:{postgres_port}/{postgres_db_name}"
    )
    print("Engine Created\n\n")

    print("Creating Tables...")
    Base.metadata.create_all(engine)
    print("Tables Created\n\n")

    print("Creating Session...")
    Session = sessionmaker(bind=engine)
    session = Session()
    print("Session Created\n\n")

    print(f"Inserting ({len(user_response.data)}) Users Into Database...")
    upsert(session=session, model=user_db_model)
    print("Users Synchronization Complete!\n")

    print(f"Inserting ({len(namespace_response.data)}) Namespaces Into Database...")
    upsert(session=session, model=namespace_db_model)
    print("Namespaces Synchronization Complete!\n")

    print(f"Inserting ({len(project_response.data)}) Projects Into Database...\n")
    upsert(session=session, model=project_db_model)
    print("Projects Synchronization Complete!\n")

    print(
        f"Inserting ({len(merge_request_response.data)}) Merge Requests Into Database..."
    )
    upsert(session=session, model=merge_request_db_model)
    print("Merge Request Synchronization Complete!\n")

    print(
        f"Inserting ({len(pipeline_job_response.data)}) Pipeline Jobs Into Database..."
    )
    upsert(session=session, model=pipeline_db_model)
    print("Pipeline Jobs Synchronization Complete!\n")

    session.close()
    print("Session Closed")
```

### Experimental GraphQL Support

The `gitlab_gql.py` module provides a GraphQL interface to interact with GitLab's GraphQL API, offering parity with the REST API functionality in `gitlab_api.py`. It supports queries and mutations for managing projects, branches, tags, commits, merge requests, pipelines, jobs, packages, users, memberships, releases, issues, to-dos, environments, test reports, namespaces, groups, and wikis.

### Key Features
- **Generic Query Execution**: Use the `execute_gql` method to run custom GraphQL queries or mutations.
- **Consistent Interface**: Leverages the same Pydantic models, exceptions, and response handling as the REST API wrapper.
- **Pagination Support**: Handles cursor-based pagination with `first` and `after` parameters.
- **Authentication**: Supports Bearer token authentication, SSL verification, and proxy configuration.

### Usage Example
```python
from gitlab_api.gitlab_gql import GraphQL

# Initialize the GraphQL client
gql_api = GraphQL(url="https://gitlab.com", token="your_token")

# Fetch a project
result = gql_api.get_project(project_id="group/project")
print(result.data)

# Create a branch
result = gql_api.create_branch(project_id="group/project", branch="new-branch", ref="main")
print(result.data)
```

### Notes
- Requires the `gitlab-api[gql]` package (`pip install gitlab-api[gql]`).
- Some features (e.g., deploy tokens, wiki attachments) are not supported in GitLab's GraphQL API and require the REST API.
- See the [GitLab GraphQL API documentation](https://docs.gitlab.com/ee/api/graphql/) for available queries and mutations.

### Use with AI

Configure `mcp.json`

Recommended: Store secrets in environment variables with lookup in JSON file.

For Testing Only: Plain text storage will also work, although **not** recommended.

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "gitlab-api",
        "gitlab-mcp",
        "--transport",
        "http",
        "--host",
        "0.0.0.0",
        "--port",
        "8002",
        "--auth-type",
        "jwt",
        "--token-jwks-uri",
        "https://example.com/.well-known/jwks.json",
        "--token-issuer",
        "https://example.com",
        "--token-audience",
        "gitlab-mcp",
        "--eunomia-type",
        "embedded",
        "--eunomia-policy-file",
        "mcp_policies.json"
      ],
      "env": {
        "GITLAB_INSTANCE": "https://gitlab.com/api/v4/",
        "GITLAB_ACCESS_TOKEN": "glpat-askdfalskdvjas",
        "GITLAB_VERIFY": "True"
      },
      "timeout": 200000
    }
  }
}
```

### Deploy MCP Server as a Container

#### Using `docker run`
Pull the latest GitLab MCP image and run it with custom configuration:

```bash
docker pull knucklessg1/gitlab:latest

docker run -d \
  --name gitlab-mcp \
  -p 8002:8002 \
  -e HOST=0.0.0.0 \
  -e PORT=8002 \
  -e TRANSPORT=http \
  -e AUTH_TYPE=jwt \
  -e TOKEN_JWKS_URI=https://example.com/.well-known/jwks.json \
  -e TOKEN_ISSUER=https://example.com \
  -e TOKEN_AUDIENCE=gitlab-mcp \
  -e EUNOMIA_TYPE=embedded \
  -e EUNOMIA_POLICY_FILE=mcp_policies.json \
  knucklessg1/gitlab:latest
```

#### Using `docker-compose`
Create or modify a `docker-compose.yml` file:

```yaml
services:
  gitlab-mcp:
    image: knucklessg1/gitlab:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8002
      - TRANSPORT=http
      - AUTH_TYPE=jwt
      - TOKEN_JWKS_URI=https://example.com/.well-known/jwks.json
      - TOKEN_ISSUER=https://example.com
      - TOKEN_AUDIENCE=gitlab-mcp
      - EUNOMIA_TYPE=embedded
      - EUNOMIA_POLICY_FILE=mcp_policies.json
    ports:
      - 8002:8002
```

Run the container:

```bash
docker-compose up -d
```

</details>

<details>
  <summary><b>Installation Instructions:</b></summary>

### Install Python Package

```bash
python -m pip install gitlab-api
```

or

```bash
uv pip install --upgrade gitlab-api
```

</details>

<details>
  <summary><b>Tests:</b></summary>

pre-commit check
```bash
pre-commit run --all-files
```

pytest
```bash
python -m pip install -r test-requirements.txt
pytest ./test/test_gitlab_models.py
```

Full pytests

```bash
rm -rf ./dist/* \
&& python setup.py bdist_wheel --universal \
&& python -m pip uninstall gitlab-api -y \
&& python -m pip install ./dist/*.whl \
&& pytest -vv ./test/test_gitlab_models.py \
&& pytest -vv ./test/test_gitlab_db_models.py \
&& python ./test/test_sqlalchemy.py
```

Validate MCP Server

```bash
npx @modelcontextprotocol/inspector gitlab-mcp
```

</details>

<details>
  <summary><b>Repository Owners:</b></summary>

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

</details>
