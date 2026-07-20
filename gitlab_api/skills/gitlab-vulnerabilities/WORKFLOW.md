# Gitlab Vulnerabilities

Dependency & security-vulnerability review on GitLab via the gitlab-api MCP server — the GitLab counterpart to GitHub Dependabot. Read a project's Dependency List, review a project's or group's security vulnerabilities/findings, and fetch a single vulnerability by ID. Use when the agent must audit a project's dependencies for known vulnerabilities, review the security posture of a project or group, or inspect one vulnerability. Do NOT use for package publishing or registry reads (gitlab-packages), pipelines/CI (gitlab-pipelines), or issues (gitlab-issues); prefer those.

# GitLab Vulnerabilities

Domain-typed review of a GitLab project's **Dependency List** and **security vulnerabilities** —
the GitLab equivalent of GitHub's Dependabot dependency/vulnerability review. Covers dependencies
at **project** scope, vulnerabilities at **project** and **group** scope, and a single
vulnerability by its global ID.

## When to use
- Audit a **project's dependencies** (the Dependency List) — optionally filtered by package manager.
- Review a **project's** security **vulnerabilities** (Ultimate).
- Review a **group's** security **vulnerability findings** across its projects (Ultimate).
- Fetch **one vulnerability** by its global `vulnerability_id`.

## When NOT to use
- Publishing/reading packages in the package registry → `gitlab-packages`.
- CI/CD pipeline results and job logs → `gitlab-pipelines`.
- Issues / epics / milestones → `gitlab-issues`.
- Branch/commit/tag/project reads → `gitlab-repositories`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gitlab-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GITLAB_URL` | ✅ | GitLab instance base URL |
| `GITLAB_TOKEN` | ✅ | Access token with `api` scope; project/group Reporter+ for security data |
| `GITLAB_TLS_PROFILE` | optional | Runtime TLS profile selector; verification is mandatory |
| `VULNERABILITIESTOOL` | optional | Tool-group toggle (defaults `True`); set `False` to disable |

Full env/tag matrix: the mcp-client reference `agent-tools/mcp-client/references/gitlab-api.md`.
`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed vs. one-to-one verbose tools.

> The Vulnerabilities and findings endpoints require **GitLab Ultimate** with security scanning
> enabled. The Dependency List requires a Dependency Scanning job to have run. Without these the
> endpoints return empty results or `403`/`404` — that is a licensing/config state, not a tool bug.

## Tools & actions
| Condensed tool | Actions |
|----------------|---------|
| `gitlab_vulnerabilities` | `dependencies`, `get_project`, `get_group`, `get` |

Action → REST endpoint → client method:
- `dependencies` → `GET /projects/{project_id}/dependencies` → `get_project_dependencies`
- `get_project` → `GET /projects/{project_id}/vulnerabilities` → `get_project_vulnerabilities`
- `get_group` → `GET /groups/{group_id}/vulnerability_findings` → `get_group_vulnerabilities`
- `get` → `GET /vulnerabilities/{vulnerability_id}` → `get_vulnerability`

### Key parameters
- `dependencies`: `project_id` (required); optional `package_manager` filter (e.g. `npm`,
  `bundler`, `pip`); pagination `page`, `per_page`, `max_pages`.
- `get_project`: `project_id` (required); pagination.
- `get_group`: `group_id` (required); pagination.
- `get`: `vulnerability_id` (required) — the global vulnerability ID.

## Recipes (`params_json`)
List a project's full Dependency List:
```json
{"project_id":"platform/agent-utilities","per_page":100}
```
Only the npm dependencies:
```json
{"project_id":"platform/agent-utilities","package_manager":"npm"}
```
Review a project's security vulnerabilities:
```json
{"project_id":"platform/agent-utilities","per_page":50}
```
Review a group's vulnerability findings across its projects:
```json
{"group_id":"platform","per_page":100}
```
Fetch a single vulnerability by global ID:
```json
{"vulnerability_id":12345}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- `dependencies` needs a completed **Dependency Scanning** job; `get_project`/`get_group`/`get`
  need **Ultimate** security scanning — otherwise expect empty lists or `403`/`404`.
- `get` uses a **global** `vulnerability_id` (`/vulnerabilities/{id}`), not a per-project IID.
- Group review uses `vulnerability_findings` (there is no single group-wide `/vulnerabilities`
  REST list) — results are findings, deduplicate by `identifier` when summarizing.
- Large monorepos paginate — raise `per_page`/`max_pages` or filter by `package_manager`.

## Related
- **GitHub counterpart:** this is the GitLab equivalent of **GitHub Dependabot** dependency/
  vulnerability review — use it wherever a Dependabot-style dependency + CVE audit is needed on GitLab.
- **Package registry (not security):** `gitlab-packages`.
- **KG mapping:** vulnerabilities/dependencies relate to `:Project` nodes via `gitlab_api.kg_ingest`.
