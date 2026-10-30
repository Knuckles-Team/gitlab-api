#!/usr/bin/env python

from scion_sdk.connector import Connector

from gitlab_api.api_client import Api
from gitlab_api.auth import get_client
from gitlab_api.mcp_server import register_prompts

connector = Connector(
    api=Api,
    get_client=get_client,
    tools="gitlab_api.mcp_server",
    instructions="GitLab API MCP Server - Manage projects, issues, merge requests, branches, and more.",
    extra_registrations=(register_prompts,),
)
