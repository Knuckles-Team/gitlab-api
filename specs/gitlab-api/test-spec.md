# CONN-GITLAB-API — Test specification

| Requirement | Test | Observation |
|---|---|---|
| `CONN-GITLAB-API-R001` | `tests/test_ingest_sources.py::test_declares_ingestible_sources` | The declaration validates and its tool is the read operation `get_projects`. |

## CONN-GITLAB-API-R002

`tests/test_fleet_name.py::test_connector_name_is_the_fleet_name` reads every connector name in the package. Each one is `gitlab-mcp`.

## CONN-GITLAB-API-R003

`tests/test_gitlab_gql.py::test_wrapper_delegates_to_shared_graphql_client` builds the wrapper with a fake shared client. It checks the endpoint, bearer header, TLS profile and schema fetch.
