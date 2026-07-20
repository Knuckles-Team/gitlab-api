# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`gitlab-api` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "gitlab-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
gitlab-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/gitlab-api@sha256:<digest> gitlab-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "gitlab": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
<!-- END GENERATED: deployment-options -->

This page covers running `gitlab-api` as long-lived servers: the transports, a Docker
Compose stack, the optional A2A agent server, putting it behind a Caddy reverse proxy,
and giving it a DNS name with Technitium. To provision the **GitLab instance** it
connects to, see [Backing Platform](platform.md).

> `gitlab-api` ships both an **MCP server** (console script `gitlab-mcp`) and an
> **A2A agent server** (console script `gitlab-agent`). The MCP server is a typed,
> deterministic tool surface a policy router / agent calls; the agent server is a
> Pydantic-AI graph agent that wraps that surface with an AG-UI web interface.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    gitlab-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    gitlab-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    gitlab-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`gitlab-api` is configured entirely from the environment. The **required** set:

| Var | Default | Meaning |
|---|---|---|
| `GITLAB_URL` | `https://gitlab.com` | GitLab instance base URL |
| `GITLAB_TOKEN` | _(unset)_ | Personal / project / group access token |
| `GITLAB_TLS_PROFILE` | _(unset)_ | Optional runtime TLS profile selector; verification is mandatory |
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8000` | Listen port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |

Each tool module is independently togglable with a `*TOOL` flag (for example
`BRANCHESTOOL`, `PIPELINESTOOL`, `GRAPHQLTOOL`) — every variable, with its default,
is documented in
[`.env.example`](https://github.com/Knuckles-Team/gitlab-api/blob/main/.env.example).
Copy it to `.env` and fill in only what you use; the connector remains inactive when
`GITLAB_TOKEN` is absent.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/gitlab-api/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  gitlab-api-mcp:
    image: example/gitlab-api@sha256:<digest>
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
```

```bash
cp .env.example .env          # then edit GITLAB_URL / GITLAB_TOKEN
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Agent server (A2A)

`gitlab-api` also ships an A2A **agent server** (console script `gitlab-agent`). It
runs the Pydantic-AI graph agent, calls the MCP tool surface over `MCP_URL`, and
exposes an AG-UI web interface on port `9017`. The repo ships
[`docker/agent.compose.yml`](https://github.com/Knuckles-Team/gitlab-api/blob/main/docker/agent.compose.yml),
which deploys the MCP server and the agent server together:

```yaml
services:
  gitlab-api-mcp:
    image: example/gitlab-api@sha256:<digest>
    container_name: gitlab-api-mcp
    hostname: gitlab-api-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"

  gitlab-api-agent:
    image: example/gitlab-api@sha256:<digest>
    container_name: gitlab-api-agent
    hostname: gitlab-api-agent
    restart: always
    depends_on:
      - gitlab-api-mcp
    env_file:
      - ../.env
    command: ["gitlab-agent"]
    environment:
      - HOST=0.0.0.0
      - PORT=9017
      - MCP_URL=http://gitlab-api-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
    ports:
      - "9017:9017"
```

```bash
docker compose -f docker/agent.compose.yml up -d
curl -s http://localhost:9017/health        # {"status":"OK"}
```

The agent reaches the MCP server by container name through `MCP_URL`; set `PROVIDER`
and `MODEL_ID` (plus the matching provider API key) to select the model.

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .example.invalid zone
gitlab-api.example.invalid {
    tls internal
    reverse_proxy gitlab-api-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
gitlab-api.example.com {
    reverse_proxy gitlab-api-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=gitlab-api.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `gitlab-api.example.invalid → <caddy-host-ip>` in the Technitium web
console (`http://technitium.example.invalid:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "gitlab-api": {
      "command": "uv",
      "args": ["run", "gitlab-mcp"],
      "env": {
        "GITLAB_URL": "https://gitlab.example.com",
        "GITLAB_TOKEN": "<your-gitlab-token>"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://gitlab-api.example.invalid/mcp` instead.
