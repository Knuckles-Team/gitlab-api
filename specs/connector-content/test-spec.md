# CONN-GITLAB-API-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-GITLAB-API-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |
| T-002 | `CONN-GITLAB-API-CONNECTOR-CONTENT-R002` | `tests/test_ontology_parent_link.py` | Every declared class reaches a parent class; the import of the parent IRI is present. |
| T-004 | `CONN-GITLAB-API-CONNECTOR-CONTENT-R004` | `tests/test_cq_paths.py` | The test finds no shared-class declaration, the `state` domain on `Issue` and no null mapping. |
| T-005 | `CONN-GITLAB-API-CONNECTOR-CONTENT-R005` | `tests/test_catalog_edges.py` | Every declared edge is an ontology property of its record type; project and issue references become owner and assignee edges. |
