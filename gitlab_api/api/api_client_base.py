#!/usr/bin/python

import logging
from base64 import b64encode
from typing import Any, TypeVar

import requests
import urllib3
from agent_utilities.base_utilities import get_logger

logger = get_logger(__name__)

from agent_utilities.core.exceptions import (
    AuthError,
    MissingParameterError,
    ParameterError,
    UnauthorizedError,
)

T = TypeVar("T")


class GitLabApiBase:
    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        tokens: list | None = None,
        proxies: dict | None = None,
        verify: bool = True,
        debug: bool = False,
    ):
        if debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")
        else:
            logger.setLevel(logging.ERROR)
        if url is None:
            raise MissingParameterError

        self._session = requests.Session()
        self.url = url.rstrip("/")
        forbidden = ["/api/v4", "/api/v4/"]
        for end in forbidden:
            if url.endswith(end):
                self.url = url[: -len(end)]
        self.url = self.url + "/api/v4"
        self.headers = None
        self.headers_parallel = None
        self.verify = verify
        self.proxies = proxies
        self.debug = debug
        self._current_header_index = 0

        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self.headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        elif tokens:
            self.headers_parallel = []
            for token in tokens:
                self.headers_parallel.append(
                    {
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    }
                )
            self.headers = self.headers_parallel[self._current_header_index]
        elif username and password:
            user_pass = f"{username}:{password}".encode()
            user_pass_encoded = b64encode(user_pass).decode()
            self.headers = {
                "Authorization": f"Basic {user_pass_encoded}",
                "Content-Type": "application/json",
            }
        else:
            raise MissingParameterError

        headers_to_check = (
            self.headers_parallel if self.headers_parallel else [self.headers]
        )
        for header in headers_to_check:
            response = self._session.get(
                url=f"{self.url}/projects",
                headers=header,
                verify=self.verify,
                proxies=self.proxies,
                timeout=10,
            )
            if response.status_code in (401, 403):
                logger.error(f"Authentication Error with header: {response.content}")  # type: ignore
                raise AuthError if response.status_code == 401 else UnauthorizedError
            elif response.status_code == 404:
                logger.error(f"Parameter Error: {response.content}")  # type: ignore
                raise ParameterError

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
            verify=self.verify,
            proxies=self.proxies,
        )
        page_data = response.json()
        return page_data if isinstance(page_data, list) else []

    def _fetch_all_pages(
        self,
        endpoint: str,
        model: T,
        id_field: str | None = None,
        id_value: Any | None = None,
    ) -> tuple[requests.Response, list[dict]]:
        """Generic method to fetch all pages with parallelization"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        if id_field and getattr(model, id_field) is None:
            raise MissingParameterError
        all_data = []
        headers_to_use = (
            self.headers_parallel if self.headers_parallel else [self.headers]
        )

        initial_endpoint = (
            endpoint.format(id=id_value) if "{id}" in endpoint else endpoint
        )
        total_pages_response = self._session.get(
            url=f"{self.url}{initial_endpoint}",
            params=model.api_parameters,  # type: ignore
            headers=headers_to_use[0],
            verify=self.verify,
            proxies=self.proxies,
        )
        total_pages = int(total_pages_response.headers.get("X-Total-Pages", 1))
        try:
            initial_data = total_pages_response.json()
        except Exception:
            logging.error(f"Failed to decode JSON from {self.url}{initial_endpoint}")
            logging.error(f"Status Code: {total_pages_response.status_code}")
            logging.error(f"Response Content: {total_pages_response.text}")
            raise
        if isinstance(initial_data, list):
            all_data.extend(initial_data)

        # Fetch all pages by default (max up to 10 pages) if max_pages is None, 0, or not set
        if not hasattr(model, "max_pages") or model.max_pages is None or model.max_pages == 0:  # type: ignore
            model.max_pages = min(total_pages, 10)  # type: ignore
        elif model.max_pages > total_pages:  # type: ignore
            model.max_pages = total_pages  # type: ignore

        if model.max_pages > 1:  # type: ignore
            with ThreadPoolExecutor(max_workers=len(headers_to_use)) as executor:
                future_to_page = {}
                header_idx = 0

                for page in range(2, model.max_pages + 1):  # type: ignore
                    header = headers_to_use[header_idx % len(headers_to_use)]
                    future = executor.submit(
                        self._fetch_next_page,  # type: ignore[arg-type]
                        initial_endpoint,
                        model,
                        header,
                        page,
                    )
                    future_to_page[future] = page
                    header_idx += 1

                for future in as_completed(future_to_page):
                    try:
                        page_data = future.result()
                        all_data.extend(page_data)
                    except Exception as e:
                        logging.error(
                            f"Error fetching page {future_to_page[future]}: {str(e)}"
                        )

        return total_pages_response, all_data
