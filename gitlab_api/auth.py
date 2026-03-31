import os
import threading
from typing import Optional

import requests
from agent_utilities.base_utilities import to_boolean, get_logger
from gitlab_api.api_wrapper import Api
from agent_utilities.exceptions import AuthError, UnauthorizedError

local = threading.local()
logger = get_logger(__name__)


def get_client(
    instance: str = os.getenv("GITLAB_URL", "https://gitlab.com"),
    token: Optional[str] = os.getenv("GITLAB_TOKEN", None),
    verify: bool = to_boolean(string=os.getenv("GITLAB_SSL_VERIFY", "True")),
    config: Optional[dict] = None,
) -> Api:
    """
    Factory function to create the Api client, either with fixed credentials or delegated token.
    Uses server-side logging for visibility into token exchange process.
    """
    if config is None:
        from agent_utilities.mcp_utilities import config as default_config

        config = default_config

    if config["enable_delegation"]:
        user_token = getattr(local, "user_token", None)
        if not user_token:
            logger.error("No user token available for delegation")
            raise ValueError("No user token available for delegation")

        logger.info(
            "Initiating OAuth token exchange",
            extra={
                "audience": config["audience"],
                "scopes": config["delegated_scopes"],
            },
        )

        exchange_data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": user_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
            "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
            "audience": config["audience"],
            "scope": config["delegated_scopes"],
        }
        auth = (config["oidc_client_id"], config["oidc_client_secret"])
        try:
            response = requests.post(
                config["token_endpoint"], data=exchange_data, auth=auth
            )
            response.raise_for_status()
            new_token = response.json()["access_token"]
            logger.info(
                "Token exchange successful", extra={"new_token_length": len(new_token)}
            )
        except Exception as e:
            logger.error(
                "Token exchange failed",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            raise RuntimeError(f"Token exchange failed: {str(e)}")

        try:
            return Api(
                url=instance,
                token=new_token,
                verify=verify,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The delegated GitLab credentials are not valid for '{instance}'. "
                f"Please check your OIDC configuration and permissions. "
                f"Error details: {str(e)}"
            ) from e
    else:
        logger.info("Using fixed credentials for API")
        try:
            return Api(
                url=instance,
                token=token,
                verify=verify,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The GitLab credentials provided are not valid for '{instance}'. "
                f"Please check your GITLAB_TOKEN and GITLAB_URL environment variables. "
                f"Error details: {str(e)}"
            ) from e
