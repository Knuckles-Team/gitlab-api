"""GitLab Authentication Module.

Authentication priority:
1. **OIDC Delegation** — If ``ENABLE_DELEGATION`` is active, exchanges
   the caller's verified MCP token for a downstream GitLab access token
   via RFC 8693 Token Exchange using ``agent_connector_sdk.auth.delegation``.
2. **Fixed Credentials** — Falls back to ``GITLAB_TOKEN`` env var.
"""

import threading
from typing import Any

from agent_connector_sdk.auth.delegation import DelegationSettings, delegated_token
from agent_connector_sdk.config import setting
from agent_connector_sdk.exceptions import AuthError, UnauthorizedError
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile
from agent_connector_sdk.utilities import get_logger

local = threading.local()
from gitlab_api.api_client import Api

logger = get_logger(__name__)


def _resolve_tls_profile_for(
    tls_profile: ResolvedTLSProfile | None, profile_name: str | None
) -> ResolvedTLSProfile:
    """An explicit runtime profile wins over the configured profile selector."""
    return tls_profile or resolve_tls_profile("GITLAB", profile_name=profile_name)


def _resolve_url_connection(
    instance: str,
    token: str | None,
    tls_profile: ResolvedTLSProfile | None,
) -> tuple[str, str | None, ResolvedTLSProfile]:
    """A URL is used directly; its token remains caller-owned."""
    return (
        instance,
        token,
        _resolve_tls_profile_for(tls_profile, setting("GITLAB_TLS_PROFILE")),
    )


def _resolve_unconfigured_connection(
    instance: str | None,
    token: str | None,
    tls_profile: ResolvedTLSProfile | None,
) -> tuple[str, str | None, ResolvedTLSProfile]:
    """No structured tenant config: fall back to single-host env settings."""
    if instance:
        raise RuntimeError(
            f"GitLab instance '{instance}' is not configured. Add it to "
            "gitlab_instances in ~/.config/agent-utilities/config.json, or pass "
            "a full URL / set GITLAB_URL+GITLAB_TOKEN."
        )
    return (
        setting("GITLAB_URL", "https://gitlab.com"),
        token or setting("GITLAB_TOKEN"),
        _resolve_tls_profile_for(tls_profile, setting("GITLAB_TLS_PROFILE")),
    )


def _resolve_named_instance_connection(
    inst: Any,
    token: str | None,
    tls_profile: ResolvedTLSProfile | None,
) -> tuple[str, str | None, ResolvedTLSProfile]:
    return (
        inst.url,
        token or inst.token or setting("GITLAB_TOKEN"),
        _resolve_tls_profile_for(
            tls_profile, inst.tls_profile_name or setting("GITLAB_TLS_PROFILE")
        ),
    )


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

    if instance and str(instance).startswith(("http://", "https://")):
        return _resolve_url_connection(instance, token, tls_profile)

    # A name (or None=default) resolves against the configured tenants.
    inst = get_instance(instance)
    if inst is None:
        return _resolve_unconfigured_connection(instance, token, tls_profile)
    return _resolve_named_instance_connection(inst, token, tls_profile)


def get_client(
    instance: str | None = None,
    token: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
) -> Api:
    """Factory function to create the GitLab Api client.

    Multi-tenant (CONCEPT:AU-KG.backend.declared-columns-so-schema): ``instance`` selects a configured tenant by
    name (from the shared ``gitlab_instances`` config), accepts a bare URL, or
    defaults to the first configured instance / ``GITLAB_URL``. Supports OIDC
    delegation and fixed credentials (token) via ``agent_connector_sdk.auth.delegation``.
    """
    instance, token, tls_profile = _resolve_connection(instance, token, tls_profile)
    settings = DelegationSettings.from_settings()

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if settings.enabled:
        try:
            token_value = delegated_token(settings)
            logger.info(
                "Using OIDC delegated token for GitLab API",
            )
            return Api(url=instance, token=token_value, tls_profile=tls_profile)
        except Exception as e:
            logger.error(
                "OIDC delegation failed for GitLab",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": type(e).__name__,
                },
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
) -> Any:
    """Factory function to create the GitLab GraphQL client.

    Multi-tenant (CONCEPT:AU-KG.backend.declared-columns-so-schema): ``instance`` selects a configured tenant by
    name, a bare URL, or the default. Supports OIDC delegation and fixed
    credentials (token).
    """
    instance, token, tls_profile = _resolve_connection(instance, token, tls_profile)
    from gitlab_api.gitlab_gql import GraphQL

    settings = DelegationSettings.from_settings()

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if settings.enabled:
        try:
            token_value = delegated_token(settings)
            logger.info(
                "Using OIDC delegated token for GitLab GraphQL API",
            )
            return GraphQL(
                url=instance,
                token=token_value,
                tls_profile=tls_profile,
            )
        except Exception as e:
            logger.error(
                "OIDC delegation failed for GitLab GraphQL",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": type(e).__name__,
                },
            )
            raise RuntimeError(f"Token exchange failed: {type(e).__name__}") from e

    # --- Path 2: Fixed Credentials (GITLAB_TOKEN) ---
    logger.info("Using fixed credentials for GitLab GraphQL API")
    if not token:
        raise RuntimeError("GITLAB_TOKEN environment variable or parameter is missing.")
    return GraphQL(url=instance, token=token, tls_profile=tls_profile)
