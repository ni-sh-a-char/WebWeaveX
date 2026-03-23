"""HTTP fetcher for WebWeaveX."""

import httpx
from typing import Optional, Dict, Any
import time

from .utils import get_spec


class Fetcher:
    """HTTP fetcher with retries and timeout."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the fetcher."""
        self.spec = config or get_spec()
        self.fetch_config = self.spec.get("fetch", {})
        self.timeout = self.fetch_config.get("timeout", 10)
        self.retries = self.fetch_config.get("retries", 3)
        self.retry_delay = self.fetch_config.get("retry_delay", 1)
        self.user_agent = self.fetch_config.get("user_agent", "WebWeaveX/1.0")
        self.follow_redirects = self.fetch_config.get("follow_redirects", True)
        self.max_redirects = self.fetch_config.get("max_redirects", 5)

    def fetch(self, url: str) -> str:
        """Fetch content from URL with retries."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept-Language": self.fetch_config.get("accept_language", "en-US,en;q=0.9"),
            "Accept-Encoding": self.fetch_config.get("accept_encoding", "gzip, deflate"),
        }

        last_error = None
        for attempt in range(self.retries):
            try:
                with httpx.Client(
                    timeout=self.timeout,
                    max_redirects=self.max_redirects,
                    headers=headers,
                ) as client:
                    response = client.get(url)
                    response.raise_for_status()
                    return response.text
            except httpx.HTTPError as e:
                last_error = e
                if attempt < self.retries - 1:
                    time.sleep(self.retry_delay)
                continue

        raise last_error or Exception(f"Failed to fetch {url} after {self.retries} attempts")

    async def fetch_async(self, url: str) -> str:
        """Fetch content from URL asynchronously."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept-Language": self.fetch_config.get("accept_language", "en-US,en;q=0.9"),
            "Accept-Encoding": self.fetch_config.get("accept_encoding", "gzip, deflate"),
        }

        last_error = None
        for attempt in range(self.retries):
            try:
                async with httpx.AsyncClient(
                    timeout=self.timeout,
                    follow_redirects=self.follow_redirects,
                    max_redirects=self.max_redirects,
                    headers=headers,
                ) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.text
            except httpx.HTTPError as e:
                last_error = e
                if attempt < self.retries - 1:
                    time.sleep(self.retry_delay)
                continue

        raise last_error or Exception(f"Failed to fetch {url} after {self.retries} attempts")
