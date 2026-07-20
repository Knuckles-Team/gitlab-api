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
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

local = threading.local()
from gitlab_api.api_client import Api

logger = get_logger(__name__)


def _resolve_connection(
    instance: str | None,
    token: str | None,
    tls_profile: ResolvedTLSProfile | None,
) -> tuple[str, str | None, ResolvedTLSProfile]:
    """Resolve URL, token, and strict transport profile for a target tenant.

    ``instance`` may be a configured instance name, a URL, or ``None`` (the
    default instance, then ``GITLAB_URL``). An explicit runtime profile wins
    over the configured profile selector.
    """
    from gitlab_api.instances import get_instance

    # A URL is used directly; its token remains caller-owned.
    if instance and str(instance).startswith(("http://", "https://")):
        return (
            instance,
            token,
            tls_profile
            or resolve_configured_tls_profile(
                "GITLAB", profile_name=setting("GITLAB_TLS_PROFILE")
            ),
        )

    # A name (or None=default) resolves against the configured tenants.
    inst = get_instance(instance)
    if inst is None:
        if instance:
            raise RuntimeError(
                f"GitLab instance '{instance}' is not configured. Add it to "
                "gitlab_instances in ~/.config/agent-utilities/config.json, or pass "
                "a full URL / set GITLAB_URL+GITLAB_TOKEN."
            )
        # No structured config: use the single-host environment settings.
        return (
            setting("GITLAB_URL", "https://gitlab.com"),
            token or setting("GITLAB_TOKEN"),
            tls_profile
            or resolve_configured_tls_profile(
                "GITLAB", profile_name=setting("GITLAB_TLS_PROFILE")
            ),
        )
    return (
        inst.url,
        token or inst.token or setting("GITLAB_TOKEN"),
        tls_profile
        or resolve_configured_tls_profile(
            "GITLAB",
            profile_name=inst.tls_profile_name or setting("GITLAB_TLS_PROFILE"),
        ),
    )


def get_client(
    instance: str | None = None,
    token: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
    config: dict | None = None,
) -> Api:
    """Factory function to create the GitLab Api client.

    Multi-tenant (CONCEPT:AU-KG.backend.declared-columns-so-schema): ``instance`` selects a configured tenant by
    name (from the shared ``gitlab_instances`` config), accepts a bare URL, or
    defaults to the first configured instance / ``GITLAB_URL``. Supports OIDC
    delegation and fixed credentials (token) via the shared ``delegated_auth``
    helper from agent-utilities.
    """
    instance, token, tls_profile = _resolve_connection(instance, token, tls_profile)
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
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
            )
            logger.info(
                "Using OIDC delegated token for GitLab API",
            )
            return Api(url=instance, token=delegated_token, tls_profile=tls_profile)
        except Exception as e:
            logger.error(
                "OIDC delegation failed for GitLab",
                extra={"error_type": type(e).__name__, "error_message": type(e).__name__},
            )
            raise RuntimeError(f"Token exchange failed: {type(e).__name__}") from e

    # --- Path 2: Fixed Credentials (GITLAB_TOKEN) ---
    logger.info("Using fixed credentials for GitLab API")
    try:
        return Api(url=instance, token=token, tls_profile=tls_profile)
    except (AuthError, UnauthorizedError) as e:
        raise RuntimeError(
            f"AUTHENTICATION ERROR: The GitLab credentials provided are not valid for '{instance}'. "
            f"Please check your GITLAB_TOKEN and GITLAB_URL environment variables. "
            f"Error details: {type(e).__name__}"
        ) from e


def get_graphql_client(
    instance: str | None = None,
    token: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
    config: dict | None = None,
) -> Any:
    """Factory function to create the GitLab GraphQL client.

    Multi-tenant (CONCEPT:AU-KG.backend.declared-columns-so-schema): ``instance`` selects a configured tenant by
    name, a bare URL, or the default. Supports OIDC delegation and fixed
    credentials (token).
    """
    instance, token, tls_profile = _resolve_connection(instance, token, tls_profile)
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
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
            )
            logger.info(
                "Using OIDC delegated token for GitLab GraphQL API",
            )
            return GraphQL(
                url=instance,
                token=delegated_token,
                tls_profile=tls_profile,
            )
        except Exception as e:
            logger.error(
                "OIDC delegation failed for GitLab GraphQL",
                extra={"error_type": type(e).__name__, "error_message": type(e).__name__},
            )
            raise RuntimeError(f"Token exchange failed: {type(e).__name__}") from e

    # --- Path 2: Fixed Credentials (GITLAB_TOKEN) ---
    logger.info("Using fixed credentials for GitLab GraphQL API")
    if not token:
        raise RuntimeError("GITLAB_TOKEN environment variable or parameter is missing.")
    return GraphQL(url=instance, token=token, tls_profile=tls_profile)
