#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
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

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_server,
)
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from gitlab_api.auth import get_client

__version__ = "25.24.1"
print(f"Gitlab MCP v{__version__}", file=sys.stderr)

logger = get_logger(name="mcp_server")
logger.setLevel(logging.DEBUG)


DEFAULT_GITLAB_SSL_VERIFY = to_boolean(string=os.getenv("GITLAB_SSL_VERIFY", "True"))
DEFAULT_GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
DEFAULT_GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", None)


def register_misc_tools(mcp: FastMCP):
    pass
    pass

    def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})


def register_branches_tools(mcp: FastMCP):
    @mcp.tool(tags={"branches"})
    async def gitlab_branches(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab branches operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "create":
            return client.create(**kwargs)
        if action == "delete":
            return client.delete(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_protected_branches_tools(mcp: FastMCP):
    @mcp.tool(tags={"protected_branches"})
    async def gitlab_protected_branches(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'protect', 'unprotect'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab protected branches operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "protect":
            return client.protect(**kwargs)
        if action == "unprotect":
            return client.unprotect(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_commits_tools(mcp: FastMCP):
    @mcp.tool(tags={"commits"})
    async def gitlab_commits(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'diff', 'revert', 'get_comments', 'create_comment', 'get_discussions', 'get_statuses', 'post_status', 'get_merge_requests', 'get_gpg_signature'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab commits operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "create":
            return client.create(**kwargs)
        if action == "diff":
            return client.diff(**kwargs)
        if action == "revert":
            return client.revert(**kwargs)
        if action == "get_comments":
            return client.get_comments(**kwargs)
        if action == "create_comment":
            return client.create_comment(**kwargs)
        if action == "get_discussions":
            return client.get_discussions(**kwargs)
        if action == "get_statuses":
            return client.get_statuses(**kwargs)
        if action == "post_status":
            return client.post_status(**kwargs)
        if action == "get_merge_requests":
            return client.get_merge_requests(**kwargs)
        if action == "get_gpg_signature":
            return client.get_gpg_signature(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_deploy_tokens_tools(mcp: FastMCP):
    @mcp.tool(tags={"deploy_tokens"})
    async def gitlab_deploy_tokens(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_project', 'create_project', 'delete_project', 'get_group', 'create_group', 'delete_group'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab deploy tokens operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "get_project":
            return client.get_project(**kwargs)
        if action == "create_project":
            return client.create_project(**kwargs)
        if action == "delete_project":
            return client.delete_project(**kwargs)
        if action == "get_group":
            return client.get_group(**kwargs)
        if action == "create_group":
            return client.create_group(**kwargs)
        if action == "delete_group":
            return client.delete_group(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_environments_tools(mcp: FastMCP):
    @mcp.tool(tags={"environments"})
    async def gitlab_environments(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete', 'stop', 'stop_stale', 'delete_stopped', 'get_protected', 'protect', 'update_protected', 'unprotect'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab environments operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "create":
            return client.create(**kwargs)
        if action == "update":
            return client.update(**kwargs)
        if action == "delete":
            return client.delete(**kwargs)
        if action == "stop":
            return client.stop(**kwargs)
        if action == "stop_stale":
            return client.stop_stale(**kwargs)
        if action == "delete_stopped":
            return client.delete_stopped(**kwargs)
        if action == "get_protected":
            return client.get_protected(**kwargs)
        if action == "protect":
            return client.protect(**kwargs)
        if action == "update_protected":
            return client.update_protected(**kwargs)
        if action == "unprotect":
            return client.unprotect(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(tags={"groups"})
    async def gitlab_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'edit', 'get_subgroups', 'get_descendants', 'get_projects', 'get_merge_requests'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab groups operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "edit":
            return client.edit(**kwargs)
        if action == "get_subgroups":
            return client.get_subgroups(**kwargs)
        if action == "get_descendants":
            return client.get_descendants(**kwargs)
        if action == "get_projects":
            return client.get_projects(**kwargs)
        if action == "get_merge_requests":
            return client.get_merge_requests(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_jobs_tools(mcp: FastMCP):
    @mcp.tool(tags={"jobs"})
    async def gitlab_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_project_jobs', 'get_log', 'cancel', 'retry', 'erase', 'run', 'get_pipeline_jobs'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab jobs operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_project_jobs":
            return client.get_project_jobs(**kwargs)
        if action == "get_log":
            return client.get_log(**kwargs)
        if action == "cancel":
            return client.cancel(**kwargs)
        if action == "retry":
            return client.retry(**kwargs)
        if action == "erase":
            return client.erase(**kwargs)
        if action == "run":
            return client.run(**kwargs)
        if action == "get_pipeline_jobs":
            return client.get_pipeline_jobs(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_members_tools(mcp: FastMCP):
    @mcp.tool(tags={"members"})
    async def gitlab_members(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_group', 'get_project'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab members operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_group":
            return client.get_group(**kwargs)
        if action == "get_project":
            return client.get_project(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_merge_requests_tools(mcp: FastMCP):
    @mcp.tool(tags={"merge_requests"})
    async def gitlab_merge_requests(
        action: str = Field(
            description="Action to perform. Must be one of: 'create', 'get', 'get_project'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab merge requests operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "create":
            return client.create(**kwargs)
        if action == "get":
            return client.get(**kwargs)
        if action == "get_project":
            return client.get_project(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_merge_rules_tools(mcp: FastMCP):
    @mcp.tool(tags={"merge_rules"})
    async def gitlab_merge_rules(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_project_level', 'create_project_level', 'update_project_level', 'delete_project_level', 'get_mr_approvals', 'get_mr_approval_state', 'get_mr_level', 'approve_mr', 'unapprove_mr', 'get_group_level', 'edit_group_level', 'edit_project_level'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab merge rules operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_project_level":
            return client.get_project_level(**kwargs)
        if action == "create_project_level":
            return client.create_project_level(**kwargs)
        if action == "update_project_level":
            return client.update_project_level(**kwargs)
        if action == "delete_project_level":
            return client.delete_project_level(**kwargs)
        if action == "get_mr_approvals":
            return client.get_mr_approvals(**kwargs)
        if action == "get_mr_approval_state":
            return client.get_mr_approval_state(**kwargs)
        if action == "get_mr_level":
            return client.get_mr_level(**kwargs)
        if action == "approve_mr":
            return client.approve_mr(**kwargs)
        if action == "unapprove_mr":
            return client.unapprove_mr(**kwargs)
        if action == "get_group_level":
            return client.get_group_level(**kwargs)
        if action == "edit_group_level":
            return client.edit_group_level(**kwargs)
        if action == "edit_project_level":
            return client.edit_project_level(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_packages_tools(mcp: FastMCP):
    @mcp.tool(tags={"packages"})
    async def gitlab_packages(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'publish', 'download'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab packages operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "publish":
            return client.publish(**kwargs)
        if action == "download":
            return client.download(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_pipelines_tools(mcp: FastMCP):
    @mcp.tool(tags={"pipelines"})
    async def gitlab_pipelines(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'run'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab pipelines operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "run":
            return client.run(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_pipeline_schedules_tools(mcp: FastMCP):
    @mcp.tool(tags={"pipeline_schedules"})
    async def gitlab_pipeline_schedules(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all', 'get', 'get_triggered', 'create', 'edit', 'take_ownership', 'delete', 'run', 'create_variable', 'delete_variable'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab pipeline schedules operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_all":
            return client.get_all(**kwargs)
        if action == "get":
            return client.get(**kwargs)
        if action == "get_triggered":
            return client.get_triggered(**kwargs)
        if action == "create":
            return client.create(**kwargs)
        if action == "edit":
            return client.edit(**kwargs)
        if action == "take_ownership":
            return client.take_ownership(**kwargs)
        if action == "delete":
            return client.delete(**kwargs)
        if action == "run":
            return client.run(**kwargs)
        if action == "create_variable":
            return client.create_variable(**kwargs)
        if action == "delete_variable":
            return client.delete_variable(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(tags={"projects"})
    async def gitlab_projects(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_nested_by_group', 'get_contributors', 'get_statistics', 'edit', 'share_with_group', 'unshare_with_group'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab projects operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "get_nested_by_group":
            return client.get_nested_by_group(**kwargs)
        if action == "get_contributors":
            return client.get_contributors(**kwargs)
        if action == "get_statistics":
            return client.get_statistics(**kwargs)
        if action == "edit":
            return client.edit(**kwargs)
        if action == "share_with_group":
            return client.share_with_group(**kwargs)
        if action == "unshare_with_group":
            return client.unshare_with_group(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_releases_tools(mcp: FastMCP):
    @mcp.tool(tags={"releases"})
    async def gitlab_releases(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_latest', 'get_latest_evidence', 'get_latest_asset', 'get_group_releases', 'download_asset', 'get_by_tag', 'create', 'create_evidence', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab releases operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "get_latest":
            return client.get_latest(**kwargs)
        if action == "get_latest_evidence":
            return client.get_latest_evidence(**kwargs)
        if action == "get_latest_asset":
            return client.get_latest_asset(**kwargs)
        if action == "get_group_releases":
            return client.get_group_releases(**kwargs)
        if action == "download_asset":
            return client.download_asset(**kwargs)
        if action == "get_by_tag":
            return client.get_by_tag(**kwargs)
        if action == "create":
            return client.create(**kwargs)
        if action == "create_evidence":
            return client.create_evidence(**kwargs)
        if action == "update":
            return client.update(**kwargs)
        if action == "delete":
            return client.delete(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_runners_tools(mcp: FastMCP):
    @mcp.tool(tags={"runners"})
    async def gitlab_runners(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all', 'update_details', 'pause', 'get_jobs', 'get_project', 'enable_project', 'delete_project', 'get_group', 'register', 'delete', 'verify_auth', 'reset_gitlab_token', 'reset_project_token', 'reset_group_token', 'reset_token'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab runners operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_all":
            return client.get_all(**kwargs)
        if action == "update_details":
            return client.update_details(**kwargs)
        if action == "pause":
            return client.pause(**kwargs)
        if action == "get_jobs":
            return client.get_jobs(**kwargs)
        if action == "get_project":
            return client.get_project(**kwargs)
        if action == "enable_project":
            return client.enable_project(**kwargs)
        if action == "delete_project":
            return client.delete_project(**kwargs)
        if action == "get_group":
            return client.get_group(**kwargs)
        if action == "register":
            return client.register(**kwargs)
        if action == "delete":
            return client.delete(**kwargs)
        if action == "verify_auth":
            return client.verify_auth(**kwargs)
        if action == "reset_gitlab_token":
            return client.reset_gitlab_token(**kwargs)
        if action == "reset_project_token":
            return client.reset_project_token(**kwargs)
        if action == "reset_group_token":
            return client.reset_group_token(**kwargs)
        if action == "reset_token":
            return client.reset_token(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_tags_tools(mcp: FastMCP):
    @mcp.tool(tags={"tags"})
    async def gitlab_tags(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'delete', 'get_protected', 'get_protected_tag', 'protect', 'unprotect'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage gitlab tags operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            return client.get(**kwargs)
        if action == "create":
            return client.create(**kwargs)
        if action == "delete":
            return client.delete(**kwargs)
        if action == "get_protected":
            return client.get_protected(**kwargs)
        if action == "get_protected_tag":
            return client.get_protected_tag(**kwargs)
        if action == "protect":
            return client.protect(**kwargs)
        if action == "unprotect":
            return client.unprotect(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_custom_api_tools(mcp: FastMCP):
    @mcp.tool(tags={"custom-api"})
    async def api_request(
        action: str = Field(description="Action to perform. Must be one of: "),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage api request operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        raise ValueError(f"Unknown action: {action}")


def register_prompts(mcp: FastMCP):
    @mcp.prompt
    def create_branch_prompt(
        new_branch: str,
        source_branch: str,
        project_id: str | int,
    ) -> str:
        """
        Generates a prompt for creating a branch
        """
        return f"Create a branch called '{new_branch}' from the '{source_branch}' for project id {project_id}"

    @mcp.prompt
    def create_merge_request_prompt(
        new_branch: str,
        source_branch: str,
        project_id: str | int,
        title: str,
        description: str,
    ) -> str:
        """
        Generates a prompt for creating a merge request
        """
        return (
            f"Create a new merge request for project id {project_id} from the '{new_branch}' to the '{source_branch}' "
            f"with a title: '{title}' and a description: '{description}'"
        )

    @mcp.prompt
    def get_project_statistics_prompt(
        project_id: str | int,
    ) -> str:
        """
        Generates a prompt for getting project statistics
        """
        return f"What are the details for project id: {project_id}"

    @mcp.prompt
    def trigger_pipeline_prompt(
        branch: str,
        project_id: str | int,
    ) -> str:
        """
        Generates a prompt for triggering a pipeline
        """
        return f"Run the pipeline for project: '{project_id}' on the '{branch}' branch"

    @mcp.prompt
    def get_latest_release_prompt(
        project_id: str | int,
    ) -> str:
        """
        Generates a prompt for getting the latest gitlab release.
        """
        return f"What is the latest release for project id: {project_id}"


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
    ) -> dict:
        """Execute raw GraphQL queries and mutations natively on GitLab."""
        if ctx:
            await ctx.info("Executing GitLab GraphQL query...")
        import json

        try:
            vars_dict = json.loads(variables) if variables else None
        except Exception as e:
            return {"error": f"Invalid variables JSON: {e}"}

        try:
            return client.execute_gql(
                query_str=query, variables=vars_dict, operation_name=operation_name
            )
        except Exception as e:
            return {"error": f"GraphQL execution failed: {str(e)}"}


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the GitLab MCP instance, args, and middlewares."""
    load_dotenv(find_dotenv())
    os.environ["FASTMCP_LOG_LEVEL"] = "ERROR"
    os.environ["TERM"] = "dumb"
    os.environ["NO_COLOR"] = "1"

    args, mcp, middlewares = create_mcp_server(
        name="GitLab",
        version=__version__,
        instructions="GitLab API MCP Server - Manage projects, issues, merge requests, branches, and more.",
    )

    DEFAULT_GRAPHQLTOOL = to_boolean(os.getenv("GRAPHQLTOOL", "True"))
    if DEFAULT_GRAPHQLTOOL:
        register_graphql_tools(mcp)

    DEFAULT_MISCTOOL = to_boolean(os.getenv("MISCTOOL", "True"))
    if DEFAULT_MISCTOOL:
        register_misc_tools(mcp)
    DEFAULT_BRANCHESTOOL = to_boolean(os.getenv("BRANCHESTOOL", "True"))
    if DEFAULT_BRANCHESTOOL:
        register_branches_tools(mcp)
    DEFAULT_COMMITSTOOL = to_boolean(os.getenv("COMMITSTOOL", "True"))
    if DEFAULT_COMMITSTOOL:
        register_commits_tools(mcp)
    DEFAULT_DEPLOY_TOKENSTOOL = to_boolean(os.getenv("DEPLOY_TOKENSTOOL", "True"))
    if DEFAULT_DEPLOY_TOKENSTOOL:
        register_deploy_tokens_tools(mcp)
    DEFAULT_ENVIRONMENTSTOOL = to_boolean(os.getenv("ENVIRONMENTSTOOL", "True"))
    if DEFAULT_ENVIRONMENTSTOOL:
        register_environments_tools(mcp)
    DEFAULT_GROUPSTOOL = to_boolean(os.getenv("GROUPSTOOL", "True"))
    if DEFAULT_GROUPSTOOL:
        register_groups_tools(mcp)
    DEFAULT_JOBSTOOL = to_boolean(os.getenv("JOBSTOOL", "True"))
    if DEFAULT_JOBSTOOL:
        register_jobs_tools(mcp)
    DEFAULT_MEMBERSTOOL = to_boolean(os.getenv("MEMBERSTOOL", "True"))
    if DEFAULT_MEMBERSTOOL:
        register_members_tools(mcp)
    DEFAULT_MERGE_REQUESTSTOOL = to_boolean(os.getenv("MERGE_REQUESTSTOOL", "True"))
    if DEFAULT_MERGE_REQUESTSTOOL:
        register_merge_requests_tools(mcp)
    DEFAULT_MERGE_RULESTOOL = to_boolean(os.getenv("MERGE_RULESTOOL", "True"))
    if DEFAULT_MERGE_RULESTOOL:
        register_merge_rules_tools(mcp)
    DEFAULT_PACKAGESTOOL = to_boolean(os.getenv("PACKAGESTOOL", "True"))
    if DEFAULT_PACKAGESTOOL:
        register_packages_tools(mcp)
    DEFAULT_PIPELINESTOOL = to_boolean(os.getenv("PIPELINESTOOL", "True"))
    if DEFAULT_PIPELINESTOOL:
        register_pipelines_tools(mcp)
    DEFAULT_PIPELINE_SCHEDULESTOOL = to_boolean(
        os.getenv("PIPELINE_SCHEDULESTOOL", "True")
    )
    if DEFAULT_PIPELINE_SCHEDULESTOOL:
        register_pipeline_schedules_tools(mcp)
    DEFAULT_PROJECTSTOOL = to_boolean(os.getenv("PROJECTSTOOL", "True"))
    if DEFAULT_PROJECTSTOOL:
        register_projects_tools(mcp)
    DEFAULT_PROTECTED_BRANCHESTOOL = to_boolean(
        os.getenv("PROTECTED_BRANCHESTOOL", "True")
    )
    if DEFAULT_PROTECTED_BRANCHESTOOL:
        register_protected_branches_tools(mcp)
    DEFAULT_RELEASESTOOL = to_boolean(os.getenv("RELEASESTOOL", "True"))
    if DEFAULT_RELEASESTOOL:
        register_releases_tools(mcp)
    DEFAULT_RUNNERSTOOL = to_boolean(os.getenv("RUNNERSTOOL", "True"))
    if DEFAULT_RUNNERSTOOL:
        register_runners_tools(mcp)  # type: ignore
    DEFAULT_TAGSTOOL = to_boolean(os.getenv("TAGSTOOL", "True"))
    if DEFAULT_TAGSTOOL:
        register_tags_tools(mcp)
    DEFAULT_CUSTOM_APITOOL = to_boolean(os.getenv("CUSTOM_APITOOL", "True"))
    if DEFAULT_CUSTOM_APITOOL:
        register_custom_api_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    registered_tags: list[str] = []
    return mcp, args, middlewares, registered_tags


def mcp_server() -> None:
    mcp, args, middlewares, registered_tags = get_mcp_instance()
    print(f"{'gitlab-api'} MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {len(set(registered_tags))}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
