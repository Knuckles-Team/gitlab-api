"""GitLab DevOps ontology contribution (CONCEPT:AU-KG.ontology.federation-provider-leg).

Data-only subpackage: it carries ``gitlab.ttl`` (the ``owl:Ontology``
``http://knuckles.team/kg/gitlab`` module — groups, projects, merge requests,
pipelines, jobs, issues, epics, milestones, commits, branches, releases and runners
with their review and delivery relationships) which the scion-sdk hub federates
in via the ``scion_sdk.ontology_providers`` entry-point. It holds no business
logic and no heavy imports so the hub can resolve it cheaply.
"""
