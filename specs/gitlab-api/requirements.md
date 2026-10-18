# CONN-GITLAB-API — Requirements

Governing spec: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-GITLAB-API-R001` | **Declare the `projects` source.** The connector ships `gitlab_api/ontology/ingest_sources.json` with the `projects` source. The source pages records through the read-only tool `gitlab_get_projects`. | `tests/test_ingest_sources.py::test_declares_ingestible_sources` validates the packaged file, resolves its tool to a client read operation and its record type to a manifest `schema_mappings` entry. |
