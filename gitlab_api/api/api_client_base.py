#!/usr/bin/python

import logging
from base64 import b64encode
from typing import Any, TypeVar

import requests
from agent_utilities.base_utilities import get_logger
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_tls_profile,
)

logger = get_logger(__name__)

from agent_utilities.core.exceptions import (
    AuthError,
    MissingParameterError,
    ParameterError,
    UnauthorizedError,
)

T = TypeVar("T")


def _normalize_base_url(url: str) -> str:
    """Strip a trailing /api/v4 (with or without slash) and re-append it once."""
    base = url.rstrip("/")
    for suffix in ("/api/v4", "/api/v4/"):
        if url.endswith(suffix):
            base = url[: -len(suffix)]
            break
    return base + "/api/v4"


def _bearer_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _basic_auth_header(username: str, password: str) -> dict:
    user_pass = f"{username}:{password}".encode()
    user_pass_encoded = b64encode(user_pass).decode()
    return {
        "Authorization": f"Basic {user_pass_encoded}",
        "Content-Type": "application/json",
    }


def _build_auth_headers(
    token: str | None,
    tokens: list | None,
    username: str | None,
    password: str | None,
) -> tuple[dict, list[dict] | None]:
    """Resolve the primary header (+ optional parallel headers) for one auth mode."""
    if token:
        return _bearer_header(token), None
    if tokens:
        headers_parallel = [_bearer_header(t) for t in tokens]
        return headers_parallel[0], headers_parallel
    if username and password:
        return _basic_auth_header(username, password), None
    raise MissingParameterError


class GitLabApiBase:
    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        tokens: list | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
        debug: bool = False,
    ):
        self._configure_logging(debug)
        if url is None:
            raise MissingParameterError

        self._session = requests.Session()
        self.url = _normalize_base_url(url)
        self.headers, self.headers_parallel = _build_auth_headers(
            token, tokens, username, password
        )
        self.tls_profile = tls_profile or resolve_tls_profile("GITLAB")
        self.tls_profile.configure_requests_session(self._session)
        self.debug = debug
        self._current_header_index = 0

        self._verify_connectivity()

    @staticmethod
    def _configure_logging(debug: bool) -> None:
        if debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")
        else:
            logger.setLevel(logging.ERROR)

    @staticmethod
    def _raise_for_auth_status(response: requests.Response) -> None:
        if response.status_code in (401, 403):
            logger.error("GitLab request rejected by authentication or authorization")
            raise AuthError if response.status_code == 401 else UnauthorizedError
        elif response.status_code == 404:
            logger.error("GitLab resource lookup failed")
            raise ParameterError

    def _verify_connectivity(self) -> None:
        headers_to_check = (
            self.headers_parallel if self.headers_parallel else [self.headers]
        )
        for header in headers_to_check:
            response = self._session.get(
                url=f"{self.url}/projects",
                headers=header,
                timeout=10,
            )
            self._raise_for_auth_status(response)

    def switch_to_next_headers(self) -> bool:
        """
        Switches self.headers to the next set of headers in self.headers_parallel.

        Returns:
        - bool: True if headers were switched, False if no switch occurred (e.g., no parallel headers).
        """
        if not self.headers_parallel or len(self.headers_parallel) <= 1:
            logging.debug("No parallel headers available to switch to.")
            return False

        self._current_header_index = (self._current_header_index + 1) % len(
            self.headers_parallel
        )
        self.headers = self.headers_parallel[self._current_header_index]
        logging.debug(f"Switched to headers at index {self._current_header_index}")
        return True

    def _fetch_next_page(
        self, endpoint: str, model: T, header: dict, page: int
    ) -> list[dict]:
        """Fetch a single page of data from the specified endpoint"""
        import copy

        local_model = copy.copy(model)
        local_model.page = page  # type: ignore
        local_model.model_post_init(local_model)  # type: ignore
        response = self._session.get(
            url=f"{self.url}{endpoint}",
            params=local_model.api_parameters,  # type: ignore
            headers=header,
        )
        page_data = response.json()
        return page_data if isinstance(page_data, list) else []

    def _fetch_initial_page(
        self, initial_endpoint: str, model: T, headers_to_use: list[dict]
    ) -> tuple[requests.Response, int, list[dict]]:
        """Fetch page 1 and report the total page count GitLab returns for the query."""
        response = self._session.get(
            url=f"{self.url}{initial_endpoint}",
            params=model.api_parameters,  # type: ignore
            headers=headers_to_use[0],
        )
        total_pages = int(response.headers.get("X-Total-Pages", 1))
        try:
            initial_data = response.json()
        except Exception:
            logging.error(
                "GitLab response decoding failed: status_code=%s",
                response.status_code,
            )
            raise
        page_data = initial_data if isinstance(initial_data, list) else []
        return response, total_pages, page_data

    @staticmethod
    def _resolve_max_pages(model: T, total_pages: int) -> int:
        """Cap model.max_pages at the server total, defaulting to up to 10 pages."""
        # Fetch all pages by default (max up to 10) if max_pages is None, 0, or unset
        current = getattr(model, "max_pages", None)
        if not current:
            model.max_pages = min(total_pages, 10)  # type: ignore
        elif current > total_pages:
            model.max_pages = total_pages  # type: ignore
        return model.max_pages  # type: ignore

    def _fetch_remaining_pages(
        self, initial_endpoint: str, model: T, headers_to_use: list[dict]
    ) -> list[dict]:
        """Fetch pages 2..max_pages in parallel, rotating across available headers."""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        collected: list[dict] = []
        with ThreadPoolExecutor(max_workers=len(headers_to_use)) as executor:
            future_to_page = {
                executor.submit(
                    self._fetch_next_page,  # type: ignore[arg-type]
                    initial_endpoint,
                    model,
                    headers_to_use[header_idx % len(headers_to_use)],
                    page,
                ): page
                for header_idx, page in enumerate(range(2, model.max_pages + 1))  # type: ignore
            }
            for future in as_completed(future_to_page):
                try:
                    collected.extend(future.result())
                except Exception as e:
                    logging.error(
                        "Paginated request failed: error_type=%s",
                        type(e).__name__,
                    )
        return collected

    def _fetch_all_pages(
        self,
        endpoint: str,
        model: T,
        id_field: str | None = None,
        id_value: Any | None = None,
    ) -> tuple[requests.Response, list[dict]]:
        """Generic method to fetch all pages with parallelization"""
        if id_field and getattr(model, id_field) is None:
            raise MissingParameterError

        headers_to_use = (
            self.headers_parallel if self.headers_parallel else [self.headers]
        )
        initial_endpoint = (
            endpoint.format(id=id_value) if "{id}" in endpoint else endpoint
        )

        total_pages_response, total_pages, all_data = self._fetch_initial_page(
            initial_endpoint, model, headers_to_use
        )
        max_pages = self._resolve_max_pages(model, total_pages)

        if max_pages > 1:
            all_data.extend(
                self._fetch_remaining_pages(initial_endpoint, model, headers_to_use)
            )

        return total_pages_response, all_data
