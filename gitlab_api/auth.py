import os
import threading
from typing import Optional

import requests
from fastmcp.server.middleware import MiddlewareContext, Middleware
from agent_utilities.base_utilities import to_boolean, get_logger
from gitlab_api.gitlab_api import Api

local = threading.local()
logger = get_logger(__name__)

def get_client(
    config: dict,
    instance: str = os.getenv("GITLAB_INSTANCE", "https://gitlab.com"),
    token: Optional[str] = os.getenv("GITLAB_ACCESS_TOKEN", None),
    verify: bool = to_boolean(string=os.getenv("GITLAB_VERIFY", "True")),
) -> Api:
    """
    Factory function to create the Api client, either with fixed credentials or delegated token.
    Uses server-side logging for visibility into token exchange process.
    """
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

        return Api(
            url=instance,
            token=new_token,
            verify=verify,
        )
    else:
        logger.info("Using fixed credentials for API")
        return Api(
            url=instance,
            token=token,
            verify=verify,
        )
