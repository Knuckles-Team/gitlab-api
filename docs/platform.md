# Backing Platform — GitLab

`gitlab-api` is a **client** of a GitLab instance. This page provides a Docker recipe
for deploying one locally to serve as the target of `GITLAB_URL`. For production
topologies, follow the upstream
[GitLab installation documentation](https://docs.gitlab.com/ee/install/).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

GitLab publishes the `gitlab/gitlab-ce` image. The following stack runs one GitLab
Community Edition instance on `:8080` with the container registry on `:5050`:

```yaml
# docker/gitlab.compose.yml
services:
  gitlab:
    image: gitlab/gitlab-ce:18.2.1-ce.0
    container_name: gitlab
    hostname: gitlab.example.com
    restart: unless-stopped
    ports:
      - "8080:80"              # web / REST / GraphQL
      - "5050:5000"            # container registry
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://gitlab.example.com'
        prometheus_monitoring['enable'] = false
        puma['worker_processes'] = 2
        sidekiq['max_concurrency'] = 10
    volumes:
      - gitlab_config:/etc/gitlab
      - gitlab_data:/var/opt/gitlab
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:80/-/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 300s

volumes:
  gitlab_config:
  gitlab_data:
```

```bash
docker compose -f docker/gitlab.compose.yml up -d

# GitLab takes several minutes to initialize on first boot
curl -fsS http://localhost:8080/-/health
```

Retrieve the initial root password and create a personal access token (scopes `api`,
`read_api`) under **User Settings → Access Tokens** in the web UI:

```bash
docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```

## Connect gitlab-api

```bash
export GITLAB_URL=http://localhost:8080
export GITLAB_TOKEN=<your-gitlab-token>
export GITLAB_TLS_PROFILE=private-pki
export SSL_CERT_FILE=/run/secrets/private-ca-bundle.pem

gitlab-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places GitLab and the MCP server on one Docker network, so the
server reaches GitLab by container name:

```yaml
# docker/stack.compose.yml
services:
  gitlab:
    image: gitlab/gitlab-ce:18.2.1-ce.0
    hostname: gitlab
    ports: ["8080:80"]
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://gitlab'
    volumes:
      - gitlab_config:/etc/gitlab
      - gitlab_data:/var/opt/gitlab

  gitlab-api-mcp:
    image: example/gitlab-api@sha256:<digest>
    depends_on: [gitlab]
    environment:
      - GITLAB_URL=http://gitlab
      - GITLAB_TOKEN=<your-gitlab-token>
      - GITLAB_TLS_PROFILE=private-pki
      - SSL_CERT_FILE=/run/secrets/private-ca-bundle.pem
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

volumes:
  gitlab_config:
  gitlab_data:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

With the instance running, the MCP tools and the [`Api` client](usage.md#as-a-python-api)
operate against it directly — list projects, manage merge requests, trigger
pipelines, and publish releases.
