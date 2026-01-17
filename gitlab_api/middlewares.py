import threading
from typing import Optional

import requests
from fastmcp.server.middleware import MiddlewareContext, Middleware
from fastmcp.utilities.logging import get_logger
from gitlab_api.gitlab_api import Api

# Thread-local storage for user token
local = threading.local()
logger = get_logger(name="TokenMiddleware")


class UserTokenMiddleware(Middleware):
    def __init__(self, config: dict):
        self.config = config

    async def on_request(self, context: MiddlewareContext, call_next):
        logger.debug(f"Delegation enabled: {self.config['enable_delegation']}")
        if self.config["enable_delegation"]:
            headers = getattr(context.message, "headers", {})
            auth = headers.get("Authorization")
            if auth and auth.startswith("Bearer "):
                token = auth.split(" ")[1]
                local.user_token = token
                local.user_claims = None  # Will be populated by JWTVerifier

                # Extract claims if JWTVerifier already validated
                if hasattr(context, "auth") and hasattr(context.auth, "claims"):
                    local.user_claims = context.auth.claims
                    logger.info(
                        "Stored JWT claims for delegation",
                        extra={"subject": context.auth.claims.get("sub")},
                    )
                else:
                    logger.debug("JWT claims not yet available (will be after auth)")

                logger.info("Extracted Bearer token for delegation")
            else:
                logger.error("Missing or invalid Authorization header")
                raise ValueError("Missing or invalid Authorization header")
        return await call_next(context)


class JWTClaimsLoggingMiddleware(Middleware):
    async def on_response(self, context: MiddlewareContext, call_next):
        response = await call_next(context)
        logger.info(f"JWT Response: {response}")
        if hasattr(context, "auth") and hasattr(context.auth, "claims"):
            logger.info(
                "JWT Authentication Success",
                extra={
                    "subject": context.auth.claims.get("sub"),
                    "client_id": context.auth.claims.get("client_id"),
                    "scopes": context.auth.claims.get("scope"),
                },
            )


def get_client(
    instance: str,
    token: Optional[str],
    verify: bool,
    config: dict,
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

        # Perform token exchange
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
