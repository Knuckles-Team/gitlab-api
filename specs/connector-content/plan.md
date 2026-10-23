# CONN-GITLAB-API-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `gitlab-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `gitlab_api` from it.
