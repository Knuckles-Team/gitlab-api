# CONN-GITLAB-API — Requirements

Governing spec: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-GITLAB-API-R001` | **Declare the `projects` and `issues` sources.** The connector ships `gitlab_api/ontology/ingest_sources.json` with the `projects` and `issues` sources. The sources page records through the read-only tools `gitlab_get_projects` and `gitlab_get_issues`. | `tests/test_ingest_sources.py::test_declares_ingestible_sources` validates the packaged file, resolves its tool to a client read operation and its record type to a manifest `schema_mappings` entry. |
| `CONN-GITLAB-API-R002` | **Fleet name.** `pyproject.toml` declares `gitlab-mcp` as the single `agent_connector_sdk.connector` entry point. The content pack, the manifest `connector`, the fingerprints and the ingest binding all carry `gitlab-mcp`. Proving test: `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name`. | Every connector name in the package is `gitlab-mcp`. |
| `CONN-GITLAB-API-R003` | **Shared GraphQL client.** The connector's GraphQL calls go through the SDK shared GraphQL client. It declares GraphQL only through the SDK `graphql` extra. | `tests/test_gitlab_gql.py::test_wrapper_delegates_to_shared_graphql_client` checks endpoint, auth header, TLS profile and schema fetch. |
