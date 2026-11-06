#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

from typing import Any

from scion_sdk.config import setting
from scion_sdk.mcp.concurrency import run_blocking

from gitlab_api.auth import get_client

DEFAULT_GITLAB_URL = setting("GITLAB_URL", "https://gitlab.com")
DEFAULT_GITLAB_TOKEN = setting("GITLAB_TOKEN", None)


def _records_as_dicts(resp: Any) -> list[dict[str, Any]]:
    """Normalize an Api response into a list of plain dicts."""
    data = getattr(resp, "data", resp)
    records = data if isinstance(data, list) else [data]
    return [
        r.model_dump() if hasattr(r, "model_dump") else r
        for r in records
        if r is not None
    ]


async def _fetch_pipeline_jobs(
    client: Any, project_id: str, pipelines: list[dict[str, Any]]
) -> dict[Any, list[dict[str, Any]]]:
    """Fetch each pipeline's jobs, keyed by pipeline id."""
    jobs_by_pipeline: dict[Any, list[dict[str, Any]]] = {}
    for pipe in pipelines:
        pid = pipe.get("id")
        if pid is None:
            continue
        jresp = await run_blocking(
            client.get_pipeline_jobs, project_id=project_id, pipeline_id=pid
        )
        jobs_by_pipeline[pid] = _records_as_dicts(jresp)
    return jobs_by_pipeline


