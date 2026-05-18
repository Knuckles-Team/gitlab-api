"""GitLab Authentication Module.

Authentication priority:
1. **OIDC Delegation** — If ``ENABLE_DELEGATION`` is active, exchanges
   the IdP-issued user token for a downstream GitLab access token
   via RFC 8693 Token Exchange using the shared ``delegated_auth`` helper.
2. **Fixed Credentials** — Falls back to ``GITLAB_TOKEN`` env var.

See ``docs/guides/oauth_sso.md`` in agent-utilities for full details.
"""

import os
import threading

from agent_utilities.base_utilities import get_logger, to_boolean
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

from gitlab_api.api_client import Api

local = threading.local()
logger = get_logger(__name__)


def get_client(
    instance: str = os.getenv("GITLAB_URL", "https://gitlab.com"),
    token: str | None = os.getenv("GITLAB_TOKEN", None),
    verify: bool = to_boolean(string=os.getenv("GITLAB_SSL_VERIFY", "True")),
    config: dict | None = None,
) -> Api:
    """Factory function to create the GitLab Api client.

    Supports OIDC delegation and fixed credentials (token).
    Uses the shared ``delegated_auth`` helper from agent-utilities.
    """
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        get_user_identity,
        is_delegation_enabled,
    )

    # Resolve delegation config — prefer shared mcp_auth_config
    delegation_enabled = is_delegation_enabled(config)

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if delegation_enabled:
        try:
            delegated_token = get_delegated_token(
                config=config,
                audience=(config or {}).get("audience", instance),
                scopes=(config or {}).get("delegated_scopes", "api"),
                verify=verify,
            )
            identity = get_user_identity()
            logger.info(
                "Using OIDC delegated token for GitLab API",
                extra={
                    "user_email": identity.get("email"),
                    "instance": instance,
                },
            )
            return Api(url=instance, token=delegated_token, verify=verify)
        except Exception as e:
            logger.error(
                "OIDC delegation failed for GitLab",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            raise RuntimeError(f"Token exchange failed: {str(e)}") from e

    # --- Path 2: Fixed Credentials (GITLAB_TOKEN) ---
    logger.info("Using fixed credentials for GitLab API")
    try:
        return Api(url=instance, token=token, verify=verify)
    except (AuthError, UnauthorizedError) as e:
        raise RuntimeError(
            f"AUTHENTICATION ERROR: The GitLab credentials provided are not valid for '{instance}'. "
            f"Please check your GITLAB_TOKEN and GITLAB_URL environment variables. "
            f"Error details: {str(e)}"
        ) from e
