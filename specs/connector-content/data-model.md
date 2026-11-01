# CONN-GITLAB-API-CONNECTOR-CONTENT — Data model

Entities, classes and tables this spec adds, one section per row.

## CONN-GITLAB-API-CONNECTOR-CONTENT-R002

Row title: Ontology joins the parent graph.

Definition from the row: Ontology joins the parent graph. Each `<package>/ontology/*.ttl` that declares classes imports `http://knuckles.team/kg`, and each class reaches an medulla parent class through `rdfs:subClassOf`. 1 class(es) with no fitting parent class are listed as pending in that test. Proving test: `tests/test_o.
