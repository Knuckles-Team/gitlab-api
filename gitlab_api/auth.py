"""GitLab Authentication Module.

Authentication priority:
1. **OIDC Delegation** — If ``ENABLE_DELEGATION`` is active, exchanges
   the IdP-issued user token for a downstream GitLab access token
   via RFC 8693 Token Exchange using the shared ``delegated_auth`` helper.
2. **Fixed Credentials** — Falls back to ``GITLAB_TOKEN`` env var.

See ``docs/guides/oauth_sso.md`` in agent-utilities for full details.
"""

import threading
from typing import Any

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

local = threading.local()
from gitlab_api.api_client import Api

logger = get_logger(__name__)


def _resolve_connection(
    instance: str | None, token: str | None, verify: bool | None
) -> tuple[str, str | None, bool]:
    """Resolve ``(url, token, verify)`` for a target tenant (CONCEPT:AU-KG.backend.declared-columns-so-schema).

    ``instance`` may be a configured instance NAME (resolved from the shared
    ``gitlab_instances`` config), a bare URL (used as-is, back-compat), or ``None``
    (the default instance, else ``GITLAB_URL``). Explicit ``token``/``verify`` args
    always win over the instance's stored values.
    """
    from gitlab_api.instances import get_instance

    env_verify = setting("GITLAB_SSL_VERIFY", True)

    # A bare URL is used directly (the historical call shape) — the caller owns
    # the token it passes (no env fallback, so an explicit token=None stays None).
    if instance and str(instance).startswith(("http://", "https://")):
        return (instance, token, env_verify if verify is None else verify)

    # A name (or None=default) resolves against the configured tenants.
    inst = get_instance(instance)
    if inst is None:
        if instance:
            raise RuntimeError(
                f"GitLab instance '{instance}' is not configured. Add it to "
                "gitlab_instances in ~/.config/agent-utilities/config.json, or pass "
                "a full URL / set GITLAB_URL+GITLAB_TOKEN."
            )
        # No config at all → legacy single-host env defaults.
        return (
            setting("GITLAB_URL", "https://gitlab.com"),
            token or setting("GITLAB_TOKEN"),
            env_verify if verify is None else verify,
        )
    return (
        inst.url,
        token or inst.token or setting("GITLAB_TOKEN"),
        inst.verify_ssl if verify is None else verify,
    )


def get_client(
    instance: str | None = None,
    token: str | None = None,
    verify: bool | None = None,
    config: dict | None = None,
) -> Api:
    """Factory function to create the GitLab Api client.

    Multi-tenant (CONCEPT:AU-KG.backend.declared-columns-so-schema): ``instance`` selects a configured tenant by
    name (from the shared ``gitlab_instances`` config), accepts a bare URL, or
    defaults to the first configured instance / ``GITLAB_URL``. Supports OIDC
    delegation and fixed credentials (token) via the shared ``delegated_auth``
    helper from agent-utilities.
    """
    instance, token, verify = _resolve_connection(instance, token, verify)
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


def get_graphql_client(
    instance: str | None = None,
    token: str | None = None,
    verify: bool | None = None,
    config: dict | None = None,
) -> Any:
    """Factory function to create the GitLab GraphQL client.

    Multi-tenant (CONCEPT:AU-KG.backend.declared-columns-so-schema): ``instance`` selects a configured tenant by
    name, a bare URL, or the default. Supports OIDC delegation and fixed
    credentials (token).
    """
    instance, token, verify = _resolve_connection(instance, token, verify)
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        get_user_identity,
        is_delegation_enabled,
    )

    from gitlab_api.gitlab_gql import GraphQL

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
                "Using OIDC delegated token for GitLab GraphQL API",
                extra={
                    "user_email": identity.get("email"),
                    "instance": instance,
                },
            )
            return GraphQL(url=instance, token=delegated_token, verify=verify)
        except Exception as e:
            logger.error(
                "OIDC delegation failed for GitLab GraphQL",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            raise RuntimeError(f"Token exchange failed: {str(e)}") from e

    # --- Path 2: Fixed Credentials (GITLAB_TOKEN) ---
    logger.info("Using fixed credentials for GitLab GraphQL API")
    if not token:
        raise RuntimeError("GITLAB_TOKEN environment variable or parameter is missing.")
    return GraphQL(url=instance, token=token, verify=verify)
