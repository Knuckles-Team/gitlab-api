#!/usr/bin/env python

from scion_sdk.connector import Connector

from gitlab_api.api_client import Api
from gitlab_api.auth import get_client

#: Operations the SDK refuses to serve unless they declare the owner-approval
#: flag (SCION-SCM-R003.3): every non-read method whose name holds the
#: ``merge`` token.
OWNER_APPROVAL_OPERATIONS: tuple[str, ...] = (
    "accept_merge_request",
    "approve_merge_request",
    "create_merge_request",
    "unapprove_merge_request",
)

connector = Connector(
    verbose_targets=(
        {
            "client_cls": Api,
            "get_client": get_client,
            "manifest": [
                {"method": method, "owner_approval_required": True}
                for method in OWNER_APPROVAL_OPERATIONS
            ],
        },
    ),
    instructions="GitLab API MCP Server - Manage projects, issues, merge requests, branches, and more.",
    tools="gitlab_api.mcp_server",
)