def register_misc_tools(mcp: FastMCP):
    @mcp.tool(tags={"misc", "multitenant"}, annotations={"readOnlyHint": True})
    async def gitlab_instances_list(ctx: Context | None = None) -> Any:
        """List the configured GitLab tenants by name (tokens are never returned).

        Multi-tenancy is driven by the shared scion-sdk XDG config
        (``gitlab_instances`` in ~/.config/scion-sdk/config.json). Falls back to the
        single-host GITLAB_URL/GITLAB_TOKEN.
        """
        from gitlab_api.instances import instance_summaries

        return {"instances": instance_summaries()}

    @mcp.tool(tags={"misc", "multitenant"}, annotations={"readOnlyHint": True})
    async def gitlab_instances_get(
        name: str = Field(description="Instance name."), ctx: Context | None = None
    ) -> Any:
        """Read one configured GitLab tenant: url, whether a token and a TLS profile are set."""
        from gitlab_api.instances import get_instance

        inst = get_instance(name or None)
        if inst is None:
            return {"error": f"instance '{name}' not configured"}
        return {
            "name": inst.name,
            "url": inst.url,
            "tls_profile_configured": bool(inst.tls_profile_name),
            "has_token": bool(inst.token),
        }

    @mcp.tool(tags={"misc", "kg"})
    async def gitlab_ingest_projects(
        membership: bool | None = Field(
            default=None, description="Only projects the caller is a member of."
        ),
        owned: bool | None = Field(default=None, description="Only owned projects."),
        search: str | None = Field(
            default=None, description="Only projects matching this text."
        ),
        per_page: int | None = Field(default=None, description="Projects per page."),
        max_pages: int | None = Field(
            default=None, description="Maximum pages to read."
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Natively ingest GitLab projects into medulla as typed :Project nodes.

        Lists projects via the GitLab API and pushes them (with their :GitLabGroup +
        :partOfGroup links) into the knowledge graph via the fast engine client.
        Native-ingestion failures propagate to the caller.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from gitlab_api.kg_ingest import ingest_projects

        kwargs = {
            k: v
            for k, v in {
                "membership": membership,
                "owned": owned,
                "search": search,
                "per_page": per_page,
                "max_pages": max_pages,
            }.items()
            if v is not None
        }
        resp = await run_blocking(client.get_projects, **kwargs)
        projects = _records_as_dicts(resp)
        result = await ingest_projects(projects)
        return {"listed": len(projects), "ingested": result}

    @mcp.tool(tags={"misc", "kg"})
    async def gitlab_ingest_pipelines(
        project_id: str = Field(
            description="GitLab project id or URL-encoded path to ingest recent pipeline runs for."
        ),
        status: str | None = Field(
            default=None, description="Only pipelines with this status."
        ),
        ref: str | None = Field(
            default=None, description="Only pipelines on this ref."
        ),
        per_page: int | None = Field(default=None, description="Pipelines per page."),
        include_jobs: bool = Field(
            default=True,
            description="Also fetch + ingest each pipeline's jobs as :Job/:CheckRun nodes.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Natively ingest GitLab CI pipeline runs (+ jobs) into medulla.

        Lists recent pipelines for ``project_id`` and pushes them as typed
        ``:PipelineRun``/``:CheckRun`` nodes (the same classes github-agent uses, so
        GitLab CI/CD and GitHub Actions unify) into the knowledge graph. Best-effort:
        returns ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from gitlab_api.kg_ingest import ingest_pipeline_runs

        kwargs = {
            k: v
            for k, v in {"status": status, "ref": ref, "per_page": per_page}.items()
            if v is not None
        }
        kwargs["project_id"] = project_id
        resp = await run_blocking(client.get_pipelines, **kwargs)
        pipelines = _records_as_dicts(resp)

        jobs_by_pipeline: dict[Any, list[dict[str, Any]]] = {}
        if include_jobs:
            jobs_by_pipeline = await _fetch_pipeline_jobs(client, project_id, pipelines)

        result = await ingest_pipeline_runs(
            project_id, pipelines, jobs_by_pipeline=jobs_by_pipeline
        )
        return {"listed": len(pipelines), "ingested": result}


def register_graphql_ops_tools(mcp: FastMCP):
    """Typed GitLab GraphQL operations that have no REST tool."""
    from gitlab_api.auth import get_graphql_client

    rw = {"readOnlyHint": False, "destructiveHint": False}

    @mcp.tool(tags={"graphql_ops"}, annotations={"readOnlyHint": True})
    async def gitlab_graphql_ops_get_job(
        project_id: str = Field(description="Project id or full path."),
        job_id: int = Field(description="Job id."),
        client=Depends(get_graphql_client),
        ctx: Context | None = None,
    ) -> Any:
        """Read one CI job through GraphQL."""
        return await run_blocking(client.get_job, project_id=project_id, job_id=job_id)

    @mcp.tool(tags={"graphql_ops"}, annotations=rw)
    async def gitlab_graphql_ops_create_pipeline(
        project_id: str = Field(description="Project id or full path."),
        ref: str = Field(description="Branch, tag or SHA to run the pipeline on."),
        variables: dict[str, Any] | None = Field(
            default=None, description="Pipeline variables."
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = None,
    ) -> Any:
        """Create a pipeline through GraphQL."""
        return await run_blocking(
            client.create_pipeline, project_id=project_id, ref=ref, variables=variables
        )

    @mcp.tool(tags={"graphql_ops"}, annotations=rw)
    async def gitlab_graphql_ops_retry_pipeline(
        project_id: str = Field(description="Project id or full path."),
        pipeline_id: int = Field(description="Pipeline id."),
        client=Depends(get_graphql_client),
        ctx: Context | None = None,
    ) -> Any:
        """Retry the failed jobs of a pipeline through GraphQL."""
        return await run_blocking(
            client.retry_pipeline, project_id=project_id, pipeline_id=pipeline_id
        )

    @mcp.tool(tags={"graphql_ops"}, annotations=rw)
    async def gitlab_graphql_ops_cancel_pipeline(
        project_id: str = Field(description="Project id or full path."),
        pipeline_id: int = Field(description="Pipeline id."),
        client=Depends(get_graphql_client),
        ctx: Context | None = None,
    ) -> Any:
        """Cancel a running pipeline through GraphQL."""
        return await run_blocking(
            client.cancel_pipeline, project_id=project_id, pipeline_id=pipeline_id
        )

    @mcp.tool(tags={"graphql_ops"}, annotations=rw)
    async def gitlab_graphql_ops_update_merge_request(
        project_id: str = Field(description="Project id or full path."),
        merge_request_iid: int = Field(description="Merge request iid."),
        title: str | None = Field(default=None, description="New title."),
        description: str | None = Field(default=None, description="New description."),
        target_branch: str | None = Field(
            default=None, description="New target branch."
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = None,
    ) -> Any:
        """Change a merge request's title, description or target branch through GraphQL."""
        return await run_blocking(
            client.update_merge_request,
            project_id=project_id,
            merge_request_iid=merge_request_iid,
            title=title,
            description=description,
            target_branch=target_branch,
        )

    @mcp.tool(
        tags={"graphql_ops"},
        annotations={"readOnlyHint": False, "destructiveHint": True},
    )
    async def gitlab_graphql_ops_delete_merge_request(
        project_id: str = Field(description="Project id or full path."),
        merge_request_iid: int = Field(description="Merge request iid."),
        confirm: bool = Field(
            default=False, description="Must be true; set only after the person agrees."
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = None,
    ) -> Any:
        """Close a merge request through GraphQL (GitLab does not delete over GraphQL)."""
        if not confirm:
            return {
                "error": "confirmation_required",
                "message": "Pass confirm=true after the person agrees.",
            }
        return await run_blocking(
            client.delete_merge_request,
            project_id=project_id,
            merge_request_iid=merge_request_iid,
        )


def register_graphql_tools(mcp: FastMCP):
    from gitlab_api.auth import get_graphql_client

    @mcp.tool(tags={"graphql"})
    async def gitlab_graphql(
        query: str = Field(
            description="The raw GraphQL query or mutation string to execute against the GitLab API."
        ),
        variables: str = Field(
            default="{}",
            description="JSON string of variables to pass along with the query.",
        ),
        operation_name: str | None = Field(
            default=None,
            description="Optional operation name if executing a specific query within the document.",
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute raw GraphQL queries and mutations natively on GitLab."""
        if ctx:
            await ctx.info("Executing GitLab GraphQL query...")
        import json

        try:
            vars_dict = json.loads(variables) if variables else None
        except Exception:
            return {"error": "Operation failed"}

        try:
            return await run_blocking(
                client.execute_gql,
                query_str=query,
                variables=vars_dict,
                operation_name=operation_name,
            )
        except Exception as e:
            return {"error": f"GraphQL execution failed: {type(e).__name__}"}

    @mcp.tool(tags={"graphql"})
    async def gitlab_discover_graphql_schema(
        type_name: str | None = Field(
            default=None,
            description="Optional specific GraphQL type name to inspect details for (e.g., 'Project', 'Issue'). If omitted, lists all available types in the schema.",
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Discover the dynamic GitLab GraphQL schema including types, fields, and custom attributes in real-time."""
        from scion_sdk.mcp.graphql import (
            ctx_graphql_get_type_details,
            ctx_graphql_list_types,
        )

        if ctx:
            await ctx.info("Retrieving dynamic GitLab GraphQL schema...")

        # Safe wrapper to call execute_gql
        async def execute_fn(q, variables=None):
            return await run_blocking(
                client.execute_gql, query_str=q, variables=variables
            )

        try:
            if type_name:
                return await ctx_graphql_get_type_details(execute_fn, type_name)
            return await ctx_graphql_list_types(execute_fn)
        except Exception:
            return {"error": "Failed to discover GitLab GraphQL schema"}
