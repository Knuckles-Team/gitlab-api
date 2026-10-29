# CONN-GITLAB-API — Plan

Component: Connector

Code: ../../gitlab_api/ontology/ingest_sources.json ../../tests/test_ingest_sources.py

## Design

The declaration file lists one source, `projects`. Its record type is `Project`. The tool `gitlab_get_projects` is the operation tool of the client method `get_projects`. `register_tool_surface` serves the file as `gitlab_ingest_sources`. A host syncs the source through the SDK sync runner (SCION-SOURCE-INGEST-R004.20).
