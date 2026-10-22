# CONN-GITLAB-API — Test specification

| Requirement | Test | Observation |
|---|---|---|
| `CONN-GITLAB-API-R001` | `tests/test_ingest_sources.py::test_declares_ingestible_sources` | The declaration validates and its tool is the read operation `get_projects`. |

## CONN-GITLAB-API-R002

`tests/test_fleet_name.py::test_connector_name_is_the_fleet_name` reads every connector name in the package. Each one is `gitlab-mcp`.
